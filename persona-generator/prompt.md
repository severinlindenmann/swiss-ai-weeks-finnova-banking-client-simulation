# Banking-Persona Generator Prompt

Generiere eine detaillierte Banking-Persona basierend auf den folgenden statistischen Eingabedaten einer realen Person. Die Persona soll für die Simulation von Banking-Verhalten verwendet werden.

## Eingabedaten (Input-Parameter)

### Statistische Basisdaten:
{statistical_data}

### Demografische Zusatzinformationen:
- **Alter**: {alter} Jahre
- **Geschlecht**: {geschlecht} (m/w)
- **Freies Vermögen**: {vermoegen} (< 10k, 10k-100k, >100k)
- **Verfügbares Einkommen**: {verfuegbares_einkommen} (Einkommen - Ausgaben: < 60k, 60k-100k, >100k)
- **Geplante größere Ausgaben/Investitionen**: {grosse_ausgaben} (ja/nein)
- **Job/Beruf**: {beruf}
- **Kinder**: {kinder} (ja=1/nein=0)
- **Wohnsituation**: {eigentum} (Eigentum=1/Miete=0)
- **Beziehungsstatus**: {single} (Single=1/Partnerschaft=0)
- **Erfahrung mit Finanzprodukten**: {finanz_erfahrung} (Einsteiger/Fortgeschritten/Experte)

## Aufgabe

Erstelle eine kohärente Banking-Persona, die:
1. **Alle statistischen Daten** logisch in eine stimmige Persönlichkeit integriert
2. **Realistische Banking-Bedürfnisse** basierend auf der Lebenssituation entwickelt
3. **Schweizer Kontext** berücksichtigt (regional, kulturell, sprachlich)
4. **Finanzverhalten** authentisch aus den Daten ableitet

## Gewünschtes JSON-Output-Format

```json
{{
  "persona_id": "string",
  "basic_info": {{
    "name": "string (Schweizer Vorname + Nachname)",
    "age": "number",
    "gender": "string (männlich/weiblich)",
    "nationality": "string",
    "languages": ["string"] 
  }},
  "demographics": {{
    "canton": "string",
    "municipality_type": "string (urban/periurban/rural)",
    "region": "string",
    "household_size": "number",
    "marital_status": "string",
    "children": "boolean",
    "housing": "string (owner/renter)"
  }},
  "professional": {{
    "employment_status": "string",
    "job_title": "string",
    "industry": "string",
    "company_size": "string",
    "employment_percentage": "number",
    "leadership_position": "boolean",
    "work_location": "string",
    "tenure_years": "number"
  }},
  "financial": {{
    "annual_gross_income_chf": "number",
    "disposable_income_category": "string (< 60k, 60k-100k, >100k)",
    "net_worth_category": "string (< 10k, 10k-100k, >100k)",
    "planned_major_expenses": "boolean",
    "financial_experience": "string (Einsteiger/Fortgeschritten/Experte)"
  }},
  "banking_persona": {{
    "risk_tolerance": "string (konservativ/ausgewogen/risikofreudig)",
    "investment_interest": "string (niedrig/mittel/hoch)",
    "banking_preferences": {{
      "channel_preference": "string (online/mobile/filiale/hybrid)",
      "service_level": "string (selbständig/beratung/premium)",
      "product_complexity": "string (einfach/standard/komplex)"
    }},
    "financial_goals": ["string"],
    "pain_points": ["string"],
    "banking_frequency": "string (täglich/wöchentlich/monatlich)"
  }},
  "personality": {{
    "traits": ["string"],
    "values": ["string"],
    "lifestyle": "string",
    "technology_affinity": "string (niedrig/mittel/hoch)",
    "decision_making_style": "string (spontan/überlegt/analytisch)"
  }},
  "narrative": {{
    "life_story": "string (2-3 Sätze Hintergrundgeschichte)",
    "current_situation": "string (aktuelle Lebensphase)",
    "future_aspirations": "string (Ziele und Träume)",
    "typical_day": "string (kurzer Einblick in den Alltag)"
  }},
  "banking_scenarios": {{
    "likely_products": ["string"],
    "service_triggers": ["string"],
    "communication_preferences": ["string"],
    "loyalty_factors": ["string"]
  }}
}}
```

## Wichtige Hinweise

1. **Konsistenz**: Alle Werte müssen sich logisch aus den Eingabedaten ableiten lassen
2. **Schweizer Kontext**: Namen, Orte und kulturelle Referenzen sollen authentisch Schweizer sein
3. **Banking-Relevanz**: Fokus auf Eigenschaften, die Banking-Entscheidungen beeinflussen
4. **Realismus**: Keine Extreme oder Klischees, sondern glaubwürdige Durchschnittspersonen
5. **Sprachliche Konsistenz**: Deutsche Begriffe, an Schweizer Kontext angepasst
6. **JSON-Format**: Antworte ausschließlich mit gültigem JSON - keine Erklärungen oder zusätzlicher Text

## Ausgabeanforderung

Generiere nun die Banking-Persona basierend auf den obigen Eingabedaten. 

**KRITISCH WICHTIG: 
- Antworte ausschließlich mit dem JSON-Objekt
- Beginne die Antwort direkt mit {{
- Keine Erklärungen, kein zusätzlicher Text
- Keine Markdown-Formatierung
- Kein ```json oder ```
- Keine Kommentare im JSON (// text ist verboten)
- Reines, valides JSON ohne jegliche Anmerkungen** 