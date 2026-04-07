# Changelog

Alle wesentlichen Änderungen an VIVODEPOT werden in dieser Datei dokumentiert.

## [1.0.0-beta.4] — 2026-04-07

### Fokus-Wizard — echtes Field-Filtering
- **FOCUSED_RENDERERS**: 8 fokussierte Step-Varianten — nur relevante Felder sichtbar
- **Arztbesuch**: Über mich (Basis) → Arzt / Allergien / Medikamente / KV → Arztbesuch-Bogen
- **Notfall**: Über mich → Notfallkontakte → Allergien / Medikamente → Notfall-Dokumente
- **Mein Wille**: Über mich → Testament / Vollmachten / Assistenten
- **Familie absichern**: Über mich + Kinder / Sorgerecht → Kontakte → Testament / Vollmachten
- **Alles ordnen**: alle 19 Schritte wie bisher
- Fokus startet immer bei Schritt 1 „Über mich"
- Sidebar zeigt im Fokus-Modus nur relevante Schritte (irrelevante gedimmt)
- „Fokus ändern" und „Alle anzeigen" Button in Sidebar und Einstellungen

### Mobile (iOS, Android, alle Touch-Geräte)
- **Bottom-Navigation**: Fixe Leiste unten mit ← Schritt-Name → (nur Mobile, ≤700px)
- **Topbar aufgeräumt**: Dekorative Buttons auf Mobile ausgeblendet — Topbar bleibt einzeilig
- **Notfall-Button**: Springt auf Mobile über die Navigation-Leiste (bottom: 74px)
- **Kein Auto-Zoom**: font-size 16px auf Inputs (iOS + Android)
- **Kein Tap-Delay**: touch-action: manipulation (ältere Android)
- **Kein Tap-Highlight**: -webkit-tap-highlight-color entfernt (Android)
- **Schriftgröße bei Rotation**: -webkit-text-size-adjust: 100%
- **Smarte Tastatur**: type="tel" automatisch für Telefon-Felder, type="date" für Datumsfelder
- **Autocomplete**: Vorname, Nachname, E-Mail, Telefon, Adresse
- **Safe area insets**: Bottom-Nav und Notfall-Button halten Abstand zur Home-Leiste (iPhone X+)
- **Keyboard overlap fix**: Aktives Feld scrollt automatisch in Sicht wenn Tastatur erscheint
- **Share API**: Goldener Teilen-Button — öffnet natives Share-Sheet (AirDrop, WhatsApp etc.)
- **Vom Telefon importieren**: Web Contacts API in Vertrauenspersonen + Wichtige Kontakte
- **Dokument fotografieren**: Kamera-Button in Meine Dateien öffnet direkt Rückkamera

### PWA & Branding
- **Echtes Logo**: Vivodepot-Logo (512×512, quadratisch) als PWA-Icon, Apple Touch Icon, Favicon
- **SVG Favicon**: Funktioniert in DuckDuckGo (PNG data: URLs werden geblockt)
- **viewport-fit=cover**: Safe-area-insets aktiviert

### Neue Felder
- **Pflegekinder** + **Pflegekinder Besonderheiten**: In Familie-Sektion, Hinweis auf fehlende Erbrechte

### Fixes
- **E-Mail**: feedback@vivodepot.de (war vivodepot1.odoo.com)
- **DuckDuckGo**: localStorage-Konflikt behoben, SVG Favicon statt PNG data-URL
- **Fokus-Wizard**: startet jetzt immer bei Schritt 1 Über mich

### Tests
- **126 Tests** — alle grün (war 89)

---

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

## [1.0.0-beta.4] — 2026-04-07

### Fokus-Wizard — echtes Field-Filtering
- **8 fokussierte Step-Varianten** (FOCUSED_RENDERERS) — jeder Fokus zeigt nur relevante Felder
- **Arztbesuch**: Basisdaten → Arzt, Allergien, Medikamente, KV → Arztbesuch-Bogen
- **Notfall**: Basisdaten → Notfallkontakte → Allergien, Medikamente → Notfall-Dokumente
- **Meinen Willen**: Basisdaten → Testament, Vollmachten, Assistenten
- **Familie absichern**: Basisdaten + Kinder/Sorgerecht → Kontakte → Testament
- Navigation springt direkt zum ersten relevanten Schritt
- Sidebar zeigt nur relevante Schritte im Fokus-Modus (gedimmt entfernt)

### Navigation & UX
- **Return-Overlay Weiche**: "Wer öffnet dieses Vivodepot?" — Inhaberin oder Angehörige/r
- **Angehörigen-Modus**: aus App erreichbar via ⋮-Menü
- **Fokus-Button** in Sidebar — Wizard jederzeit neu wählbar
- **vivoConfirm**: alle nativen confirm()-Dialoge ersetzt
- **Alle Bereiche anzeigen** Button erscheint im Fokus-Modus

### Mobile (iOS, Android, alle Touch-Geräte)
- **Bottom-Navigation**: Fixe Leiste ← Schritt-Name → (nur Mobile)
- **Kein Auto-Zoom**: font-size 16px auf Inputs
- **Safe area insets**: Bottom-Nav über iPhone Home-Leiste
- **Keyboard overlap fix**: visualViewport scrollt aktives Feld in Sicht
- **Share API**: Teilen-Button öffnet AirDrop/WhatsApp/iCloud
- **Dokument fotografieren**: Kamera-Button in Meine Dateien
- **Telefonbuch-Import**: Web Contacts API + vCard-Anleitung
- touch-action, tap-highlight, overscroll für alle Geräte

### Bugfixes
- **DuckDuckGo localStorage-Konflikt** (_ls) behoben — Login-Loop behoben
- **safeRender()**: Render-Fehler fangen onerror-Loop ab
- **Heimaufnahme/FHIR-Karten**: Nesting-Bug behoben
- **Behördendaten-PDFs**: jsPDF Emoji-Encoding-Fehler behoben
- **Angehörigen-View**: falscher Feldname bestattung_musik → musik

### Design & Assets
- **253 Emojis bereinigt** aus UI, Overlays, PDFs
- **Hint-Texte** unter Eingabefelder (Spalten fluchten korrekt)
- **PWA-Logo**: echtes Vivodepot-Logo (512×512, quadratisch)
- **SVG-Favicon**: funktioniert in DuckDuckGo
- **Umbenennung**: VIVODEPOT.html → index.html (GitHub Pages)

### Neue Felder
- **Pflegekinder** + Pflegekinder Besonderheiten (Erbrechts-Hinweis)

### Meine Dateien
- Kategorie-first UX, Namensabfrage beim Upload
- Download-Button für jede Datei
- Kategorie inline korrigierbar

### Angehörigen-View verbessert
- Hausarzt, Facharzt, laufende Behandlung
- Hochgeladene Befunde und Vollmachten mit Download

### Tests
- **126 Tests** (89 + 37 User-Journey-Tests) — alle grün

---

## [1.0.0-beta.4] — 2026-04-07

### Fokus-Wizard — echtes Field-Filtering
- **8 fokussierte Step-Renderer**: Jeder Fokus zeigt nur relevante Felder
- **Arztbesuch**: Basisdaten → Arzt/Allergien/Medikamente/KV → Arztbesuch-Bogen Button
- **Notfall**: Basisdaten → Kontakte → Allergien/Medikamente → Notfall-Dokumente Button
- **Mein Wille**: Basisdaten → Testament/Vollmachten/Assistenten
- **Familie absichern**: Basisdaten+Kinder → Kontakte → Testament/Vollmachten
- **Alles ordnen**: alle 19 Schritte wie bisher
- Fokus startet immer bei Schritt 1 (Über mich) in fokussierter Ansicht
- Sidebar blendet nicht relevante Schritte aus (gedimmt)
- Fokus-Button in Sidebar jederzeit aufrufbar

### Navigation & UX
- **Return-Overlay**: Weiche Inhaberin / Angehörige beim Öffnen
- **Angehörigen-Modus**: aus App heraus über ⋮-Menü testbar
- **vivoConfirm**: alle nativen confirm()-Dialoge ersetzt
- **DuckDuckGo-Fix**: localStorage-Namenskonflikt (_ls) behoben
- **safeRender()**: Render-Fehler fangen onerror-Loop ab

### Mobile (iOS, Android, alle Touch-Geräte)
- **Bottom-Navigation**: ← Schritt-Name → (nur Mobile)
- **Topbar**: Dekorative Buttons auf Mobile ausgeblendet
- **Safe area insets**: Bottom-Nav + Notfall-Button über iPhone Home-Leiste
- **Kein Auto-Zoom**: font-size 16px auf Inputs
- **Keyboard-Fix**: visualViewport scrollt aktives Feld in Sicht
- **touch-action, tap-highlight, text-size-adjust**: alle Touch-Geräte
- **Share API**: Teilen-Button auf Mobile (AirDrop, WhatsApp etc.)
- **Kamera-Capture**: Dokument fotografieren in Meine Dateien
- **Telefonbuch-Import**: Web Contacts API + vCard-Anleitung
- **Smarte Tastatur**: type=tel/date automatisch per Feldname

### Meine Dateien
- Kategorie-first UX, Namensabfrage beim Upload
- Download-Button für jede Datei
- Kategorie inline korrigierbar
- Angehörigen-View zeigt relevante Dateien mit Download

### Neue Felder
- **Pflegekinder** + Besonderheiten (Erbrechts-Hinweis, Jugendamt)

### Exporte
- **PDF-Encoding behoben**: Behördendaten-PDFs ohne kryptische Zeichen
- **Arbeitgeber-Notfallkarte entfernt** (Datenschutz)
- **Heimaufnahme**: Label korrigiert (PDF, nicht Word)

### PWA & Branding
- **Echtes Logo**: quadratisches Icon (512×512) für Home-Bildschirm, Apple Touch Icon
- **SVG Favicon**: funktioniert in DuckDuckGo
- **index.html**: umbenannt von VIVODEPOT.html (GitHub Pages)
- **feedback@vivodepot.de**: E-Mail aktualisiert

### Tests
- 89 → 126 Tests (User-Journey, Export, Mobile, Fokus)

---

## [1.0.0-beta.4] — 2026-04-07

### Fokus-Wizard (komplett neu)
- **FOCUSED_RENDERERS**: 8 fokussierte Schritt-Varianten — nur relevante Felder sichtbar
- **Arztbesuch**: Über mich → Gesundheit (Arzt, Allergien, Medikamente, KV) → Arztbesuch-Bogen
- **Notfall**: Über mich → Notfallkontakte → Notfall-Gesundheit → Notfall-Dokumente
- **Mein Wille**: Über mich → Testament/Vollmachten → Assistenten
- **Familie**: Über mich + Kinder/Sorgerecht → Vertrauenspersonen → Testament
- **Weiter/Zurück** überspringt irrelevante Schritte im Fokus-Modus
- Sidebar blendet nicht relevante Schritte aus
- Immer Start bei „Über mich"

### Mobile (iOS, Android, alle Touch-Geräte)
- **Bottom-Navigation**: Fixe Leiste unten mit ← Schritt-Name → (nur Mobile, ≤700px)
- **Topbar aufgeräumt**: Dekorative Buttons auf Mobile ausgeblendet — Topbar bleibt einzeilig
- **Notfall-Button**: Springt auf Mobile über die Navigation-Leiste (calc 74px + safe-area)
- **Kein Auto-Zoom**: font-size 16px auf Inputs verhindert Reinzoomen (iOS + Android)
- **Kein Tap-Delay**: touch-action: manipulation (ältere Android)
- **Kein Tap-Highlight**: -webkit-tap-highlight-color (Android)
- **Schriftgröße bei Rotation**: -webkit-text-size-adjust: 100%
- **Smarte Tastatur**: type="tel" für Telefon-Felder, type="date" für Datums-Felder automatisch
- **Autocomplete**: Vorname, Nachname, E-Mail, Telefon, Adresse
- **Vom Telefon importieren**: Web Contacts API (iOS Safari 14.1+, Chrome Android)
- **Dokument fotografieren**: Kamera-Button in Meine Dateien (capture=environment)
- **Safe area insets**: Bottom-Nav + Notfall-Button über iPhone Home-Leiste
- **Keyboard overlap fix**: visualViewport scrollt aktives Feld in Sicht
- **Share API**: Teilen-Button öffnet AirDrop/WhatsApp/iCloud (iOS + Android)

### Neue Felder
- **Pflegekinder** + **Pflegekinder Besonderheiten**: Jugendamt, Vormund, Erbrechts-Hinweis

### PWA & Icons
- **Echtes Logo** als PWA-Icon, Apple Touch Icon (512x512, quadratisch)
- **SVG Favicon**: funktioniert in DuckDuckGo (PNG data-URLs werden geblockt)
- **viewport-fit=cover**: safe-area-inset aktiv

### Bugfixes
- **Feedback-E-Mail**: feedback@vivodepot.de (war vivodepot1.odoo.com)
- **vCard-Button**: immer sichtbar, zeigt Anleitung wenn Web Contacts API fehlt

### Mobile (Nachtrag)
- **Fokus-Wizard auf Mobile**: goldener „Fokus"-Button direkt in Bottom-Nav + ⋮ Menü
- **Topbar-Fix**: Profil und ⋮ bekommen flex-shrink:0 — werden nie abgeschnitten
- **Sehr kleine Bildschirme (<400px)**: A⁺ und 🌙 ausgeblendet, Profil + ⋮ + Speichern bleiben immer sichtbar

### Tests
- **160 Tests** alle grün (126 + 34 neue für Fokus-Wizard, Mobile, UX)

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
