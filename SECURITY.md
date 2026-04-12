# VIVODEPOT — Sicherheitsrichtlinie

*Version 1.0.0-beta.7 · April 2026*

---

## Unterstützte Versionen

| Version | Support |
|---|---|
| 1.0.0-beta.7 | Aktiv |
| 1.0.0-beta.6 | Sicherheitsrelevanter Fehler (BUG-SALT) — Update empfohlen |
| < 1.0.0-beta.6 | Nicht unterstützt |

---

## Sicherheitsarchitektur

VIVODEPOT ist durch seine Architektur maximal sicher:

- **Keine Netzwerkkommunikation:** Die App sendet keinerlei Daten an externe Server. Es gibt keinen Angriffspunkt über das Netzwerk.
- **Lokale Verschlüsselung:** AES-256-GCM mit PBKDF2-HMAC-SHA256 (100.000 Iterationen, kryptographisch zufälliger Salt). Implementiert über die Web Crypto API des Browsers — keine externe Kryptobibliothek.
- **Salt in gespeicherter Datei (seit beta.7):** Der Salt ist in die gespeicherte HTML-Datei eingebettet. Die Datei ist damit auf jedem Gerät mit dem korrekten Passwort entschlüsselbar — ohne Abhängigkeit vom localStorage des Ursprungsgeräts.
- **Kein Server:** Es gibt keinen Server, der kompromittiert werden könnte.
- **Kein Account:** Keine Passwort-Datenbank, kein Credential-Leak.
- **Inline-Bibliotheken:** Alle Drittbibliotheken sind direkt eingebettet — kein Supply-Chain-Angriff über CDNs möglich.

---

## Sicherheitslücken melden

Wenn Sie eine Sicherheitslücke entdecken, melden Sie diese bitte vertraulich:

**E-Mail:** [feedback@vivodepot.de](mailto:feedback@vivodepot.de)
**Betreff:** `[SECURITY] Kurzbeschreibung`

Bitte keine öffentlichen GitHub-Issues für Sicherheitslücken.

### Was wir benötigen

- Beschreibung der Lücke
- Schritte zur Reproduktion
- Betroffene Version(en)
- Potenzielle Auswirkungen

### Was Sie erwarten können

- Bestätigung des Eingangs innerhalb von 48 Stunden
- Regelmäßige Updates zum Bearbeitungsstand
- Anerkennung in der Versionsnote (wenn gewünscht)

---

## Behobene Sicherheitsprobleme

### BUG-SALT (behoben in beta.7)

**Beschreibung:** Der kryptographische Salt wurde ausschließlich im `localStorage` des Browsers gespeichert. Beim Öffnen einer gespeicherten Datei auf einem anderen Gerät fehlte der Salt — die Entschlüsselung schlug fehl, obwohl das Passwort korrekt war. Betroffene Nutzende erhielten keinen Hinweis auf den eigentlichen Fehler.

**Auswirkung:** Daten waren auf dem Ursprungsgerät weiterhin zugänglich. Auf anderen Geräten war der Zugang ohne manuellen localStorage-Eingriff nicht möglich.

**Fix:** `saveAsHTML()` bettet den Salt jetzt in die HTML-Datei ein. Beim Öffnen wird er idempotent in `localStorage` wiederhergestellt.

---

## Bekannte Einschränkungen

- **localStorage ohne Passwortschutz:** Daten sind unverschlüsselt, wenn kein Passwort gesetzt wurde. Empfehlung: Passwortschutz immer aktivieren.
- **Gerätesicherheit:** Wenn das Gerät kompromittiert ist (Malware, Keylogger), kann auch VIVODEPOT nicht schützen.
- **Passwort nicht wiederherstellbar:** By Design — nur der Nutzer kennt das Passwort. Es gibt keinen Reset-Mechanismus.

---

## Responsible Disclosure

Wir verpflichten uns zu verantwortungsvollem Umgang mit gemeldeten Sicherheitslücken. Bitte geben Sie uns angemessene Zeit zur Behebung, bevor Sie eine Lücke öffentlich machen.
