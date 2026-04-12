# VIVODEPOT

**Ihr persönlicher Vorsorge-Assistent. Keine Cloud. Kein Abo. Volle Kontrolle.**

[![Version](https://img.shields.io/badge/Version-1.0.0--beta.7-gold)](https://github.com/carolaklessen/vivodepot)
[![Lizenz](https://img.shields.io/badge/Lizenz-EUPL--1.2-green)](LICENSE)
[![Offline](https://img.shields.io/badge/Offline-100%25-brightgreen)](#offline)
[![Tests](https://img.shields.io/badge/Tests-846%2F846-brightgreen)](#tests)
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

Am Ende erstellt VIVODEPOT mit einem Klick druckfertige Dokumente: PDF, Word, Notfallblatt, Arztbogen und mehr.

---

## Funktionen

### Dateneingabe (20 Schritte)

| Schritt | Inhalt |
|---|---|
| Über mich | Persönliche Daten, Foto |
| Vertrauenspersonen | Kontaktliste mit Rollen, vCard-Import |
| Zu informieren | Wer wird wann kontaktiert |
| Finanzen | Konten, Depots, Schulden |
| Versicherungen | Alle Policen |
| Immobilien | Eigentum, Schlüssel |
| Verträge & Abos | Kündigungsfristen |
| Testament & Vollmachten | inkl. BGB-Referenzen (2023) |
| Gesundheit | Blutgruppe, Allergien, Medikamente |
| Pflege | Pflegegrad, Biografie-Modul |
| Haustiere | Tierarzt, Notfallbetreuung |
| Digitales Erbe | E-Mail, Cloud, Passwort-Manager |
| Persönliches | Erinnerungen, Botschaft |
| Bestattung | Wünsche, Trauerfeier |
| Assistenten | Geführte Wizards |
| Notfall | BBK-Ampelkarten, Katastrophenschutz-PDF |
| Dokumente | Alle Exporte |
| Erinnerungen | Ampel-Status Schlüsseldokumente |
| Einstellungen | Passwort, Barrierefreiheit, Profile |

### Exporte (13 Formate)

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

VIVODEPOT ist eine vollständig selbsttragende Einzeldatei. Alle Bibliotheken (jsPDF, docx.js, QR-Code-Generator) sind direkt eingebettet. Keine einzige externe Anfrage beim Öffnen oder Nutzen der App.

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
- Systemschriften (keine Google Fonts)
- EUPL-1.2 Lizenz

---

## Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

**842 Tests** in 33 Sektionen: Syntax, Verschlüsselung, Navigation, PDF-Export, Word-Export, Barrierefreiheit, Mobile, Offline, Krypto-Portabilität, Rechtsinhalte und mehr.

---

## Mitmachen

Bitte lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md) und [SECURITY.md](SECURITY.md).

Feedback und Fehlerberichte: [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

---

## Lizenz

[EUPL-1.2](LICENSE) — Europäische Union Public Licence

© 2026 Vivodepot UG (haftungsbeschränkt) · Berlin · [vivodepot.de](https://vivodepot.de)

*Entwickelt mit KI-Unterstützung (EU AI Act Art. 50) · Keine Rechtsberatung · Alle Dokumente sind Entwürfe.*
