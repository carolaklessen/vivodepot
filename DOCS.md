# VIVODEPOT — Technische Dokumentation

*Version 1.0.0-beta.16 · April 2026*

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
│   ├── STEP_RENDERERS (22 Schritte)
│   ├── Export-Funktionen (16 Formate)
│   ├── Import-Funktionen (FHIR, FIM, JSON, EUDI, QR)
│   ├── Weitergabe-Datei-System (wg-*)
│   ├── QR-Übergabe-System (qr-* / qre-*) — URL-Format seit beta.10
│   ├── Solid Pod Export (sp-*)
│   ├── Vorlagen-Editor (tplEditor-*) — seit beta.16
│   ├── Feedback-Formular (feedback-*) — seit beta.16
│   ├── Prüftermin-Erinnerungen (erinnerung-*) — seit beta.16
│   ├── Wizard-System
│   └── Barrierefreiheits-Funktionen
└── HTML (UI-Struktur)

vivodepot-lesen.html
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

`saveAsHTML()` liest den Salt vor dem Speichern aus `localStorage` und bettet ihn in den INIT-Block der HTML-Datei ein. Beim Öffnen auf einem neuen Gerät schreibt der INIT-Block den Salt synchron in `localStorage`, bevor `loadData()` ihn benötigt. Der bestehende Salt wird dabei nicht überschrieben (idempotent).

---

## Step-System

22 Schritte (seit beta.11):

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
| 8 | prom | Wohlbefinden & Seele |
| 9 | pflege | Pflege |
| 10 | testament | Mein Wille |
| 11 | bestattung | Mein Abschied |
| 12 | persoenliches | Erinnerungsstücke |
| 13 | haustiere | Haustiere |
| 14 | digital | Digitales Erbe |
| 15 | assistenten | Assistenten |
| 16 | notfall | Notfall & Katastrophenschutz |
| 17 | dokumente | Dokumente erstellen |
| 18 | datenaustausch | Datenaustausch |
| 19 | erinnerung | Prüftermine |
| 20 | exportStep | Export (intern) |
| 21 | einstellungen | Einstellungen |
| Sonderposition | institutionen | Für Institutionen |

---

## Weitergabe-Datei (seit beta.8)

### Sicherheitsarchitektur

```
Nutzerdaten (gefiltert nach Profil)
  + eigener Salt (getRandomValues())
  + separates Passwort
  → PBKDF2 (200.000 Iterationen) → AES-256-GCM
  → eigenständige HTML-Datei
```

### Zentrale Funktionen

| Funktion | Aufgabe |
|---|---|
| `weitergabeOpen()` | Öffnet das Modal, setzt Zustand zurück |
| `weitergabeClose()` | Schliesst das Modal |
| `wgZeigeSchritt(nr)` | Wechselt zwischen Schritt 1, 2 und 3 |
| `wgWaehleProfilCard(profil)` | Profil-Auswahl |
| `wgErstellen()` | Kern-Logik: filtern, verschlüsseln, HTML bauen, herunterladen |
| `wgBaueHtmlDatei()` | Generiert die eigenständige Empfänger-HTML |

---

## QR-Übergabe (seit beta.8, URL-Format seit beta.10)

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

### Mehr-Teile-Logik

| Konstante | Wert | Bedeutung |
|---|---|---|
| `SINGLE_MAX` | 1800 Zeichen | Schwellwert für Einzel-QR |
| `CHUNK_SIZE` | 1200 Zeichen | Größe eines Chunks |
| Max. Chunks | 6 | Bei Überschreitung: Fehlermeldung |

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

Eigenständige Empfänger-Seite. Kein Account, keine Installation, kein Netzwerkzugriff, kein Speichern.

URL: `carolaklessen.github.io/vivodepot/vivodepot-lesen.html`

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

## Institutionen-Bereich

### Companion-Schema (v1.0)

Fragebogen-Vorlagen folgen dem Companion-Schema v1.0 (JSON). Pflichtfelder: `schemaVersion`, `id`, `version`, `locale`, `title`, `issuer`, `scale`, `items`, `scoring`, `license`.

### Vorlagen-Editor (seit beta.16)

Erstellt und bearbeitet Vorlagen direkt in der App — kein Texteditor, kein JSON-Wissen erforderlich.

| Funktion | Aufgabe |
|---|---|
| `tplEditorNew()` | Öffnet leere Vorlage im Editor |
| `tplEditorClose()` | Schließt Editor nach Rückfrage (vivoConfirm) |
| `tplEditorReadForm()` | Liest Formularfelder in Draft zurück |
| `tplEditorAddItem()` | Frage hinzufügen |
| `tplEditorRemoveItem(idx)` | Frage entfernen (min. 1 bleibt) |
| `tplEditorAddOption()` | Skala-Option hinzufügen |
| `tplEditorRemoveOption(idx)` | Skala-Option entfernen (min. 2 bleiben) |
| `tplEditorTogglePreview()` | Vorschau ein-/ausblenden |
| `tplEditorBuildTemplate()` | Finales Template-Objekt bauen, Scoring automatisch |
| `tplEditorSave()` | Validiert und speichert in App (localStorage) |
| `tplEditorExport()` | Validiert und lädt als .json herunter |
| `tplEditorRender()` | Gibt HTML des Editor-Formulars zurück |

**Zustandsvariablen:** `_tplEditorOpen`, `_tplEditorDraft`, `_tplEditorPreview`.

**Validierung:** `tplValidate()` wird in `tplEditorSave()` und `tplEditorExport()` aufgerufen. Fehlermeldung listet alle Probleme verständlich auf.

**Scoring-Ranges** werden automatisch aus Skala und Fragenanzahl berechnet. Keine manuelle Konfiguration erforderlich (manuell anpassbar nach Export).

### Vorlagen-Verwaltung

| Funktion | Aufgabe |
|---|---|
| `tplValidate(t)` | Prüft Template gegen Companion-Schema v1.0 |
| `tplGetLoaded()` | Gibt Liste geladener Templates zurück |
| `tplSave(t)` | Speichert Template in localStorage |
| `tplRemove(id)` | Entfernt Template nach Rückfrage |
| `tplLoadFromFile(file)` | Liest JSON-Datei, validiert und speichert |
| `downloadInstitutionTemplate()` | Lädt Muster-Vorlage herunter |
| `tplRenderItems(t)` | Rendert Fragen als Chip-Buttons |
| `tplCalcScore(t)` | Berechnet Gesamtscore |
| `tplDownloadFhir(id)` | Exportiert ausgefüllte Vorlage als FHIR-JSON |

---

## Feedback-Formular (seit beta.16)

Fallback wenn die externe E-Mail-App nicht öffnet (ältere Android-Geräte).

| Funktion | Aufgabe |
|---|---|
| `feedbackOpen()` | Öffnet Formular-Overlay, setzt Fokus |
| `feedbackClose()` | Schließt Formular |
| `feedbackBuildText()` | Baut Text: Nutzertext + Version + Gerät + Browser |
| `feedbackSend()` | Öffnet E-Mail-App per mailto: |
| `feedbackCopy()` | Kopiert Text per Clipboard-API |
| `feedbackCopyFallback(full)` | execCommand-Fallback für ältere Browser |

**HTML-Element:** `#feedback-overlay` (display:none, Overlay-Modal).

---

## Prüftermin-Erinnerungen (seit beta.16)

Primär: Web Notifications API. Fallback: Hinweis-Balken.

| Funktion | Aufgabe |
|---|---|
| `erinnerungFaelligeItems()` | Gibt fällige (≥11 Monate) und überfällige (≥14 Monate) Einträge zurück |
| `erinnerungNotifRequest()` | Fordert Browser-Berechtigung an (nur auf Nutzeraktion) |
| `erinnerungNotifSend(items)` | Sendet eine gebündelte Benachrichtigung |
| `erinnerungNotifCheck(force)` | Haupt-Logik: Notification oder Balken; wird in enterApp() aufgerufen |
| `erinnerungHinweisShow(items)` | Zeigt Amber-Balken bei überfälligen Einträgen |
| `erinnerungHinweisHide()` | Blendet Balken aus |

**HTML-Element:** `#erinnerung-hinweis-bar` (display:none, amber, position:fixed top).

**localStorage-Schlüssel:** `vivodepot_notif_date` — Datum der letzten gesendeten Notification (verhindert mehrfaches Senden pro Tag).

**enterApp():** `erinnerungNotifCheck(false)` wird nach 800 ms aufgerufen.

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
| `generateFHIR()` | JSON (FHIR R4 + IPS 2.0) | vanilla |
| `wgErstellen()` | HTML (verschlüsselt) | Web Crypto API |
| `qrErstellen()` | QR-Code URL | Web Crypto API + QRCode |
| `solidPodExport()` | TTL (Turtle) | vanilla |
| `tplDownloadFhir(id)` | JSON (FHIR PROM) | vanilla |
| `tplEditorExport()` | JSON (Companion-Schema v1.0) | vanilla |

---

## Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

**1.499 Tests in 83 Sektionen — 1.499 bestehen.**

Abgedeckt: Syntax, Verschlüsselung, Navigation, PDF/Word-Export, Barrierefreiheit, Mobile, Offline, Krypto-Portabilität, Weitergabe-Datei, QR-Übergabe, Leseansicht-Logik, EUDI/FHIR-Import, Solid Pod, PROM-Modul, Institutionen-Bereich, DSGVO-Consent, Nutzungsstatistik, Vorlagen-Editor, Feedback-Formular, Prüftermin-Erinnerungen.

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

Bis zu 5 Passwort-Fehlversuche. Danach wird die Sitzung beendet.

### Sitzungsende

`sessionKey = null` beim Schließen des Tabs (`beforeunload`). Nächstes Öffnen erfordert erneute Passworteingabe.

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
- **localStorage-Limit:** Ca. 5 MB pro Domain.
- **Safari iOS:** `showSaveFilePicker` nicht unterstützt — Fallback auf `a.click()`.
- **QR-Kapazität:** Bei sehr großen Profilen (> 6 Chunks) ist die Weitergabe-Datei der geeignete Kanal.
- **Web Notifications iOS:** Nicht unterstützt — Fallback-Balken wird verwendet.
