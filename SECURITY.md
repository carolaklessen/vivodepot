# VIVODEPOT — Sicherheitsrichtlinie

*Version 1.0.0-beta.11 · April 2026*

---

## Unterstützte Versionen

| Version | Support |
|---|---|
| 1.0.0-beta.11 | Aktiv |
| 1.0.0-beta.10 | Unterstützt — Update empfohlen |
| 1.0.0-beta.9 | Unterstützt — Update empfohlen |
| 1.0.0-beta.8 | Unterstützt |
| 1.0.0-beta.7 | Unterstützt |
| 1.0.0-beta.6 | Sicherheitsrelevanter Fehler (BUG-SALT) — Update empfohlen |
| < 1.0.0-beta.6 | Nicht unterstützt |

---

## Sicherheitsarchitektur

### VIVODEPOT.html

- **Keine Netzwerkkommunikation:** Die App sendet keinerlei Daten an externe Server.
- **Lokale Verschlüsselung:** AES-256-GCM mit PBKDF2-HMAC-SHA256 (200.000 Iterationen, kryptographisch zufälliger Salt). Web Crypto API — keine externe Bibliothek.
- **Salt in gespeicherter Datei (seit beta.7):** Auf jedem Gerät mit korrektem Passwort entschlüsselbar.
- **Kein Server, kein Account, kein CDN.**
- **Inline-Bibliotheken:** Kein Supply-Chain-Angriff möglich.

### QR-Übergabe — Hash-Fragment (seit beta.10)

Der verschlüsselte Payload steckt im `#`-Fragment der URL:

```
vivodepot-lesen.html#BASE64URL_PAYLOAD
```

Das Fragment wird nicht an den Server gesendet. Nur der Browser und der Empfänger kennen den Payload. Selbst wenn die URL abgefangen wird, ist der Payload ohne PIN nicht entschlüsselbar.

### vivodepot-lesen.html

- Kein Speichern — entschlüsselte Daten existieren nur im RAM.
- Kein Netzwerkzugriff nach dem Laden.
- Keine Cookies, kein localStorage, kein Tracking.
- Logo als Base64 eingebettet — vollständig selbsttragend.

---

## Sicherheitslücken melden

**E-Mail:** [feedback@vivodepot.de](mailto:feedback@vivodepot.de)  
**Betreff:** `[SECURITY] Kurzbeschreibung`

Bitte keine öffentlichen GitHub-Issues für Sicherheitslücken.

### Was wir benötigen

- Beschreibung der Lücke
- Schritte zur Reproduktion
- Betroffene Version(en)
- Potenzielle Auswirkungen

### Was Sie erwarten können

- Eingangsbestätigung innerhalb 48 Stunden
- Regelmäßige Updates zum Bearbeitungsstand
- Anerkennung in der Versionsnote (wenn gewünscht)

---

## Behobene Sicherheitsprobleme

### BUG-SALT (behoben in beta.7)

**Beschreibung:** Salt ausschließlich in `localStorage`. Auf anderen Geräten fehlte er — Entschlüsselung schlug fehl trotz korrektem Passwort.

**Fix:** `saveAsHTML()` bettet Salt in die HTML-Datei ein. Beim Öffnen idempotent wiederhergestellt.

---

## Bekannte Einschränkungen

- **Kein Passwortschutz:** Ohne gesetztes Passwort sind Daten unverschlüsselt im localStorage. Empfehlung: Passwortschutz immer aktivieren.
- **Gerätesicherheit:** Kompromittiertes Gerät (Malware, Keylogger) kann auch VIVODEPOT nicht schützen.
- **Passwort nicht wiederherstellbar:** By Design.
- **Privathandy bei QR-Übergabe:** Technisch nicht erzwingbar. Die Leseansicht enthält einen Hinweis auf Praxis-/Dienstgeräte. Verantwortung liegt bei der Institution.
