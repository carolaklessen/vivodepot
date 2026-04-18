# VIVODEPOT — Mitmachen

*Version 1.0.0-beta.10 · April 2026*

Vielen Dank für Ihr Interesse an VIVODEPOT. Jede Rückmeldung hilft.

---

## Wie Sie beitragen können

### Fehler melden

1. Prüfen Sie, ob der Fehler in der aktuellen Version (1.0.0-beta.10) noch vorhanden ist
2. Öffnen Sie ein [GitHub Issue](https://github.com/carolaklessen/vivodepot/issues)
3. Beschreiben Sie: Was haben Sie getan? Was ist passiert? Was hätten Sie erwartet?
4. Nennen Sie Browser, Betriebssystem und Gerätetyp

### Verbesserungen vorschlagen

- GitHub Issues mit dem Label `enhancement`
- E-Mail an [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

### Code-Beiträge

Da VIVODEPOT aus zwei selbsttragenden HTML-Dateien besteht, sind Code-Beiträge direkt möglich:

1. Fork erstellen
2. Änderungen in `VIVODEPOT.html` und/oder `vivodepot-lesen.html` vornehmen
3. Tests ausführen: `python3 test_vivodepot.py VIVODEPOT.html`
4. Pull Request erstellen

**Bitte beachten:**
- Keine externen Abhängigkeiten einführen (alles muss inline bleiben)
- Barrierefreiheit nicht verschlechtern (Touch-Targets 44px, ARIA-Labels)
- Bestehende Tests müssen weiterhin bestehen (1050/1051)
- Neue Funktionen sollten durch Tests abgedeckt werden
- Korrekte Orthographie und Kommasetzung in allen Texten, Labels und Fehlermeldungen

---

## Testlauf

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

Ergebnis muss `0 FAIL` sein (beim Lauf aus dem Repo-Root), bevor eine Änderung als Baseline akzeptiert wird.

---

## Projektstruktur

| Datei | Inhalt |
|---|---|
| `VIVODEPOT.html` | Hauptanwendung — Einzeldatei, ca. 1,3 MB |
| `vivodepot-lesen.html` | Eigenständige Leseansicht für QR-Codes und Weitergabe-Dateien |
| `test_vivodepot.py` | Automatisierte Tests (Python, 1051 Checks in 65 Sektionen) |
| `CHANGELOG.md` | Versionshistorie |
| `DOCS.md` | Technische Dokumentation |
| `FAQ.md` | Häufige Fragen |
| `QUICKSTART.md` | Schnellstart-Anleitung |
| `SECURITY.md` | Sicherheitsrichtlinie |
| `SOVEREIGNTY.md` | ZenDiS-Souveränitätsprüfung |

---

## KI-Entwicklung

VIVODEPOT wird mit KI-Unterstützung (Claude, Anthropic) entwickelt. Das ist in der App, im Code und in allen Dokumenten transparent ausgewiesen (EU AI Act Art. 50).

---

## Lizenz

Durch Ihren Beitrag stimmen Sie zu, dass Ihre Änderungen unter der [EUPL-1.2](LICENSE) veröffentlicht werden.

---

## Kontakt

[feedback@vivodepot.de](mailto:feedback@vivodepot.de) · [vivodepot.de](https://vivodepot.de)
