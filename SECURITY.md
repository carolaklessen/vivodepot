# Sicherheitsrichtlinie / Security Policy

## Unterstützte Versionen / Supported Versions

| Version | Unterstützt |
|---------|-------------|
| 1.0.x-beta.4 | ✅ Ja |

## Sicherheitslücke melden / Reporting a Vulnerability

Wenn Sie eine Sicherheitslücke in VIVODEPOT gefunden haben, melden Sie diese bitte **nicht** über ein öffentliches GitHub Issue.

Senden Sie stattdessen eine E-Mail an:

**feedback@vivodepot1.odoo.com**

Bitte beschreiben Sie:
- Die Art der Sicherheitslücke
- Schritte zur Reproduktion
- Mögliche Auswirkungen
- Ggf. einen Lösungsvorschlag

Wir werden innerhalb von **72 Stunden** antworten und die Meldung vertraulich behandeln.

---

## Architektur-Sicherheit

VIVODEPOT wurde mit folgenden Sicherheitsprinzipien entwickelt:

### Datenhoheit
- **Keine Server-Kommunikation** — alle Daten bleiben lokal
- **Kein Tracking, keine Cookies, keine Analytics**
- **Kein Account-System** — keine Registrierung nötig
- Externe CDN-Bibliotheken werden nur für PDF/Word-Erzeugung geladen

### Verschlüsselung
- **AES-256-GCM** über die Web Crypto API
- Schlüsselableitung via PBKDF2 (100.000 Iterationen, SHA-256)
- Session-Key wird nur im RAM gehalten
- Salt wird pro Verschlüsselung neu generiert

### DuckDuckGo Browser
- DuckDuckGo überschreibt bestimmte globale JavaScript-Variablen (u.a. `_ls`) mit `localStorage` — VIVODEPOT arbeitet daher ohne globale localStorage-Wrapper
- Spracheingabe ist in DuckDuckGo nicht unterstützt und standardmäßig deaktiviert

### Bekannte Einschränkungen
- **localStorage** ist nicht verschlüsselt auf Betriebssystem-Ebene — physischer Zugriff auf den Rechner ermöglicht Zugriff auf unverschlüsselte Daten
- **CDN-Bibliotheken** (docx, jsPDF, qrcode) werden ohne SRI-Hashes geladen — für erhöhte Sicherheit in Unternehmensumgebungen können SRI-Hashes nachgerüstet werden
- **Service Worker via Blob-URL** — kann in Browsern mit strenger Content Security Policy blockiert werden
- **Web Crypto API** ist unter `file://`-Protokoll auf iOS Safari nicht verfügbar — die App erkennt dies und bietet einen Fallback
