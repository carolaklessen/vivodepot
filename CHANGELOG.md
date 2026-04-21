# VIVODEPOT — Änderungsprotokoll

Alle wichtigen Änderungen werden in dieser Datei dokumentiert.

---

## [1.0.0-beta.16] — April 2026

### Lastenheft v2 vollständig abgearbeitet

Diese Version schließt alle Anforderungen aus dem Lastenheft v2 ab und
enthält außerdem alle Änderungen aus beta.15, die bislang nicht mit einer
Versionsnummer veröffentlicht worden waren.

### Neu — Vorlagen-Editor für Institutionen (P1, Sektion 81)

- **Vorlagen direkt in der App erstellen** — Kein Texteditor, kein JSON-Wissen
  erforderlich. Neuer Button „Neue Vorlage erstellen" im Institutionen-Bereich
  öffnet den Editor direkt in der App.
- **Editor-Felder:** Kurztitel, vollständiger Titel, Herausgeber, Antwort-Skala
  (Optionen hinzufügen/entfernen, Wert und Bezeichnung), Fragen
  (hinzufügen/entfernen, Reihenfolge durch Position).
- **Vorschau** — Zeigt den Fragebogen vor dem Speichern in der App-Ansicht.
- **Zwei Ausgabewege:** In App speichern (localStorage, direkt verwendbar) oder
  als `.json`-Datei herunterladen (für externe Weitergabe).
- **Validierung** — `tplValidate()` wird vor jedem Speichern und vor jedem
  Export aufgerufen. Fehlermeldung listet alle Probleme verständlich auf.
- **Scoring automatisch** — Ranges werden aus Skala und Fragenanzahl berechnet;
  kein manueller Eingriff erforderlich (manuell anpassbar nach Export).
- **Schließen mit Rückfrage** — `vivoConfirm()` verhindert versehentlichen
  Datenverlust.
- Nicht enthalten (bewusst ausgeschlossen): Verzweigungslogik, Safety-Regeln
  per UI, Mehrsprachige Vorlagen.
- **Neue Funktionen (13):** `tplEditorNew`, `tplEditorClose`, `tplEditorReadForm`,
  `tplEditorAddItem`, `tplEditorRemoveItem`, `tplEditorAddOption`,
  `tplEditorRemoveOption`, `tplEditorTogglePreview`, `tplEditorBuildTemplate`,
  `tplEditorSave`, `tplEditorExport`, `tplEditorRender`.

### Neu — Inline-Feedback-Formular (P2, Sektion 82)

- **Fallback für hilfe@vivodepot.de** — Das mailto:-Link öffnet auf älteren
  Android-Geräten nicht zuverlässig. Das Formular ist als robuste Alternative
  immer erreichbar.
- **Einstiegspunkte:** More-Menu-Eintrag „Hilfe — hilfe@vivodepot.de" und
  neuer Button „E-Mail-App klappt nicht? Formular öffnen" in Einstellungen.
- **Formular:** Textarea mit Platzhaltertext. Gerät, Browser und Version werden
  automatisch angehängt — kein manuelles Kopieren nötig.
- **Zwei Ausgabewege:** „Per E-Mail senden" öffnet die E-Mail-App fertig
  ausgefüllt. „Text kopieren" legt den Text in die Zwischenablage (Clipboard-API
  mit execCommand-Fallback für ältere Browser).
- Kein Server. Kein Datei-Upload.
- **Neue Funktionen (6):** `feedbackOpen`, `feedbackClose`, `feedbackBuildText`,
  `feedbackSend`, `feedbackCopy`, `feedbackCopyFallback`.

### Neu — Prüftermin-Erinnerungen (P3, Sektion 83)

- **Primär: Web Notifications API** — In Einstellungen (neuer Block
  „Prüftermin-Erinnerungen") per Button aktivierbar. Erlaubnis wird nie
  automatisch angefragt. Max. eine Benachrichtigung pro Tag. Alle fälligen
  Einträge in einer einzigen Meldung zusammengefasst. Unterscheidet
  „bald fällig" (11–14 Monate) und „überfällig" (>14 Monate).
- **Fallback: Hinweis-Balken** — Amber-Balken am oberen Rand, erscheint nur
  bei tatsächlich überfälligen Einträgen (>14 Monate), nicht blockierend,
  kein Erlaubnis-Popup. Schaltflächen: „Jetzt prüfen" (navigiert direkt zum
  Prüftermine-Schritt) und „Schließen" (gilt für diese Sitzung).
- Prüft alle 7 Dokumenttypen: Vorsorgevollmacht, Gesundheitsvollmacht,
  Patientenverfügung, Testament, Bankvollmacht, Schwerbehindertenausweis,
  Vivodepot (diese Datei).
- Status-Anzeige in Einstellungen: Aktiviert / Nicht aktiviert /
  Vom Browser blockiert / Nicht unterstützt (iOS).
- **Neue Funktionen (6):** `erinnerungFaelligeItems`, `erinnerungNotifRequest`,
  `erinnerungNotifSend`, `erinnerungNotifCheck`, `erinnerungHinweisShow`,
  `erinnerungHinweisHide`.

### Tests

77 neue Tests in 3 neuen Sektionen:

| Sektion | Inhalt | Tests |
|---|---|---|
| 81 | Vorlagen-Editor: Zustand, Funktionen, Validierung, Renderer, Export | 27 |
| 82 | Inline-Feedback-Formular: Overlay, Funktionen, Clipboard, kein Server | 21 |
| 83 | Prüftermin-Erinnerungen: Balken, Funktionen, Web Notifications, Einstellungen | 29 |

Gesamt: **1.499 Tests, 0 Fehler, 0 Altlasten.**

### Dateien

| Datei | Änderung |
|---|---|
| `VIVODEPOT.html` | Vorlagen-Editor, Feedback-Formular, Prüftermin-Erinnerungen, Version 1.0.0-beta.16 |
| `test_vivodepot.py` | +77 Tests (Sektionen 81–83) |

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

### IPS-Upgrade — FHIR-Export (beta.14)

- **IPS-Dokument-Export** — `generateFHIR()` erzeugt jetzt ein vollständiges
  IPS-Dokument (`Bundle.type: document`) statt einer FHIR-Collection.
  Erste Ressource ist eine `Composition` mit LOINC-Sektionen.

- **IPS-Validierung** — Validator-Ergebnis gegen `hl7.fhir.uv.ips 2.0.0`
  und `hl7.fhir.eu.base 2.0.0-ballot`: **0 Fehler, 0 Warnungen.**

- **17 Validator-Fehler behoben** — echte UUIDs für alle Ressourcen,
  valide URI in `meta.source`, IPS-Profile in allen Ressourcen (`meta.profile`),
  `section.text` (Narrativ) in jeder Sektion, drei Pflichtsektionen immer
  vorhanden (mit `emptyReason` wenn leer), `verificationStatus` in
  AllergyIntolerance, Blutgruppe als `Observation` statt ungültiger Extension.

- **Syntaxfehler in Bibliotheken behoben** — 13 rohe Control-Characters
  (jsPDF: `0x01`, ZIP: `0x03`–`0x07`, Farbbibliothek: `0x1B`) durch
  `\xNN`-Escapes ersetzt. Behebt `Uncaught SyntaxError` in der Browser-Konsole.

- **Dateiname:** `IPS_Nachname_Datum.fhir.json`

### Tests

10 neue UX-Tests, 4 veraltete Tests aktualisiert, 37 neue IPS/Bibliotheks-Tests:

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
| Abschnitt 74: IPS-Upgrade (33 Tests) | IPS-Konformität |
| Abschnitt 75: Bibliotheken (4 Tests) | Syntaxfehler-Prüfung |

### Konformitätsnachweise

| Datei | Profil | Ergebnis |
|---|---|---|
| `Vivodepot_HL7_Konformitaetsbericht_2026-04-19.docx` | hl7.fhir.eu.base 2.0.0-ballot | 0 Fehler, 0 Warnungen |
| `Vivodepot_IPS_Konformitaetsbericht_2026-04-20.docx` | hl7.fhir.uv.ips 2.0.0 | 0 Fehler, 0 Warnungen |

### Dateien

| Datei | Änderung |
|---|---|
| `VIVODEPOT.html` | UX-Überarbeitung, IPS-Upgrade, Syntaxfehler-Fix |
| `test_vivodepot.py` | 10 neue UX-Tests, 37 neue IPS/Bibliotheks-Tests |
| `SOVEREIGNTY.md` | Neu — WCAG 3.3.8-Begründung |
| `Vivodepot_HL7_Konformitaetsbericht_2026-04-19.docx` | Neu — HL7 EU Base IG Konformitätsnachweis |
| `Vivodepot_IPS_Konformitaetsbericht_2026-04-20.docx` | Neu — IPS 2.0.0 Konformitätsnachweis |

---

## [1.0.0-beta.15] — April 2026

### Neu — Datenweitergabe an Institutionen

- **DSGVO-Einwilligungsdokumentation im FHIR-Export** — `generateFHIR()` erzeugt
  jetzt eine `Consent`-Ressource mit Status `active`, Scope `patient-privacy`,
  LOINC-Code 59284-0, GDPR-Art.-6-Policy-URI, Zweck `TREAT` und einer Extension
  mit der Liste der exportierten Sektionen. UUID wird pro Export neu generiert.

- **Institutionelles Request-Template** — `downloadInstitutionTemplate()` erzeugt
  eine herunterladbare Muster-Vorlage (`Vivodepot_Muster_Vorlage_v1.json`) im
  Companion-Schema 1.0. Enthält Beispielfragen, Skala, Scoring und leeres
  Safety-Array. Button „Muster-Vorlage herunterladen" im Institutionen-Bereich.

- **Supportkanal** — E-Mail-Adresse `hilfe@vivodepot.de` in Einstellungen
  (Block „Hilfe & Kontakt" mit Schaltfläche „Nachricht schreiben") und im
  More-Menu (Link „Hilfe — hilfe@vivodepot.de" mit vorausgefülltem Betreff
  und Körper). Institutionen-Bereich: `support@vivodepot.de`.

### E-Mail-Migration

- `feedback@vivodepot.de` vollständig durch `hilfe@vivodepot.de` (sichtbarer
  Bereich) und `support@vivodepot.de` (Institutionen) ersetzt.

### Technische Schuld bereinigt — Einstellungen

- **Doppelter Fokus-Abschnitt entfernt** — Ein redundanter erster Fokus-Block
  in den Einstellungen (Zeile ~16838) wurde entfernt. Der funktionale zweite
  Block (zeigt aktuellen Zustand, „Fokus ändern", „Alle anzeigen") bleibt.
  Neuer Test (Sektion 79) sichert Einmaligkeit dauerhaft ab.

### Neu — Lokale Nutzungsstatistik (Sektion 80)

- **Drei neue Funktionen:** `statsIncrement()`, `statsGet()`, `statsRenderBlock()`.
- **Vier Zähler** im localStorage — kein Server, keine Übertragung:
  - `vivo_stat_fhir_export` — Anzahl FHIR-Exporte + Datum des letzten
  - `vivo_stat_template_download` — Anzahl Muster-Vorlage-Downloads
  - `vivo_stat_tpl_complete` — Anzahl vollständig ausgefüllter Vorlagen
  - `vivo_stat_result_download` — Anzahl Ergebnis-Downloads (`tplDownloadFhir`)
- **Anzeigeblock** in Einstellungen unter „Über Vivodepot" — natürlichsprachliche
  Sätze, z.B. „Sie haben Vivodepot 7 Mal exportiert."

### Neu — STEP_TIMES-Objekt

- **Geschätzte Bearbeitungszeiten** für alle Schritte als JavaScript-Objekt
  eingeführt. Enthält alle 22 Steps inkl. `notfall:2` und `institutionen:2`,
  die bisher fehlten.

### Altlasten bereinigt (alle offenen Fälle)

- **ANF-UX-01 Lock-Button** — Testprüfung auf veraltetes Emoji durch Prüfung
  auf SVG-Button mit korrekten ARIA-Attributen ersetzt. Funktionale Absicherung
  bleibt vollständig erhalten.
- **Script-Syntax-Test** — Drittanbieter-Bibliotheken (jsPDF, pako, JSZip)
  werden anhand eindeutiger Signaturen erkannt und übersprungen. Eigener
  Projektcode wird weiterhin vollständig geprüft.
- **Externe Dateien** (SOVEREIGNTY.md, phq9/gad7/who5-de-v1.json) —
  Fallback-Suchpfad auf bekannte Projektverzeichnisse ergänzt. In
  Produktionsumgebungen verhält sich der Test unverändert.

### Tests

42 neue Tests, 5 bestehende Tests angepasst:

| Sektion | Inhalt | Tests |
|---|---|---|
| 76 | DSGVO-Consent im FHIR-Export | 10 |
| 77 | Institutionelles Template | 8 |
| 78 | Supportkanal: hilfe@ in Einstellungen und More-Menu | 12 |
| 79 | Fokus-Abschnitt Einmaligkeit | 1 |
| 80 | Lokale Nutzungsstatistik | 11 |

Gesamt: **1.422 Tests, 0 Fehler, 0 Altlasten.**

### Dateien

| Datei | Änderung |
|---|---|
| `VIVODEPOT.html` | DSGVO-Consent, Template-Download, Supportkanal, E-Mail-Migration, Fokus-Bereinigung, Statistikfunktionen, STEP_TIMES |
| `test_vivodepot.py` | +42 Tests (Sektionen 76–80), 5 angepasst |

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
