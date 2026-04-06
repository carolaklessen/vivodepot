# Changelog

Alle wesentlichen Änderungen an VIVODEPOT werden in dieser Datei dokumentiert.

## [1.0.0-beta.4] — 2026-04-07

### UX & Navigation
- **Weiche beim Öffnen**: Return-Overlay zeigt jetzt „Wer öffnet dieses Vivodepot?" — Inhaberin oder Angehörige/r
- **Angehörigen-Modus aus App heraus**: Neuer Menüpunkt im ⋮-Menü „Angehörigen-Ansicht testen"
- **Fokus neu wählen**: Button am Ende der Sidebar — Fokus-Wizard jederzeit aufrufbar
- **Zurück zur App**: Angehörigen-Overlay hat „← Zurück zur App" statt „← Zurück"
- **vivoConfirm**: Alle nativen `confirm()`-Dialoge ersetzt durch kleines App-eigenes Overlay (kein „Eine Nachricht von" mehr)

### Bugfixes
- **DuckDuckGo localStorage-Konflikt**: `_ls` war ein reservierter Name in DuckDuckGo — ersetzt durch direkte `localStorage`-Aufrufe
- **Welcome-Loop behoben**: `window.onerror` zeigte nach Render-Fehlern die Startseite — `safeRender()` fängt Fehler ab
- **Heimaufnahme/FHIR-Karten**: Waren in einem `<div>` verschachtelt — getrennt
- **Doppeltes `lockApp`**: Zweite Definition entfernt
- **Angehörigen-View**: `get('bestattung_musik')` → `get('musik')` (falscher Feldname)
- **Leere Divs nach Emoji-Entfernung**: Alle leeren Emoji-Platzhalter bereinigt
- **Führende Leerzeichen**: In Buttons, Labels und Overlays nach Emoji-Entfernung behoben

### Meine Dateien (komplett überarbeitet)
- **Kategorie-zuerst UX**: Flache Liste aller Dateien, Upload per Kategorie-Button
- **Namensabfrage beim Upload**: `prompt()` fragt direkt nach aussagekräftigem Namen (z.B. „Geburtsurkunde Carola")
- **Kategorie korrigierbar**: Inline-Dropdown pro Datei
- **Download-Button**: Jede Datei direkt öffenbar (⬇ Öffnen)
- **Klare Erklärung**: „Ihr persönlicher Dokumenten-Tresor — verschlüsselt gespeichert, auf dem USB-Stick dabei"

### Angehörigen-View verbessert
- **Neue Felder**: Hausarzt, Facharzt 1+2, laufende Behandlung im Krankenhaus-Szenario
- **Hochgeladene Dateien**: Befunde (Krankenhaus) und Vollmachten (Todesfall) mit Download-Button sichtbar
- **Passwort-Dialog**: Schloss-Symbol statt leerem Div, saubere Fehlermeldungen

### Emojis entfernt
- **253 Emojis entfernt** aus Feldtiteln, Infoboxen, Overlays, Startseite, Willkommen-Seite, PDFs
- **Behalten**: Topbar-Funktionssymbole (🔊 🌙 🔎 🚨 🎤), Export-Karten-Icons

### Exporte
- **PDF-Encoding behoben**: jsPDF konnte Emojis nicht rendern — alle 41 Emoji-Codes in Behördendaten-PDFs durch lesbaren Text ersetzt (`[ ]` statt kaputter Checkboxen)
- **Arbeitgeber-Notfallkarte entfernt**: Datenschutzbedenken — Medizindaten gehören nicht zur Personalabteilung
- **Heimaufnahme-Paket**: Button-Label war fälschlicherweise „Word erstellen" — korrigiert auf „PDF erstellen" (die Funktion erzeugte schon immer ein PDF)
- **Sektionsbezeichnung**: „Für Pflegeeinrichtung & Arbeitgeber" → „Für Pflegeeinrichtung & Klinik"

### Felder & Hints
- **Hint-Position**: Hint-Texte jetzt unter dem Eingabefeld (nicht mehr zwischen Label und Feld) — Spalten fluchten korrekt
- **Label-Großschreibung entfernt**: Feldbezeichnungen in normaler Groß-/Kleinschreibung

### Tests
- **User-Journey-Tests**: Welcome → GoalWizard → App, Angehörigen-Flow, Export-Vollständigkeit
- **126 Tests** (89 + 37 neue User-Journey-Tests) — alle grün

---

## [1.0.0-beta.3] — 2026-04-06

### Neue Features
- **4 Export-Tabs**: Mein Vivodepot, Vollmachten, Notfall & Arzt, Ämter & Einrichtungen
- **Behördendaten-Exporte**: Kindergeld, Arbeitsamt, Pflegegrad (je PDF+QR)
- **FIM-JSON Export**: Maschinenlesbarer Behördendaten-Export
- **Structured Import**: FHIR R4, FIM-JSON, Auto-Erkennung mit Vorschau
- **Gesundheitsvollmacht-Wizard**: 5 Schritte, Word-Export
- **Fokus-Wizard**: 5 Ziele mit Sidebar-Filterung
- **PWA-Installation**: Anleitung in Einstellungen
- **13 Persona-Tests**: Neue Felder für Scheidung, Krebs/Behinderung, Krypto, Patchwork etc.

### Verbesserungen
- 89 Tests (vorher 70)
- Export-Tab-Struktur statt Scrollseite
- Mikrofon-Toggle in Einstellungen (Standard: aus)

## [1.0.0-beta.2] — 2026-04-05

### Neue Features
- Globale Suche, Einstellungen-Step, Datenschutz-Banner
- Notfall-Button ohne Passwort, transparentes Logo
- Meine Dateien (Upload)

### Verbesserungen
- 19 Steps statt 17

## [1.0.0-beta.1] — 2026-04-05

### Initiale Version
- Einzelne HTML-Datei (~375 KB)
- 17 Eingabe-Steps
- AES-256-GCM Verschlüsselung
- 5 Wizards, 11 Export-Formate
- Profil-System, EUPL-1.2 Lizenz
