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
│   └── jsQR 1.4.0 (256 KB) — QR-Code-Scan (Empfang)
├── JavaScript (Hauptlogik)
│   ├── Datenspeicherung (localStorage + AES-256-GCM)
│   ├── STEP_RENDERERS (21 Schritte)
│   ├── Export-Funktionen (16 Formate)
│   ├── Import-Funktionen (FHIR, FIM, JSON, EUDI, QR)
│   ├── Weitergabe-Datei-System (wg-*)
│   ├── QR-Übergabe-System (qr-* / qre-*)
│   ├── Solid Pod Export (sp-*)
│   ├── Wizard-System
│   └── Barrierefreiheits-Funktionen
└── HTML (UI-Struktur)
```

---

## Datenspeicherung

### Primär: localStorage

```javascript
localStorage.setItem('vivodepot_v1_enc', JSON.stringify(verschluesselt));
```

### Verschlüsselung (optional)

- Algorithmus: AES-256-GCM
- Schlüsselableitung: PBKDF2-HMAC-SHA256 (100.000 Iterationen)
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
| 17 | datenaustausch | Datenaustausch (neu in beta.9) |
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
  → PBKDF2 → AES-256-GCM
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

## QR-Übergabe (seit beta.8)

### Übersicht

Verschlüsselte Datenübergabe per QR-Code. Erzeuger-Seite (qr-*) und Empfänger-Seite (qre-*) sind vollständig getrennt — keine gemeinsamen Zustandsvariablen.

### Sicherheitsarchitektur

```
Nutzerdaten (gefiltert nach Profil)
  + eigener Salt (getRandomValues())
  + PIN
  + Zeitstempel iat + Ablauf exp (24 Stunden)
  → PBKDF2 → AES-256-GCM → QR-Code
```

### Zentrale Funktionen

| Funktion | Aufgabe |
|---|---|
| `qrErstellen()` | Verschlüsselt Payload, erzeugt QR-Code |
| `qrEmpfangOpen()` | Öffnet Empfänger-Modal |
| `qreStartKamera()` | Startet getUserMedia + jsQR-Scan |
| `qreScanFrame()` | Liest Kamerabild alle 200 ms |
| `qreEntschluesseln()` | Entschlüsselt und prüft Ablauf (payload.exp) |

---

## Solid Pod Export (seit beta.9)

### Übersicht

Export persönlicher Daten im Turtle-Format (.ttl) für den Upload in einen Solid Pod. Vollständig offline, EUPL-konform.

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
| `solidPodExport()` | TTL (Turtle) | vanilla |

---

## Datenaustausch-Step (seit beta.9)

Der neue Schritt `datenaustausch` bündelt alle Import- und Export-Wege:

Import-Karten: FHIR R4, FIM-JSON, JSON (automatisch), EUDI-Wallet (SD-JWT).

Export-/Übergabe-Karten: Weitergabe-Datei (wgErstellen), QR-Übergabe (qrErstellen), QR-Empfang (qrEmpfangOpen), Solid Pod (solidPodOpen).

Der Import-Block wurde aus dem Behördendaten-Tab verschoben. Die wg-Link-Zeilen wurden aus dem Export-Tab verschoben.

---

## Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

**898 Tests in 53 Sektionen:**

1. JavaScript-Syntax
2. Bekannte Bugs
3. Steps und Navigation
4. Kernfunktionen (set/get/esc/tl)
5. Verschlüsselung
6. Import/Export
7. Wizards
8. Robustheit
9. Profile und Multi-Profil
10. Branding und Logo
11. User Journeys
12. Kern/Mehr-System
13. Persona-Felder
14. Update-System
15. Mobile und Responsive
16. Fokus-System
17. Keyboard und Navigation
18. FAB und Draggable
19. vCard Export
20. ARIA und Barrierefreiheit
21. Notfallvorsorge und BBK
22. PWA Details
23. Verschlüsselung Details
24. Datenspeicher und Profil
25. Schritt-Inhalte
26. Recht und externe Links
27. Mobile und Responsive
28. Fokus-System
29. Barrierefreiheit (erweitert)
30. vCard und Kontakte
31. Notfall und Katastrophenschutz
32. Browser-Verhalten und Robustheit
33. Export-Qualität
34. Datenspeicherung
35. Internationalisierung
36. PWA und Installation
37. Legal und Compliance
38. Wizards (erweitert)
39. Import-System
40. UX-Details
41. Inhaltliche Vollständigkeit
42. Update-System (erweitert)
43. Exporte — Qualität
44. Vollmachten und Dokumente
45. Robustheit und Fehlerbehandlung
46. Update-System Integration
47. Eingabe-Hilfe und Validierung
48. Vollständigkeits-Regression (Chat-Abgleich)
49. Viewport und Layout-Regression
50. Neue Bugs (BUG-NEW)
51. Krypto-Portabilität (Salt in Datei) — neu in beta.7
52. Weitergabe-Datei — neu in beta.8
53. WCAG 2.2 Barrierefreiheit — neu in beta.10

---

## Krypto-Details

### Schlüssel-Lifecycle (Hauptdatei)

```
Passwort + Salt → PBKDF2 → sessionKey (im RAM, nie persistent)
sessionKey + IV  → AES-GCM-Encrypt → ct (in localStorage)
Salt             → localStorage (STORE_META) + HTML-Datei (seit beta.7)
```

### Schlüssel-Lifecycle (Weitergabe-Datei / QR-Übergabe)

```
Separates Passwort / PIN + eigener Salt (getRandomValues())
  → PBKDF2 → wgKey / qrKey (im RAM, nie persistent)
  → AES-GCM-Encrypt → in generierter HTML-Datei / QR-Code eingebettet
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
