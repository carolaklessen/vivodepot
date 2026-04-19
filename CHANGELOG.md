# VIVODEPOT — Änderungsprotokoll

Alle wichtigen Änderungen werden in dieser Datei dokumentiert.

---

## [1.0.0-beta.17] — April 2026

### Neu

- **PROM-Modul Phase 1 vollständig** — Alle vier Public-Domain-Fragebögen implementiert, FHIR-konform exportierbar, EHDS-aligniert.

- **PHQ-4 Routing-UI** — Nach Ausfüllen des PHQ-4-Ultrakurzscreenings erscheint automatisch ein Hinweis mit Schaltfläche: bei Depressivitäts-Subscore ≥ 3 → PHQ-9, bei Angst-Subscore ≥ 3 → GAD-7. Scrollen direkt zum Fragebogen. Kein Routing bei unvollständigem PHQ-4.

- **FHIR-Export: PROM-Ressourcen** — `generateFHIR()` erzeugt für jeden vollständig ausgefüllten PROM zwei neue FHIR-Ressourcen: `QuestionnaireResponse` (Einzelantworten mit LOINC-Fragebogen-Code) und `Observation` (Gesamtscore mit LOINC-Score-Code). WHO-5 als Prozentscore (×4). PGHD-Tag (`Patient-Generated Health Data`) im `meta.tag` — explizite EHDS-Kategorie.

- **EHDS-Konformitätsindikator** — Statischer Block im Export-Step. Zweischichtig: Bürger-Schicht in einfacher Sprache, Institutions-Schicht mit technischem Zertifizierungssignal (FHIR R4 · HL7 EU Base IG 1.0 · PGHD · EUPL-1.2). Grüner linker Rand, ARIA-konform.

- **JSON-Vorlagen: Ordner `templates/`** — Alle vier PROM-Vorlagen im neuen Unterordner `templates/`. Standardisiertes Schema 1.0: Pflichtfelder, LOINC-Codes, Scoring-Bereiche, Safety-Regeln.

### JSON-Vorlagen (Schema 1.0)

| Datei | Instrument | Items | Skala | Max | LOINC |
|---|---|---|---|---|---|
| `phq9-de-v1.json` | PHQ-9 Stimmung | 9 | 0–3 | 27 | 44249-1 |
| `gad7-de-v1.json` | GAD-7 Angst | 7 | 0–3 | 21 | 69737-5 |
| `who5-de-v1.json` | WHO-5 Wohlbefinden | 5 | 0–5 | 25 | 71969-0 |
| `phq4-de-v1.json` | PHQ-4 Kurzscreening | 4 | 0–3 | 12 | 69724-3 |

PHQ-4 enthält zusätzlich `scoring.subscores` (Depression, Angst) und `scoring.routing` (Weiterleitung zu PHQ-9 bzw. GAD-7 bei Subscore ≥ 3).

### FHIR-LOINC-Codes

| Instrument | Fragebogen | Score |
|---|---|---|
| PHQ-9 | 44249-1 | 44261-6 |
| GAD-7 | 69737-5 | 70274-6 |
| WHO-5 | 71969-0 | 71969-0 |

### Tests

101 neue Tests in 4 neuen Sektionen:

| Sektion | Inhalt | Tests |
|---|---|---|
| 29 | JSON-Vorlagen: Pflichtfelder, Schema, Lückenlosigkeit, Safety, PHQ-4-Subscores/Routing | 58 |
| 30 | FHIR-PROM-Export: QuestionnaireResponse, Observation, LOINC-Codes, PGHD-Tag | 25 |
| 31 | EHDS-Indikator: Funktion, Texte, CSS, ARIA, Export-Step-Einbindung | 17 |
| 32 | PHQ-4-Routing-UI: Subscore-Berechnung, Schwellenwert, Texte, CSS, ARIA, Scroll-Ziele | 24 |

Gesamt: **1459 Tests, 1458 bestehen.** (1 schlägt nur außerhalb des Repos fehl: SOVEREIGNTY.md-Pfadtest)

### Dateien

| Datei | Änderung |
|---|---|
| `VIVODEPOT.html` | FHIR-PROM-Export, EHDS-Indikator, PHQ-4-Routing-UI, PHQ4_FRAGEN |
| `test_vivodepot.py` | +101 Tests (Sektionen 29–32), Pfad auf `templates/` |
| `templates/phq9-de-v1.json` | Neu |
| `templates/gad7-de-v1.json` | Neu |
| `templates/who5-de-v1.json` | Neu |
| `templates/phq4-de-v1.json` | Neu |

---

## [1.0.0-beta.11] — April 2026

### Neu

- **Schritt „Wohlbefinden & Seele" (PROM)** — Neuer Schritt nach „Meine Gesundheit" mit drei gemeinfreien, validierten Selbstauskunft-Fragebögen: PHQ-9 (Stimmung, 9 Fragen, Score 0–27), GAD-7 (Angst, 7 Fragen, Score 0–21) und WHO-5 (Wohlbefinden, 5 Fragen, Score 0–25 / 0–100 %). Antworten werden als Chip-Buttons ausgewählt; Score und Schweregrad erscheinen automatisch nach der letzten Antwort. Alle Ergebnisse werden im Autosave gespeichert. Datenschutzhinweis, Quellenangaben und Haftungsausschluss direkt im Schritt sichtbar. Fokus-Ziel „Für den Arztbesuch" enthält den neuen Schritt.

- **QR-Export: PROM-Scores im Notfall-Profil** — Das QR-Übergabe-Profil „Notfall" enthält jetzt automatisch PHQ-9-Score und -Datum, GAD-7-Score und -Datum sowie WHO-5-Score, Prozentwert und Datum.

### Tests

35 neue Tests in 2 neuen Sektionen:

| Sektion | Inhalt | Tests |
|---|---|---|
| 66 | PROM: STEPS-Eintrag, Zeitmessung, Fokus-Ziel, Arrays, Hilfsfunktionen, Score-Logik, Renderer, Quellenangaben | 24 |
| 67 | QR-PROM: PROM-Felder im notfall-Profil, lesbare Feldnamen | 11 |

Gesamt: **1086 Tests, 1085 bestehen.**

### Dateien

| Datei | Änderung |
|---|---|
| `VIVODEPOT.html` | Neuer Schritt prom, 4 Hilfsfunktionen, QR-Profilerweiterung |
| `test_vivodepot.py` | +35 Tests (Sektionen 66–67) |

---

## [1.0.0-beta.10] — April 2026

- **vivodepot-lesen.html** — Eigenständige Leseansicht für QR-Übergabe und Weitergabe-Dateien.
- **QR-Übergabe: URL-Format mit Hash-Fragment** — Payload erreicht Server nie.
- **QR-Übergabe: Mehr-Teile-QR** — Bis zu 6 QR-Codes für größere Datensätze.
- UX-Korrekturen ANF-UX-01 bis ANF-UX-07.

Gesamt: **1051 Tests, 1050 bestehen.**

---

## [1.0.0-beta.9] — April 2026

- Solid Pod Export (Turtle, .ttl), Datenaustausch-Step.

Gesamt: 1093 Tests, 0 Fehler.

---

## [1.0.0-beta.8] — April 2026

Weitergabe-Datei (4 Profile), QR-Übergabe, Einkommensdaten, Kind-Daten, EUDI-Wallet, FHIR.

Gesamt: 1050 Tests, 0 Fehler.

---

## [1.0.0-beta.7] — April 2026

BUG-SALT behoben: Salt in gespeicherter Datei eingebettet.

---

## [1.0.0-beta.6] — April 2026

Offline-Vollständigkeit, Notfall & Katastrophenschutz, Barrierefreiheit, BUG-10, BUG-11.

---

## [1.0.0-beta.5] — März 2026

Fokus-System, Einstiegs-Wizard, Multi-Profil, Angehörigen-Ansicht, Diktat-Eingabe.

---

## [1.0.0-beta.4] — Februar 2026

Weiche Inhaberin / Angehörige/r, 20 Schritte.

---

## [1.0.0-beta.3] — Januar 2026

AES-256-GCM, saveAsHTML(), vCard 4.0, FHIR R4, QR-Aufkleber, Arztbogen PDF.

---

## [1.0.0-beta.1] — Dezember 2025

Erste Version — Notfallmappe als PDF und Word, 17 Dateneingabe-Schritte.
