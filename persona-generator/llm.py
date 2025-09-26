"""
Generic LLM utility for Swiss AI Platform API with rate limiting and error handling.
"""
import os
import time
import logging
from typing import Optional, Iterator
from dataclasses import dataclass
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RateLimitInfo:
    """Information about current rate limits from response headers."""
    remaining_tokens: Optional[int] = None
    reset_tokens_time: Optional[str] = None


class SwissAIClient:
    """
    A wrapper client for Swiss AI Platform API with built-in rate limiting and error handling.
    
    Rate limits:
    - 5 requests per second
    - 100,000 tokens per minute
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the Swiss AI client.
        
        Args:
            api_key: API key for Swiss AI Platform. If None, reads from SWISS_AI_PLATFORM_API_KEY env var.
            base_url: Base URL for the API. If None, uses default Swiss AI Platform URL.
        """
        self.api_key = api_key or os.getenv("SWISS_AI_PLATFORM_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Set SWISS_AI_PLATFORM_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = base_url or "https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1"
        self.model = "swiss-ai/Apertus-70B"
        
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # Rate limiting tracking
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 5 requests per second = 0.2 seconds between requests
        
    def _wait_for_rate_limit(self):
        """Ensure we don't exceed the rate limit of 5 requests per second."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _extract_rate_limit_info(self, response) -> RateLimitInfo:
        """Extract rate limit information from response headers."""
        headers = getattr(response, 'headers', {}) or {}
        
        return RateLimitInfo(
            remaining_tokens=headers.get('X-Ratelimit-Remaining-Tokens'),
            reset_tokens_time=headers.get('X-Ratelimit-Reset-Tokens')
        )
    
    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> str:
        """
        Generate a completion using the Swiss AI Platform.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The generated text response (or iterator if streaming)
            
        Example:
            client = SwissAIClient()
            response = client.complete(
                "What are the best places to visit in Switzerland?",
                system_prompt="You are a travel agent. Be descriptive and helpful"
            )
            print(response)
        """
        # Wait to respect rate limits
        self._wait_for_rate_limit()
        
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Prepare API call parameters
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            **kwargs
        }
        
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        
        try:
            logger.debug(f"Making completion request, stream={stream}")
            response = self.client.chat.completions.create(**params)
            
            # Log rate limit info if available
            rate_limit_info = self._extract_rate_limit_info(response)
            if rate_limit_info.remaining_tokens:
                logger.info(f"Remaining tokens: {rate_limit_info.remaining_tokens}")
            
            if stream:
                return response
            else:
                return response.choices[0].message.content
            
        except openai.RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise
        except openai.APIError as e:
            logger.error(f"API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    def stream_complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Iterator[str]:
        """
        Helper for streaming text completion that yields content chunks.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            **kwargs: Additional parameters for complete
            
        Yields:
            Content chunks as strings
            
        Example:
            client = SwissAIClient()
            for chunk in client.stream_complete("Tell me about Switzerland"):
                print(chunk, end="", flush=True)
        """
        stream = self.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            stream=True,
            **kwargs
        )
        
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content


# Convenience function for quick usage
def create_client(api_key: Optional[str] = None) -> SwissAIClient:
    """
    Create a SwissAIClient instance.
    
    Args:
        api_key: Optional API key. If not provided, reads from environment.
        
    Returns:
        SwissAIClient instance
    """
    return SwissAIClient(api_key=api_key)