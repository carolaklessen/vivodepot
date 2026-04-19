# VIVODEPOT — Häufige Fragen

*Version 1.0.0-beta.17 · April 2026*

---

## Allgemein

**Was ist VIVODEPOT?**
Eine Einzeldatei-HTML-App zur Vorsorgedokumentation — Kontakte, Finanzen, Gesundheit, Vollmachten, Bestattungswünsche und mehr. Vollständig offline. Keine Cloud, kein Abo, keine Registrierung.

**Kostet VIVODEPOT etwas?**
Die Basisversion ist kostenlos. Zukünftige Premium-Funktionen sind in Planung.

**Wer steckt dahinter?**
Vivodepot UG (haftungsbeschränkt), Berlin. Kontakt: [feedback@vivodepot.de](mailto:feedback@vivodepot.de)

---

## Daten & Datenschutz

**Wo werden meine Daten gespeichert?**
Ausschließlich in Ihrem Browser (`localStorage`) und in der gespeicherten HTML-Datei. Kein Server, keine Cloud, keine Übertragung.

**Kann VIVODEPOT meine Daten sehen?**
Nein. Die Daten verlassen Ihr Gerät nicht. Auch wir als Entwickler haben keinen Zugriff.

**Sind meine Daten verschlüsselt?**
Ja — wenn Sie Passwortschutz einrichten. AES-256-GCM mit 200.000 PBKDF2-Iterationen.

**Was passiert, wenn ich meinen Browser-Cache leere?**
Die `localStorage`-Daten gehen verloren. Empfehlung: Regelmäßig über „Speichern" eine HTML-Datei erstellen und sichern.

**Kann ich die Daten exportieren?**
Ja — als HTML-Datei (Speichern), als Weitergabe-Datei für Dritte, als QR-Code, als PDF, Word oder FHIR R4 JSON.

**Kann ich die Daten importieren?**
Ja — FHIR R4, FIM-JSON, EUDI-Wallet (SD-JWT) und allgemeines JSON.

---

## Wohlbefinden & Seele (PROM)

**Was sind die Fragebögen im Schritt „Wohlbefinden & Seele"?**
Vier validierte Selbstauskunft-Instrumente: PHQ-4 (Kurzscreening, 4 Fragen), PHQ-9 (Stimmung, 9 Fragen), GAD-7 (Angst, 7 Fragen) und WHO-5 (Wohlbefinden, 5 Fragen). Alle sind Public Domain — keine Genehmigung erforderlich.

**Was passiert nach dem PHQ-4?**
Wenn Ihr PHQ-4-Ergebnis einen Hinweis auf Depressivität oder Angst zeigt, erscheint automatisch ein Hinweis mit einer Schaltfläche. Ein Klick bringt Sie direkt zum empfohlenen ausführlicheren Fragebogen (PHQ-9 oder GAD-7).

**Ersetzen die Fragebögen eine ärztliche Diagnose?**
Nein. Die Ergebnisse sind Orientierungswerte für das Gespräch mit Ihrer Ärztin oder Ihrem Arzt — keine Diagnose.

**Was passiert mit meinen Antworten?**
Sie bleiben ausschließlich auf Ihrem Gerät. Kein Server, keine Übertragung. Sie können die Ergebnisse im FHIR-Export für Arztgespräche nutzen.

**Werden meine PROM-Antworten im FHIR-Export enthalten?**
Ja — wenn Sie einen Fragebogen vollständig ausgefüllt haben. Der FHIR-Export enthält die Einzelantworten (QuestionnaireResponse) und den Gesamtscore (Observation) mit internationalen LOINC-Codes.

---

## FHIR & EHDS

**Was ist FHIR?**
FHIR (Fast Healthcare Interoperability Resources) ist der internationale Standard für den Austausch von Gesundheitsdaten. VIVODEPOT exportiert Ihre Daten in FHIR R4 — das Format, das Arztpraxen, Kliniken und Behörden zunehmend verstehen.

**Was ist EHDS?**
Der European Health Data Space (Verordnung EU 2025/327, in Kraft seit März 2025) regelt den Austausch von Gesundheitsdaten in der EU. VIVODEPOT implementiert die bürgerseitige Dateneingabe — den Teil, den der EHDS selbst nicht spezifiziert.

**Was bedeutet PGHD?**
Patient-Generated Health Data — Gesundheitsdaten, die Bürgerinnen und Bürger selbst erfassen. Das ist eine explizite Kategorie im EHDS. Alle PROM-Scores in VIVODEPOT sind als PGHD gekennzeichnet.

**Was sind die JSON-Vorlagen im Ordner `templates/`?**
Maschinenlesbare Definitionen der Fragebögen nach Schema 1.0 — für Institutionen, Entwickler und Forschungsprojekte, die VIVODEPOT-Daten weiterverarbeiten möchten. Jede Vorlage enthält LOINC-Codes, Scoring-Bereiche und Safety-Regeln.

---

## Technisches

**Welche Browser werden unterstützt?**
Chrome, Firefox, Edge (ab Version 90), Safari (ab Version 14). DuckDuckGo Browser auf iOS unterstützt keine lokalen HTML-Dateien.

**Funktioniert VIVODEPOT ohne Internet?**
Vollständig. Alle Bibliotheken sind direkt eingebettet — keine externe Anfrage.

**Wie groß ist die Datei?**
Ca. 1,7 MB (VIVODEPOT.html). Die Leseansicht (vivodepot-lesen.html) ist deutlich kleiner.

**Kann ich VIVODEPOT auf einem USB-Stick nutzen?**
Ja — HTML-Datei kopieren und in Chrome oder Firefox öffnen.

**Kann ich die Datei auf einem anderen Gerät öffnen?**
Ja — vollständig seit beta.7. Der Salt ist in der Datei eingebettet. Passwort eingeben genügt.

**iPhone: Die Datei öffnet sich in PocketBook.**
Datei in der Dateien-App lang drücken → Teilen → Safari wählen.

---

## Weitergabe & QR-Übergabe

**Was ist die Weitergabe-Datei?**
Eine eigenständige, verschlüsselte HTML-Datei mit gefiltertem Datensatz — z.B. nur medizinische Daten für den Hausarzt. Separates Passwort, per E-Mail oder USB weitergeben.

**Was ist die QR-Übergabe?**
Ein QR-Code, der auf die Leseansicht verlinkt und einen verschlüsselten Datensatz enthält. Empfänger scannt mit Smartphone → Browser öffnet Leseansicht → PIN eingeben → Daten sehen. Kein USB, keine App.

**Was ist die Leseansicht?**
Die Seite `carolaklessen.github.io/vivodepot/vivodepot-lesen.html` — öffnet QR-Codes und Weitergabe-Dateien. Kein Account, kein Speichern, kein Netzwerkzugriff.

---

## Lizenz & Quellen

**Unter welcher Lizenz steht VIVODEPOT?**
EUPL-1.2 — Europäische Union Public Licence. Open Source, Copyleft, bevorzugte EU-Lizenz für öffentliche Förderung.

**Unter welcher Lizenz stehen die Fragebögen?**
PHQ-9, GAD-7, PHQ-4: Public Domain (Kroenke, Spitzer & Williams). WHO-5: WHO Regionalbüro Europa, frei nutzbar. Keine Genehmigung für nicht-kommerzielle Nutzung erforderlich.
