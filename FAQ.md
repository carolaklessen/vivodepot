# VIVODEPOT — Häufige Fragen

*Version 1.0.0-beta.16 · April 2026*

---

## Allgemein

**Was ist VIVODEPOT?**
Eine Einzeldatei-HTML-App zur Vorsorgedokumentation — Kontakte, Finanzen, Gesundheit, Vollmachten, Bestattungswünsche und mehr. Vollständig offline. Keine Cloud, kein Abo, keine Registrierung.

**Kostet VIVODEPOT etwas?**
Die Basisversion ist kostenlos. Zukünftige Premium-Funktionen sind in Planung.

**Wer steckt dahinter?**
Vivodepot UG (haftungsbeschränkt), Berlin. Kontakt: [hilfe@vivodepot.de](mailto:hilfe@vivodepot.de)

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
Ja — als HTML-Datei (Speichern), als Weitergabe-Datei für Dritte, als QR-Code, als PDF oder Word.

**Kann ich die Daten importieren?**
Ja — FHIR R4, FIM-JSON, EUDI-Wallet (SD-JWT) und allgemeines JSON.

---

## Technisches

**Welche Browser werden unterstützt?**
Chrome, Firefox, Edge (ab Version 90), Safari (ab Version 14). DuckDuckGo Browser auf iOS unterstützt keine lokalen HTML-Dateien.

**Funktioniert VIVODEPOT ohne Internet?**
Vollständig. Alle Bibliotheken sind direkt eingebettet — keine externe Anfrage.

**Wie groß ist die Datei?**
Ca. 1,3 MB (VIVODEPOT.html). Die Leseansicht (vivodepot-lesen.html) ist deutlich kleiner.

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

**Was wenn der QR-Code zu groß ist?**
VIVODEPOT teilt den Payload automatisch auf bis zu 6 QR-Codes auf. Die Leseansicht sammelt alle Teile und fragt einmal den PIN.

**Braucht der Empfänger auch VIVODEPOT?**
Nein — die Leseansicht ist frei verfügbar und braucht keine Installation.

**Ist der QR-Code sicher?**
Ja. AES-256-GCM-verschlüsselt, PIN-geschützt, 24 Stunden gültig. Der Hash-Teil der URL erreicht den Server nie.

---

## Für Institutionen

**Was ist der Institutionen-Bereich?**
Institutionen (Pflegeheime, Kliniken, Behörden) können Fragebogen-Vorlagen im Companion-Schema v1.0 erstellen und bereitstellen. Nutzer füllen den Fragebogen in der App aus. Das Ergebnis kann als FHIR-konformes JSON weitergegeben werden — mit automatisch erstelltem DSGVO-Einwilligungsnachweis.

**Wie erstellt eine Institution eine Vorlage?**
Direkt in der App: Schritt „Für Institutionen" → „Neue Vorlage erstellen". Titel, Herausgeber, Fragen und Antwort-Skala per Formular eingeben, Vorschau anzeigen, als Datei speichern oder direkt in der App speichern. Kein Texteditor, kein JSON-Wissen erforderlich.

**Kann die Vorlage auch manuell bearbeitet werden?**
Ja — die exportierte .json-Datei kann in einem Texteditor nachbearbeitet und anschließend wieder eingelesen werden.

---

## Erinnerungen & Benachrichtigungen

**Kann VIVODEPOT mich erinnern, Dokumente zu erneuern?**
Ja. In Einstellungen → „Prüftermin-Erinnerungen" können Browser-Benachrichtigungen aktiviert werden. Wenn etwas fällig ist, erscheint einmal täglich eine Meldung. Auf iPhone und iPad werden stattdessen Hinweise beim App-Start angezeigt.

**Werden Erinnerungen automatisch eingeschaltet?**
Nein. Die Browser-Berechtigung wird nur eingeholt, wenn Sie in den Einstellungen auf „Erinnerungen aktivieren" klicken.

---

## Notfall & Katastrophenschutz

**Was zeigt die Notfall-Kategorie?**
Sechs Statuskarten (Wasser, Lebensmittel, Medikamente, Dokumente, Licht & Kommunikation, Bargeld), Evakuierungsplan, lokale Kontakte, Notrufnummern. Nach BBK-Empfehlungen.

**Was enthält das Notfall-Blatt?**
Notrufnummern, Vorratsstatus, Evakuierungsplan, Sammelplatz, medizinische Hinweise. Zum Ausdrucken.

---

## Hilfe & Kontakt

**Wie kann ich Hilfe bekommen?**
Drei-Punkte-Menü → „Hilfe" oder Einstellungen → „Hilfe & Kontakt". Wenn Ihre E-Mail-App nicht öffnet, steht ein Formular bereit, das den Text in Ihre Zwischenablage kopiert.

[hilfe@vivodepot.de](mailto:hilfe@vivodepot.de) · [github.com/carolaklessen/vivodepot](https://github.com/carolaklessen/vivodepot)
