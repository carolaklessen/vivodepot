# ❓ Vivodepot — Häufige Fragen (FAQ)

---

## Datenschutz & Sicherheit

### Werden meine Daten ins Internet gesendet?

**Nein.** Vivodepot hat keinen Server. Keine Daten verlassen Ihr Gerät — nicht beim Ausfüllen, nicht beim Speichern, nicht beim Erstellen von PDFs. Alles passiert lokal in Ihrem Browser.

### Wie sicher ist die Verschlüsselung?

Vivodepot verwendet **AES-256-GCM** — denselben Standard, den Banken, Behörden und das Militär einsetzen. Der Schlüssel wird aus Ihrem Passwort mit 100.000 Iterationen abgeleitet (PBKDF2). Ohne Ihr Passwort kann niemand die Daten lesen.

### Kann jemand meine Daten hacken?

Nur wenn jemand physischen Zugang zu Ihrem Gerät oder USB-Stick hat **und** Ihr Passwort kennt. Da keine Daten online gespeichert werden, gibt es keinen Server, den man angreifen könnte.

### Kann Vivodepot meine Daten lesen?

**Nein.** Es gibt kein „Vivodepot" als Unternehmen mit Zugang zu Ihren Daten. Der Code läuft lokal auf Ihrem Gerät. Selbst wenn wir wollten — wir haben keinen Zugriff.

### Was sieht jemand, der meinen Stick findet?

Ohne Passwort: Nur den Anmeldebildschirm und die **Notfall-Informationen** (Blutgruppe, Allergien, Medikamente, Notfallkontakt). Das ist Absicht — im medizinischen Notfall müssen diese Daten sofort zugänglich sein.

Alles andere (Finanzen, Testament, Verträge, Passwörter) ist verschlüsselt.

---

## Passwort

### Was passiert, wenn ich mein Passwort vergesse?

**Die Daten sind dann verloren.** Es gibt kein „Passwort zurücksetzen", weil es keinen Server gibt, der das tun könnte. Deshalb: Schreiben Sie Ihr Passwort auf Papier und legen Sie es in einen versiegelten Umschlag im Tresor.

### Kann ich das Passwort ändern?

**Ja.** Im Schritt **„Einstellungen"** (Nr. 18) können Sie Ihr Passwort jederzeit ändern oder entfernen. Die Daten werden dann mit dem neuen Passwort neu verschlüsselt.

### Muss ich ein Passwort setzen?

Nein. Ohne Passwort werden die Daten unverschlüsselt gespeichert. Das ist weniger sicher, aber einfacher. Für den USB-Stick empfehlen wir ein Passwort.

---

## Speichern & Backup

### Wo werden meine Daten gespeichert?

Im **localStorage** Ihres Browsers — das ist ein lokaler Speicher auf Ihrem Gerät. Wenn Sie die Datei auf einem USB-Stick öffnen und über „💾 Speichern" herunterladen, werden die Daten in die HTML-Datei eingebettet.

### Warum muss ich auf „💾 Speichern" klicken?

Die App speichert automatisch im Browser. Aber wenn Sie den Browser-Cache löschen oder einen anderen Browser verwenden, sind die Daten weg. Mit „💾 Speichern" laden Sie eine neue HTML-Datei herunter, die Ihre Daten enthält — das ist Ihr echtes Backup.

### Kann ich meine Daten in der Cloud sichern?

Ja. Ihre Vivodepot-Datei ist AES-256 verschlüsselt. Sie können sie sicher in iCloud, Google Drive oder OneDrive ablegen. Ohne Ihr Passwort kann niemand die Datei lesen — auch nicht Apple oder Google.

### Ich habe die Datei versehentlich gelöscht. Kann ich sie wiederherstellen?

Wenn die Daten noch im Browser-Speicher sind: Öffnen Sie eine frische Kopie von VIVODEPOT.html — die Daten werden automatisch geladen. Wenn der Browser-Speicher gelöscht wurde und kein Backup existiert: leider nein.

### Kann ich Vivodepot auf mehreren Geräten nutzen?

Die Daten sind an den Browser und das Gerät gebunden. Um auf einem anderen Gerät weiterzuarbeiten, speichern Sie die Datei (💾) und öffnen Sie sie auf dem neuen Gerät.

---

## Bedienung

### Muss ich alles auf einmal ausfüllen?

Nein. Sie können jederzeit aufhören und später weitermachen. Die App zeigt Ihnen mit dem Fortschrittsbalken, wie weit Sie sind. Jeder Abschnitt hat eine Zeitschätzung (z.B. „⏱ ca. 3 Min.").

### Muss ich alle Felder ausfüllen?

Nein. Nur die Felder mit * (Vorname, Nachname) sind Pflicht — für das Deckblatt. Alles andere ist freiwillig. Füllen Sie nur aus, was Ihnen wichtig ist.

### Kann ich Abschnitte überspringen?

Ja. Klicken Sie in der Seitenleiste auf jeden Abschnitt, den Sie bearbeiten möchten. Die Reihenfolge ist egal.

### Wofür sind die ❓-Icons neben den Feldern?

Das sind Hilfe-Hinweise. Tippen Sie darauf, um zu erfahren, warum das Feld wichtig ist und was Sie eintragen sollten.

### Kann ich Kontakte aus meinem Handy importieren?

Ja. Im Schritt „Vertrauenspersonen" gibt es einen **vCard-Import** — exportieren Sie Kontakte aus Ihrem Handy als .vcf-Datei und laden Sie sie hoch. Auch **CSV-Import** ist möglich.

---

## Dokumente & Exporte

### Sind die erstellten Dokumente rechtsgültig?

Die Vorsorgevollmacht und Patientenverfügung sind **Entwürfe** nach aktuellem deutschem Recht (BGB). Sie müssen handschriftlich unterschrieben werden. Eine notarielle Beurkundung ist empfehlenswert, aber nicht zwingend.

**Wichtig:** Vivodepot bietet keine Rechtsberatung. Bei komplexen Familienverhältnissen oder großen Vermögen empfehlen wir einen Notar oder Anwalt.

### Warum sieht mein PDF anders aus als erwartet?

PDFs werden mit jsPDF generiert — das Ergebnis kann je nach Browser leicht variieren. Falls das Logo nicht erscheint: Stellen Sie sicher, dass JavaScript aktiviert ist.

### Kann ich die Word-Dokumente bearbeiten?

Ja. Die DOCX-Dateien können in Microsoft Word, LibreOffice oder Google Docs geöffnet und bearbeitet werden.

### Was ist der Arztbesuch-Bogen?

Ein 1-2 seitiges PDF mit allen Daten, die bei jedem Arztbesuch abgefragt werden: Stammdaten, Krankenversicherung, Allergien, Medikamente, Vorerkrankungen, Familienanamnese. Einmal ausdrucken und zum Arzt mitbringen — statt jedes Mal per Hand ausfüllen.

### Was ist die Notfall-Tasche?

Eine Checkliste für den Ernstfall (Hochwasser, Brand, Evakuierung): Welche Dokumente sofort einpacken, was auf den USB-Stick speichern, wichtige Kontakte und Notrufnummern. Basiert auf Empfehlungen des Bundesamts für Bevölkerungsschutz (BBK).

---

## Technik

### Welche Browser werden unterstützt?

Chrome 90+, Firefox 90+, Safari 15+, Edge 90+. Empfohlen: Chrome oder Firefox für alle Funktionen (insbesondere Spracheingabe).

### Funktioniert die App auf dem iPhone?

Ja, mit Einschränkungen:
- **Safari** funktioniert vollständig
- **Verschlüsselung** funktioniert über HTTPS (GitHub Pages), aber nicht bei `file://`-Zugriff (z.B. direkt vom Stick)
- **Spracheingabe** ist nur in Chrome/Edge verfügbar, nicht in Safari

### Warum ist die Datei so groß (ca. 450 KB)?

Die Datei enthält alles: HTML, CSS, JavaScript, Logo und drei eingebettete Bibliotheken (jsPDF, docx, QRCode). Keine externen Abhängigkeiten. Das ist Absicht — so funktioniert alles offline.

### Kann ich den Quellcode einsehen?

Ja. Vivodepot ist Open Source unter der EUPL-1.2 Lizenz. Der Quellcode ist auf [GitHub](https://github.com/carolaklessen/vivodepot) verfügbar.

### Wird KI verwendet?

Vivodepot wurde mit KI-Unterstützung entwickelt (EU AI Act Art. 50 konform). Die App selbst enthält optional eine Claude-API-Anbindung für Dokumenten-Review — diese ist deaktiviert und erfordert einen eigenen API-Schlüssel.

---

## Zielgruppe & Anwendungsfälle

### Für wen ist Vivodepot gedacht?

Für alle, die ihre persönlichen Daten und Vorsorge-Dokumente an einem Ort sammeln möchten — insbesondere:
- Menschen ab 50, die Ordnung schaffen wollen
- Angehörige, die für pflegebedürftige Eltern vorsorgen
- Familien mit minderjährigen Kindern (Sorgerecht!)
- Alleinstehende ohne nahe Verwandte
- Vielreisende (ELEFAND-Registrierung)

### Ersetzt Vivodepot einen Notar?

Nein. Vivodepot hilft beim Sammeln und Organisieren — aber bei Testament, Vorsorgevollmacht und Patientenverfügung empfehlen wir immer eine rechtliche Beratung, insbesondere bei:
- Patchwork-Familien
- Immobilienbesitz
- Unternehmensbeteiligungen
- Internationalen Bezügen (mehrere Staatsangehörigkeiten)

### Ersetzt Vivodepot die elektronische Patientenakte (ePA)?

Nein. Die ePA enthält medizinische Befunde und Behandlungsdaten. Vivodepot enthält keine Befunde selbst — nur Ablageorte und Übersichten. Vivodepot ergänzt die ePA um alles, was dort nicht steht: Finanzen, Testament, persönliche Wünsche, Kontakte.

---

## Probleme & Fehlerbehebung

### Die App zeigt nach dem Öffnen nur eine leere Seite

JavaScript ist vermutlich deaktiviert. Aktivieren Sie JavaScript in den Browser-Einstellungen.

### Meine Daten sind verschwunden

Mögliche Ursachen:
- Browser-Cache wurde gelöscht → Lösung: Regelmäßig „💾 Speichern" nutzen
- Anderer Browser geöffnet → Daten sind browser-gebunden
- Privates/Inkognito-Fenster → dort wird localStorage beim Schließen gelöscht

### Die Spracheingabe funktioniert nicht

Spracheingabe (🎤) benötigt Chrome oder Edge. Safari und Firefox unterstützen die Web Speech API nicht. Außerdem muss die Mikrofonfreigabe erteilt werden.

### PDFs werden nicht heruntergeladen

Prüfen Sie, ob Ihr Browser Downloads erlaubt. Einige Browser (insbesondere mobile) blockieren automatische Downloads. Versuchen Sie es mit einem Desktop-Browser.

---

*Version 1.0.0-beta · © 2026 Vivodepot · [Schnellstart →](QUICKSTART.md) · [Dokumentation →](DOCS.md)*
