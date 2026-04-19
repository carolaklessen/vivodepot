# VIVODEPOT — Änderungsprotokoll

Alle wichtigen Änderungen werden in dieser Datei dokumentiert.

---

## [1.0.0-beta.14] — April 2026

### UX-Optimierung für Senioren (Schwerpunkt dieser Version)

Diese Version konzentriert sich vollständig auf Nutzbarkeit, Barrierefreiheit
und technische Robustheit — keine neuen Funktionen, aber eine substanziell
bessere Erfahrung für die Zielgruppe (60+, nicht digital-affin).

### Behobene Bugs

- **Scroll-Sprung bei Listenoperationen** — `addItem()`, `moveItem()`, `removeItem()`
  ersetzten bisher das gesamte `mc.innerHTML`, was auf iOS den Scroll-Container
  zurücksetzte. Neue Lösung: `refreshList(key)` aktualisiert nur den betroffenen
  Container-Div ohne `mc.innerHTML` anzufassen. Kein Scroll-Sprung mehr auf
  keinem Browser, inkl. DuckDuckGo/iOS.

- **`mehr()`-Sektion klappt nach Daten-Eingabe zu** — `mehr()` renderte Sektionen
  immer mit `display:none`. Nach jedem `renderStep()` blieb die Sektion zu,
  auch wenn Daten vorhanden waren. Fix: `isOpen = filled > 0` beim Rendern.

- **`mehrToggle()` zeigt „Weniger anzeigen" statt Sektionsname** — beim manuellen
  Öffnen einer bereits-daten-gefüllten Sektion erschien generischer Text statt
  des Sektionstitels. Behoben.

- **Sortier-Pfeile ▲▼ Unicode unzuverlässig** — auf manchen Systemen leer
  dargestellt. Durch SVG-Icons ersetzt (alle drei Buttons im Block-Header:
  rauf, runter, entfernen).

- **Minutenanzeige in Schrittüberschrift** — handgeschriebene Schätzwerte
  (immer gleich, unabhängig vom Füllstand) entfernt. Zeigt jetzt klaren Text
  „X von Y Bereichen ausgefüllt".

### Neue Struktur: Wiederholungsmasken

- **Volljährige Kinder** — Neues `renderKinderErwachsenBlocks()` mit Feldern
  Vorname, Nachname, Geburtsjahr, Wohnort, Telefon, Anmerkung. Ersetzt das
  frühere Einzeltextfeld. Unbegrenzt erweiterbar.

- **Unterhaltspflichten** — Neues `renderUnterhaltBlocks()` mit Feldern Person,
  Art (Kindes-/Ehe-/Trennungs-/Elternunterhalt/Sonstiges), Betrag, Richtung
  (Ich zahle/Ich erhalte), Anmerkung. Jede Pflicht einzeln dokumentierbar.

- **Export-Helfer** — `getKinderMjText()`, `getKinderErwText()`,
  `getUnterhaltText()` formatieren die neuen Listen für alle 31 Export-Aufrufe
  (PDFs, Szenario-PDF, Katastrophenschutzplan, FIM-Export, QR-Sticker).
  Rückwärtskompatibel: Fallback auf alte Einzeltextfelder.

### Icons und Darstellung

- **Alle Emojis durch SVG ersetzt** — Topbar (9 Icons), Export-Karten (23),
  Notfall-FAB, blockHeader-Pfeile, Fokus-Wizard (5 Ziel-Icons). Kein Rendering-
  Risiko mehr auf altem Windows oder Safari.

- **Eingabefelder**: Schriftgrösse 0.88rem → 1rem (16px). Labels, Buttons,
  Hilfstext, Warn-/OK-Meldungen ebenfalls angehoben.

- **Hilfstext** (`.field-hint`): Kursivschrift entfernt, Farbe aufgehellt.
  Kursiv + klein + gedimmt war dreifach schwer lesbar.

### Navigation und Orientierung

- **Alle Bereiche ohne Fokus sichtbar** — vorher wurden 14 von 22 Bereichen
  hinter einem kleinen Toggle versteckt. Ohne gewählten Fokus sind jetzt
  alle Bereiche sichtbar.

- **Fokus-Button repositioniert** — ohne Fokus erscheint „Thema wählen …"
  direkt oben in der Sidebar (nach Startseite-Button). Mit Fokus: subtil
  am unteren Rand als „▷ Thema ändern".

- **Mobile Step-Picker** — Counter in der Bodenleiste (z.B. „3/22") ist
  klickbar und öffnet ein Sheet mit allen Bereichen zum direkten Springen.
  Vorher: nur lineares ←/→.

- **Navigationsbegriffe** — 6 Bereiche erhalten Untertitel (`.nav-sub`)
  in einfacher Sprache, z.B. „Mein Wille → Vollmacht · Verfügung · Testament".

### Sprache und Konsistenz

- „Fokus" → „Thema" durchgehend (Sidebar, Wizard, mobile Bar)
- „App sperren" → „Bildschirm sperren" (Tooltip und Bestätigungsdialog)
- Bestätigungstext bei Bildschirmsperre erklärt was passiert
- Fokus-Wizard-Titel: „Welchen Fokus möchten Sie setzen?" →
  „Welches Thema möchten Sie bearbeiten?"

### Barrierefreiheit

- `for/id`-Verknüpfung in allen Wiederholungsblöcken (Kinder, Erwachsene, Unterhalt)
- `aria-label` auf Mikrofon-Button (beide Stellen)
- `aria-label` auf Notfall-FAB
- `autocomplete`-Attribute auf Standardfelder (Name, Telefon, Adresse, Datum)
- `SOVEREIGNTY.md` erstellt mit WCAG 3.3.8-Begründung

### Tests

10 neue Tests, 4 veraltete Tests aktualisiert:

| Änderung | Grund |
|---|---|
| `Thema-Button in Sidebar` (war: Fokus) | Umbenennung |
| `preserveScroll in renderStep` (war: times-Objekt) | Feature entfernt |
| `refreshList-Funktion vorhanden` (war: institutionen:2) | Neue Architektur |
| `aria-label Bildschirm sperren` (war: 🔒-Emoji) | SVG-Ersatz |
| Minifizierte Bibliotheken überspringen (jsPDF) | False Positive |
| `SESSION: renderKinderErwachsenBlocks` | Neue Funktion |
| `SESSION: renderUnterhaltBlocks` | Neue Funktion |
| `SESSION: getKinderMjText/Erw/Unterhalt` | Export-Helfer |
| `SESSION: vd-list Container-IDs` | Neue Architektur |
| `SESSION: showStepPicker` | Mobile Navigation |
| `SESSION: Thema-Konsistenz` | Sprach-Audit |
| `SESSION: keine Emoji in ec-icon` | Icon-Audit |

**Gesamt: 1342 Tests, 1342 grün.**

### Dateien

| Datei | Änderung |
|---|---|
| `VIVODEPOT.html` | UX-Überarbeitung, Bug-Fixes, neue Masken, Export-Helfer |
| `test_vivodepot.py` | 10 neue Tests, 4 aktualisiert, minif. Libs übersprungen |
| `SOVEREIGNTY.md` | Neu — WCAG 3.3.8-Begründung |

---

## [1.0.0-beta.17] — April 2026

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
