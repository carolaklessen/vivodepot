# Vivodepot — Mitwirken

*Stand: Mai 2026*

Vielen Dank für Ihr Interesse an Vivodepot. Beiträge sind willkommen — Code, Dokumentation, kritische Reviews, Anwendungsszenarien, nationale Anpassungen.

---

## Aktueller Entwicklungsstand

Vivodepot **beta.16** liegt öffentlich auf GitHub. **Version 1.0** mit Sorge-Struktur, übergabefähigen Vollmachten, Anlass-Wizards und neuer Nutzerführung wird derzeit auf einem internen Arbeitsbranch entwickelt; sie wird mit dem v1-Release in dieses Repository überführt.

**Beiträge zur beta.16-Codebasis** sind willkommen, aber bitte beachten: beta.16 ist auf Stabilisierung ausgelegt, nicht auf Funktionserweiterung. Strukturelle Änderungen, neue Module und Architektur-Vorschläge gehen in den v1-Strang ein, nicht in beta.16.

**Beiträge zur Architektur-Diskussion** (Konzepte, ADRs, Standardisierungs-Beiträge, nationale Anpassungen) sind unabhängig vom Release-Strang willkommen.

---

## Wie Sie beitragen können

### Fehler melden

1. Prüfen Sie, ob der Fehler in der aktuellen veröffentlichten Version (beta.16) reproduzierbar ist.
2. Öffnen Sie ein [GitHub Issue](https://github.com/carolaklessen/vivodepot/issues).
3. Beschreiben Sie:
   - Was haben Sie getan?
   - Was ist passiert?
   - Was hätten Sie erwartet?
   - Browser, Betriebssystem, Gerätetyp.
4. Wenn der Fehler reproduzierbar Sicherheitsrelevanz hat, melden Sie ihn bitte über [SECURITY.md](SECURITY.md), nicht öffentlich.

### Verbesserungen vorschlagen

GitHub Issues mit dem Label `enhancement` oder per E-Mail an [kontakt@vivodepot.de](mailto:kontakt@vivodepot.de). Beschreiben Sie:

- Welches Problem die Verbesserung lösen würde — möglichst aus konkreter Bürger- oder Institutions-Sicht.
- Wie eine mögliche Lösung aussieht — auch grobe Skizzen helfen.
- Welche Abwägungen oder Konsequenzen Sie bereits sehen.

### Code-Beiträge

Vivodepot besteht aus zwei selbsttragenden HTML-Dateien (`VIVODEPOT.html` und `vivodepot-lesen.html`) plus Test-Suite. Code-Beiträge folgen dem üblichen Fork-and-Pull-Request-Workflow:

1. Repository forken
2. Branch anlegen mit sprechendem Namen (`feature/...`, `fix/...`, `docs/...`)
3. Änderungen vornehmen
4. Tests ausführen: `python3 test_vivodepot.py VIVODEPOT.html`
5. Pull Request erstellen, Bezug zu Issue oder Konzept-Diskussion verlinken

### Bitte beachten

- **Keine externen Abhängigkeiten einführen.** Vivodepot ist Single-File. Alle Bibliotheken bleiben inline. Pull Requests, die externe Netzwerkaufrufe oder CDN-Bezüge hinzufügen, werden abgelehnt.
- **Vanilla-Tech-Stack.** Kein npm, kein Webpack, kein Framework, kein Transpiler. Pures HTML, CSS, JavaScript. Damit der Code in zehn Jahren noch in jedem Browser läuft.
- **Barrierefreiheit nicht verschlechtern.** Touch-Targets ≥ 44 px (WCAG 2.2), ARIA-Labels, Tastaturnavigation, Schriftgrößen-Anpassung.
- **Bestehende Tests müssen weiterhin laufen.** Neue Funktionen sollten durch Tests abgedeckt werden.
- **Korrekte Orthographie und Kommasetzung** in allen Texten, Labels, Fehlermeldungen.

---

## Beiträge auf Architektur-Ebene

Besonders gesucht — und in vielen Fällen wichtiger als Code-Beiträge — sind Beiträge zur Architektur-Diskussion:

### Nationale Anpassungen

Vivodepot ist in Deutschland gebaut, mit deutschen rechtlichen Rahmen (BGB-Vollmachten, DSGVO-Umsetzung, Patientenrechtegesetz, ZenDiS-Souveränitätsprüfung). Eine in Deutschland gebaute Version bildet nicht automatisch ab, was in Frankreich, der Schweiz, Großbritannien, den Niederlanden oder den nordischen Ländern benötigt wird. Vivodepot ist so angelegt, dass nationale Versionen entstehen können — getragen von Personen, die das jeweilige Recht und die jeweilige Lebenswirklichkeit kennen.

### Migrations-, Flucht- und Einwanderungsgeschichte

Die Lebenswirklichkeit von Menschen mit Asyl-, Duldungs-, Aufenthalts- oder Einbürgerungsgeschichte ist datenarchitektonisch bisher nicht abgebildet. Beiträge in diese Richtung brauchen Kenntnis des Aufenthalts- und Asylrechts plus Mehrsprachigkeit über die häufigsten Sprachen der Einwanderergruppen hinweg. Vivodepot ist offen für solche Kooperationen.

### Begleitete Souveränität

Datensouveränität aus eigener Hand setzt voraus, dass die Person diese Hand auch hat. Wer auf Stellvertretung angewiesen ist, in Gewaltkontexten lebt, keinen sicheren Aufbewahrungsort hat oder digitale Kompetenzgefälle überbrücken muss — für diese Lebenslagen braucht es Begleitstrukturen. Vivodepot ist offen für die Zusammenarbeit mit Sozialverbänden, Beratungsstellen, Betreuungs- und Vormundschaftseinrichtungen.

### Standardisierungs-Beiträge

Vivodepot positioniert sich als Standardschicht, nicht als Anwendung. Beiträge in Standardisierungs-Gremien (HL7, IHE, ZenDiS-Konsultation, FIM, EUDI, EHDS) sind willkommen. Wer in solchen Gremien aktiv ist und Vivodepot dort sichtbar machen will, ist eingeladen, direkten Kontakt aufzunehmen.

---

## Projektstruktur

| Datei | Inhalt |
|---|---|
| `VIVODEPOT.html` | Hauptanwendung — Single-File |
| `vivodepot-lesen.html` | Leseansicht für QR-Codes und Weitergabe-Dateien |
| `test_vivodepot.py` | Test-Suite |
| `README.md` / `README.en.md` | Architektur-Beschreibung plus Stand beta.16 |
| `LICENSE` | Lizenz-Volltext (BUSL-1.1 → EUPL-1.2) |
| `LICENSING.md` | Lizenzpolitik in einfacher Sprache |
| `TRADEMARK.md` | Markenrichtlinie zur Wortmarke „Vivodepot" |
| `SECURITY.md` | Sicherheitsrichtlinie und Meldewege |
| `SOVEREIGNTY.md` | Selbstbewertung nach Souveränitätsrahmenwerken |
| `DOCS.md` | Technische Dokumentation |
| `INTEROPERABILITY.md` | Austauschformate, Standards, Konformitätsnachweise |
| `FAQ.md` | Häufige Fragen |
| `QUICKSTART.md` | Schnellstart-Anleitung |
| `CHANGELOG.md` | Versionshistorie |
| `publiccode.yml` | Metadaten für openCode/ZenDiS-Registrierung |

---

## KI-Transparenz

Vivodepot wird mit Unterstützung von KI-Werkzeugen (Claude, Anthropic) entwickelt. Der Code wird vor Aufnahme in die veröffentlichte Version von der Verantwortlichen geprüft, getestet und freigegeben. Wenn Sie KI-Werkzeuge für Ihre Beiträge verwenden, kennzeichnen Sie dies bitte im Pull Request — entsprechend EU AI Act Art. 50.

---

## Lizenz

Mit Ihrem Beitrag stimmen Sie zu, dass Ihre Änderungen unter den im Repository hinterlegten Lizenzbedingungen veröffentlicht werden — siehe [LICENSE](LICENSE) und [LICENSING.md](LICENSING.md). Für die jeweils aktuelle Version bedeutet das: BUSL-1.1, mit automatischer Konversion zu EUPL-1.2 nach vier Jahren.

Beiträge zur Vivodepot-Codebasis dürfen Sie in Ihrem Lebenslauf, auf Ihrer Website und in beruflichen Profilen nennen — siehe Markenrichtlinie [TRADEMARK.md](TRADEMARK.md) §3.

---

## Kontakt

- Allgemein: [kontakt@vivodepot.de](mailto:kontakt@vivodepot.de)
- Sicherheitslücken: [security@vivodepot.de](mailto:security@vivodepot.de) (siehe [SECURITY.md](SECURITY.md))
- Lizenzfragen: [lizenz@vivodepot.de](mailto:lizenz@vivodepot.de)
- Markenfragen: [marken@vivodepot.de](mailto:marken@vivodepot.de)
- Web: [vivodepot.de](https://vivodepot.de)
