# VIVODEPOT — Änderungsprotokoll

Alle wichtigen Änderungen werden in dieser Datei dokumentiert.

---

## [1.0.0-beta.6]

### Neu
- **Offline-Vollständigkeit:** Alle Bibliotheken inline eingebettet (jsPDF, docx.js, QR-Code) — keine CDN-Abhängigkeit mehr
- **Google Fonts entfernt:** Systemschriften (Georgia, -apple-system) statt externe Ladeabhängigkeit
- **Notfall & Katastrophenschutz:** Vollständig überarbeiteter Schritt mit 6 klickbaren Ampelkarten (rot/gelb/grün), Evakuierungsplan, lokalen Kontakten, Notrufnummern-Grid, Notrufblatt-PDF
- **Barrierefreiheit im ⋮-Menü:** Schriftgröße, Kontrast, Nachtmodus, Vorlesen, Lupe — direkt erreichbar
- **iOS-Speicher-Anleitung:** Automatischer Dialog mit Schritt-für-Schritt-Anleitung beim Speichern auf iPhone
- **iOS: .htm-Endung:** Auf iOS werden Dateien mit `.htm` statt `.html` gespeichert, um PocketBook-Konflikt zu umgehen
- **Scroll-Fix:** Navigation zu neuer Seite scrollt korrekt nach oben (auch auf Mobil)

### Verbessert
- `saveAsHTML()` INIT-Block-Regex korrigiert — gespeicherte Dateien enthielten vorher keine Daten
- `nextStep()`/`prevStep()` leiten über `goToStep()` für einheitlichen Code-Pfad
- PDF-Bibliothek-Nachlader mit automatischem Retry und Fallback-CDN
- `generateKatastrophenschutzPDF()`, `generatePDF()`, `generateDocx()` nutzen `ensureJsPDF()`/`ensureDocx()`
- `console.log` → `console.error` (Produktionsbereinigung)
- INIT-Kommentar-Reihenfolge korrigiert für korrekte Regex-Erkennung

### Behoben
- BUG-10: vCard-Code lag außerhalb `<script>`-Tags
- BUG-11: `mehr()`-Funktion wurde mit falschem Argument-Typ aufgerufen
- Emojis aus Abschnitts-Titeln in Notfall-Kategorie entfernt
- Warnsymbole ⚠️ in Hinweistexten (Brandfall, Kohlenmonoxid) behalten

---

## [1.0.0-beta.5]

### Neu
- Fokus-System: Zielgeführte Navigation (Notfall, Familie, Vorsorge, Haustiere)
- Einstiegs-Wizard für neue Nutzer
- Multi-Profil-Unterstützung
- Angehörigen-Ansicht mit separatem Zugang
- Globale Suche (🔍) in der Topbar
- Diktat-Eingabe (Web Speech API)
- Dokument-Upload (PDF, Bilder, HEIC) mit Kategorie-Verwaltung
- Gesundheitsvollmacht-Wizard + Word-Export
- Notfall-Tasche Szenario-PDF
- BundID und ELEFAND-Felder
- Datenschutz-Modal

### Verbessert
- vivoConfirm ersetzt alle nativen `confirm()`-Dialoge
- PDF-Encoding-Fehler in Behördendaten-PDFs behoben
- Heimaufnahme/FHIR-Karten-Nesting behoben
- DuckDuckGo localStorage-Konflikt behoben

---

## [1.0.0-beta.4]

### Neu
- Weiche beim Öffnen: Inhaberin oder Angehörige/r
- Angehörigen-Modus aus App heraus (⋮-Menü)
- Fokus-Button in Sidebar
- 20 Schritte (statt 19)
- Einstellungen als eigener Schritt
- Logo transparent (Baum ohne Text)

### Verbessert
- User Journey komplett überarbeitet
- 253 Emojis aus Feldtiteln entfernt
- Alle nativen confirm() durch vivoConfirm ersetzt
- Tests: 89 → 126

---

## [1.0.0-beta.3]

### Neu
- AES-256-GCM Verschlüsselung
- Passwortschutz mit PBKDF2
- saveAsHTML() — Datei mit eingebetteten Daten speichern
- vCard 4.0 Export
- FHIR R4 JSON Export
- QR-Code Aufkleber
- Arztbogen PDF
- Szenario-PDFs (Krankenhaus, Todesfall)
- Vorsorgevollmacht + Patientenverfügung Word
- Vorlesen (Web Speech API)
- Hoher Kontrast + Nachtmodus

---

## [1.0.0-beta.1]

Erste Version — vollständige Notfallmappe als PDF und Word, 17 Dateneingabe-Schritte, Wizard für Vollmachten und Haustier-Notfallplan.
