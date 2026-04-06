# VIVODEPOT — Persönliche Vorsorge- & Nachlassdokumentation

**Eine einzelne HTML-Datei. Kein Server. Keine Cloud. Alle Daten bleiben auf Ihrem Gerät.**

*Souveränität by Design.*

VIVODEPOT hilft Ihnen, alle wichtigen Informationen für den Notfall, die Vorsorge und den Nachlass an einem Ort zu sammeln — strukturiert, verschlüsselt und offline nutzbar. Angehörige finden im Ernstfall alles, was sie brauchen: Kontakte, Vollmachten, Medikamente, Bestattungswünsche und persönliche Worte.

---

## Schnellstart

1. **`VIVODEPOT.html` herunterladen** (eine einzige Datei, ca. 500 KB)
2. **Im Browser öffnen** (Chrome, Edge, Firefox oder Safari)
3. **Fokus wählen** — Arztbesuch? Notfall? Vorsorge? Alles?
4. **Daten eingeben** — die App führt Sie Schritt für Schritt
5. **Speichern** (💾 oben rechts) — erzeugt eine neue HTML-Datei mit Ihren Daten

> Empfehlung: Speichern Sie die Datei auf einem USB-Stick und legen Sie diesen an einem sicheren Ort ab. Oder installieren Sie Vivodepot als App über Ihren Browser (Einstellungen → 📲 Als App installieren).

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
| Meine Dateien | Upload von Befunden, Fotos, Vollmachten |
| Prüftermine | Jährliche Erinnerungen für Vollmachten und Testament |
| Einstellungen | Passwort, Darstellung, Profile, PWA-Installation |
| Dokumente erstellen | 4 Export-Tabs mit allen Ausgabeformaten |

### Assistenten (6 Wizards)

| Wizard | Schritte | Ergebnis |
|--------|----------|----------|
| 💳 Notfall-Gesundheitskarte | 6 | Druckbare Scheckkarte 85×54mm |
| ⚖️ Vorsorgevollmacht | 6 | Word-Dokument (auto-Download) |
| 🏥 Patientenverfügung | 6 | Word-Dokument (auto-Download) |
| 💚 Gesundheitsvollmacht | 5 | Word-Dokument (auto-Download) |
| 🕊️ Bestattungswünsche | 8 | Felder automatisch ausgefüllt |
| 🐾 Haustier-Notfallplan | 6 | Felder automatisch ausgefüllt |

### Exporte (4 Tabs, 17+ Formate)

| Tab | Dokument | Format |
|-----|----------|--------|
| 📋 Mein Vivodepot | Gesamtexport | PDF |
| 📋 Mein Vivodepot | Gesamtexport | Word (.docx) |
| 📋 Mein Vivodepot | Fortschritts-Checkliste | HTML |
| ⚖️ Vollmachten | Vorsorgevollmacht | Word |
| ⚖️ Vollmachten | Patientenverfügung | Word |
| ⚖️ Vollmachten | Gesundheitsvollmacht | Word |
| 🚑 Notfall & Arzt | Krankenhaus-Blatt | PDF |
| 🚑 Notfall & Arzt | Todesfall-Krisenplan | PDF |
| 🚑 Notfall & Arzt | Haustier-Notfallkarte | PDF |
| 🚑 Notfall & Arzt | Notfall-Tasche Checkliste | PDF |
| 🚑 Notfall & Arzt | Arztbesuch-Bogen | PDF |
| 🚑 Notfall & Arzt | QR-Sticker (3 Stück) | Druck |
| 🏛️ Ämter & Einrichtungen | Heimaufnahme-Paket | Word |
| 🏛️ Ämter & Einrichtungen | Arbeitgeber-Notfallkarte | Druck |
| 🏛️ Ämter & Einrichtungen | Gesundheitsdaten für Klinik | FHIR R4 JSON |
| 🏛️ Ämter & Einrichtungen | Kindergeld-Datenblatt | PDF + QR |
| 🏛️ Ämter & Einrichtungen | Arbeitsamt-Datenblatt | PDF + QR |
| 🏛️ Ämter & Einrichtungen | Pflegegrad-Datenblatt | PDF + QR |
| 🏛️ Ämter & Einrichtungen | FIM-JSON Export | JSON |

### Import

| Format | Quelle |
|--------|--------|
| FHIR R4 JSON | ePA, Arztbriefe, Medikationspläne |
| FIM-JSON | Eigener Export, Verwaltungsportale |
| Allgemeines JSON | Automatische Felderkennung |

### Barrierefreiheit (10 Features)

Schriftgröße (3 Stufen), Vorlesen, Hoher Kontrast, Nachtmodus, Bildschirmlupe, Spracheingabe, Drucken, Globale Suche, Notfall-Button (ohne Passwort), Fokus-Wizard.

### Sicherheit

- AES-256-GCM Verschlüsselung (Web Crypto API)
- PBKDF2 Schlüsselableitung (100.000 Iterationen)
- Optionaler Passwortschutz
- Kein Server, kein Netzwerk, kein Login
- 6 Notfall-Felder ohne Passwort zugänglich

---

## Technische Details

| Eigenschaft | Wert |
|-------------|------|
| Dateigröße | ~500 KB (eine HTML-Datei) |
| Zeilen | ~8.200 |
| Funktionen | ~220 |
| Externe Bibliotheken | jsPDF, docx, QRCode.js (MIT, CDN-gecacht) |
| Verschlüsselung | AES-256-GCM / PBKDF2 |
| Lizenz | EUPL-1.2 |
| Tests | 89 (test_vivodepot.py) |
| PWA | Manifest + Service Worker |

---

## Projektstruktur

```
VIVODEPOT.html          ← Die App (eine Datei)
test_vivodepot.py       ← Regressions-Tests (89 Tests)
README.md               ← Diese Datei
QUICKSTART.md           ← 10-Minuten-Anleitung
DOCS.md                 ← Technische Dokumentation
FAQ.md                  ← Häufige Fragen
CHANGELOG.md            ← Versionshistorie
SOVEREIGNTY.md          ← ZenDiS Souveränitätsbewertung
CONTRIBUTING.md         ← Beitragsrichtlinien
SECURITY.md             ← Sicherheitsrichtlinie
LICENSE                 ← EUPL-1.2
```

---

## Herausgeber

Vivodepot UG (haftungsbeschränkt)
Website: [vivodepot.de](https://vivodepot.de)
E-Mail: feedback@vivodepot.de
Quellcode: [github.com/carolaklessen/vivodepot](https://github.com/carolaklessen/vivodepot)
Lizenz: [EUPL-1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)
