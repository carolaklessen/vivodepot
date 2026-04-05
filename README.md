# VIVODEPOT — Persönliche Vorsorge- & Nachlassdokumentation

**Eine einzelne HTML-Datei. Kein Server. Keine Cloud. Alle Daten bleiben auf Ihrem Gerät.**

VIVODEPOT hilft Ihnen, alle wichtigen Informationen für den Notfall, die Vorsorge und den Nachlass an einem Ort zu sammeln — strukturiert, verschlüsselt und offline nutzbar. Angehörige finden im Ernstfall alles, was sie brauchen: Kontakte, Vollmachten, Medikamente, Bestattungswünsche und persönliche Worte.

---

## Schnellstart

1. **`VIVODEPOT.html` herunterladen** (eine einzige Datei, ca. 375 KB)
2. **Im Browser öffnen** (Chrome, Edge, Firefox oder Safari)
3. **Daten eingeben** — die App führt Sie Schritt für Schritt
4. **Speichern** (💾 oben rechts) — erzeugt eine neue HTML-Datei mit Ihren Daten

> Empfehlung: Speichern Sie die Datei auf einem USB-Stick (z.B. beschriftet mit „Vivodepot") und legen Sie diesen an einem sicheren Ort ab. Informieren Sie Ihre Vertrauenspersonen über den Ablageort.

---

## Features

### Eingabe (18 Schritte)
- Persönliche Daten mit optionalem Profilfoto
- Vertrauenspersonen & Sofortkontakte
- Zu informierende Personen (Sofort / Erste Woche / Erste 4 Wochen)
- Finanzen (Konten, IBAN-Validierung)
- Versicherungen
- Immobilien
- Testament & Vollmachten (inkl. Vollmachten für andere Personen)
- Verträge & Abonnements
- Gesundheit (Blutgruppe, Allergien, Medikamente, Befunde, Implantate)
- Haustiere
- Pflege & Biografie (Pflegegrad, Kommunikation, Ernährung, Alltag)
- Digitales Erbe (Passwort-Manager, Krypto-Wallets, Legacy Contacts, Hardware-Wallets)
- Persönliches & Briefe (Krankenhaus- und Abschiedsbriefe)
- Bestattungswünsche

### Assistenten (5 Wizards)
- 💳 Notfall-Gesundheitskarte (druckbare Scheckkarte 85×54mm)
- ⚖️ Vorsorgevollmacht-Assistent
- 🏥 Patientenverfügung-Assistent
- 🕊️ Bestattungs-Assistent
- 🐾 Haustier-Assistent

### Exporte (11 Formate)

| Kategorie | Export | Format |
|-----------|--------|--------|
| 📋 Komplett | Notfallmappe komplett | PDF |
| 📋 Komplett | Notfallmappe komplett | Word (.docx) |
| 📋 Komplett | Fortschritts-Checkliste | HTML |
| ⚖️ Rechtlich | Vorsorgevollmacht (§§ 1814 ff. BGB) | Word (.docx) |
| ⚖️ Rechtlich | Patientenverfügung (§ 1827 BGB) | Word (.docx) |
| 🚑 Notfall | Krankenhaus-Einweisung | PDF |
| 🚑 Notfall | Krisenplan — Im Todesfall | PDF |
| 🚑 Notfall | Haustier-Notfallkarte | PDF |
| 🏠 Pflege | Heimaufnahme-Paket (5 Seiten) | PDF |
| 💼 Arbeit | Arbeitgeber-Notfallkarte | PDF |
| 📱 QR | QR-Sticker Paket (3 Sticker) | Druckbar |
| 🔬 Technik | FHIR R4 JSON | JSON |

### Sicherheit & Technik
- **AES-256-GCM Verschlüsselung** (Web Crypto API) — optionaler Passwortschutz
- **Angehörigen-Passwort** — separater Zugang für Angehörige mit Passwortabfrage
- **Multi-Profil-System** — bis zu 4 Profile in einer Datei (löschbar)
- **Profilfoto** — Smart-Crop für Portraits, in PDFs eingebettet
- **Offline-fähig** — PWA mit Service Worker, kein Internet nötig
- **Feld-Validierung** — IBAN (Mod-97), Steuer-ID, PLZ, Geburtsdatum, E-Mail
- **Storage-Meter** — Speicherverbrauch im ⋮-Menü sichtbar
- **File System Access API** — direktes Speichern auf USB-Stick (Chrome/Edge)
- **Zweisprachig** — Deutsch/Englisch umschaltbar (140+ Übersetzungen)
- **Barrierearm** — 3-stufige Schriftgröße, Tap-Targets min. 44px

### Externe Bibliotheken (3)
- [docx 8.5.0](https://github.com/dolanmiu/docx) — Word-Dokument-Erzeugung
- [jsPDF 2.5.1](https://github.com/parallax/jsPDF) — PDF-Erzeugung
- [qrcode-generator 1.4.4](https://github.com/nickvdyck/qrcode-generator) — QR-Codes

Alle über CDN (jsdelivr/cdnjs) geladen, kein npm/build-System nötig.

---

## Deutsches Recht

VIVODEPOT referenziert aktuelle BGB-Paragraphen nach der **Betreuungsrechtsreform 2023**:
- Vorsorgevollmacht: §§ 1814 ff. BGB
- Patientenverfügung: § 1827 BGB (ehemals § 1901a)
- Betreuungsverfügung: § 1831 BGB (ehemals § 1906)

Links zu offiziellen Formularen des Bundesjustizministeriums, der Bundesnotarkammer (ZVR), des Organspende-Registers und der Verbraucherzentralen sind integriert.

> ⚠️ VIVODEPOT ersetzt keine Rechtsberatung. Alle erzeugten Dokumente sind Entwürfe und sollten ggf. anwaltlich oder notariell geprüft werden.

---

## Systemvoraussetzungen

- Moderner Browser (Chrome 80+, Edge 80+, Firefox 78+, Safari 14+)
- JavaScript aktiviert
- Kein Internet nötig (nach dem ersten Laden)
- Empfohlen: Chrome oder Edge (für File System Access API / USB-Stick-Speicherung)

---

## Datenschutz

- **Keine Daten verlassen Ihr Gerät** — kein Server, kein Tracking, keine Cookies
- Alle Daten werden ausschließlich im `localStorage` des Browsers gespeichert
- Optionale AES-256-GCM-Verschlüsselung für sensible Daten
- Beim Speichern als HTML-Datei werden die Daten in der Datei selbst eingebettet
- Kein Account, keine Registrierung, keine E-Mail-Adresse nötig

---

## Entwicklung

VIVODEPOT wurde mit Unterstützung von KI-Werkzeugen (Claude, Anthropic) entwickelt. Der gesamte Code wurde vom Projektinhaber geprüft, getestet und freigegeben. Die rechtlichen Textbausteine (Vorsorgevollmacht, Patientenverfügung) basieren auf den offiziellen Formulierungen des Bundesministeriums der Justiz und wurden an die aktuelle Rechtslage (Betreuungsrechtsreform 2023) angepasst.

> ⚠️ Trotz sorgfältiger Prüfung ersetzt VIVODEPOT keine Rechtsberatung. Alle erzeugten Dokumente sind Entwürfe.

VIVODEPOT ist eine einzelne HTML-Datei ohne Build-System. Zum Entwickeln:

```bash
# Repository klonen
git clone https://github.com/carolaklessen/vivodepot.git

# Datei im Browser öffnen
open VIVODEPOT.html        # macOS
xdg-open VIVODEPOT.html    # Linux
start VIVODEPOT.html        # Windows

# Tests ausführen (Python 3 nötig)
python3 test_notfallmappe.py VIVODEPOT.html
```

### Architektur
- **Single-File-Architecture** — alles in einer HTML-Datei (~375 KB, ~5.900 Zeilen)
- **Keine Build-Pipeline** — kein Webpack, kein npm, kein Transpiler
- **Vanilla JS** — kein Framework, kein React, kein jQuery
- **CSS Custom Properties** — Farbpalette über CSS-Variablen
- **Progressive Enhancement** — funktioniert ohne Service Worker, ohne Crypto API

### Tests
69 automatisierte Tests prüfen:
- HTML-Struktur und Vollständigkeit
- JavaScript-Syntax aller Script-Blöcke
- Vorhandensein aller 18 Schritte, 11 Export-Funktionen, 5 Wizards
- Sicherheitsmerkmale (AES-256, Passwort-Felder, EUPL-Lizenz)
- Branding und Copyright

---

## Lizenz

Copyright © 2026 Vivodepot.

Lizenziert unter der **European Union Public Licence (EUPL), Version 1.2**.

Den vollständigen Lizenztext finden Sie in der Datei [LICENSE](LICENSE) oder unter:
https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

---

## Feedback

📩 **feedback@vivodepot1.odoo.com**

Fehler gefunden? Feature-Wunsch? Verbesserungsvorschlag?
Wir freuen uns über jede Rückmeldung.
