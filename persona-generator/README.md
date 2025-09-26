# Banking Persona Generator

🎭 **KI-gestützte Banking-Persona-Generierung** - Erstelle realistische Schweizer Banking-Kunden mit modernster AI-Technologie.

## 📋 Überblick

Der Banking Persona Generator ist eine moderne Streamlit-Anwendung, die echte Schweizer demographische Daten mit KI-generierten Banking-Verhaltensmustern kombiniert, um detaillierte und realistische Kundenpersonas zu erstellen. Entwickelt für die Swiss AI Weeks 2025.

## ✨ **Multi-Page Anwendung**

Die Anwendung bietet fünf Hauptseiten über die Seitenleiste:

### 1. 👤 **Single Persona** 
*Generiere eine Persona mit Echtzeit-Feedback*

- **Demographische Filter**: Altersgruppen, Geschlecht, Kanton, Sprachregion, Einkommen, Bildung, Erwerbsstatus
- **Banking-Parameter**: Vermögen, verfügbares Einkommen, geplante Ausgaben, Wohnsituation, Finanz-Erfahrung  
- **Echtzeit-Generierung**: Sofortiges Feedback mit Debug-Modus
- **Strukturierte Anzeige**: Übersichtliche Darstellung mit JSON-Export

### 2. 🎯 **Batch Generation**
*Generiere 1-100 Personas gleichzeitig mit Fortschritts-Tracking*

#### **Hauptfunktionen:**
- **Batch-Größe**: Bis zu 100 Personas in einem Vorgang
- **Fortschritts-Tracking**: Echtzeit-Fortschrittsbalken mit Status-Updates
- **Parameter-Modi**:
  - **Fix**: Alle Personas teilen identische Banking-Parameter
  - **Zufällig**: Jede Persona erhält zufällig variierte Banking-Eigenschaften
- **Konsistente Filter**: Alle Personas folgen denselben demographischen Kriterien
- **Auto-Speichern**: Batches werden automatisch mit Zeitstempel gespeichert
- **Export-Optionen**: Vollständige JSON-Batch-Datei oder CSV-Zusammenfassung

#### **Anwendungsfälle:**
- Marktforschung und Kundensegmentierung
- Bulk-Testdaten für Banking-Systeme
- Demographische Studien spezifischer Populationen
- Kundenerfahrungs-Simulationsdatensätze

### 3. 📚 **Persona Library**
*Durchsuche, analysiere und verwalte deine generierten Personas*

#### **Features:**
- **Batch-Management**: Alle gespeicherten Persona-Batches mit Metadaten anzeigen
- **Suchen & Filtern**: Spezifische Personas nach Name, Job, Kanton usw. finden
- **Einzelansicht**: Detaillierte Ansicht jeder Persona mit vollständigen Daten
- **Analytics Dashboard**: 
  - Demographische Charts (Alter, Geschlecht, Kanton, Einkommen)
  - Banking-Verhaltensanalyse (Risikotoleranz, Kanal-Präferenzen)
  - Kreuzanalyse (Investment-Interesse vs. Risikotoleranz)
  - Zusammenfassende Statistiken für numerische Felder
- **Export-Optionen**: 
  - Individuelle Persona JSON-Dateien
  - Batch CSV-Zusammenfassungen
  - Vollständige Batch JSON-Dateien
- **Batch-Löschung**: Unerwünschte Batches entfernen

### 4. 💬 **Persona Chat**
*Interaktive 1-zu-1 Gespräche mit generierten Personas*

#### **Features:**
- **Realistische Gespräche**: KI-gestützte Antworten in Persona-Rolle
- **Banking-Fokus**: Spezialisiert auf Finanz- und Banking-Themen
- **Chat-Export**: Speichere Unterhaltungen als JSON
- **Quick Actions**: Vorgefertigte Fragen für häufige Banking-Szenarien

### 5. 👥 **Batch Chat**
*Gleichzeitige Befragung mehrerer Personas für Marktforschung*

#### **Features:**
- **Multi-Persona Befragung**: Stelle eine Frage an bis zu 10 Personas gleichzeitig
- **Vergleichsanalyse**: Sammle diverse Perspektiven zu Banking-Produkten
- **Batch-Auswahl**: Wähle spezifische Persona-Gruppen für Befragungen

## 🔧 **Technische Features**

### **Datenspeicherung:**
- Personas gespeichert im `generated_personas/` Verzeichnis
- JSON-Format mit Metadaten und Zeitstempeln
- Batch-IDs für eindeutige Identifikation

### **Analytics:**
- Plotly-basierte interaktive Charts
- Demographische Verteilungsanalyse
- Banking-Verhaltens-Insights
- Kreuzkorrelations-Studien

### **Fehlerbehandlung:**
- Robuste JSON-Parsing mit Auto-Fix-Funktionen
- Fortschritts-Tracking mit Fehlerberichterstattung
- Graceful Handling von Generierungsfehlern

## 📊 **Generierte Datenstruktur**

Jede Persona umfasst:
- **Grundinfo**: Name, Alter, Geschlecht, Nationalität, Sprachen
- **Demographie**: Kanton, Region, Haushaltsinformationen, Wohnsituation
- **Beruflich**: Job, Branche, Erwerbsstatus, Einkommen
- **Finanziell**: Einkommen, Vermögen, Ausgaben, Erfahrungslevel
- **Banking-Profil**: Risikotoleranz, Investment-Interesse, Präferenzen
- **Persönlichkeit**: Eigenschaften, Werte, Lifestyle, Technologie-Affinität
- **Narrative**: Lebensgeschichte, aktuelle Situation, Zukunftsvorstellungen
- **Banking-Szenarien**: Produkte, Auslöser, Kommunikationspräferenzen

## 🎯 **Empfohlener Workflow**

1. **Mit Single Persona beginnen**: Filter und Parameter testen
2. **Kleine Batches generieren**: 5-10 Personas zum Validieren der Einstellungen
3. **Skalieren**: Größere Batches (50-100) für Analysen generieren
4. **Library nutzen**: Muster analysieren und Daten für weitere Verwendung exportieren

## 🚀 **Schnellstart**

### Installation
```bash
# Abhängigkeiten installieren
pip install streamlit pandas plotly python-dotenv

# Mit UV (empfohlen)
uv pip install -r requirements.txt
```

### Konfiguration
```bash
# .env Datei erstellen
echo "SWISS_AI_PLATFORM_API_KEY=your_api_key_here" > .env
```

### Start
```bash
# Multi-Page App starten
streamlit run main_app.py

# Oder Single-Page Version
streamlit run streamlit_app.py
```

### Zugriff
1. Navigiere zu `http://localhost:8501`
2. Nutze die Seitenleiste zum Wechseln zwischen Seiten
3. Beginne mit "Single Persona" um das System zu verstehen
4. API Key eingeben (falls nicht in .env gesetzt)
5. Move to Batch Generation for bulk creation
6. Explore Persona Library for analysis and management

The system is now production-ready for comprehensive banking persona generation and analysis!