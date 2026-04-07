# Vivodepot

Version: v1.0.0-beta.4

# VIVODEPOT — Persönliche Vorsorge- & Nachlassdokumentation

**Eine einzelne HTML-Datei. Kein Server. Keine Cloud. Alle Daten bleiben auf Ihrem Gerät.**

*Souveränität by Design.*

VIVODEPOT hilft Ihnen, alle wichtigen Informationen für den Notfall, die Vorsorge und den Nachlass an einem Ort zu sammeln — strukturiert, verschlüsselt und offline nutzbar. Angehörige finden im Ernstfall alles, was sie brauchen: Kontakte, Vollmachten, Medikamente, Bestattungswünsche und persönliche Worte.

---

## Schnellstart

## Alleinstellungsmerkmal: FHIR R4 & FIM-JSON

Vivodepot ist der **einzige Vorsorge-Assistent im DACH-Markt**, der Gesundheitsdaten im internationalen Standard **FHIR R4 (HL7)** exportiert und importiert.

### Was das bedeutet

| Standard | Verwendung | Wer nutzt es |
|---|---|---|
| **FHIR R4** | Medizinische Stammdaten (Diagnosen, Medikamente, Allergien) | Krankenhäuser, ePA, Arztpraxen weltweit |
| **FIM-JSON** | Behördliche Stammdaten (FITKO-Schema) | Verwaltungsportale, OZG-Umsetzung |

### Für Nutzer
- Einmal eingeben → überall mitbringen
- Krankenhaus-Aufnahme ohne Abtippen
- ePA-Import (sobald Krankenkassen APIs öffnen)

### Für Institutionen
- FHIR R4 Export direkt in Kliniksysteme importierbar
- FIM-JSON für Behördenformulare (Kindergeld, Pflegegrad, ALG)
- QR-Code auf PDF → Sachbearbeiter scannt, Formular füllt sich


1. **`index.html` herunterladen** (eine einzige Datei, ca. 1 MB)
2. **Im Browser öffnen** (Chrome, Edge, Firefox oder Safari)
3. **Fokus wählen** — Arztbesuch? Notfall? Vorsorge? Alles?
4. **Daten eingeben** — die App führt Sie Schritt für Schritt
5. **Speichern** (💾 oben rechts) — erzeugt eine neue HTML-Datei mit Ihren Daten

> Empfehlung: Speichern Sie die Datei auf einem USB-Stick und legen Sie diesen an einem sicheren Ort ab. Oder installieren Sie Vivodepot als App über Ihren Browser (Einstellungen → Als App installieren).

---

## Features

### Eingabe (19 Schritte)

| Schritt | Inhalt |
|---------|--------|
| Über mich | Persönliche Daten, Profilfoto, Familienstand |
| Vertrauenspersonen | Notfallkontakte mit Bevollmächtigungen |
| Wichtige Kontakte | Zu informierende Personen (Sofort / 1. Woche / 4 Wochen) |
| Geld & Konten | Bankkonten, Depots, Altersvorsorge, Steuern, Schulden |
| Versicherungen | Alle laufenden Policen |
| Wohnen & Eigentum | Wohnung, Immobilien, Fahrzeuge |
| Verträge & Abos | Laufende Verträge und Mitgliedschaften |
| Mein Wille | Testament, Vorsorgevollmacht, Patientenverfügung, Dokumente |
| Meine Gesundheit | Blutgruppe, Allergien, Medikamente, Vorsorge, Anamnese |
| Pflege & Lebenslauf | Pflegegrad, Biografie, Bildung, Beruf |
| Meine Tiere | Haustiere mit Tierarzt und Betreuungsplan |
| Online & Zugänge | Passwort-Manager, BundID, ELEFAND, Geräte |
| Erinnerungsstücke & Briefe | Fotos, persönliche Gegenstände, Abschiedsbriefe |
| Mein Abschied | Bestattungswünsche, Trauerfeier, Musik |
| Assistenten | 6 geführte Schritt-für-Schritt-Wizards |
| Meine Dateien | Upload von Befunden, Fotos, Vollmachten — nach Kategorie |
| Prüftermine | Jährliche Erinnerungen für Vollmachten und Testament |
| Einstellungen | Passwort, Darstellung, Profile, PWA-Installation |
| Dokumente erstellen | 4 Export-Tabs mit allen Ausgabeformaten |

### Assistenten (6 Wizards)

| Wizard | Schritte | Ergebnis |
|--------|----------|----------|
| Notfall-Gesundheitskarte | 6 | Druckbare Scheckkarte 85×54mm |
| Vorsorgevollmacht | 6 | Word-Dokument (auto-Download) |
| Patientenverfügung | 6 | Word-Dokument (auto-Download) |
| Gesundheitsvollmacht | 5 | Word-Dokument (auto-Download) |
| Bestattungswünsche | 8 | Felder automatisch ausgefüllt |
| Haustier-Notfallplan | 6 | Felder automatisch ausgefüllt |

### Exporte (4 Tabs, 13+ Formate)

| Tab | Enthält |
|-----|---------|
| Mein Vivodepot | Gesamt-PDF, Gesamt-Word, Fortschritts-Checkliste |
| Vollmachten | Vorsorgevollmacht, Patientenverfügung, Gesundheitsvollmacht (je Word) |
| Notfall & Arzt | Arztbesuch-Bogen, Notfall-Tasche, QR-Sticker, Krankenhaus-Einweisung, Haustier-Notfallkarte, Im Todesfall |
| Ämter & Einrichtungen | Heimaufnahme-Paket (PDF), Gesundheitsdaten FHIR R4 (JSON), Kindergeld-Datenblatt, Arbeitsamt-Datenblatt, Pflegegrad-Datenblatt |

---

## Zwei Zugangsmodi

### Inhaberin / Inhaber
- Alle Daten bearbeiten und ergänzen
- Alle Exporte erstellen
- Fokus wählen (Sidebar passt sich an)

### Angehörige/r
Beim Öffnen einer gespeicherten Datei — oder über ⋮-Menü → „Angehörigen-Ansicht testen":

- **Krankenhaus-Einweisung**: Allergien, Medikamente, Blutgruppe, Vollmachten, Ärzte
- **Im Todesfall**: Testament, Bestattungswünsche, Kontakte, persönliche Botschaft
- Hochgeladene Befunde und Vollmachten direkt downloadbar
- Optional durch Passwort geschützt

---

## Sicherheit

- **AES-256-GCM Verschlüsselung** (Web Crypto API) — optionales Passwort
- **Kein Server**, keine Übertragung, keine Telemetrie
- **Offline-fähig** (PWA mit Service Worker)
- Alle Daten bleiben ausschließlich im Browser (`localStorage`) und in der gespeicherten HTML-Datei

---

## Kompatibilität

| Browser | Status |
|---------|--------|
| Chrome / Edge | Vollständig (inkl. Spracheingabe) |
| Firefox | Vollständig |
| Safari (macOS/iOS) | Vollständig |
| DuckDuckGo Browser | Vollständig (Spracheingabe deaktiviert) |
| Android Chrome | Vollständig (inkl. Telefonbuch-Import) |
| iOS Safari 14.1+ | Vollständig (inkl. Telefonbuch-Import) |

---

## Mobile

Vivodepot ist vollständig mobil-optimiert:

- **Fokus-Wizard** — Arztbesuch (4 Schritte), Notfall (5), Mein Wille (4), Familie (5): nur relevante Schritte, Felder und Exporte
- **Mobile Fokus** — „Fokus"-Button in Bottom-Nav, korrekte Schrittzahl (z.B. „1 von 4"), Pfeile ← → respektieren Fokus
- **Bottom-Navigation** — ← Schritt → Fokus-Button, immer sichtbar auf Mobile
- **Kein Auto-Zoom** — Inputs haben `font-size: 16px`, kein ungewolltes Reinzoomen
- **Smarte Tastatur** — Telefonnummern öffnen den Ziffernblock, Datumsfelder den Datepicker
- **Telefonbuch-Import** — Vom Telefon Button in Vertrauenspersonen und Wichtige Kontakte
- **Dokument fotografieren** — Kamera-Button in Meine Dateien oeffnet direkt die Rueckkamera
- **Teilen** — natives Share-Sheet (AirDrop, WhatsApp, iCloud Drive) (AirDrop, WhatsApp, iCloud Drive) statt nur Download
- **Safe area insets** — Bottom-Nav haelt Abstand zur Home-Leiste auf iPhone X+
- **Keyboard fix** — aktives Feld scrollt in Sicht wenn Tastatur erscheint
- **PWA-Logo** — echtes Vivodepot-Logo auf Home-Bildschirm und Desktop (kein generisches V mehr)
- **Touch-optimiert** — kein Tap-Delay, kein Tap-Highlight, 44px Mindestgröße für alle Buttons

## Technischer Aufbau

- **Eine HTML-Datei**, keine externen Abhängigkeiten zur Laufzeit
- CDN-Bibliotheken werden vom Service Worker gecacht (jsPDF, docx.js, qrcode-generator)
- **~1 MB** unkomprimiert, ~8.500 Zeilen
- Lizenz: **EUPL v1.2**

---

## Entwicklung & Tests

```bash
python3 test_vivodepot.py index.html
```

183 Tests (Desktop, Mobile, Exporte, User-Journey) — Syntax, Funktionen, Exporte, Wizards, Barrierefreiheit, User-Journey, Fokus-Renderer.

Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Entwicklungshinweise.
