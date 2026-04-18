# VIVODEPOT — Änderungsprotokoll

Alle wichtigen Änderungen werden in dieser Datei dokumentiert.

---

## [1.0.0-beta.11] — April 2026

### Neu

- **Schritt „Wohlbefinden & Seele" (PROM)** — Neuer Schritt nach „Meine Gesundheit" mit drei gemeinfreien, validierten Selbstauskunft-Fragebögen: PHQ-9 (Stimmung, 9 Fragen, Score 0–27), GAD-7 (Angst, 7 Fragen, Score 0–21) und WHO-5 (Wohlbefinden, 5 Fragen, Score 0–25 / 0–100 %). Antworten werden als Chip-Buttons ausgewählt; Score und Schweregrad erscheinen automatisch nach der letzten Antwort. Alle Ergebnisse werden im Autosave gespeichert. Datenschutzhinweis, Quellenangaben und Haftungsausschluss direkt im Schritt sichtbar. Fokus-Ziel „Für den Arztbesuch" enthält den neuen Schritt.

- **QR-Export: PROM-Scores im Notfall-Profil** — Das QR-Übergabe-Profil „Notfall" enthält jetzt automatisch PHQ-9-Score und -Datum, GAD-7-Score und -Datum sowie WHO-5-Score, Prozentwert und Datum. Keine manuelle Auswahl nötig. Lesbare Bezeichnungen für alle sieben neuen Felder in `WG_FELDNAMEN` ergänzt.

### Tests

35 neue Tests in 2 neuen Sektionen:

| Sektion | Inhalt | Tests |
|---|---|---|
| 66 | PROM: STEPS-Eintrag, Zeitmessung, Fokus-Ziel, Arrays, Hilfsfunktionen, Score-Logik, Renderer, Quellenangaben | 24 |
| 67 | QR-PROM: PROM-Felder im notfall-Profil, lesbare Feldnamen | 11 |

Gesamt: **1086 Tests, 1085 bestehen.** (1 schlägt nur außerhalb des Repos fehl: SOVEREIGNTY.md-Pfadtest)

### Neue Hilfsfunktionen

| Funktion | Aufgabe |
|---|---|
| `promRadioRow(prefix, qnum, text)` | Rendert eine Frage mit Chip-Buttons |
| `promCalcScore(prefix, count)` | Berechnet Score aus gespeicherten Antworten |
| `promScoreBox(prefix, count)` | Rendert Ergebnis-Box mit Schweregrad |
| `promRenderBlock(prefix, fragen)` | Rendert den vollständigen Fragebogenblock |

### Neue globale Konstanten

`PHQ9_FRAGEN`, `GAD7_FRAGEN`, `WHO5_FRAGEN` — Arrays mit den Fragetexten der drei Instrumente (Public Domain).

### Dateien

| Datei | Änderung |
|---|---|
| `VIVODEPOT.html` | Neuer Schritt prom, 4 Hilfsfunktionen, QR-Profilerweiterung |
| `test_vivodepot.py` | +35 Tests (Sektionen 66–67) |

---

## [1.0.0-beta.10] — April 2026

### Neu

- **vivodepot-lesen.html — Eigenständige Leseansicht** — Neue Begleitdatei für die sichere Datenübergabe ohne gemeinsame App-Installation. Zwei Eingabewege: QR-Code (Kamerascan, inkl. automatischer Mehr-Teile-Erkennung) und Weitergabe-Datei (Drag & Drop oder Auswahl). Entschlüsselungslogik identisch zu VIVODEPOT (PBKDF2 + AES-256-GCM). Kein Speichern, kein Netzwerkzugriff, keine Datenhaltung. Logo als Base64 eingebettet. Versionsnummer korrespondiert mit VIVODEPOT.html. Bereitgestellt unter `carolaklessen.github.io/vivodepot/vivodepot-lesen.html`.

- **QR-Übergabe: URL-Format mit Hash-Fragment** — QR-Codes verlinken direkt auf die Leseansicht. Das verschlüsselte Hash-Fragment (`#PAYLOAD`) verlässt den Server nie — vollständig datenschutzkonform. Empfänger ohne VIVODEPOT scannen mit normalem Smartphone; der Browser öffnet die Leseansicht direkt. Konfiguriert über Konstante `QR_LESEN_URL`. Rückwärtskompatibel: `qreQrErkannt()` versteht URL- und Legacy-JSON-Format.

- **QR-Übergabe: Mehr-Teile-QR-Codes** — Löst das USB-Verbotsproblem in Institutionen (Arztpraxen, Kanzleien, Behörden). Payload > 1800 Zeichen → automatische Aufteilung in Chunks à 1200 Zeichen (max. 6). Jeder Chunk trägt gemeinsame ID + Teilnummer. Schritt-3: Karussell mit ◀ / ▶, Beschriftung „Code X von Y — zuerst zeigen". Leseansicht sammelt Teile automatisch und startet Kamera nach jedem Teil neu.

- **Leseansicht: Hash-Erkennung beim Laden** — URL mit `#`-Fragment automatisch erkannt → direkt zur PIN-Eingabe.

- **Leseansicht: Weitergabe-Datei öffnen** — Die Leseansicht entschlüsselt auch `VIVODEPOT_Weitergabe_*.html`-Dateien.

### Verbessert (UX-Korrekturen ANF-UX-01 bis ANF-UX-07)

- **ANF-UX-01** — Lock-Button: Emoji 🔒 als sichtbarer Inhalt (war leer).
- **ANF-UX-02** — Welcome-Modal: Schriftgröße-Hinweis → direkt auf „A⁺"-Button in Topbar; ⋮ als Alternative.
- **ANF-UX-03** — EUDI-Import-Karte: `w&auml;hlen` → `wählen`.
- **ANF-UX-04** — Infobox „Daten weitergeben": ASCII-Umschreibungen → korrekte Umlaute.
- **ANF-UX-05** — Solid Pod: eigene Gruppe „Eigener Datenspeicher" mit Infobox + solidcommunity.net-Hinweis.
- **ANF-UX-06** — Import-Infobox: EUDI Wallet (SD-JWT) als viertes Format ergänzt.
- **ANF-UX-07** — Export-Tabs: Führende Leerzeichen entfernt.

### Weitere Verbesserungen

- FIM-Karte: `\uFE0F` aus ec-icon entfernt → Leerraum über Kartentitel beseitigt.
- Solid Pod Karte: Untertitel auf „Daten in den eigenen Pod exportieren — kompatibel mit solidcommunity.net" geändert.

### Tests

29 neue Tests in 3 neuen Sektionen:

| Sektion | Inhalt | Tests |
|---|---|---|
| 63 | QR-URL-Format: `QR_LESEN_URL`, GitHub-URL, Base64url, Hash-Fragment, Rückwärtskompatibilität | 7 |
| 64 | Mehr-Teile-QR: Schwellwerte, Chunk-Logik, Zustandsvariablen, Karussell-UI | 14 |
| 65 | ANF-UX-01–07: Lock-Button, Umlaute, Infobox, Solid-Pod-Gruppe, FIM-Icon | 8 |

Gesamt: **1051 Tests, 1050 bestehen.** (1 schlägt nur außerhalb des Repos fehl: SOVEREIGNTY.md-Pfadtest)

### Dateien

| Datei | Änderung |
|---|---|
| `VIVODEPOT.html` | UX-Fixes, QR-URL-Format, Mehr-Teile-QR, Karussell-UI |
| `vivodepot-lesen.html` | **Neu** |
| `test_vivodepot.py` | +29 Tests (Sektionen 63–65) |

---

## [1.0.0-beta.9] — April 2026

### Neu

- **ANF-05 Solid Pod Export** — Turtle-Format (.ttl), Linked-Data (vcard:, schema:), Modal mit Kategorienauswahl.
- **Datenaustausch-Step** — Neuer Schritt bündelt alle Import- und Export-Wege.
- **Strukturumstellung Sidebar** — 21 Schritte (bisher 20).

### Tests

43 neue Tests — Gesamt: 1093 Tests, 0 Fehler.

---

## [1.0.0-beta.8] — April 2026

Weitergabe-Datei (4 Profile), QR-Übergabe (ANF-06), Einkommensdaten (ANF-01), Kind-Daten (ANF-02), EUDI-Wallet (ANF-03), FHIR (ANF-04).
Gesamt: 1050 Tests, 0 Fehler.

---

## [1.0.0-beta.7] — April 2026

BUG-SALT behoben: Salt in gespeicherter Datei eingebettet.

---

## [1.0.0-beta.6] — April 2026

Offline-Vollständigkeit, Notfall & Katastrophenschutz, Barrierefreiheit, BUG-10, BUG-11.

---

## [1.0.0-beta.5] — März 2026

Fokus-System, Einstiegs-Wizard, Multi-Profil, Angehörigen-Ansicht, Diktat-Eingabe.

---

## [1.0.0-beta.4] — Februar 2026

Weiche Inhaberin / Angehörige/r, 20 Schritte.

---

## [1.0.0-beta.3] — Januar 2026

AES-256-GCM, saveAsHTML(), vCard 4.0, FHIR R4, QR-Aufkleber, Arztbogen PDF.

---

## [1.0.0-beta.1] — Dezember 2025

Erste Version — Notfallmappe als PDF und Word, 17 Dateneingabe-Schritte.
