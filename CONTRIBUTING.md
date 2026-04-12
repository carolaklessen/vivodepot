# VIVODEPOT — Mitmachen

*Version 1.0.0-beta.7 · April 2026*

Vielen Dank für Ihr Interesse an VIVODEPOT. Jede Rückmeldung hilft.

---

## Wie Sie beitragen können

### Fehler melden

1. Prüfen Sie, ob der Fehler in der aktuellen Version (1.0.0-beta.7) noch vorhanden ist
2. Öffnen Sie ein [GitHub Issue](https://github.com/carolaklessen/vivodepot/issues)
3. Beschreiben Sie: Was haben Sie getan? Was ist passiert? Was hätten Sie erwartet?
4. Nennen Sie Browser, Betriebssystem und Gerätetyp

### Verbesserungen vorschlagen

- GitHub Issues mit dem Label `enhancement`
- E-Mail an [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

### Code-Beiträge

Da VIVODEPOT eine Einzeldatei-HTML-App ist, sind Code-Beiträge direkt möglich:

1. Fork erstellen
2. Änderungen in `VIVODEPOT.html` vornehmen
3. Tests ausführen: `python3 test_vivodepot.py VIVODEPOT.html`
4. Pull Request erstellen

**Bitte beachten:**
- Keine externen Abhängigkeiten einführen (alles muss inline bleiben)
- Barrierefreiheit nicht verschlechtern (Touch-Targets 44px, ARIA-Labels)
- Bestehende Tests müssen weiterhin bestehen (842/842)
- Neue Funktionen sollten von Tests abgedeckt werden
- Korrekte Orthographie und Kommasetzung in allen Texten, Labels und Fehlermeldungen

---

## Testlauf

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

Ergebnis muss `0 FAIL` sein, bevor eine Änderung als Baseline akzeptiert wird.

---

## KI-Entwicklung

VIVODEPOT wird mit KI-Unterstützung (Claude, Anthropic) entwickelt. Das ist in der App, im Code und in allen Dokumenten transparent ausgewiesen (EU AI Act Art. 50).

---

## Lizenz

Durch Ihren Beitrag stimmen Sie zu, dass Ihre Änderungen unter der [EUPL-1.2](LICENSE) veröffentlicht werden.

---

## Kontakt

[feedback@vivodepot.de](mailto:feedback@vivodepot.de) · [vivodepot.de](https://vivodepot.de)
