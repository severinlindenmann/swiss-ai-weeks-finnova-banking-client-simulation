Wir möchten Personas generieren, dafür geben wir dir die Daten einer Person und du generierst dafür ein Banking Persona. 

| Spaltenname (Deutsch)               | Spaltenname (CSV)         | Beschreibung                                                                                     |
|--------------------------------------|----------------------------|-------------------------------------------------------------------------------------------------|
| Haushaltsgröße                      | hhgroesse                  | Anzahl der Personen im Haushalt.                                                                |
| Alter                                | alter                      | Alter der Person in Jahren.                                                                     |
| Erwerbstätig                         | arbeit                     | Binär: 1 = erwerbstätig, 0 = nicht erwerbstätig.                                                 |
| Betriebszugehörigkeit (Tage)        | tenure                     | Dauer der Betriebszugehörigkeit in Tagen.                                                      |
| Führungsposition                     | leitung                    | Binär: 1 = Führungsposition, 0 = keine Führungsposition.                                        |
| Beschäftigungsgrad (%)               | beschaeftgrad              | Beschäftigungsgrad in Prozent.                                                                  |
| Geburtsjahr                          | gebjahr                    | Geburtsjahr der Person.                                                                         |
| Schweizer Staatsangehörigkeit       | schweizer                  | Binär: 1 = Schweizer Staatsangehörigkeit, 0 = keine Schweizer Staatsangehörigkeit.             |
| Gewichtungsfaktor                    | gewichte                   | Gewichtungsfaktor für die Stichprobe.                                                           |
| Bruttojahreseinkommen (CHF)          | bruttojahr                 | Bruttojahreseinkommen in Schweizer Franken.                                                     |
| Kinder im Haushalt                   | kinder                     | Binär: 1 = Kinder im Haushalt, 0 = keine Kinder im Haushalt.                                    |
| Deutschschweiz                       | deutschschweiz             | Binär: 1 = Wohnort in der Deutschschweiz, 0 = Wohnort nicht in der Deutschschweiz.               |
| Wohnort Zürich                       | amzuerich                  | Binär: 1 = Wohnort im Kanton Zürich, 0 = Wohnort nicht im Kanton Zürich.                        |
| Ledig                                | ledig                      | Binär: 1 = ledig, 0 = nicht ledig.                                                              |
| Großbetrieb                          | grossbetrieb               | Binär: 1 = Beschäftigung in einem Großbetrieb, 0 = keine Beschäftigung in einem Großbetrieb.   |
| Ausbildungsdauer (Jahre)             | ausbildungsdauer           | Dauer der Ausbildung in Jahren.                                                                 |
| Kanton                               | kanton                     | Kanton des Wohnorts.                                                                            |
| Gemeindetyp                          | gemeindetyp                | Typ der Wohngemeinde (z. B. ländlich, periurban, urban).                                        |
| Sprachgebiet                         | sprachgebiet               | Sprachgebiet (z. B. deutsch, französisch).                                                     |
| Region                               | amregion                   | Region des Wohnorts.                                                                            |
| Gebietstyp                           | gebiettyp                  | Typ des Gebiets (z. B. Agglomerationsgemeinde, ländliche Gemeinde).                            |
| Großregion                           | grossregion                | Großregion der Schweiz (z. B. Espace Mittelland, Zentralschweiz).                               |
| Unterstellte Mitarbeiter             | unterstellte               | Anzahl der unterstellten Mitarbeiter (z. B. "3 Personen").                                      |
| Arbeitsort                           | arbeitsort                 | Art des Arbeitsorts (z. B. "Fester Arbeitsort außerhalb Wohnung").                              |
| Familienstand                        | fam_status                 | Familienstand (z. B. verheiratet, ledig).                                                      |
| Berufsgruppe                         | beruf                      | Berufsgruppe der Person (z. B. "Fachkräfte in Land- und Forstwirtschaft").                      |
| Erwerbsstatus                        | erwerbsstatus              | Erwerbsstatus (z. B. Arbeitnehmer, Selbständige).                                               |
| Ausbildung                           | ausbildung                 | Art der Ausbildung (z. B. "Obligatorische Grundschule", "Universität, ETH, FH, PH").           |
| Bildungsniveau                       | bildungsniveau             | Höchstes erreichtes Bildungsniveau (z. B. Sekundarstufe I, Tertiärstufe).                       |
| Position                             | position                   | Position im Beruf (z. B. "Arbeitnehmer mit Vorgesetztenfunktion").                              |
| Weiblich                             | weiblich                   | Binär: 1 = weiblich, 0 = männlich.                                                              |
| Letzter Job                          | letzterjob                  | Bezeichnung des letzten Jobs (z. B. "Führungskräfte").                                          |
| ID                                   | id                         | Eindeutige Identifikationsnummer der Person.                                                     |
| Teilzeit (Dummy)                     | Teilzeit_Dummy             | Binär: 1 = Teilzeitbeschäftigung, 0 = Vollzeitbeschäftigung.                                    |

Personen Daten
{PersonData}