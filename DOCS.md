# VIVODEPOT — Technische Dokumentation

*Version 1.0.0-beta.8 · April 2026*

---

## Architektur

VIVODEPOT ist eine **Einzeldatei-HTML-Anwendung** (ca. 1,3 MB). Keine Build-Pipeline, kein Framework, kein CDN.

```
VIVODEPOT.html
├── CSS (eingebettet)
├── Inline-Bibliotheken
│   ├── jsPDF 2.5.1 (364 KB) — PDF-Erstellung
│   ├── docx.js 8.5.0 (368 KB) — Word-Erstellung
│   └── QRCode-Generator 1.4.4 (20 KB) — QR-Codes
├── JavaScript (Hauptlogik)
│   ├── Datenspeicherung (localStorage + AES-256-GCM)
│   ├── STEP_RENDERERS (20 Schritte)
│   ├── Export-Funktionen (13 Formate)
│   ├── Wizard-System
│   ├── Weitergabe-Datei-System (neu in beta.8)
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

```javascript
// Eingebettet in die gespeicherte Datei (vereinfacht):
(function(){
  try { data = { /* Nutzerdaten */ }; } catch(e){ data={}; }
  try {
    if (!localStorage.getItem('vivodepot_v1_meta')) {
      localStorage.setItem('vivodepot_v1_meta', '<salt-base64>');
    }
  } catch(e) {}
  showSavedFileWelcome();
})();
```

### Datei-Speicherung

`saveAsHTML()` erstellt eine HTML-Datei mit eingebetteten Daten und eingebettetem Salt. Der INIT-Block wird durch regulären Ausdruck ersetzt:

```
/\/\/ [═]+\s*\/\/ INIT[\s\S]*?\}\)\(\);/
```

Der Kommentar lautet in allen Varianten:

```
// ═══════════════════════════════════════════════
// INIT  (bzw. INIT (mit eingebetteten Daten))
// ═══════════════════════════════════════════════
```

---

## Weitergabe-Datei (neu in beta.8)

### Übersicht

Die Weitergabe-Funktion erstellt eine eigenständige HTML-Datei mit einem gefilterten Datensatz und separater Verschlüsselung. Die Empfängerin öffnet die Datei im Browser — ohne VIVODEPOT, ohne Installation.

### Sicherheitsarchitektur

```
Nutzerdaten (gefiltert nach Profil)
  + eigener Salt (getRandomValues())
  + separates Passwort
  → PBKDF2 → AES-256-GCM
  → eigenständige HTML-Datei
```

Das Hauptpasswort kann die Weitergabe-Datei nicht entschlüsseln. Die Verschlüsselungen sind vollständig unabhängig.

### Profile und Felder

| Profil | Felder |
|---|---|
| Notfall | vorname, nachname, geburtsdatum, adresse, plz, ort, blutgruppe, allergien, medikamente, krankheiten, hausarzt, notfallkontakte, patientenverf_vorhanden, patientenverf_ort |
| Vollmacht | vorname, nachname, geburtsdatum, adresse, plz, ort, vollmacht_person, vollmacht_ort, vollmacht_vorhanden, patientenverf_vorhanden, patientenverf_ort, betreuer, nachlassgericht |
| Familie | vorname, nachname, geburtsdatum, adresse, plz, ort, konten, versicherungen, vertraege, testament_vorhanden, testament_ort, testamentsvollstrecker, bestattungswunsch, persoenliche_botschaft, notfallkontakte |
| Behörde | vorname, nachname, geburtsdatum, adresse, plz, ort, ausweis_nr, steuer_id, iban, kv_name, kv_nr, rv_nr |

### Zentrale Funktionen

| Funktion | Aufgabe |
|---|---|
| `weitergabeOpen()` | Öffnet das Modal, setzt Zustand zurück |
| `weitergabeClose()` | Schliesst das Modal |
| `wgZeigeSchritt(nr)` | Wechselt zwischen Schritt 1, 2 und 3 |
| `wgWaehleProfilCard(profil)` | Profil-Auswahl, zeigt Behörden-Dropdown bei Bedarf |
| `wgPwInput()` | Passwort-Stärke prüfen, Weiter-Button freischalten |
| `wgErstellen()` | Kern-Logik: filtern, verschlüsseln, HTML bauen, herunterladen |
| `wgBegleitKopieren()` | Begleittext in Zwischenablage |
| `wgBaueHtmlDatei()` | Generiert die eigenständige Empfänger-HTML |
| `wgReminderPruefen()` | Hinweis nach 12 Monaten, max. 1x pro Woche |

### Overlay-Verwaltung

`wg-overlay` ist in beiden zentralen Overlay-Verwaltungsfunktionen registriert:

```javascript
// showOverlay(id) — schliesst alle anderen Overlays zuerst
['welcome-overlay', 'return-overlay', ..., 'wg-overlay']

// hideAllOverlays() — schliesst alle Overlays
['welcome-overlay', 'return-overlay', ..., 'wg-overlay']
```

### Reminder

Beim Wechsel zum Export-Tab wird `wgReminderPruefen()` aufgerufen. Der Reminder erscheint, wenn:

- eine Weitergabe-Datei erstellt wurde (`localStorage: vivodepot_wg_datum`)
- diese älter als 365 Tage ist
- der letzte Hinweis mindestens 7 Tage zurückliegt

Der Banner ist nicht blockierend und hat einen Schliessen-Button.

---

## Step-System

20 Schritte (0-indexiert):

| Index | ID | Label |
|---|---|---|
| 0 | start | Über mich |
| 1 | kontakte | Vertrauenspersonen |
| 2 | infokontakte | Zu informieren |
| 3 | finanzen | Finanzen |
| 4 | versich | Versicherungen |
| 5 | immobilien | Immobilien |
| 6 | vertraege | Verträge & Abos |
| 7 | testament | Testament & Vollmachten |
| 8 | gesundheit | Gesundheit |
| 9 | pflege | Pflege |
| 10 | haustiere | Haustiere |
| 11 | digital | Digitales Erbe |
| 12 | persoenliches | Persönliches |
| 13 | bestattung | Bestattung |
| 14 | assistenten | Assistenten |
| 15 | notfall | Notfall & Katastrophenschutz |
| 16 | dokumente | Dokumente erstellen |
| 17 | erinnerung | Erinnerungen |
| 18 | einstellungen | Einstellungen |
| 19 | exportStep | Export (intern) |

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

---

## Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

**877 Tests in 52 Sektionen:**

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
17. Barrierefreiheit
18. vCard
19. Notfall/BBK
20. Browser-Kompatibilität
21. Export-Qualität
22. Datenspeicherung
23. Internationalisierung
24. PWA
25. Rechtliche Inhalte
26. Externe Links
27. Exporte gesamt
28. Vollmachten
29. Robustheit (erweitert)
30. Update-Integration
31. Eingabe-Hilfe
32. Vollständigkeits-Regression
33. Krypto-Portabilität (Salt in Datei)
34–51. Weitere Regressions- und Qualitätssektionen
52. Weitergabe-Datei (WG-01 bis WG-16b) — neu in beta.8

---

## Krypto-Details

### Schlüssel-Lifecycle (Hauptdatei)

```
Passwort + Salt → PBKDF2 → sessionKey (im RAM, nie persistent)
sessionKey + IV  → AES-GCM-Encrypt → ct (in localStorage)
Salt             → localStorage (STORE_META) + HTML-Datei (seit beta.7)
```

### Schlüssel-Lifecycle (Weitergabe-Datei)

```
Separates Passwort + eigener Salt (getRandomValues())
  → PBKDF2 → wgKey (im RAM, nie persistent)
  → AES-GCM-Encrypt → in generierter HTML-Datei eingebettet
```

### Fehlversuche

Bis zu 5 Passwort-Fehlversuche. Danach wird die Sitzung beendet. Kein automatischer Reset.

### Sitzungsende

`sessionKey = null` beim Schließen des Tabs (`beforeunload`). Nächstes Öffnen erfordert erneute Passworteingabe.

---

## Notfall-Ampelkarten

Die Katastrophenschutz-Karten haben drei Zustände:

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

- **iOS/PocketBook:** HTML-Dateien werden von PocketBook als Standard-App geöffnet. Workaround: Datei auf iOS mit `.htm`-Endung speichern und in der Dateien-App über Teilen → Safari öffnen.
- **DuckDuckGo Browser:** Unterstützt keine lokalen HTML-Dateien (file://-Protokoll).
- **localStorage-Limit:** Ca. 5 MB pro Domain. Bei vielen hochgeladenen Dateien kann dieses Limit erreicht werden.
- **Safari iOS:** `showSaveFilePicker` nicht unterstützt — Fallback auf `a.click()` mit iOS-spezifischer Anleitung.
