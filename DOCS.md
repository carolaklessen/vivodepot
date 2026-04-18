# VIVODEPOT — Technische Dokumentation

*Version 1.0.0-beta.10 · April 2026*

---

## Architektur

VIVODEPOT ist eine **Einzeldatei-HTML-Anwendung** (ca. 1,3 MB). Keine Build-Pipeline, kein Framework, kein CDN.

```
VIVODEPOT.html
├── CSS (eingebettet)
├── Inline-Bibliotheken
│   ├── jsPDF 2.5.1 (364 KB) — PDF-Erstellung
│   ├── docx.js 8.5.0 (368 KB) — Word-Erstellung
│   ├── QRCode-Generator 1.4.4 (20 KB) — QR-Codes
│   └── jsQR 1.4.0 (256 KB) — QR-Code-Scan (Empfang und Leseansicht)
├── JavaScript (Hauptlogik)
│   ├── Datenspeicherung (localStorage + AES-256-GCM)
│   ├── STEP_RENDERERS (21 Schritte)
│   ├── Export-Funktionen (16 Formate)
│   ├── Import-Funktionen (FHIR, FIM, JSON, EUDI, QR)
│   ├── Weitergabe-Datei-System (wg-*)
│   ├── QR-Übergabe-System (qr-* / qre-*) — URL-Format seit beta.10
│   ├── Solid Pod Export (sp-*)
│   ├── Wizard-System
│   └── Barrierefreiheits-Funktionen
└── HTML (UI-Struktur)

vivodepot-lesen.html (neu in beta.10)
├── Eigenständige Empfänger-Seite
├── jsQR 1.4.0 (inline)
├── Hash-Fragment-Erkennung
├── Multi-Part Chunk-Sammler
└── AES-256-GCM Entschlüsselung (identisch zu VIVODEPOT)
```

---

## Datenspeicherung

### Primär: localStorage

```javascript
localStorage.setItem('vivodepot_v1_enc', JSON.stringify(verschluesselt));
```

### Verschlüsselung (optional)

- Algorithmus: AES-256-GCM
- Schlüsselableitung: PBKDF2-HMAC-SHA256 (**200.000 Iterationen**)
- Salt: 16 Byte, kryptographisch zufällig (Web Crypto API)
- IV: 12 Byte, kryptographisch zufällig
- Implementierung: Web Crypto API (browser-nativ, keine externe Bibliothek)

### Salt-Portabilität (seit beta.7)

Vor beta.7 wurde der Salt ausschließlich in `localStorage` (Schlüssel `STORE_META`) gespeichert. Beim Öffnen der gespeicherten Datei auf einem anderen Gerät fehlte er — die Entschlüsselung schlug fehl, obwohl das Passwort korrekt war.

**Fix:** `saveAsHTML()` liest den Salt vor dem Speichern aus `localStorage` und bettet ihn in den INIT-Block der HTML-Datei ein. Beim Öffnen auf einem neuen Gerät schreibt der INIT-Block den Salt synchron in `localStorage`, bevor `loadData()` ihn benötigt. Der bestehende Salt wird dabei nicht überschrieben (idempotent).

### Datei-Speicherung

`saveAsHTML()` erstellt eine HTML-Datei mit eingebetteten Daten und eingebettetem Salt. Der INIT-Block wird durch regulären Ausdruck ersetzt:

```
/\/\/ [═]+\s*\/\/ INIT[\s\S]*?\}\)\(\);/
```

---

## Step-System

21 Schritte (seit beta.9, zuvor 20):

| Index | ID | Label |
|---|---|---|
| 0 | start | Über mich |
| 1 | kontakte | Vertrauenspersonen |
| 2 | infokontakte | Zu informieren |
| 3 | finanzen | Finanzen |
| 4 | versich | Versicherungen |
| 5 | immobilien | Immobilien |
| 6 | vertraege | Verträge & Abos |
| 7 | gesundheit | Gesundheit |
| 8 | pflege | Pflege |
| 9 | testament | Mein Wille |
| 10 | bestattung | Mein Abschied |
| 11 | persoenliches | Erinnerungsstücke |
| 12 | haustiere | Haustiere |
| 13 | digital | Digitales Erbe |
| 14 | assistenten | Assistenten |
| 15 | notfall | Notfall & Katastrophenschutz |
| 16 | dokumente | Dokumente erstellen |
| 17 | datenaustausch | Datenaustausch (seit beta.9) |
| 18 | erinnerung | Erinnerungen |
| 19 | exportStep | Export (intern) |
| 20 | einstellungen | Einstellungen |

---

## Weitergabe-Datei (seit beta.8)

### Übersicht

Die Weitergabe-Funktion erstellt eine eigenständige HTML-Datei mit einem gefilterten Datensatz und separater Verschlüsselung.

### Sicherheitsarchitektur

```
Nutzerdaten (gefiltert nach Profil)
  + eigener Salt (getRandomValues())
  + separates Passwort
  → PBKDF2 (200.000 Iterationen) → AES-256-GCM
  → eigenständige HTML-Datei
```

Das Hauptpasswort kann die Weitergabe-Datei nicht entschlüsseln.

### Zentrale Funktionen

| Funktion | Aufgabe |
|---|---|
| `weitergabeOpen()` | Öffnet das Modal, setzt Zustand zurück |
| `weitergabeClose()` | Schliesst das Modal |
| `wgZeigeSchritt(nr)` | Wechselt zwischen Schritt 1, 2 und 3 |
| `wgWaehleProfilCard(profil)` | Profil-Auswahl |
| `wgErstellen()` | Kern-Logik: filtern, verschlüsseln, HTML bauen, herunterladen |
| `wgBaueHtmlDatei()` | Generiert die eigenständige Empfänger-HTML |
| `wgReminderPruefen()` | Hinweis nach 12 Monaten, max. 1x pro Woche |

---

## QR-Übergabe (seit beta.8, URL-Format seit beta.10)

### Übersicht

Verschlüsselte Datenübergabe per QR-Code. Ab beta.10 verlinken QR-Codes direkt auf die Leseansicht (`vivodepot-lesen.html`). Erzeuger-Seite (`qr-*`) und Empfänger-Seite (`qre-*`) sind vollständig getrennt — keine gemeinsamen Zustandsvariablen.

### Sicherheitsarchitektur

```
Nutzerdaten (gefiltert nach Profil)
  + eigener Salt (getRandomValues())
  + PIN
  + Zeitstempel iat + Ablauf exp (24 Stunden)
  → PBKDF2 (200.000 Iterationen) → AES-256-GCM
  → Base64url-Payload
  → URL: vivodepot-lesen.html#PAYLOAD   (≤ 1800 Zeichen: 1 QR)
     oder: vivodepot-lesen.html#{p,t,id,d} (> 1800 Zeichen: bis zu 6 QR)
```

### URL-Format (seit beta.10)

Das Hash-Fragment der URL enthält den verschlüsselten Payload als Base64url-String. Das Fragment wird nicht an den Server gesendet — vollständig datenschutzkonform.

```javascript
const QR_LESEN_URL = 'https://carolaklessen.github.io/vivodepot/vivodepot-lesen.html';
// Einzel-QR:
QR_LESEN_URL + '#' + base64url(JSON.stringify({s, c}))
// Chunk-QR:
QR_LESEN_URL + '#' + base64url(JSON.stringify({p, t, id, d}))
```

### Mehr-Teile-Logik (seit beta.10)

| Konstante | Wert | Bedeutung |
|---|---|---|
| `SINGLE_MAX` | 1800 Zeichen | Schwellwert für Einzel-QR |
| `CHUNK_SIZE` | 1200 Zeichen | Größe eines Chunks |
| Max. Chunks | 6 | Bei Überschreitung: Fehlermeldung |

Chunk-Metadaten: `{p: Teilnummer, t: Gesamt, id: "zufällig6", d: "chunkData"}`

### Zentrale Funktionen

| Funktion | Aufgabe |
|---|---|
| `qrErstellen()` | Verschlüsselt Payload, erzeugt 1–6 QR-Codes |
| `qrZeigeCode(idx)` | Rendert QR-Code Nr. idx im Karussell |
| `qrMultiPrev()` / `qrMultiNext()` | Karussell-Navigation |
| `qrEmpfangOpen()` | Öffnet Empfänger-Modal |
| `qreStartKamera()` | Startet getUserMedia + jsQR-Scan |
| `qreScanFrame()` | Liest Kamerabild alle 200 ms |
| `qreQrErkannt()` | Erkennt URL-Format und Legacy-JSON-Format |
| `qreEntschluesseln()` | Entschlüsselt und prüft Ablauf (payload.exp) |

---

## Leseansicht — vivodepot-lesen.html (seit beta.10)

### Übersicht

Eigenständige Empfänger-Seite. Kein Account, keine Installation, kein Netzwerkzugriff, kein Speichern. Logo als Base64 eingebettet. Versionsnummer korrespondiert mit VIVODEPOT.html.

URL: `carolaklessen.github.io/vivodepot/vivodepot-lesen.html`

### Eingabewege

1. **QR-Code scannen** — Kamera via `getUserMedia`, jsQR-Scan alle 200 ms
2. **Weitergabe-Datei öffnen** — Klick oder Drag & Drop, Extraktion via Regex

### Hash-Erkennung beim Laden

```javascript
window.addEventListener('load', function() {
  const hash = window.location.hash.slice(1);
  if (hash && hash.length > 20) ladeVonHash(hash);
});
```

Wenn ein gültiger VIVODEPOT-Payload im Hash-Fragment steckt, springt die Seite direkt zur PIN-Eingabe.

### Multi-Part Chunk-Sammler

```javascript
let _chunks = {}; // { id: { total, parts: {1: data, 2: data, ...} } }
```

Nach jedem erkannten Chunk: Fortschrittsanzeige + automatischer Kameraneustart (1,2 Sekunden). Wenn alle Teile vorliegen: Zusammensetzen → Entschlüsseln → Anzeigen.

### Zentrale Funktionen

| Funktion | Aufgabe |
|---|---|
| `ladeVonHash(hash)` | Parst Hash-Fragment beim Seitenload |
| `startKamera()` | Öffnet Kamera via getUserMedia |
| `scanFrame()` | jsQR-Scan alle 200 ms |
| `verarbeiteQRText(text)` | Erkennt Einzel-QR, Chunk oder Legacy-JSON |
| `verarbeiteChunk(chunk)` | Sammelt Chunks, reassembliert wenn vollständig |
| `ladeDatei(file)` | Liest Weitergabe-HTML, extrahiert Kryptodaten |
| `entschluesseln()` | PBKDF2 + AES-GCM-Entschlüsselung |
| `zeigeDaten(daten, ...)` | Rendert entschlüsselte Felder |
| `zuruecksetzen()` | Setzt Zustand inkl. _chunks zurück |

---

## Solid Pod Export (seit beta.9)

### Übersicht

Export persönlicher Daten im Turtle-Format (.ttl) für den Upload in einen Solid Pod. Vollständig offline, EUPL-konform. Gruppe „Eigener Datenspeicher" im Datenaustausch-Step (seit beta.10 von „Daten weitergeben" getrennt).

### Format

```turtle
@prefix vcard: <http://www.w3.org/2006/vcard/ns#> .
@prefix schema: <https://schema.org/> .
```

### Zentrale Funktionen

| Funktion | Aufgabe |
|---|---|
| `solidPodOpen()` | Öffnet Modal sp-overlay |
| `solidPodClose()` | Schliesst Modal |
| `solidPodExport()` | Baut Turtle-Datei und löst Download aus |
| `solidPodZeigStatus(meldung)` | Zeigt Statusmeldung im Modal |
| `solidPodEsc(s)` | Escaped Sonderzeichen für Turtle |

---

## Export-Funktionen

| Funktion | Format | Bibliothek |
|---|---|---|
| `generatePDF()` | PDF | jsPDF |
| `generateDocx()` | DOCX | docx.js |
| `generateArztbogen()` | PDF | jsPDF |
| `generateArztbogenRadiologie()` | PDF | jsPDF |
| `generateArztbogenPraeop()` | PDF | jsPDF |
| `generateArztbogenGeriatrie()` | PDF | jsPDF |
| `generateScenarioPDF()` | PDF | jsPDF |
| `generateKatastrophenschutzPDF()` | PDF | jsPDF |
| `generateHeimaufnahme()` | PDF | jsPDF |
| `generateBehoerdendaten()` | PDF | jsPDF |
| `generateQRStickers()` | PDF | jsPDF + QRCode |
| `generateVorsorgevollmacht()` | DOCX | docx.js |
| `generatePatientenverfuegung()` | DOCX | docx.js |
| `generateGesundheitsvollmacht()` | DOCX | docx.js |
| `exportVCard()` | VCF | vanilla |
| `exportJSON()` | JSON | vanilla |
| `generateFHIR()` | JSON | vanilla |
| `wgErstellen()` | HTML (verschlüsselt) | Web Crypto API |
| `qrErstellen()` | QR-Code URL | Web Crypto API + QRCode |
| `solidPodExport()` | TTL (Turtle) | vanilla |

---

## Datenaustausch-Step (seit beta.9)

Der Schritt `datenaustausch` bündelt alle Import- und Export-Wege:

**Import-Karten:** FHIR R4, FIM-JSON, JSON (automatisch), EUDI-Wallet (SD-JWT).

**Export-/Übergabe-Karten:** Weitergabe-Datei (`wgErstellen`), QR-Übergabe (`qrErstellen`), QR-Empfang (`qrEmpfangOpen`).

**Eigener Datenspeicher (seit beta.10):** Solid Pod (`solidPodOpen`) — eigene Gruppe, abgegrenzt von Weitergabe-Funktionen.

---

## Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

**1051 Tests in 65 Sektionen** (1050 bestehen, 1 schlägt nur außerhalb des Repos fehl):

1–50. Syntax, bekannte Bugs, Steps, Kernfunktionen, Verschlüsselung, Import/Export, Wizards, Robustheit, Profile, Branding, UX, Notfall, Barrierefreiheit, Mobile, Keyboard, FAB, vCard, ARIA, PWA, Datenspeicher, Recht, Legal, Viewport, Regression
51. Krypto-Portabilität — Salt in Datei (beta.7)
52. Weitergabe-Datei (beta.8)
53. WCAG 2.2 Barrierefreiheit (6 neue Kriterien gegenüber 2.1)
54. Immobilien — Kaufvertrag und Kreditvertrag
55. Testament — Ehevertrag
56. Kinder — Betreuungsmodell und Geburtsurkunde
57. Finanzen — Altersvorsorge
58. Dokumenten-Übersicht im Export
59–62. ANF-07a–c — Basis-Anamnese, Fachspezifische Sicherheitsfelder, Arztbogen-Exporte und Wizard
63. **beta.10 — QR-URL-Format** (7 Tests): `QR_LESEN_URL`, GitHub-Pages-URL, Base64url-Generator, Hash-Fragment, Rückwärtskompatibilität
64. **beta.10 — Mehr-Teile-QR** (14 Tests): `SINGLE_MAX`, `CHUNK_SIZE`, Chunk-Schleife, >6-Fehlerfall, Metadaten-Format, Zustandsvariablen, Karussell-UI-Elemente
65. **beta.10 — ANF-UX-01–07** (8 Tests): Lock-Button-Emoji, Umlaute, Weitergabe-Infobox, Solid-Pod-Gruppe, EUDI-Import, FIM-ec-icon

---

## Krypto-Details

### Schlüssel-Lifecycle (Hauptdatei)

```
Passwort + Salt → PBKDF2 (200.000 It.) → sessionKey (im RAM, nie persistent)
sessionKey + IV  → AES-GCM-Encrypt → ct (in localStorage)
Salt             → localStorage (STORE_META) + HTML-Datei (seit beta.7)
```

### Schlüssel-Lifecycle (Weitergabe-Datei / QR-Übergabe / Leseansicht)

```
Separates Passwort / PIN + eigener Salt (getRandomValues())
  → PBKDF2 (200.000 It.) → wgKey / qrKey (im RAM, nie persistent)
  → AES-GCM-Encrypt
  → in generierter HTML-Datei / QR-URL-Fragment eingebettet
```

### Fehlversuche

Bis zu 5 Passwort-Fehlversuche. Danach wird die Sitzung beendet. Kein automatischer Reset.

### Sitzungsende

`sessionKey = null` beim Schließen des Tabs (`beforeunload`). Nächstes Öffnen erfordert erneute Passworteingabe.

---

## Notfall-Ampelkarten

| Wert | Farbe | Label |
|---|---|---|
| Vorhanden | Grün | Vorhanden |
| Teilweise | Gelb | Teilweise |
| Fehlt noch | Rot | Fehlt noch |
| (leer) | Grau | Antippen |

Klick zyklisch: leer → Vorhanden → Teilweise → Fehlt noch → Vorhanden …

---

## Barrierefreiheits-Funktionen

```javascript
cycleFontSize()     // 3 Stufen: normal, fs-medium, fs-large
toggleKontrast()    // CSS-Klasse 'high-contrast'
toggleNacht()       // CSS-Klasse 'dark-mode'
toggleVorlesen()    // Web Speech API
toggleLupe()        // Lupe-Overlay
startDiktat()       // SpeechRecognition API
```

---

## Bekannte Einschränkungen

- **iOS/PocketBook:** HTML-Dateien werden von PocketBook als Standard-App geöffnet. Workaround: Datei mit `.htm`-Endung speichern und über Teilen → Safari öffnen.
- **DuckDuckGo Browser:** Unterstützt keine lokalen HTML-Dateien (file://-Protokoll).
- **localStorage-Limit:** Ca. 5 MB pro Domain. Bei vielen hochgeladenen Dateien kann dieses Limit erreicht werden.
- **Safari iOS:** `showSaveFilePicker` nicht unterstützt — Fallback auf `a.click()` mit iOS-spezifischer Anleitung.
- **QR-Kapazität:** Bei sehr großen Profilen (> 6 Chunks) ist die Weitergabe-Datei der geeignete Kanal.
