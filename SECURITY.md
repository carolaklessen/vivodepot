# VIVODEPOT — Sicherheitsrichtlinie

## Unterstützte Versionen

| Version | Support |
|---|---|
| 1.0.0-beta.6 | ✅ Aktiv |
| < 1.0.0-beta.6 | ❌ Nicht mehr unterstützt |

## Sicherheitsarchitektur

**VIVODEPOT ist by Design maximal sicher:**

- **Keine Netzwerkkommunikation:** Die App sendet keinerlei Daten an externe Server. Es gibt keinen Angriffspunkt über das Netzwerk.
- **Lokale Verschlüsselung:** AES-256-GCM mit PBKDF2-HMAC-SHA256 (100.000 Iterationen, zufälliger Salt). Implementiert über die Web Crypto API des Browsers — keine externe Kryptobibliothek.
- **Kein Server:** Es gibt keinen Server, der gehackt werden könnte.
- **Kein Account:** Keine Passwort-Datenbank, kein Credential-Leak.
- **Inline-Bibliotheken:** Alle Drittbibliotheken sind direkt eingebettet — kein Supply-Chain-Angriff über CDNs möglich.

## Sicherheitslücken melden

Wenn Sie eine Sicherheitslücke entdecken, melden Sie diese bitte **vertraulich**:

**E-Mail:** [feedback@vivodepot.de](mailto:feedback@vivodepot.de)
**Betreff:** `[SECURITY] Kurzbeschreibung`

Bitte **keine** öffentlichen GitHub-Issues für Sicherheitslücken.

### Was wir benötigen

- Beschreibung der Lücke
- Schritte zur Reproduktion
- Betroffene Version(en)
- Potenzielle Auswirkungen

### Was Sie erwarten können

- Bestätigung des Eingangs innerhalb von 48 Stunden
- Regelmäßige Updates zum Bearbeitungsstand
- Anerkennung in der Versionsnote (wenn gewünscht)

## Bekannte Einschränkungen

- **localStorage ist nicht verschlüsselt** ohne aktivierten Passwortschutz. Empfehlung: Passwortschutz immer aktivieren.
- **Browser-Sicherheit gilt:** Wenn das Gerät kompromittiert ist (Malware, Keylogger), kann auch VIVODEPOT nicht schützen.
- **iOS/PocketBook-Problem:** HTML-Dateien öffnen sich auf iOS möglicherweise in PocketBook statt im Browser. Das ist kein Sicherheitsproblem, aber ein Nutzungsproblem.

## Responsible Disclosure

Wir verpflichten uns zu verantwortungsvollem Umgang mit gemeldeten Sicherheitslücken. Bitte geben Sie uns angemessene Zeit zur Behebung, bevor Sie eine Lücke öffentlich machen.
