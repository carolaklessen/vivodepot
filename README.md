# VIVODEPOT

**Ihr persönlicher Vorsorge-Assistent. Keine Cloud. Kein Abo. Volle Kontrolle.**

[![Version](https://img.shields.io/badge/Version-1.0.0--beta.9-gold)](https://github.com/carolaklessen/vivodepot)
[![Lizenz](https://img.shields.io/badge/Lizenz-EUPL--1.2-green)](LICENSE)
[![Offline](https://img.shields.io/badge/Offline-100%25-brightgreen)](#offline)
[![Tests](https://img.shields.io/badge/Tests-1093%2F1093-brightgreen)](#tests)
[![ZenDiS](https://img.shields.io/badge/ZenDiS-20%2F20-blue)](#souveränität)

VIVODEPOT ist eine vollständig offline-fähige Einzeldatei-HTML-Anwendung zur Vorsorgedokumentation. Alle Daten bleiben ausschließlich auf Ihrem Gerät — keine Cloud, kein Server, keine Übertragung.

---

## Schnellstart

1. [`VIVODEPOT.html`](VIVODEPOT.html) herunterladen
2. In Chrome oder Firefox öffnen (Doppelklick genügt)
3. Loslegen — keine Installation, keine Registrierung

**Online-Version:** [carolaklessen.github.io/vivodepot/](https://carolaklessen.github.io/vivodepot/)

---

## Was ist VIVODEPOT?

VIVODEPOT hilft Menschen dabei, alle wichtigen Informationen für den Notfall an einem Ort zu dokumentieren:

- Vertrauenspersonen und Kontakte
- Finanzen, Versicherungen, Immobilien
- Gesundheit, Medikamente, Vollmachten
- Testament, Bestattungswünsche
- Haustiere, digitales Erbe
- Notfall & Katastrophenschutz (BBK-Empfehlungen)
- Persönliche Erinnerungen und Botschaften

Am Ende erstellt VIVODEPOT mit einem Klick druckfertige Dokumente: PDF, Word, Notfallblatt, Arztbogen und mehr. Mit der Weitergabe-Funktion können gezielt ausgewählte Daten verschlüsselt an Dritte weitergegeben werden. Mit der QR-Übergabe können Daten direkt per Kamerascan übergeben werden. Mit dem Solid Pod Export können Daten in einen persönlichen Datentresor exportiert werden.

---

## Funktionen

### Dateneingabe (21 Schritte)

| Schritt | Inhalt |
|---|---|
| Über mich | Persönliche Daten, Foto |
| Vertrauenspersonen | Kontaktliste mit Rollen, vCard-Import |
| Zu informieren | Wer wird wann kontaktiert |
| Finanzen | Konten, Depots, Schulden, Einkommensdaten |
| Versicherungen | Alle Policen |
| Immobilien | Eigentum, Schlüssel |
| Verträge & Abos | Kündigungsfristen |
| Gesundheit | Blutgruppe, Allergien, Medikamente |
| Pflege | Pflegegrad, Biografie-Modul |
| Mein Wille | Testament & Vollmachten, BGB-Referenzen (2023) |
| Mein Abschied | Bestattungswünsche, Trauerfeier |
| Erinnerungsstücke | Persönliches, Botschaft |
| Haustiere | Tierarzt, Notfallbetreuung |
| Digitales Erbe | E-Mail, Cloud, Passwort-Manager |
| Assistenten | Geführte Wizards |
| Notfall | BBK-Ampelkarten, Katastrophenschutz-PDF |
| Dokumente erstellen | Alle PDF- und Word-Exporte |
| Datenaustausch | Import und Export (FHIR, FIM, EUDI, Weitergabe, QR, Solid Pod) |
| Erinnerungen | Ampel-Status Schlüsseldokumente |
| Dokumente (intern) | Export-Step |
| Einstellungen | Passwort, Barrierefreiheit, Profile |

### Exporte (16 Formate)

- Word-Dokument (vollständige Notfallmappe)
- PDF (druckfertig mit Branding)
- Notfall-Checkliste
- Katastrophenschutz-Blatt (Notrufnummern, Evakuierungsplan)
- Arztbogen (Krankenhaus-Schnellinfo)
- Szenario: Krankenhaus
- Szenario: Todesfall
- Szenario: Notfall-Tasche
- Vorsorgevollmacht (Word)
- Patientenverfügung (Word)
- Gesundheitsvollmacht (Word)
- QR-Aufkleber
- vCard-Export
- Weitergabe-Datei (HTML, verschlüsselt)
- QR-Übergabe (AES-verschlüsselt, Kamerascan)
- Solid Pod Export (Turtle-Format, .ttl)

### Weitergabe-Datei (seit beta.8)

Eine zweite, eigenständige HTML-Datei — verschlüsselt mit einem separaten Passwort, geöffnet im Browser, ohne Installation.

| Profil | Empfängerin |
|---|---|
| Notfall | Krankenhaus, Rettungsdienst, Hausarzt |
| Vollmacht | Notar, Klinik-Sozialdienst |
| Familie | Angehörige, Erben |
| Behörde | Ämter, Kassen, Rentenversicherung |

### QR-Übergabe (seit beta.8)

Daten direkt per QR-Code übergeben — AES-256-GCM-verschlüsselt, PIN-geschützt, 24 Stunden gültig. Empfang per Kamerascan, vollständig offline.

### Solid Pod Export (seit beta.9)

Export im Turtle-Format (.ttl) mit Linked-Data-Standards (vcard:, schema:). Auswahl der Datenkategorien im Dialog. EUPL-konform.

### Import (seit beta.8)

- EUDI-Wallet-Import (SD-JWT) — 8 Felder automatisch gemappt
- FHIR R4 Import — AllergyIntolerance, Condition, MedicationStatement, Observation, Immunization, CarePlan

### Barrierefreiheit

- Schriftgröße A+ (3 Stufen)
- Hoher Kontrast
- Nachtmodus
- Vorlesen (Web Speech API)
- Bildschirmlupe
- Diktat-Eingabe
- Touch-Targets 44px (WCAG 2.1)

---

## Sicherheit & Datenschutz

| Merkmal | Details |
|---|---|
| Verschlüsselung | AES-256-GCM |
| Schlüsselableitung | PBKDF2-HMAC-SHA256 (100.000 Iterationen) |
| Salt | Zufällig, in gespeicherter Datei eingebettet (seit beta.7) |
| Weitergabe-Datei | Eigener Salt, eigenes Passwort — unabhängig vom Hauptpasswort |
| QR-Übergabe | Eigener Salt, PIN, Ablauf 24 Stunden |
| Datenspeicherung | Ausschließlich `localStorage` des Browsers |
| Netzwerkanfragen | Keine — vollständig offline |
| Cloud | Nicht vorhanden |
| Telemetrie | Nicht vorhanden |
| Cookies | Nicht vorhanden |
| Externe Skripte | Nicht vorhanden (alle Bibliotheken inline eingebettet) |

---

## Digitale Souveränität

VIVODEPOT wurde gegen das ZenDiS-Diskussionspapier „Kriterien zur Bewertung von Digitaler Souveränität" (März 2026) geprüft:

**Ergebnis: 20 von 20 Kriterien erfüllt.**

Weitere Rahmenwerke: BSI IT-Grundschutz++, EU Cyber Resilience Act, DSGVO (Privacy by Design), EU AI Act Art. 50, OSBA, EUPL-1.2.

Vollständige Bewertung: [SOVEREIGNTY.md](SOVEREIGNTY.md)

---

## Offline-Fähigkeit

VIVODEPOT ist eine vollständig selbsttragende Einzeldatei. Alle Bibliotheken (jsPDF, docx.js, QR-Code-Generator, jsQR) sind direkt eingebettet. Keine einzige externe Anfrage beim Öffnen oder Nutzen der App.

Funktioniert auf: USB-Stick (ohne Internet), im Flugmodus, auf Krankenhaus-Computern, auf jedem Gerät mit Chrome, Firefox, Edge oder Safari.

---

## Technologie

- Einzeldatei HTML (ca. 1,3 MB)
- Kein Build-System, kein Framework, kein CDN
- Vanilla JavaScript (ES5/ES6)
- AES-256-GCM via Web Crypto API
- jsPDF 2.5.1 (inline)
- docx.js 8.5.0 (inline)
- QRCode-Generator 1.4.4 (inline)
- jsQR 1.4.0 (inline, für QR-Übergabe-Empfang)
- Systemschriften (keine Google Fonts)
- EUPL-1.2 Lizenz

---

## Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

**1093 Tests** in 55 Sektionen: Syntax, Verschlüsselung, Navigation, PDF-Export, Word-Export, Barrierefreiheit, Mobile, Offline, Krypto-Portabilität, Rechtsinhalte, Weitergabe-Datei, QR-Übergabe, EUDI-Wallet-Import, FHIR-Import, Einkommensdaten, Kind-Daten, ANF-05 Solid Pod, Datenaustausch-Step, Strukturumstellung und mehr.

---

## Mitmachen

Bitte lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md) und [SECURITY.md](SECURITY.md).

Feedback und Fehlerberichte: [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

---

## Lizenz

[EUPL-1.2](LICENSE) — Europäische Union Public Licence

© 2026 Vivodepot UG (haftungsbeschränkt) · Berlin · [vivodepot.de](https://vivodepot.de)

*Entwickelt mit KI-Unterstützung (EU AI Act Art. 50) · Keine Rechtsberatung · Alle Dokumente sind Entwürfe.*
