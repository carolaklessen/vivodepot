# Changelog

Alle wesentlichen Änderungen an VIVODEPOT werden in dieser Datei dokumentiert.

## [1.0.0-beta.3] — 2026-04-06

### Neue Features
- **4 Export-Tabs** statt endloser Scrollseite: Mein Vivodepot, Vollmachten, Notfall & Arzt, Ämter & Einrichtungen
- **Behördendaten-Exporte**: Kindergeld (PDF+QR), Arbeitsamt (PDF+QR), Pflegegrad (PDF+QR)
- **FIM-JSON Export**: Maschinenlesbarer Behördendaten-Export (12 Kategorien)
- **Structured Import**: FHIR R4, FIM-JSON und Auto-Erkennung mit Vorschau-Dialog
- **Gesundheitsvollmacht-Wizard**: 5 Schritte, Word-Export, § 1820 Abs. 3 BGB
- **Notfall-Tasche Checkliste**: Orientiert an BBK-Empfehlungen
- **Arztbesuch-Bogen**: PDF mit allen Stammdaten für die Praxis
- **BundID & ELEFAND**: Felder für digitale Behördenzugänge
- **Familie & Sorgerecht**: Familienstand, Kinder, Unterhalt
- **Anamnese & Krankenversicherung**: Erweiterte Gesundheitsdaten
- **Fokus-Wizard**: 4 Ziele (Arztbesuch, Notfall, Vorsorge, Alles) + 4 Toggles
- **PWA-Installation**: Sichtbare Anleitung in Einstellungen (📲 Als App installieren)
- **Favicon**: Browser-Tab-Icon
- **Slogan**: „Souveränität by Design" auf Welcome-Screen und in Einstellungen

### Verbesserungen
- **Logo aufgehellt**: Weißer Kreishintergrund für Sichtbarkeit auf dunkler Topbar
- **Wizards erzeugen Dokumente automatisch**: Vorsorgevollmacht + Patientenverfügung → Word-Download statt confirm()-Dialog
- **„Schnellhilfe" → „Assistenten"**: Klarerer Name in Sidebar
- **„Notfallmappe" → „Mein Vivodepot"**: Durchgängiges Branding
- **Navigation zeigt nächsten Step**: „Weiter: Versicherungen →" statt nur „Weiter →"
- **Fortschrittsleiste**: „3 von 18 Bereichen ausgefüllt" statt „Vollständig: 3/18"
- **Abhaken**: „Fertig? Abhaken" statt „Als vollständig markieren"
- **Return-Overlay**: 🎯 Fokus-Auswahl entfernt (war redundant), nur noch in Einstellungen + Logo-Klick
- **Mobile Tabs**: Horizontal scrollbar, kleinere Buttons
- **Micro-Copy**: Ermutigende Step-Beschreibungen (Gesundheit, Finanzen, Mein Wille, Mein Abschied)

### Entfernt
- **Technik-Tab**: Aufgelöst — QR-Sticker nach „Notfall & Arzt", FHIR nach „Ämter & Einrichtungen"
- **„Alle Dokumente erstellen"**-Button: War zu unspezifisch
- **Sperren-Button**: War verwirrend bei unverschlüsselten Dateien
- **confirm()-Dialoge** in Wizards: Ersetzt durch auto-Download

### Testskript
- Umbenannt: `test_notfallmappe.py` → `test_vivodepot.py`
- Erweitert: 70 → 89 Tests
- Neue Kategorien: Wizards (7), UI & Branding (10)

## [1.0.0-beta.2] — 2026-04-05

### Neue Features
- Globale Suche (durchsucht alle Felder)
- Einstellungen-Step (Passwort, Darstellung, Profile)
- Datenschutz-Banner + Modal (DSGVO)
- Cloud-Backup-Empfehlung (Info, kein Upload)
- Notfall-Button ohne Passwort
- Transparentes Logo (Icon-only, ohne Text)
- Meine Dateien (Upload von Befunden, Fotos)

### Verbesserungen
- 19 Steps statt 17
- Step-Umbenennung + Umsortierung
- Startseite aufgeräumt
- Schnellhilfe: 2×3 Grid mit menschlichen Untertiteln

## [1.0.0-beta.1] — 2026-04-05

### Initiale Version
- Einzelne HTML-Datei (~375 KB)
- 17 Eingabe-Steps
- AES-256-GCM Verschlüsselung
- 5 Wizards (Gesundheitskarte, Vorsorgevollmacht, Patientenverfügung, Bestattung, Haustier)
- 11 Export-Formate
- Profil-System (Mehrpersonen)
- EUPL-1.2 Lizenz
