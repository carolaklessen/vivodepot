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

### Mobile (iOS, Android, alle Touch-Geräte)
- **Bottom-Navigation**: Fixe Leiste unten mit ← Schritt-Name → (nur Mobile, ≤700px)
- **Topbar aufgeräumt**: Dekorative Buttons auf Mobile ausgeblendet — Topbar bleibt einzeilig
- **Notfall-Button**: Springt auf Mobile über die Navigation-Leiste (bottom: 74px)
- **Kein Auto-Zoom**: `font-size: 16px` auf Inputs verhindert Reinzoomen (iOS + Android)
- **Kein Tap-Delay**: `touch-action: manipulation` entfernt 300ms Verzögerung (ältere Android)
- **Kein Tap-Highlight**: `-webkit-tap-highlight-color` entfernt blaues Aufleuchten (Android)
- **Schriftgröße bei Rotation**: `-webkit-text-size-adjust: 100%` verhindert Skalierung
- **Smarte Tastatur**: `type="tel"` automatisch für Telefon-Felder, `type="date"` für Datums-Felder
- **Autocomplete**: Vorname, Nachname, E-Mail, Telefon, Adresse für Browser-Autofill
- **Vom Telefon importieren**: Web Contacts API (iOS Safari 14.1+, Chrome Android)
- **Dokument fotografieren**: Kamera-Button in Meine Dateien, direkt Rueckkamera
- **Safe area insets**: Bottom-Nav und Notfall-Button halten Abstand zur Home-Leiste (iPhone X+)
- **Keyboard overlap fix**: Aktives Feld scrollt automatisch in Sicht wenn Tastatur erscheint
- **Share API**: Goldener Teilen-Button auf Mobile -- AirDrop, WhatsApp, iCloud Drive etc.
- **PWA-Logo**: Echtes Vivodepot-Logo als App-Icon (Home-Bildschirm, Desktop, Favicon, Apple Touch Icon)
- **vCard-Import**: Immer sichtbar mit Anleitung wenn Web Contacts API nicht verfuegbar — direkter Zugriff auf Telefonbuch (iOS Safari 14.1+, Chrome Android)

### Neue Felder
- **Pflegekinder** + **Pflegekinder Besonderheiten**: In Familie-Sektion, inkl. Hinweis auf fehlende Erbrechte

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
