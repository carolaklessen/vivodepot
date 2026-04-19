# SOVEREIGNTY.md — Datensouveränität und WCAG-Begründung
*VIVODEPOT 1.0.0-beta.14 · April 2026*

## 1. Datenhoheit

Vivodepot ist eine vollständig offline-fähige Single-File-Anwendung.
Alle Daten verbleiben ausschliesslich auf dem Gerät der Nutzenden.
Es findet keine Übertragung an Server, Clouds oder Dritte statt.

## 2. WCAG 2.2 — Begründung Abweichungen

### 2.1 Kriterium 3.3.8 — Authentifizierung (Minimum)

Vivodepot verwendet ein nutzerkontrolliertes Geheimnis (Passwort) zur
Verschlüsselung der gespeicherten Daten. Es wird kein CAPTCHA eingesetzt,
da die Anwendung vollständig offline läuft und keinen Server-Zugang benötigt.

Die Authentifizierung entspricht WCAG 2.2 Kriterium 3.3.8:
- kein CAPTCHA erforderlich
- nutzerkontrolliertes Geheimnis (selbst gewähltes Passwort)
- Passwort-Manager und Browser-Autofill werden unterstützt (autocomplete-Attribute gesetzt)

### 2.2 Abschnitt 2.7 — Technische Souveränität

Die Anwendung verwendet ausschliesslich:
- LocalStorage des Browsers (keine externe Datenbank)
- Web Crypto API für AES-256-GCM-Verschlüsselung
- Keine externen Abhängigkeiten zur Laufzeit (alle Bibliotheken eingebettet)

## 3. Lizenz und Nutzung

Alle personenbezogenen Daten bleiben unter vollständiger Kontrolle
der Nutzenden. Vivodepot erhebt, verarbeitet oder speichert keine
Daten ausserhalb des lokalen Geräts.
