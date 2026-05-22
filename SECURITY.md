# Vivodepot — Sicherheitsrichtlinie

*Stand: Mai 2026 · Version 1.0.0-beta.16*

---

## Sicherheitslücken melden

**E-Mail:** [security@vivodepot.de](mailto:security@vivodepot.de)
**Betreff:** `[SECURITY] Kurzbeschreibung`
**PGP-Fingerprint:** `30FB 9B42 7F12 095D 317B  4485 F527 3B32 959A 7D42`
**Öffentlicher Schlüssel:** [`security/pgp-pubkey.asc`](security/pgp-pubkey.asc) (RSA-4096, gültig bis 2029-05-15)

Bitte keine öffentlichen GitHub-Issues für Sicherheitslücken — diese erreichen Vivodepot über den vertraulichen Kanal schneller und schützen die Nutzer-Basis bis zur Behebung.

### Was wir benötigen

- Beschreibung der Lücke
- Schritte zur Reproduktion
- Betroffene Version(en)
- Potenzielle Auswirkungen
- Optional: Vorschlag zur Behebung

### Was Sie erwarten können

- Eingangsbestätigung innerhalb 48 Stunden
- Regelmäßige Updates zum Bearbeitungsstand
- Anerkennung in der Versionsnote (wenn gewünscht)
- Bei kritischen Lücken: koordinierte Veröffentlichung nach Behebung

---

## Unterstützte Versionen

| Version | Support |
|---|---|
| 1.0.0-beta.16 | Aktiv |
| 1.0.0-beta.15 | Unterstützt — Update empfohlen |
| 1.0.0-beta.14 | Unterstützt — Update empfohlen |
| 1.0.0-beta.13 | Unterstützt |
| 1.0.0-beta.12 | Unterstützt |
| 1.0.0-beta.11 | Unterstützt |
| 1.0.0-beta.10 | Unterstützt |
| 1.0.0-beta.9 | Unterstützt — Update empfohlen |
| 1.0.0-beta.8 | Unterstützt |
| 1.0.0-beta.7 | Unterstützt |
| 1.0.0-beta.6 | Sicherheitsrelevanter Fehler (BUG-SALT) — Update empfohlen |
| < 1.0.0-beta.6 | Nicht unterstützt |

Version 1.0 ist in Entwicklung. Bei Veröffentlichung wird diese Tabelle entsprechend ergänzt.

---

## Sicherheitsarchitektur

### VIVODEPOT.html

- **Keine Netzwerkkommunikation:** Die Anwendung sendet keinerlei Daten an externe Server.
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

### Feedback-Formular (seit beta.16)

Das Inline-Feedback-Formular sendet keine Daten an Server. Text wird entweder per `mailto:` an die E-Mail-App übergeben oder in die Zwischenablage kopiert. Der Text verlässt das Gerät nur durch die Aktion der Person.

### Prüftermin-Erinnerungen (seit beta.16)

Die Web Notifications API erfordert eine einmalige Browser-Berechtigung. Die Erlaubnis wird nie automatisch angefragt — nur auf expliziten Wunsch in den Einstellungen. Die Benachrichtigungen enthalten keine Nutzerdaten, nur generische Texte wie „Prüftermin fällig". Keine Server-Kommunikation.

---

## Behobene Sicherheitsprobleme

### BUG-SALT (behoben in beta.7)

**Beschreibung:** Salt ausschließlich in `localStorage`. Auf anderen Geräten fehlte er — Entschlüsselung schlug fehl trotz korrektem Passwort.

**Fix:** `saveAsHTML()` bettet Salt in die HTML-Datei ein. Beim Öffnen idempotent wiederhergestellt.

---

## Bekannte Einschränkungen

- **Kein Passwortschutz:** Ohne gesetztes Passwort sind Daten unverschlüsselt im localStorage. Empfehlung: Passwortschutz immer aktivieren.
- **Gerätesicherheit:** Kompromittiertes Gerät (Malware, Keylogger) kann auch Vivodepot nicht schützen.
- **Passwort nicht wiederherstellbar:** By Design.
- **Privathandy bei QR-Übergabe:** Technisch nicht erzwingbar. Die Leseansicht enthält einen Hinweis auf Praxis-/Dienstgeräte. Verantwortung liegt bei der Institution.
- **Web Notifications:** Benachrichtigungen werden vom Browser verwaltet. Auf iOS nicht unterstützt. Inhalt der Benachrichtigungen ist sichtbar auf dem Sperrbildschirm.

---

## Kontakt

- Sicherheitsmeldungen: [security@vivodepot.de](mailto:security@vivodepot.de) · PGP `30FB 9B42 7F12 095D 317B  4485 F527 3B32 959A 7D42` ([Schlüssel](security/pgp-pubkey.asc))
- Allgemein: [kontakt@vivodepot.de](mailto:kontakt@vivodepot.de)
