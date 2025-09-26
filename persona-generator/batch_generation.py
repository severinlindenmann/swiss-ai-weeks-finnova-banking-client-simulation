import streamlit as st
import pandas as pd
from pathlib import Path
import json
import time
import asyncio
from datetime import datetime
from single_persona import generate_persona, get_filter_options
import uuid
import concurrent.futures
from threading import Semaphore

def save_personas_batch(personas, filters_used, additional_params):
    """Save a batch of personas to JSON file"""
    
    # Create personas directory if it doesn't exist
    personas_dir = Path(__file__).parent / "generated_personas"
    personas_dir.mkdir(exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"personas_batch_{timestamp}.json"
    filepath = personas_dir / filename
    
    # Prepare batch data
    batch_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_personas": len(personas),
            "filters_used": filters_used,
            "additional_params": additional_params,
            "batch_id": str(uuid.uuid4())
        },
        "personas": personas
    }
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(batch_data, f, indent=2, ensure_ascii=False)
    
    return filepath, batch_data["metadata"]["batch_id"]

class RateLimiter:
    """Rate limiter for controlling API request frequency"""
    def __init__(self, max_requests_per_second=5):
        self.max_requests = max_requests_per_second
        self.semaphore = Semaphore(max_requests_per_second)
        self.request_times = []
    
    def acquire(self):
        """Acquire a request slot, blocking if necessary to maintain rate limit"""
        current_time = time.time()
        
        # Remove requests older than 1 second
        self.request_times = [t for t in self.request_times if current_time - t < 1.0]
        
        # If we've hit the rate limit, wait
        if len(self.request_times) >= self.max_requests:
            sleep_time = 1.0 - (current_time - self.request_times[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
                # Clean up again after waiting
                current_time = time.time()
                self.request_times = [t for t in self.request_times if current_time - t < 1.0]
        
        # Record this request
        self.request_times.append(current_time)

def generate_single_persona_with_rate_limit(args):
    """Generate a single persona with rate limiting"""
    persona_index, additional_params, csv_filters, rate_limiter, random_options = args
    
    try:
        # Acquire rate limit slot
        rate_limiter.acquire()
        
        import random
        
        # Create parameters for this persona
        current_params = additional_params.copy()
        
        if additional_params.get('randomize', False):
            # Generate random parameters for this persona
            current_params = {
                'vermoegen': random.choice(random_options['vermoegen']),
                'verfuegbares_einkommen': random.choice(random_options['verfuegbares_einkommen']),
                'grosse_ausgaben': random.choice(random_options['grosse_ausgaben']),
                'eigentum': random.choice(random_options['eigentum']),
                'finanz_erfahrung': random.choice(random_options['finanz_erfahrung'])
            }
        
        persona_json, person_data = generate_persona(current_params, csv_filters, debug_mode=False)
        
        if persona_json and person_data:
            # Parse JSON to validate it
            persona_dict = json.loads(persona_json)
            return {
                "success": True,
                "persona": {
                    "persona": persona_dict,
                    "source_data": person_data,
                    "parameters_used": current_params,
                    "generated_at": datetime.now().isoformat()
                },
                "index": persona_index
            }
        else:
            return {
                "success": False,
                "error": f"Failed to generate persona {persona_index + 1}",
                "index": persona_index
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error generating persona {persona_index + 1}: {str(e)}",
            "index": persona_index
        }

def generate_batch_personas_parallel(count, additional_params, csv_filters, progress_callback=None):
    """Generate multiple personas with parallel processing and rate limiting"""
    
    # Define random parameter options
    random_options = {
        'vermoegen': ["< 10k", "10k-100k", ">100k"],
        'verfuegbares_einkommen': ["< 60k", "60k-100k", ">100k"], 
        'grosse_ausgaben': ["ja", "nein"],
        'eigentum': [0, 1],  # 0=Miete, 1=Eigentum
        'finanz_erfahrung': ["Einsteiger", "Fortgeschritten", "Experte"]
    }
    
    # Create rate limiter (5 requests per second)
    rate_limiter = RateLimiter(max_requests_per_second=5)
    
    # Prepare arguments for each persona generation
    args_list = [
        (i, additional_params, csv_filters, rate_limiter, random_options)
        for i in range(count)
    ]
    
    personas = []
    errors = []
    completed = 0
    
    # Use ThreadPoolExecutor for parallel processing
    # Limit to 5 threads to match our rate limit
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks
        future_to_index = {
            executor.submit(generate_single_persona_with_rate_limit, args): args[0]
            for args in args_list
        }
        
        # Collect results with their indices
        results_with_index = []
        
        # Process completed tasks
        for future in concurrent.futures.as_completed(future_to_index):
            result = future.result()
            completed += 1
            
            if progress_callback:
                progress_callback(completed, count, f"Completed {completed}/{count} personas")
            
            results_with_index.append(result)
        
        # Sort results by index to maintain original order
        results_with_index.sort(key=lambda x: x["index"])
        
        # Separate successful personas from errors
        for result in results_with_index:
            if result["success"]:
                personas.append(result["persona"])
            else:
                errors.append(result["error"])
    
    return personas, errors

def generate_batch_personas(count, additional_params, csv_filters, progress_callback=None):
    """Generate multiple personas - choose parallel or sequential based on count"""
    if count >= 5:  # Use parallel processing for larger batches
        return generate_batch_personas_parallel(count, additional_params, csv_filters, progress_callback)
    else:
        # Use sequential for small batches (less overhead)
        return generate_batch_personas_sequential(count, additional_params, csv_filters, progress_callback)

def generate_batch_personas_sequential(count, additional_params, csv_filters, progress_callback=None):
    """Sequential generation for small batches"""
    import random
    
    personas = []
    errors = []
    
    # Define random parameter options
    random_options = {
        'vermoegen': ["< 10k", "10k-100k", ">100k"],
        'verfuegbares_einkommen': ["< 60k", "60k-100k", ">100k"], 
        'grosse_ausgaben': ["ja", "nein"],
        'eigentum': [0, 1],  # 0=Miete, 1=Eigentum
        'finanz_erfahrung': ["Einsteiger", "Fortgeschritten", "Experte"]
    }
    
    for i in range(count):
        if progress_callback:
            progress_callback(i, count, f"Generating persona {i+1}/{count}")
        
        try:
            # Create parameters for this persona
            current_params = additional_params.copy()
            
            if additional_params.get('randomize', False):
                # Generate random parameters for this persona
                current_params = {
                    'vermoegen': random.choice(random_options['vermoegen']),
                    'verfuegbares_einkommen': random.choice(random_options['verfuegbares_einkommen']),
                    'grosse_ausgaben': random.choice(random_options['grosse_ausgaben']),
                    'eigentum': random.choice(random_options['eigentum']),
                    'finanz_erfahrung': random.choice(random_options['finanz_erfahrung'])
                }
            
            persona_json, person_data = generate_persona(current_params, csv_filters, debug_mode=False)
            if persona_json and person_data:
                # Parse JSON to validate it
                persona_dict = json.loads(persona_json)
                personas.append({
                    "persona": persona_dict,
                    "source_data": person_data,
                    "parameters_used": current_params,
                    "generated_at": datetime.now().isoformat()
                })
            else:
                errors.append(f"Failed to generate persona {i+1}")
        except Exception as e:
            errors.append(f"Error generating persona {i+1}: {str(e)}")
    
    if progress_callback:
        progress_callback(count, count, f"Completed {count}/{count} personas")
    
    return personas, errors

def show():
    """Show the batch persona generation page"""
    
    st.title("🎯 Batch Persona Generator")
    st.write("Generate multiple banking personas at once with consistent filters and parameters.")
    
    # Initialize session state
    if 'batch_generated' not in st.session_state:
        st.session_state.batch_generated = False
    if 'current_batch' not in st.session_state:
        st.session_state.current_batch = None
    if 'batch_filepath' not in st.session_state:
        st.session_state.batch_filepath = None

    filter_options = get_filter_options()

    # Main interface
    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("### Batch Configuration")
        
        # Batch size
        batch_size = st.slider(
            "Number of Personas",
            min_value=1,
            max_value=100,
            value=10,
            help="How many personas to generate in this batch"
        )
        
        st.write("### CSV-Daten Filter")
        
        # Demographics filters from CSV (same as single persona)
        st.write("**Demografische Filter:**")
        
        alter_range = st.selectbox(
            "Altersgruppe",
            options=["Alle", "18-25", "26-35", "36-45", "46-65", "65+"],
            index=0,
            help="Wählen Sie eine Altersgruppe",
            key="batch_alter"
        )
        
        geschlecht_filter = st.selectbox(
            "Geschlecht",
            options=["Alle", "Männlich", "Weiblich"],
            index=0,
            help="Filtern nach Geschlecht",
            key="batch_geschlecht"
        )
        
        kanton_filter = st.selectbox(
            "Kanton",
            options=["Alle"] + filter_options['kantone'],
            index=0,
            help="Filtern nach Kanton",
            key="batch_kanton"
        )
        
        sprachgebiet_filter = st.selectbox(
            "Sprachgebiet", 
            options=["Alle"] + filter_options['sprachgebiet'],
            index=0,
            help="Filtern nach Sprachgebiet",
            key="batch_sprachgebiet"
        )
        
        bruttojahr_range = st.selectbox(
            "Bruttojahreseinkommen",
            options=["Alle", "< 60k", "60k-100k", "> 100k"],
            index=0,
            help="Filtern nach Einkommensbereich",
            key="batch_bruttojahr"
        )
        
        ausbildung_filter = st.selectbox(
            "Ausbildung",
            options=["Alle"] + filter_options['ausbildung'][:10],
            index=0,
            help="Filtern nach Ausbildung",
            key="batch_ausbildung"
        )
        
        erwerbstaetig_filter = st.selectbox(
            "Erwerbstätigkeit",
            options=["Alle", "Erwerbstätig", "Nicht erwerbstätig"],
            index=0,
            help="Filtern nach Erwerbsstatus",
            key="batch_erwerbstaetig"
        )
        
        kinder_filter = st.selectbox(
            "Kinder im Haushalt",
            options=["Alle", "Mit Kindern", "Ohne Kinder"],
            index=0,
            help="Filtern nach Kindern im Haushalt",
            key="batch_kinder"
        )
        
        # Collect CSV filters
        csv_filters = {
            'alter_range': alter_range,
            'geschlecht': geschlecht_filter,
            'kanton': kanton_filter if kanton_filter != "Alle" else None,
            'sprachgebiet': sprachgebiet_filter if sprachgebiet_filter != "Alle" else None,
            'bruttojahr_range': bruttojahr_range,
            'ausbildung': ausbildung_filter if ausbildung_filter != "Alle" else None,
            'arbeit': 1 if erwerbstaetig_filter == "Erwerbstätig" else (0 if erwerbstaetig_filter == "Nicht erwerbstätig" else None),
            'kinder': 1 if kinder_filter == "Mit Kindern" else (0 if kinder_filter == "Ohne Kinder" else None)
        }
        
        st.write("---")
        
        st.write("### Banking Parameter")
        
        # Banking parameters with randomization option
        st.write("**Parameter-Modus:**")
        param_mode = st.radio(
            "Wie sollen Banking-Parameter gesetzt werden?",
            ["Fest (alle Personas gleich)", "Zufällig variieren"],
            help="Feste Parameter = alle Personas haben dieselben Banking-Eigenschaften. Zufällig = jede Persona bekommt zufällige Werte."
        )
        
        if param_mode == "Fest (alle Personas gleich)":
            # Fixed parameters for all personas
            vermoegen = st.selectbox(
                "Freies Vermögen",
                options=["< 10k", "10k-100k", ">100k"],
                index=0,
                key="batch_vermoegen"
            )
            
            verfuegbares_einkommen = st.selectbox(
                "Verfügbares Einkommen",
                options=["< 60k", "60k-100k", ">100k"],
                index=0,
                key="batch_verfuegbar"
            )
            
            grosse_ausgaben = st.selectbox(
                "Geplante größere Ausgaben",
                options=["ja", "nein"],
                index=1,
                key="batch_ausgaben"
            )
            
            eigentum = st.selectbox(
                "Wohnsituation",
                options=["Eigentum", "Miete"],
                index=1,
                key="batch_eigentum"
            )
            
            finanz_erfahrung = st.selectbox(
                "Finanz-Erfahrung",
                options=["Einsteiger", "Fortgeschritten", "Experte"],
                index=1,
                key="batch_finanz"
            )
            
            additional_params = {
                'vermoegen': vermoegen,
                'verfuegbares_einkommen': verfuegbares_einkommen,
                'grosse_ausgaben': grosse_ausgaben,
                'eigentum': 1 if eigentum == "Eigentum" else 0,
                'finanz_erfahrung': finanz_erfahrung,
                'randomize': False
            }
        else:
            # Random parameters
            st.info("📊 Parameter werden für jede Persona zufällig gewählt")
            additional_params = {
                'randomize': True
            }
        
        st.write("---")
        
        # Generation button
        st.write("### Generation")
        
        # Show processing mode info
        processing_mode = "Parallel (5 requests/sec)" if batch_size >= 5 else "Sequential"
        estimated_time = batch_size / 5 if batch_size >= 5 else batch_size * 2  # rough estimates
        
        st.info(f"**Processing Mode**: {processing_mode} | **Estimated Time**: ~{estimated_time:.1f} seconds")
        
        if st.button("🚀 Generate Batch", type="primary", use_container_width=True):
            if batch_size > 0:
                # Show progress with enhanced tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                metrics_placeholder = st.empty()
                
                def update_progress(current, total, message=""):
                    progress = current / total
                    progress_bar.progress(progress)
                    
                    # Calculate rate and ETA
                    elapsed = time.time() - start_time
                    if current > 0:
                        rate = current / elapsed
                        eta = (total - current) / rate if rate > 0 else 0
                        
                        # Update metrics
                        with metrics_placeholder.container():
                            col_progress, col_rate, col_eta = st.columns(3)
                            with col_progress:
                                st.metric("Progress", f"{current}/{total}")
                            with col_rate:
                                st.metric("Rate", f"{rate:.1f}/sec")
                            with col_eta:
                                st.metric("ETA", f"{eta:.0f}s" if eta < 60 else f"{eta/60:.1f}m")
                    
                    status_text.text(message or f"Processing... {current}/{total}")
                
                start_time = time.time()
                
                # Generate personas
                personas, errors = generate_batch_personas(
                    batch_size, 
                    additional_params, 
                    csv_filters, 
                    update_progress
                )
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Calculate final rate
                final_rate = len(personas) / duration if duration > 0 else 0
                
                # Save batch
                if personas:
                    filepath, batch_id = save_personas_batch(personas, csv_filters, additional_params)
                    
                    st.session_state.current_batch = {
                        'personas': personas,
                        'errors': errors,
                        'metadata': {
                            'total': len(personas),
                            'duration': duration,
                            'batch_id': batch_id,
                            'filepath': str(filepath)
                        }
                    }
                    st.session_state.batch_generated = True
                    st.session_state.batch_filepath = filepath
                    
                    # Clear progress
                    progress_bar.empty()
                    status_text.empty()
                    metrics_placeholder.empty()
                    
                    # Show completion metrics
                    col_success1, col_success2, col_success3 = st.columns(3)
                    with col_success1:
                        st.success(f"✅ **{len(personas)} personas** generated")
                    with col_success2:
                        st.info(f"⏱️ **{duration:.1f} seconds** total time")
                    with col_success3:
                        st.info(f"🚀 **{final_rate:.1f} personas/sec** average rate")
                    
                    if errors:
                        st.warning(f"⚠️ {len(errors)} errors occurred")
                        with st.expander("View Errors"):
                            for error in errors:
                                st.error(error)
                else:
                    st.error("❌ No personas were generated successfully")
        
        # Show active filters summary
        if any(v for v in csv_filters.values() if v is not None and v != "Alle"):
            st.write("### Active Filters")
            active_filters = [f"{k}: {v}" for k, v in csv_filters.items() if v is not None and v != "Alle"]
            for f in active_filters:
                st.text(f"• {f}")

    with col2:
        if st.session_state.batch_generated and st.session_state.current_batch:
            batch = st.session_state.current_batch
            
            st.write("### Batch Results")
            
            # Summary stats
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Personas Generated", batch['metadata']['total'])
            with col_b:
                st.metric("Duration", f"{batch['metadata']['duration']:.1f}s")
            with col_c:
                st.metric("Errors", len(batch['errors']))
            
            # Download buttons
            st.write("### Download Options")
            col_download1, col_download2 = st.columns(2)
            
            with col_download1:
                if st.button("💾 Download Full Batch JSON"):
                    with open(st.session_state.batch_filepath, 'r', encoding='utf-8') as f:
                        batch_data = f.read()
                    
                    st.download_button(
                        label="Download Batch File",
                        data=batch_data,
                        file_name=f"personas_batch_{batch['metadata']['batch_id'][:8]}.json",
                        mime="application/json"
                    )
            
            with col_download2:
                # Create simplified CSV export
                if st.button("📊 Download Summary CSV"):
                    summary_data = []
                    for i, p in enumerate(batch['personas']):
                        persona = p['persona']
                        basic = persona.get('basic_info', {})
                        banking = persona.get('banking_persona', {})
                        financial = persona.get('financial', {})
                        
                        summary_data.append({
                            'ID': persona.get('persona_id', f'P_{i+1}'),
                            'Name': basic.get('name', ''),
                            'Age': basic.get('age', ''),
                            'Gender': basic.get('gender', ''),
                            'Canton': persona.get('demographics', {}).get('canton', ''),
                            'Income_CHF': financial.get('annual_gross_income_chf', ''),
                            'Risk_Tolerance': banking.get('risk_tolerance', ''),
                            'Investment_Interest': banking.get('investment_interest', ''),
                            'Channel_Preference': banking.get('banking_preferences', {}).get('channel_preference', ''),
                            'Service_Level': banking.get('banking_preferences', {}).get('service_level', '')
                        })
                    
                    df_summary = pd.DataFrame(summary_data)
                    csv_data = df_summary.to_csv(index=False)
                    
                    st.download_button(
                        label="Download CSV Summary",
                        data=csv_data,
                        file_name=f"personas_summary_{batch['metadata']['batch_id'][:8]}.csv",
                        mime="text/csv"
                    )
            
            # Show errors if any
            if batch['errors']:
                with st.expander("⚠️ View Errors"):
                    for error in batch['errors']:
                        st.error(error)
            
            # Preview personas
            st.write("### Persona Preview")
            if batch['personas']:
                # Persona selector
                selected_idx = st.selectbox(
                    "Select a persona to preview:",
                    range(len(batch['personas'])),
                    format_func=lambda x: f"Persona {x+1}: {batch['personas'][x]['persona'].get('basic_info', {}).get('name', 'Unknown')}"
                )
                
                if selected_idx is not None:
                    selected_persona = batch['personas'][selected_idx]['persona']
                    
                    # Show compact view of selected persona
                    col_basic, col_banking = st.columns(2)
                    
                    with col_basic:
                        st.write("**Basic Info:**")
                        basic = selected_persona.get('basic_info', {})
                        st.write(f"Name: {basic.get('name', 'N/A')}")
                        st.write(f"Age: {basic.get('age', 'N/A')}")
                        st.write(f"Gender: {basic.get('gender', 'N/A')}")
                        
                        demographics = selected_persona.get('demographics', {})
                        st.write(f"Canton: {demographics.get('canton', 'N/A')}")
                        st.write(f"Household Size: {demographics.get('household_size', 'N/A')}")
                    
                    with col_banking:
                        st.write("**Banking Profile:**")
                        banking = selected_persona.get('banking_persona', {})
                        st.write(f"Risk Tolerance: {banking.get('risk_tolerance', 'N/A')}")
                        st.write(f"Investment Interest: {banking.get('investment_interest', 'N/A')}")
                        
                        prefs = banking.get('banking_preferences', {})
                        st.write(f"Channel: {prefs.get('channel_preference', 'N/A')}")
                        st.write(f"Service Level: {prefs.get('service_level', 'N/A')}")
                    
                    # Full JSON in expander
                    with st.expander("📄 View Full JSON"):
                        st.json(selected_persona)
        else:
            st.write("### Welcome to Batch Generation!")
            st.write("Configure your filters and parameters on the left, then generate multiple personas at once.")
            
            st.write("### Features:")
            st.write("""
            - **Batch Size**: Generate 1-100 personas in one go
            - **Consistent Filters**: All personas follow the same demographic criteria
            - **Parameter Modes**: 
              - Fixed: All personas have identical banking parameters
              - Random: Each persona gets randomly varied banking characteristics
            - **Export Options**: Download as JSON or CSV summary
            - **Progress Tracking**: Real-time generation progress
            - **Error Handling**: Robust error reporting and recovery
            """)
            
            st.write("### Use Cases:")
            st.write("""
            - **Market Research**: Generate customer segments for analysis
            - **Testing**: Create test datasets for banking systems
            - **Demographics**: Study specific population groups
            - **Simulation**: Bulk data for customer journey modeling
            """)
            
            with st.expander("💡 Tips for Best Results"):
                st.write("""
                - **Start Small**: Try 5-10 personas first to test your filters
                - **Specific Filters**: Use demographic filters to create focused segments
                - **Random Mode**: Use random banking parameters for diverse personas
                - **Save Batches**: Generated files are automatically saved with timestamps
                - **Monitor Errors**: Check error reports if generation fails
                """)