# Swiss AI Weeks - Banking Client Simulation

🏦 **Banking Persona Generator** - Ein KI-gestütztes Tool zur Generierung realistischer Banking-Personas basierend auf Schweizer demographischen Daten.

![Swiss AI Weeks](https://img.shields.io/badge/Swiss%20AI%20Weeks-2025-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Überblick

Dieses Projekt wurde für die **Swiss AI Weeks 2025** entwickelt und ermöglicht es Finnova Banking-Experten, realistische Kunden-Personas zu erstellen. Das Tool kombiniert echte Schweizer demographische Daten mit KI-generierten Banking-Verhaltensmustern, um detaillierte Kundenprofile für Produktentwicklung, Marketing und Marktforschung zu generieren.

## ⚠️ Wichtige Hinweise & Einschränkungen

### 📊 Datenabhängigkeiten
- **CSV-Dateien erforderlich**: Das Tool funktioniert nur mit den zugehörigen demographischen CSV-Dateien im `data/` Verzeichnis
- **Swisscom AI API**: Benötigt Zugriff auf die Swisscom AI Platform API (nicht im Repository enthalten)
- **API-Schlüssel**: Ein gültiger Swiss AI Platform API-Schlüssel ist zwingend erforderlich

### 🛠️ Qualität & Validierung
- **Experimenteller Prototyp**: Dieses Tool wurde für Demonstrationszwecke entwickelt
- **Keine Qualitätsvalidierung**: Die Qualität der generierten Personas wurde nicht umfassend validiert
- **Fehler vorbehalten**: Mögliche Inkonsistenzen oder Fehler in den generierten Daten
- **Nicht produktionstauglich**: Nicht für produktive Banking-Anwendungen geeignet

### 🔒 Haftungsausschluss
- **Experimentelle Nutzung**: Nur für Forschung, Bildung und Prototyping
- **Keine Garantie**: Keine Gewährleistung für Vollständigkeit oder Korrektheit der Daten
- **Swiss AI Weeks Demo**: Primär für Demonstrationszwecke bei den Swiss AI Weeks 2025

## ✨ Features

### 🎭 Persona-Generierung
- **Einzelne Personas**: Generiere eine detaillierte Banking-Persona mit individuellen Eigenschaften
- **Batch-Generierung**: Erstelle mehrere Personas gleichzeitig für umfassende Analysen
- **Realistische Daten**: Basiert auf echten Schweizer demographischen Daten

### 💬 Interaktive Chats
- **Persona Chat**: Führe Gespräche mit generierten Personas über Banking-Themen
- **Batch Chat**: Stelle Fragen an mehrere Personas gleichzeitig für Marktforschung
- **Natürliche Gespräche**: KI-gestützte Antworten in der jeweiligen Persona-Rolle

### 📚 Verwaltung & Analyse
- **Persona Library**: Durchsuche und verwalte alle erstellten Personas
- **Datenexport**: Exportiere Personas als JSON für weitere Analysen
- **Filtering**: Filtere nach demographischen und Banking-spezifischen Kriterien

### 🎨 Modernes Interface
- **Responsive Design**: Funktioniert auf Desktop und Mobile
- **Intuitive Navigation**: Benutzerfreundliche Streamlit-Oberfläche
- **Professional Styling**: Modernes, konsistentes Design

## 🚀 Quick Start

### Voraussetzungen

- Python 3.8 oder höher
- **Swiss AI Platform API Key** (Swisscom AI - nicht im Repository enthalten)
- **Zugehörige CSV-Dateien** im `data/` Verzeichnis (demographische Daten)
- Git
- **Hinweis**: Vollständige Funktionalität nur mit allen Datenquellen und API-Zugang

### Installation

1. **Repository klonen**
```bash
git clone https://github.com/severinlindenmann/swiss-ai-weeks-finnova-banking-client-simulation.git
cd swiss-ai-weeks-finnova-banking-client-simulation
```

2. **Virtuelle Umgebung erstellen**
```bash
python -m venv .venv
source .venv/bin/activate  # Auf Windows: .venv\Scripts\activate
```

3. **Dependencies installieren**
```bash
cd persona-generator
pip install -r requirements.txt
# oder mit uv:
uv pip install -r requirements.txt
```

4. **Umgebungsvariablen konfigurieren**
```bash
# Erstelle .env Datei im persona-generator Verzeichnis
echo "SWISS_AI_PLATFORM_API_KEY=your_api_key_here" > .env
```

5. **Anwendung starten**
```bash
streamlit run main_app.py
```

Die Anwendung ist nun unter `http://localhost:8501` verfügbar!

## 📖 Verwendung

### 1. Einzelne Persona erstellen
- Navigiere zu "Single Persona"
- Wähle demographische Filter (Alter, Geschlecht, Kanton, etc.)
- Konfiguriere Banking-Parameter (Vermögen, Risikotoleranz, etc.)
- Klicke "Persona Generieren"

### 2. Batch-Generierung
- Gehe zu "Batch Generation" 
- Bestimme die Anzahl Personas (1-100)
- Setze Filter und Parameter
- Starte die Batch-Generierung

### 3. Chat mit Personas
- Wähle "Persona Chat" für Einzelgespräche
- Oder "Batch Chat" für Gruppendiskussionen
- Stelle Fragen über Banking, Finanzen oder persönliche Präferenzen

### 4. Personas verwalten
- "Persona Library" zeigt alle generierten Personas
- Durchsuche, analysiere und exportiere Personas
- Lösche nicht mehr benötigte Batches

## 🗂️ Projektstruktur

```
swiss-ai-weeks-finnova-banking-client-simulation/
├── README.md                      # Hauptdokumentation
├── LICENSE                        # MIT Lizenz
├── data/                         # Demographische Daten
│   ├── Demographie/
│   └── Psychologisch/
└── persona-generator/            # Hauptanwendung
    ├── README.md                 # Spezifische Dokumentation
    ├── main_app.py               # Haupt-Streamlit App
    ├── streamlit_app.py          # Alternative Einzelseite
    ├── ui_components.py          # UI-Komponenten und Styling
    ├── single_persona.py         # Einzelpersona-Generierung
    ├── batch_generation.py       # Batch-Generierung
    ├── persona_library.py        # Persona-Verwaltung
    ├── persona_chat.py           # Chat-Interface
    ├── batch_chat.py             # Batch-Chat
    ├── llm.py                    # LLM-Client
    ├── data.py                   # Datenverarbeitung
    ├── system.md                 # System-Prompt
    ├── prompt.md                 # Persona-Prompt Template
    └── generated_personas/       # Generierte Personas (wird erstellt)
```

## 🔧 Konfiguration

### API-Schlüssel

Das Tool benötigt einen Swiss AI Platform API Key:

1. Erstelle eine `.env` Datei im `persona-generator` Verzeichnis
2. Füge deinen API Key hinzu:
   ```
   SWISS_AI_PLATFORM_API_KEY=your_api_key_here
   ```

### Datenquellen

Die Anwendung nutzt echte Schweizer demographische Daten:
- **Demographie**: Zensusdaten zu Alter, Geschlecht, Bildung, Einkommen
- **Psychologisch**: Zusätzliche Verhaltensdaten aus Schweizer Studien

## 🎯 Anwendungsfälle

### Banking & Fintech
- **Produktentwicklung**: Verstehe Kundenbedürfnisse für neue Banking-Produkte
- **Marketing-Strategien**: Entwickle zielgruppenspezifische Kampagnen
- **User Experience**: Teste Interfaces mit verschiedenen Kundentypen
- **Risikobewertung**: Analysiere Verhaltenspatterns verschiedener Segmente

### Marktforschung
- **Kundensegmentierung**: Identifiziere und verstehe verschiedene Kundengruppen
- **Verhaltensanalyse**: Erkunde Banking-Verhaltensweisen und Präferenzen
- **Produkttests**: Teste Konzepte mit diversen Persona-Gruppen
- **Trend-Analyse**: Verstehe sich ändernde Kundenbedürfnisse

## 🤝 Beiträge

Wir begrüßen Beiträge zur Verbesserung des Tools! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Development Setup
```bash
# Repository forken und klonen
git clone https://github.com/your-username/swiss-ai-weeks-finnova-banking-client-simulation.git
cd swiss-ai-weeks-finnova-banking-client-simulation

# Development environment setup
python -m venv .venv
source .venv/bin/activate
cd persona-generator
pip install -r requirements.txt

# Tests ausführen
python -m pytest tests/

# Code-Qualität prüfen
black .
flake8 .
```

## 📄 Lizenz

Dieses Projekt ist unter der [MIT Lizenz](LICENSE) veröffentlicht.

### Präsentation & Demo
- **Live Demo**: [Link zur gehosteten Version]
- **Präsentation**: [Link zu Slides]
- **Video**: [Link zur Demo-Video]

---

**Entwickelt mit ❤️ für die Swiss AI Weeks 2025**

*Ein Tool für die nächste Generation von Banking-Innovation*