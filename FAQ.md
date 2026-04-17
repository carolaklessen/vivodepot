# VIVODEPOT — Häufige Fragen

*Version 1.0.0-beta.10 · April 2026*

---

## Allgemein

**Was ist VIVODEPOT?**
Eine Einzeldatei-HTML-App, mit der Sie alle wichtigen Informationen für den Notfall dokumentieren: Kontakte, Finanzen, Gesundheit, Vollmachten, Bestattungswünsche und mehr. Die App läuft vollständig offline — keine Cloud, kein Abo, keine Registrierung.

**Kostet VIVODEPOT etwas?**
Die Basisversion ist kostenlos und enthält alle wesentlichen Funktionen. Zukünftige Premium-Funktionen sind in Planung.

**Wer steckt dahinter?**
Vivodepot UG (haftungsbeschränkt), Berlin. Kontakt: [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

---

## Daten & Datenschutz

**Wo werden meine Daten gespeichert?**
Ausschließlich in Ihrem Browser (`localStorage`) und in der gespeicherten HTML-Datei. Kein Server, keine Cloud, keine Übertragung.

**Kann VIVODEPOT meine Daten sehen?**
Nein. Die Daten verlassen Ihr Gerät nicht. Auch wir als Entwickler haben keinen Zugriff.

**Sind meine Daten verschlüsselt?**
Ja — wenn Sie einen Passwortschutz einrichten. Die Verschlüsselung erfolgt mit AES-256-GCM, einem der sichersten verfügbaren Standards.

**Was passiert, wenn ich meinen Browser-Cache leere?**
Die Daten in `localStorage` gehen verloren. Empfehlung: Regelmäßig über „Speichern" eine persönliche HTML-Datei erstellen und sichern.

**Kann ich die Daten exportieren?**
Ja — als passwortgeschützte HTML-Datei (über „Speichern"), als JSON-Datei (über das Menü) oder als fertige Dokumente (PDF, Word).

**Kann ich die Daten importieren?**
Ja — über das Menü → „Daten importieren". Unterstützt werden HTML-Dateien (eigene gespeicherte VIVODEPOT-Dateien) und JSON-Dateien.

---

## Technisches

**Welche Browser werden unterstützt?**
Chrome, Firefox, Edge (ab Version 90), Safari (ab Version 14). DuckDuckGo Browser auf iOS unterstützt keine lokalen HTML-Dateien.

**Funktioniert VIVODEPOT ohne Internet?**
Vollständig. Alle Bibliotheken (PDF, Word, QR-Code) sind direkt in der HTML-Datei eingebettet — keine einzige externe Anfrage.

**Wie groß ist die Datei?**
Ca. 1,3 MB. Das entspricht etwa dem Speicherplatz einer Foto-Vorschau.

**Kann ich VIVODEPOT auf einem USB-Stick nutzen?**
Ja — einfach die HTML-Datei auf den USB-Stick kopieren und in Chrome oder Firefox öffnen.

**Kann ich die Datei auf einem anderen Gerät öffnen?**
Ja — seit Version 1.0.0-beta.7 vollständig. Der kryptographische Schlüssel wird jetzt in der Datei selbst gespeichert. Passwort eingeben genügt — egal auf welchem Gerät oder Browser.

In früheren Versionen (bis beta.6) war dies ein bekanntes Problem: Der Salt fehlte auf anderen Geräten, was zur Fehlermeldung führte, obwohl das Passwort korrekt war.

**iPhone: Die Datei öffnet sich in PocketBook statt im Browser.**
PocketBook hat sich als Standard-App für HTML-Dateien registriert. Lösung: Datei in der Dateien-App lang drücken → Teilen → Safari wählen.

**Die PDF-Erstellung schlägt fehl.**
Die PDF-Bibliothek ist vollständig eingebettet und benötigt kein Internet. Falls ein Fehler auftritt, bitte Seite neu laden und erneut versuchen. Bei anhaltenden Problemen: [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

---

## Inhalt & Exporte

**Welche Dokumente kann ich erstellen?**
PDF (Notfallmappe), Word (bearbeitbar), Notfall-Blatt (Katastrophenschutz), Arztbogen, Szenario-PDFs (Krankenhaus, Todesfall, Notfall-Tasche), Vorsorgevollmacht (Word), Patientenverfügung (Word), Gesundheitsvollmacht (Word), QR-Aufkleber, vCard-Export.

**Sind die Dokumente rechtsgültig?**
VIVODEPOT erstellt Entwürfe und Vorlagen. Für rechtliche Gültigkeit (besonders Vorsorgevollmacht, Patientenverfügung, Testament) ist in der Regel eine notarielle Beglaubigung oder eigenhändige Unterschrift erforderlich. VIVODEPOT ist keine Rechtsberatung.

**Kann ich mehrere Profile anlegen?**
Ja — über Einstellungen → Profile. Praktisch für Paare oder wenn Sie Informationen für mehrere Personen verwalten.

**Was ist die Angehörigen-Ansicht?**
Eine vereinfachte Ansicht, die beim Öffnen der gespeicherten Datei angeboten wird. Angehörige sehen nur die relevanten Informationen — keine persönlichen Details, die sie nicht brauchen.

---

## Notfall & Katastrophenschutz

**Was zeigt die Notfall-Kategorie?**
Sechs klickbare Statuskarten für Wasser, Lebensmittel, Medikamente, Dokumente, Licht & Kommunikation sowie Bargeld. Außerdem Felder für Evakuierungsplan, lokale Kontakte und Notrufnummern. Orientiert sich an den Empfehlungen des Bundesamts für Bevölkerungsschutz (BBK).

**Was enthält das Notfall-Blatt als PDF?**
Notrufnummern (112, 110, Seelsorge), Vorratsstatus, Evakuierungsplan, Sammelplatz, medizinische Hinweise, Vertrauenspersonen. Ideal zum Ausdrucken und Aufhängen.

---

## Kontakt & Feedback

Fragen, Fehlerberichte, Verbesserungsvorschläge: [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

GitHub: [github.com/carolaklessen/vivodepot](https://github.com/carolaklessen/vivodepot)
