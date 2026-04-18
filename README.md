# VIVODEPOT

**Ihr persönlicher Vorsorge-Assistent. Keine Cloud. Kein Abo. Volle Kontrolle.**

[![Version](https://img.shields.io/badge/Version-1.0.0--beta.11-gold)](https://github.com/carolaklessen/vivodepot)
[![Lizenz](https://img.shields.io/badge/Lizenz-EUPL--1.2-green)](LICENSE)
[![Offline](https://img.shields.io/badge/Offline-100%25-brightgreen)](#offline)
[![Tests](https://img.shields.io/badge/Tests-1085%2F1086-brightgreen)](#tests)
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

Am Ende erstellt VIVODEPOT druckfertige Dokumente: PDF, Word, Notfallblatt, Arztbogen und mehr. Die QR-Übergabe überträgt Daten ohne USB an Institutionen. Die Leseansicht öffnet QR-Codes und Weitergabe-Dateien ohne VIVODEPOT-Installation.

---

## Funktionen

### Dateneingabe (22 Schritte)

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
| Wohlbefinden & Seele | PHQ-9, GAD-7, WHO-5 (seit beta.11) |
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

### Exporte

- Word-Dokument (vollständige Notfallmappe)
- PDF (druckfertig)
- Notfall-Checkliste, Katastrophenschutz-Blatt
- Arztbogen (Standard, Radiologie, Präoperativ, Geriatrie)
- Szenario-PDFs (Krankenhaus, Todesfall, Notfall-Tasche)
- Vorsorgevollmacht, Patientenverfügung, Gesundheitsvollmacht (Word)
- QR-Aufkleber, vCard-Export
- Weitergabe-Datei (HTML, verschlüsselt)
- QR-Übergabe (AES-verschlüsselt, URL-basiert, Mehr-Teile-fähig)
- Solid Pod Export (Turtle, .ttl)

### Weitergabe-Datei (seit beta.8)

Eigenständige, verschlüsselte HTML-Datei mit gefiltertem Datensatz. Vier Profile: Notfall, Vollmacht, Familie, Behörde.

### QR-Übergabe (seit beta.8, URL-Format seit beta.10)

QR-Codes verlinken direkt auf die Leseansicht. Verschlüsselt per AES-256-GCM, PIN-geschützt, 24 Stunden gültig. Bei größeren Datenmengen automatische Aufteilung auf bis zu 6 QR-Codes. Löst das USB-Verbotsproblem in Institutionen.

### Leseansicht (seit beta.10)

[`vivodepot-lesen.html`](vivodepot-lesen.html) — eigenständige Empfänger-Seite für QR-Codes und Weitergabe-Dateien. Kein Account, keine Installation, kein Speichern, kein Netzwerkzugriff.

**URL:** [carolaklessen.github.io/vivodepot/vivodepot-lesen.html](https://carolaklessen.github.io/vivodepot/vivodepot-lesen.html)

### Solid Pod Export (seit beta.9)

Export im Turtle-Format (.ttl) mit Linked-Data-Standards. Eigene Gruppe „Eigener Datenspeicher". Anbieterbeispiel: solidcommunity.net.

### Import

EUDI-Wallet (SD-JWT), FHIR R4, FIM-JSON, allgemeines JSON.

### Barrierefreiheit

Schriftgröße A+ (3 Stufen), Hoher Kontrast, Nachtmodus, Vorlesen, Bildschirmlupe, Diktat, Touch-Targets 44px (WCAG 2.2).

---

## Sicherheit & Datenschutz

| Merkmal | Details |
|---|---|
| Verschlüsselung | AES-256-GCM |
| Schlüsselableitung | PBKDF2-HMAC-SHA256 (200.000 Iterationen) |
| Salt | Zufällig, in gespeicherter Datei eingebettet (seit beta.7) |
| Weitergabe-Datei | Eigener Salt, eigenes Passwort |
| QR-Übergabe | Hash-Fragment — Payload erreicht Server nie; PIN; 24h Ablauf |
| Leseansicht | Kein Speichern, kein Server, keine Cookies |
| Netzwerkanfragen | Keine — vollständig offline |
| Telemetrie | Nicht vorhanden |
| Externe Skripte | Nicht vorhanden (alle Bibliotheken inline) |

---

## Digitale Souveränität

**Ergebnis: 20 von 20 ZenDiS-Kriterien erfüllt.**

BSI IT-Grundschutz++, EU Cyber Resilience Act, DSGVO (Privacy by Design), EU AI Act Art. 50, EUPL-1.2.

Vollständige Bewertung: [SOVEREIGNTY.md](SOVEREIGNTY.md)

---

## Technologie

- Einzeldatei HTML (ca. 1,3 MB) + vivodepot-lesen.html
- Kein Build-System, kein Framework, kein CDN
- Vanilla JavaScript (ES5/ES6)
- AES-256-GCM via Web Crypto API
- jsPDF 2.5.1, docx.js 8.5.0, QRCode-Generator 1.4.4, jsQR 1.4.0 (alle inline)
- EUPL-1.2 Lizenz

---

## Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

**1086 Tests in 67 Sektionen — 1085 bestehen.**

Abgedeckt: Syntax, Verschlüsselung, Navigation, PDF/Word-Export, Barrierefreiheit, Mobile, Offline, Krypto-Portabilität, Weitergabe-Datei, QR-Übergabe (URL-Format + Mehr-Teile), Leseansicht-Logik, EUDI/FHIR-Import, Solid Pod, ANF-UX-01–07 und mehr.

---

## Mitmachen

[CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) · [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

---

## Lizenz

[EUPL-1.2](LICENSE) — Europäische Union Public Licence

© 2026 Vivodepot UG (haftungsbeschränkt) · Berlin · [vivodepot.de](https://vivodepot.de)

*Entwickelt mit KI-Unterstützung (EU AI Act Art. 50) · Keine Rechtsberatung · Alle Dokumente sind Entwürfe.*
