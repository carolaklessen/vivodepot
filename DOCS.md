# VIVODEPOT — Technische Dokumentation

*Version 1.0.0-beta.17 · April 2026*

---

## Architektur

VIVODEPOT ist eine **Einzeldatei-HTML-Anwendung** (~1,7 MB). Keine Build-Pipeline, kein Framework, kein CDN.

```
vivodepot/
├── VIVODEPOT.html              — Hauptanwendung
│   ├── CSS (eingebettet)
│   ├── Inline-Bibliotheken
│   │   ├── jsPDF 2.5.1         — PDF-Erstellung
│   │   ├── docx.js 8.5.0       — Word-Erstellung
│   │   ├── QRCode-Generator 1.4.4 — QR-Codes
│   │   └── jsQR 1.4.0          — QR-Code-Scan
│   └── JavaScript (Hauptlogik)
│       ├── Datenspeicherung (localStorage + AES-256-GCM)
│       ├── STEP_RENDERERS (22 Schritte)
│       ├── PROM-Funktionen (promCalcScore, promRenderRouting, ...)
│       ├── Export-Funktionen (16 Formate inkl. FHIR R4)
│       ├── Import-Funktionen (FHIR, FIM, JSON, EUDI, QR)
│       ├── Weitergabe-Datei-System (wg-*)
│       ├── QR-Übergabe-System (qr-* / qre-*) — URL-Format seit beta.10
│       ├── Solid Pod Export (sp-*)
│       ├── Wizard-System
│       └── Barrierefreiheits-Funktionen
├── vivodepot-lesen.html        — Eigenständige Empfänger-Seite (seit beta.10)
├── templates/                  — PROM-Vorlagen für Institutionen (seit beta.17)
│   ├── phq9-de-v1.json
│   ├── gad7-de-v1.json
│   ├── who5-de-v1.json
│   └── phq4-de-v1.json
└── test_vivodepot.py           — Regressions-Testscript
```

---

## PROM-Modul

### Übersicht

Das PROM-Modul (Patient-Reported Outcome Measures) implementiert validierte Selbstauskunft-Fragebögen. Alle Phase-1-Instrumente sind Public Domain und FHIR-konform.

### Hilfsfunktionen

| Funktion | Aufgabe |
|---|---|
| `promRadioRow(prefix, qnum, text)` | Rendert eine Frage mit Chip-Buttons |
| `promCalcScore(prefix, count)` | Berechnet Score aus gespeicherten Antworten; gibt `{score, answered, complete}` zurück |
| `promScoreBox(prefix, count)` | Rendert Ergebnis-Box mit Schweregrad und Farbe |
| `promRenderBlock(prefix, fragen)` | Rendert vollständigen Fragebogenblock |
| `promRenderRouting()` | PHQ-4-Routing: Subscore-Berechnung und Weiterleitungs-Box |
| `addPromEntries(cfg)` | FHIR-Export: erzeugt QuestionnaireResponse + Observation |
| `renderEhdsIndikator()` | EHDS-Konformitätsindikator-Block für Export-Step |

### Datenspeicherung (PROM)

Antworten werden als einzelne Felder gespeichert:

```
phq9_q1 … phq9_q9   — PHQ-9-Antworten (0–3)
phq9_score           — Berechneter Gesamtscore
phq9_datum           — Datum der Ausfüllung (ISO 8601)

gad7_q1 … gad7_q7   — GAD-7-Antworten
gad7_score, gad7_datum

who5_q1 … who5_q5   — WHO-5-Antworten
who5_score, who5_prozent, who5_datum

phq4_q1 … phq4_q4   — PHQ-4-Antworten
phq4_score, phq4_datum
```

### PHQ-4-Routing

Subscore-Berechnung nach Ausfüllen:

```
depScore = phq4_q1 + phq4_q2   (Depressivität, max 6)
anxScore = phq4_q3 + phq4_q4   (Angst, max 6)

depScore >= 3 → Routing-Box Stimmung → PHQ-9 (id="phq9-block")
anxScore >= 3 → Routing-Box Angst    → GAD-7 (id="gad7-block")
```

---

## FHIR R4 Export

### Ressourcen im Bundle

```
Bundle (collection)
├── Patient
├── AllergyIntolerance (0..n)
├── Condition (0..n)
├── MedicationStatement (0..n)
├── DeviceUseStatement (0..1)
├── QuestionnaireResponse — PHQ-9 (wenn complete)
├── Observation           — PHQ-9 Score
├── QuestionnaireResponse — GAD-7 (wenn complete)
├── Observation           — GAD-7 Score
├── QuestionnaireResponse — WHO-5 (wenn complete)
└── Observation           — WHO-5 Score (als Prozentscore ×4)
```

### LOINC-Codes

| Instrument | Fragebogen-Code | Score-Code |
|---|---|---|
| PHQ-9 | 44249-1 | 44261-6 |
| GAD-7 | 69737-5 | 70274-6 |
| WHO-5 | 71969-0 | 71969-0 |
| PHQ-4 | 69724-3 | — |

### PGHD-Tag

Alle PROM-Observations erhalten:

```json
"meta": {
  "tag": [{
    "system": "http://vivodepot.de/fhir/tag",
    "code": "pghd"
  }]
}
```

PGHD = Patient-Generated Health Data — explizite EHDS-Kategorie (Verordnung EU 2025/327).

---

## JSON-Vorlagen (Schema 1.0)

### Pflichtfelder

```json
{
  "schemaVersion": "1.0",
  "id": "phq9-de-v1",
  "version": "1.0.0",
  "locale": "de-DE",
  "title": { "short": "PHQ-9", "full": "PHQ-9 — Stimmung (letzte 2 Wochen)" },
  "issuer": { "name": "Kroenke, Spitzer & Williams" },
  "license": { "id": "Public Domain" },
  "loinc": { "code": "44249-1" },
  "instruction": "...",
  "scale": { "options": [...] },
  "items": [...],
  "scoring": { "method": "sum", "ranges": [...] },
  "safety": []
}
```

### PHQ-4-Erweiterungen

```json
"scoring": {
  "subscores": [
    { "id": "depression", "itemIds": ["PHQ4_01", "PHQ4_02"], "max": 6, "threshold": 3 },
    { "id": "anxiety",    "itemIds": ["PHQ4_03", "PHQ4_04"], "max": 6, "threshold": 3 }
  ],
  "routing": [
    { "when": { "subscoreId": "depression", "op": "gte", "value": 3 },
      "action": { "type": "recommend", "instrument": "phq9-de-v1" } },
    { "when": { "subscoreId": "anxiety", "op": "gte", "value": 3 },
      "action": { "type": "recommend", "instrument": "gad7-de-v1" } }
  ]
}
```

---

## EHDS-Alignierung

Vivodepot implementiert den bürgergesteuerten EHDS Citizen User Journey (Verordnung EU 2025/327, in Kraft seit März 2025).

| EHDS-Anforderung | Vivodepot-Status |
|---|---|
| FHIR R4 | Vollständig implementiert |
| EUPL-1.2 | Vollständig |
| Offline / kein Server | Vollständig |
| PGHD (Patient-Generated Health Data) | Tag im FHIR-Meta |
| HL7 EU Base IG 1.0 (R4) | Validierung ausstehend |
| Xt-EHR Patient Summary v0.2.1 | Mapping ausstehend |

---

## Datenspeicherung

### Primär: localStorage

```javascript
localStorage.setItem('vivodepot_v1_enc', JSON.stringify(verschluesselt));
```

### Verschlüsselung (optional)

- Algorithmus: AES-256-GCM
- Schlüsselableitung: PBKDF2-HMAC-SHA256 (**200.000 Iterationen**)
- Salt: 16 Byte, kryptographisch zufällig (Web Crypto API)
- IV: 12 Byte, kryptographisch zufällig

### Salt-Portabilität (seit beta.7)

`saveAsHTML()` bettet Salt in die HTML-Datei ein. Beim Öffnen auf einem neuen Gerät wird der Salt synchron wiederhergestellt — idempotent.

---

## Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

Die Testdatei erwartet die JSON-Vorlagen im Unterordner `templates/` relativ zur HTML-Datei.

**1459 Tests in 32 Sektionen — 1458 bestehen.**

| Sektionsbereich | Inhalt |
|---|---|
| 1–28 | Syntax, Bugs, Crypto, Navigation, Export, Import, QR, FHIR, Barrierefreiheit, ... |
| 29 | JSON-Vorlagen (PHQ-9, GAD-7, WHO-5, PHQ-4) |
| 30 | FHIR-PROM-Export |
| 31 | EHDS-Indikator |
| 32 | PHQ-4-Routing-UI |

---

## Dateiübersicht

| Datei | Größe | Inhalt |
|---|---|---|
| `VIVODEPOT.html` | ~1,7 MB | Hauptanwendung (vollständig selbsttragend) |
| `vivodepot-lesen.html` | ~300 KB | Empfänger-Seite |
| `templates/*.json` | < 5 KB je | PROM-Vorlagen (Schema 1.0) |
| `test_vivodepot.py` | ~120 KB | Regressions-Testscript |
