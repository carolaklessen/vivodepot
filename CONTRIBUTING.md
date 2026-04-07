# Vivodepot

Version: v1.0.0-beta.4

# Beitragen / Contributing

Vielen Dank für Ihr Interesse an VIVODEPOT! Wir freuen uns über jeden Beitrag.

## Erste Schritte

1. **Forken** Sie das Repository
2. **Klonen** Sie Ihren Fork: `git clone https://github.com/carolaklessen/vivodepot.git`
3. **Öffnen** Sie `index.html` im Browser — fertig, keine Build-Tools nötig
4. **Testen** Sie Ihre Änderungen: `python3 test_vivodepot.py index.html` (175 Tests)
5. **Pull Request** erstellen

## Architektur

VIVODEPOT ist bewusst als **einzelne HTML-Datei** ohne Build-System konzipiert. Das bedeutet:

- **Kein npm, kein Webpack, kein Transpiler** — Vanilla JS, Vanilla CSS
- **Alles in einer Datei** — HTML, CSS, JavaScript
- **3 externe Bibliotheken** über CDN (docx, jsPDF, qrcode-generator)
- **Kein Framework** — DOM-Manipulation direkt

### Warum Single-File?
Die Zielgruppe (ältere, nicht computeraffine Personen) soll eine Datei auf einen USB-Stick kopieren und im Browser öffnen können. Kein Installationsprozess, keine Abhängigkeiten, kein Server.

## Richtlinien

### Code-Stil
- **Kein nativer `confirm()`** — immer `vivoConfirm(text, onOk)` verwenden
- **Kein globaler localStorage-Wrapper** — direkt `localStorage` mit try/catch verwenden (DuckDuckGo-Kompatibilität)
- **safeRender()** statt direktem `renderStep()` an Einstiegspunkten
- **FOCUSED_RENDERERS**: Für neue Fokus-Varianten `goalname_stepid:` Einträge ergänzen — schlanke Versionen mit nur relevanten Feldern
- **Keine Emojis in UI-Texten** — Zielgruppe 50+, ernste Themen, professionelles Design. Emojis nur in Export-Karten-Icons (ec-icon) und Topbar-Funktionssymbolen erlaubt — ältere Screenreader haben Probleme damit
- **Tap-Targets mindestens 44×44px** — Barrierefreiheit (alle Touch-Geräte)
- **Input font-size mindestens 16px auf Mobile** — verhindert Auto-Zoom auf iOS und Android
- **`touch-action: manipulation`** auf interaktiven Elementen — kein Tap-Delay
- **`type="tel"`** für Telefonnummer-Felder, **`type="date"`** für Datums-Felder — wird automatisch per Feldname erkannt
- **Schriftgröße mindestens 14px** — Lesbarkeit für ältere Nutzer
- **Generische Feldlabels** — keine provider-spezifischen Begriffe
- **Keine Passwort-Speicherfelder** — nur Ablageort-Hinweise

### Konventionen
- Variablennamen: `camelCase`
- Datenfelder: `snake_case` (für Konsistenz mit `get()`/`set()`)
- Kommentare: `// ═══ ABSCHNITT ═══` für große Blöcke
- Deutsche UI-Texte mit `tl()`-Wrapper für Übersetzbarkeit

### Tests
Vor jedem PR: `python3 test_vivodepot.py index.html` — alle 175 Tests müssen grün sein.

### Was wir suchen
- Bug-Fixes (besonders Browser-Kompatibilität)
- Übersetzungen (EN-Texte in PDFs/Word-Exporten)
- Barrierefreiheit (ARIA-Labels, Tastaturnavigation)
- Mobile-Optimierung
- Sicherheitsverbesserungen
- Dokumentation

### Was wir nicht suchen
- Build-Systeme (npm, Webpack, etc.)
- Frontend-Frameworks (React, Vue, etc.)
- Server-Komponenten
- Datenbank-Integration
- Tracking oder Analytics

## KI-Transparenz

VIVODEPOT wurde mit Unterstützung von KI-Werkzeugen (Claude, Anthropic) entwickelt. Der gesamte Code wurde vom Projektinhaber geprüft, getestet und freigegeben. Wenn Sie KI-Werkzeuge für Ihre Beiträge verwenden, kennzeichnen Sie dies bitte im Pull Request.

## Lizenz

Mit Ihrem Beitrag stimmen Sie zu, dass dieser unter der [EUPL-1.2](LICENSE) lizenziert wird.
