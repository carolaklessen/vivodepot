# VIVODEPOT — Technische Dokumentation

*Version 1.0.0-beta.6 · April 2026*

---

## Architektur

VIVODEPOT ist eine **Einzeldatei-HTML-Anwendung** (~1,3 MB). Keine Build-Pipeline, kein Framework, kein CDN.

```
VIVODEPOT_1.html
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
│   └── Barrierefreiheits-Funktionen
└── HTML (UI-Struktur)
```

---

## Datenspeicherung

### Primär: localStorage
```javascript
localStorage.setItem('vivodepot_data_profil1', JSON.stringify(verschluesselt));
```

### Verschlüsselung (optional)
- Algorithmus: AES-256-GCM
- Schlüsselableitung: PBKDF2-HMAC-SHA256 (100.000 Iterationen)
- Salt: 16 Byte zufällig
- IV: 12 Byte zufällig
- Implementierung: Web Crypto API

### Datei-Speicherung
`saveAsHTML()` erstellt eine neue HTML-Datei mit eingebetteten Daten:
```javascript
// INIT-Block wird ersetzt:
// ═══ INIT (mit eingebetteten Daten) ═══
(function(){
  try { data = { /* vollständige Nutzerdaten */ }; } catch(e){ data={}; }
  showSavedFileWelcome();
})();
```

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

---

## Tests

```bash
python3 test_vivodepot_1.py VIVODEPOT_1.html
```

**802 Tests in 32 Sektionen:**

1. JavaScript-Syntax
2. Bekannte Bugs (BUG-10, BUG-11)
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

---

## Notfall-Ampelkarten

Die Katastrophenschutz-Karten (`ksAmpelCard()`) haben drei Zustände:

| Wert | Farbe | Label |
|---|---|---|
| 'Vorhanden' | Grün | ✅ Vorhanden |
| 'Teilweise' | Gelb/Orange | ⚠️ Teilweise |
| 'Fehlt noch' | Rot | ❌ Fehlt noch |
| (leer) | Grau | Antippen → |

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

- **iOS/PocketBook:** HTML-Dateien werden von PocketBook als Standard-App geöffnet. Workaround: Dateien auf iOS mit `.htm`-Endung speichern.
- **DuckDuckGo Browser:** Unterstützt keine lokalen HTML-Dateien (file://-Protokoll).
- **localStorage-Limit:** ~5 MB pro Domain. Bei vielen hochgeladenen Dateien kann dieses Limit erreicht werden.
- **Safari iOS:** `showSaveFilePicker` nicht unterstützt — Fallback auf `a.click()` mit iOS-spezifischer Anleitung.
