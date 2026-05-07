# Vivodepot

Eine souveräne, offline-fähige Datenschicht zwischen Bürger und Institution.

---

> **Stand:** Online ist Vivodepot **beta.16** mit den Funktionen der App-Schicht — Single-File-HTML, AES-256-GCM-Verschlüsselung, Offline-Fähigkeit, FHIR-R4-Grundgerüst, strukturierte Formulare. **Version 1.0** mit Sorge-Struktur, übergabefähigen Vollmachten und neuer Nutzerführung ist in Entwicklung. Diese Seite beschreibt zuerst die Architektur als Ganzes; den Schnellstart und die heute schon verfügbaren Funktionen finden Sie unten unter [„Vivodepot heute (beta.16)"](#vivodepot-heute-beta16).

---

## Worum es geht

In jedem Leben sammeln sich Daten, die andere über uns halten — Krankenkassen, Ärzt:innen, Versicherer, Behörden, Banken, Schulen, Arbeitgeber. Diese Daten beschreiben uns, beeinflussen Entscheidungen über uns, überdauern uns. Wir haben theoretische Rechte an ihnen — Auskunft, Berichtigung, Portabilität, Löschung — aber praktisch sind diese Rechte schwer durchsetzbar, weil die Daten technisch und organisatorisch nicht in unserer Hand liegen.

Vivodepot ist eine Architektur, die das ändert. Sie macht aus dem Recht eine Funktion: ein einfaches, prüfbares, sicheres Format, in dem ein Mensch seine Daten halten, von Institutionen empfangen, an andere Institutionen weitergeben und für die nächsten Generationen verwahren kann — auch ohne Cloud, ohne Plattform, ohne Vertrauen in Dritte.

Vivodepot ist nicht eine weitere App. Es ist eine Standardschicht für Bürger-Datenhaltung gegenüber Institutionen aller Art.

## Was diese Architektur trägt

Vivodepot löst nicht das Problem einer Person, die abstrakt mit ihren Daten umgehen will. Es löst das Problem von Menschen, die in Beziehungen und Lebensläufen leben — die Daten für sich, für Angehörige, für Schutzbefohlene halten und weitergeben müssen, in einem System, das genau diese Realität strukturell selten vorsieht.

Manche Lücken zeigen sich erst an Lebensschwellen — den schweren wie den guten. An einer Eheschließung, einer Geburt, einem Hauskauf, dem Antritt einer Erbschaft. An einer schwierigen Diagnose, in einer Pflegesituation, an einer Klinikaufnahme zur Unzeit, in einem Vormundschaftsfall, nach einem Todesfall mit Aktenkoffern voller fremder Dokumente. In solchen Momenten wird sichtbar, was sonst unsichtbar bleibt: wo das formale Recht endet und die praktische Möglichkeit beginnt, und wie groß der Spalt dazwischen ist.

Das eigene Leben zu ordnen, eigene Daten zu halten, sie weiterzugeben oder zurückzuholen — das ist nicht nur Vorsorge gegen Unwägbarkeiten. Es ist eine Form, das eigene Leben zu führen.

Vivodepot trägt diese Übergänge im Kern. Der Angehörigen-Modus, die Sorge-Struktur, die übergabefähigen Vollmachten sind keine Zusatzfeatures, sondern Voraussetzung dafür, dass Datensouveränität im Alltag von Familien und Lebensläufen ankommt — nicht nur in einem Konzeptpapier.

## Die zentrale Idee

Eine einzige Datei. Verschlüsselt. Auf einem Datenträger der Wahl. In der Hand der Person, der die Daten gehören.

Diese Datei — wir nennen die Einträge in ihr Vivos — kann Gesundheitsdaten enthalten, Versicherungsunterlagen, Schulzeugnisse, Bankdokumente, Steuerunterlagen, persönliche Aufzeichnungen, Verträge, Vollmachten, alles, was ein Mensch im Verlauf seines Lebens an Daten ansammelt oder zugespielt bekommt. Die Datei ist nach offenen Standards strukturiert (FHIR R4 für medizinische Daten, weitere Standards je nach Domäne), AES-256-GCM verschlüsselt, single-file in einer Form, die ohne Internetzugang funktioniert.

Institutionen können Vivodepot-Dateien lesen und schreiben, wenn die Person ihnen den Schlüssel gibt. Ohne Schlüssel sehen sie nichts. Mit Schlüssel sehen sie nur, was die Person freigibt.

Das ist der einfache technische Kern. Die schwierige Arbeit liegt nicht im Code — sie liegt in den Architekturentscheidungen drumherum, die diesen Kern überhaupt erst zu einer Standardschicht machen.

## Architektur-Prinzipien

Vivodepot folgt sechs Entwurfsprinzipien, die sich gegenseitig bedingen. Sie sind nicht beliebig austauschbar — sie definieren, was Vivodepot ist.

### Souveränität bei der Person

Daten gehören der Person, der sie zuzuordnen sind. Nicht der Institution, die sie erhoben hat, nicht der Plattform, die sie speichert, nicht dem Anbieter, der die Software bereitstellt. Souveränität ist nicht eine Funktion, die man einbauen kann oder weglassen — sie ist die Voraussetzung jeder weiteren Entscheidung.

### Single-File statt verteilte Systeme

Eine Vivodepot-Datei ist ein in sich geschlossenes Objekt — keine Datenbank, kein Server, keine Cloud, keine API als Voraussetzung. Sie kann auf einem USB-Stick liegen, in einem Bankschließfach, auf einem privaten NAS, auf einem verschlüsselten Cloud-Speicher der Wahl. Das macht Vivodepot übertragbar, unabhängig von Anbietern, und überlebbar — auch dann, wenn der Anbieter, der die Software gebaut hat, eines Tages nicht mehr existiert.

### Offline-fähig als Grundzustand

Vivodepot funktioniert ohne Internetverbindung. Synchronisation, Online-Funktionen, Cloud-Backups sind optional und immer entschlüsselbar nur mit dem privaten Schlüssel der Person. Die Datei selbst hat keine externen Abhängigkeiten. Das ist nicht Nostalgie — es ist Resilienz gegen Ausfälle, gegen Übergriffe, gegen geopolitische Veränderungen.

### Standards statt Eigenformate

Vivodepot baut auf FHIR R4, etablierten kryptographischen Verfahren (AES-256-GCM, demnächst auch Post-Quantum-fähige Verfahren), gängigen Datenformaten. Es erfindet nichts neu, was bereits gut steht. Das macht Vivodepot interoperabel mit allem, was institutionell schon existiert, und übergabefähig für die Zukunft.

### Lesbarkeit für die Person

Eine Vivodepot-Datei muss für ihren Inhaber:innen mit zumutbarem Aufwand lesbar sein — nicht nur durch die Vivodepot-Software, sondern strukturell. Eine Person, die in zehn Jahren ihre Daten zurückholen will, soll das auch ohne den Anbieter Vivodepot tun können. Die Spezifikation ist offen, der Code ist quellenoffen.

### Compliance-Konformität als Werkzeug, nicht als Hindernis

Vivodepot ist so gebaut, dass Institutionen ihre regulatorischen Pflichten — DSGVO, EHDS, Patientenrechtegesetz, Datenportabilität — durch Vivodepot leichter erfüllen können, nicht zusätzlich erschwert. Das ist die Brücke, über die institutionelle Adoption realistisch wird.

## Was Vivodepot nicht ist

Vivodepot ist keine Cloud-Lösung. Es ist keine zentrale Plattform. Es ist kein Login-System. Es ist keine Identity-Wallet im Sinne der EUDI Wallet (es kann mit ihr koexistieren, aber sie ersetzt nicht und sie wird nicht ersetzt). Es ist kein Konkurrent zu institutionellen Datenbanken — Institutionen behalten ihre Daten weiterhin. Es ist auch keine Blockchain, keine dezentrale Datenbank, kein neues Krypto-Konstrukt.

Es ist eine zusätzliche Schicht zwischen Person und Institution, in der die Person eine eigene, vollständige Kopie ihrer für sie relevanten Daten hält, sicher und unter ihrer Kontrolle.

## Was Vivodepot für Institutionen leistet

Institutionen, die personenbezogene Daten verarbeiten, stehen unter wachsendem regulatorischem Druck: DSGVO-Auskunfts- und Löschpflichten, EHDS-Datenportabilität, Patientenrechtegesetz, EU-Digital-Identity-Anbindung. Diese Pflichten bei steigenden Datenmengen und schrumpfenden IT-Budgets zu erfüllen, ist operativ schwierig.

Vivodepot reduziert diese Last. Statt für jede Compliance-Anforderung eigene Schnittstellen zu bauen, integrieren Institutionen einmal Vivodepot — und können Daten an die Person übergeben, von der sie kommen, in einem Format, das Bürger:innen mitnehmen, prüfen und weiterverwenden können. Das ist defensiver Compliance-Wert: niedrigere Klage-Risiken, einfachere Auskunftserteilung, sauberere Übergaben in Sektor-Wechseln.

## Warum jetzt

Die regulatorischen und technischen Voraussetzungen für eine solche Schicht sind in Europa erst seit kurzem alle gleichzeitig vorhanden:

- Der European Health Data Space (EHDS) ist seit 2025 in Kraft und verlangt von Mitgliedstaaten, Bürger:innen den Zugriff auf ihre Gesundheitsdaten in maschinenlesbarer Form zu ermöglichen.
- Die EU Digital Identity Wallet wird ab 2026/27 verpflichtend und schafft eine vertrauenswürdige Authentisierungsschicht, mit der Vivodepot zusammenwirken kann.
- Data Governance Act und Data Act haben rechtliche Rahmen geschaffen, in denen Bürger:innen-zentrierte Datenarchitekturen erstmals klar regulatorisch verortet sind.
- Strukturen wie der Sovereign Tech Fund (Förderung kritischer Open-Source-Infrastruktur) und das Zentrum Digitale Souveränität (ZenDiS) mit der Plattform OpenCode haben in Deutschland politische und finanzielle Voraussetzungen für souveräne Tech-Lösungen geschaffen.
- FHIR R4 ist als internationaler Standard für medizinische Daten in Deutschland und der EU mittlerweile breit verankert.
- Speziell in Deutschland verankert das vom Bundestag am 23. April 2026 beschlossene Vergabebeschleunigungsgesetz — vorbehaltlich der Bundesratszustimmung am 8. Mai 2026 und mit voraussichtlichem Inkrafttreten am 1. Juli 2026 — digitale Souveränität ausdrücklich als zulässiges qualitatives Zuschlagskriterium bei öffentlichen IT-Beschaffungen. Genannt sind Merkmale wie die Nutzung interoperabler und offener IT-Systeme, die Nachvollziehbarkeit und Kontrolle von Datenverarbeitungsvorgängen, Datenlokalisierung sowie die rechtliche, organisatorische und technische Immunität gegen unerwünschte Zugriffe — Eigenschaften, die Vivodepot strukturell trägt.

Vor fünf Jahren wäre Vivodepot eine isolierte Vision gewesen. Heute ist es ein anschlussfähiger Baustein in einem politisch gewollten Korridor.

## Wirtschaftlicher Ansatz

Vivodepot ist nicht karitativ — es ist strukturell tragfähig gebaut, weil eine Datenstandardschicht, die nicht weiterentwickelt wird, in einem regulierten Umfeld nicht überlebt.

Die Software ist freie Software. Bürger:innen, Forschungseinrichtungen, gemeinnützige Organisationen und kleine Akteure nutzen Vivodepot ohne Lizenzgebühren. Institutionen, die Vivodepot in ihren produktiven Geschäftsbetrieb einbauen — Krankenkassen, Versicherer, Bundesländer, Krankenhausträger, gewerbliche Anbieter — schließen kommerzielle Lizenzverträge ab, die die Weiterentwicklung finanzieren. Nach einer Übergangsfrist wird jede Version automatisch in eine vollständige Open-Source-Lizenz überführt.

Diese Konstruktion verbindet drei Dinge, die normalerweise nicht zusammenpassen: maximale Freiheit für die Personen, deren Daten gehalten werden; ausreichende kommerzielle Tragfähigkeit, um die Architektur dauerhaft zu pflegen; und ein zeitversetztes Open-Source-Versprechen, das verhindert, dass die Lösung jemals dauerhaft proprietär wird.

Details zur Lizenzpolitik finden sich in [LICENSE](LICENSE) und [LICENSING.md](LICENSING.md) sowie auf [vivodepot.de/lizenzierung](https://vivodepot.de/lizenzierung).

## Verantwortung

Vivodepot wird von Carola Klessen verantwortet. Es entstand aus jahrzehntelanger Erfahrung in unterschiedlichen Sektoren, beruflich wie privat — und aus dem konkreten Verständnis für die Realität, die diese Architektur trägt. Der Beirat ist im Aufbau, mit Persönlichkeiten aus digitaler Souveränität, klinischer Versorgung, Standardisierung und Bürgersicht. Namen werden veröffentlicht, sobald die Berufungen abgeschlossen sind.

## Trägerstruktur

Vivodepot wird in einer Form aufgesetzt, die kommerzielle Tragfähigkeit und langfristige Unabhängigkeit verbindet. Details zur Gesellschafts- und Trägerstruktur werden hier veröffentlicht, sobald die Struktur formal eingerichtet ist.

Die Wortmarke „Vivodepot" ist beim Deutschen Patent- und Markenamt zur Eintragung beantragt, gehalten privat von Carola Klessen. Details zur Markennutzung in [TRADEMARK.md](TRADEMARK.md).

## Mitwirken

Vivodepot ist ein junges, offen geführtes Projekt. Beiträge sind willkommen — Code, Dokumentation, kritische Reviews, Anwendungsszenarien. Hinweise zum Beitragsprozess und zur aktuellen Entwicklungsphase finden sich in [CONTRIBUTING.md](CONTRIBUTING.md).

Besonders gesucht ist die Anpassung von Vivodepot an andere Rechtsräume. Datensouveränität ist europäisch ein gemeinsames Thema, aber die rechtlichen Rahmen, die Vollmachts- und Erbrechtsstrukturen, die etablierten Datenstandards und die alltäglichen Gepflogenheiten unterscheiden sich von Land zu Land. Eine in Deutschland gebaute Version bildet nicht automatisch ab, was in Frankreich, in der Schweiz, in Großbritannien, in den Niederlanden oder in den nordischen Ländern benötigt wird. Vivodepot ist so angelegt, dass national sinnvolle Versionen entstehen können — getragen von Personen, die das jeweilige Recht und die jeweilige Lebenswirklichkeit kennen.

Eine zweite Lücke, die ausdrücklich benannt sein soll: die Lebenswirklichkeit von Menschen mit Migrations-, Flucht- oder Einwanderungsgeschichte. Asyl, Duldung, Einbürgerung, Aufenthaltstitel, Anerkennung von Bildungs- und Berufsabschlüssen aus Herkunftsländern — all das produziert eine eigene, oft besonders zerklüftete Datenwirklichkeit, in der die Asymmetrie zwischen Person und Institution besonders ausgeprägt ist und in der Vertrauen in digitale Systeme zu Recht nicht selbstverständlich ist. Vivodepot bildet diese Wirklichkeit derzeit nicht ab. Eine sinnvolle Antwort darauf braucht Kenntnis des Aufenthalts- und Asylrechts, Mehrsprachigkeit über die häufigsten Sprachen der Einwanderergruppen hinweg und vor allem ein Vertrauen, das sich nur in Zusammenarbeit mit etablierten Akteuren des Feldes herstellen lässt. Vivodepot ist offen für solche Kooperationen.

Eine dritte Lücke betrifft Menschen, für die Datensouveränität aus eigener Hand keine Voraussetzung ist, sondern selbst erst hergestellt werden muss — durch Begleitung, durch Stellvertretung, durch geschützte Räume. Wer keinen sicheren Aufbewahrungsort hat, wer kognitiv oder gesundheitlich auf Stellvertretung angewiesen ist, wer in Gewaltkontexten lebt, wer aus digitalen Kompetenzgefällen heraus nicht selbständig agieren kann — für diese Lebenslagen reicht eine technische Möglichkeit allein nicht. Vivodepot ist offen für die Zusammenarbeit mit Akteuren, die diese Begleitstrukturen bauen — Sozialverbänden, Beratungsstellen, Betreuungs- und Vormundschaftseinrichtungen.

Wer Interesse an strategischer Partnerschaft oder Beirats-Mitwirkung hat, ist eingeladen, direkten Kontakt aufzunehmen. Vivodepot ist offen für Co-Trägerschaft auf Augenhöhe — durch Personen, die das Thema tragen können, weil sie es im eigenen Berufs- oder Lebensweg verstehen.

## Kontakt

- Allgemein: [kontakt@vivodepot.de](mailto:kontakt@vivodepot.de)
- Lizenzfragen: [lizenz@vivodepot.de](mailto:lizenz@vivodepot.de) · [LICENSE](LICENSE) · [LICENSING.md](LICENSING.md)
- Markenfragen: [marken@vivodepot.de](mailto:marken@vivodepot.de) · [TRADEMARK.md](TRADEMARK.md)
- Sicherheitsmeldungen: [security@vivodepot.de](mailto:security@vivodepot.de) · [SECURITY.md](SECURITY.md)
- Web: [vivodepot.de](https://vivodepot.de)
- Code: [github.com/carolaklessen/vivodepot](https://github.com/carolaklessen/vivodepot)

---

## Vivodepot heute (beta.16)

Während v1 in Entwicklung ist, steht beta.16 öffentlich zur Verfügung. Diese Version trägt einen Teil der oben beschriebenen Architektur bereits funktional, anderes folgt mit v1.

### Stand-Tabelle

| Substanz | beta.16 (online) | v1 (in Entwicklung) |
|---|---|---|
| Single-File-HTML, AES-256-GCM, Offline, FHIR-R4-Grundgerüst | ✓ | ✓ |
| Strukturierte Formulare (Stammdaten, Gesundheit, Verträge usw.) | ✓ | erweitert |
| Multi-Profile (vier Profile parallel) | ✓ | abgelöst durch Sorge-Struktur |
| QR-Übergabe, Weitergabe-Datei, Leseansicht | ✓ | ✓ |
| Vorlagen-Editor für Institutionen, FHIR-PROM, FIM-JSON, Solid-Pod-Export | ✓ | ✓ |
| Sorge-Struktur (Anker-Person + Sub-Depots für Schutzbefohlene) | — | ✓ |
| Übergabefähige Vollmachten mit JWS-Signatur und Trust-Authority | — | ✓ |
| Anlass-Wizards (Krankenhaus, Arzt, Pflegegrad, Bankvollmacht, Erbschaft) | — | ✓ |
| Routing-Gate für Identitätsfrage (nur bei eingerichtetem Angehörigen-Zugang) | — | ✓ |
| FHIR-IPS-Export, Beziehungs-Codierung, anbieter-mitgebrachte Templates | teilweise | ✓ |
| CI/CD-Härtung mit Hash-Substitution, Privacy-Erzwingung (DSGVO/CSP) | — | ✓ |

### Schnellstart (beta.16)

1. [`VIVODEPOT.html`](VIVODEPOT.html) herunterladen
2. In Chrome oder Firefox öffnen (Doppelklick genügt)
3. Loslegen — keine Installation, keine Registrierung

**Online-Version:** [carolaklessen.github.io/vivodepot/](https://carolaklessen.github.io/vivodepot/)

### Funktionsumfang beta.16

Die Anwendung deckt 22 Schritte ab — Stammdaten, Vertrauenspersonen, Finanzen, Versicherungen, Immobilien, Verträge & Abos, Gesundheit, Wohlbefinden & Seele (PHQ-9, GAD-7, WHO-5), Pflege, Mein Wille (Testament & Vollmachten, BGB-Referenzen 2023), Mein Abschied, Erinnerungsstücke, Haustiere, Digitales Erbe, Assistenten, Notfall (BBK-Empfehlungen), Datenaustausch (FHIR/FIM/EUDI/QR/Solid-Pod), Prüftermine, Einstellungen.

Exporte: Word, PDF, Notfall-Checkliste, Arztbogen (verschiedene Varianten), Szenario-PDFs, Vollmacht-/Verfügungs-Word-Dokumente, vCard, QR-Aufkleber, Weitergabe-Datei (HTML, verschlüsselt), QR-Übergabe (AES-256-GCM, PIN-geschützt, 24-Stunden-Gültigkeit, Mehr-Teile-fähig), Solid-Pod-Export (Turtle), FHIR-Export mit PROM-Scores und DSGVO-Consent.

Import: EUDI-Wallet (SD-JWT), FHIR R4, FIM-JSON, allgemeines JSON.

Für Institutionen (seit beta.15/16): Companion-Schema-v1.0-Vorlagen für Fragebögen plus Vorlagen-Editor in der App. FHIR-konformer Export inklusive DSGVO-Consent-Ressource.

Barrierefreiheit: WCAG-2.2-Touch-Targets (44 px), Schriftgröße A+ in drei Stufen, hoher Kontrast, Nachtmodus, Vorlesen, Bildschirmlupe, Diktat.

Detaillierte Dokumentation: [DOCS.md](DOCS.md) · [INTEROPERABILITY.md](INTEROPERABILITY.md) · [QUICKSTART.md](QUICKSTART.md) · [FAQ.md](FAQ.md) · [SOVEREIGNTY.md](SOVEREIGNTY.md) · [CHANGELOG.md](CHANGELOG.md).

### Sicherheit beta.16

| Merkmal | Details |
|---|---|
| Verschlüsselung | AES-256-GCM via Web Crypto API |
| Schlüsselableitung | PBKDF2-HMAC-SHA256, 200.000 Iterationen, kryptographisch zufälliger Salt |
| Salt-Speicherung | In gespeicherter Datei eingebettet (seit beta.7) — auf jedem Gerät mit Passwort entschlüsselbar |
| Weitergabe-Datei | Eigener Salt, eigenes Passwort |
| QR-Übergabe | Hash-Fragment-Payload erreicht keinen Server, PIN-geschützt, 24-Stunden-Gültigkeit |
| Leseansicht | Kein Speichern, kein Server, keine Cookies, keine Tracking-Substanz |
| Netzwerkanfragen | Keine — vollständig offline |
| Telemetrie | Nicht vorhanden |
| Externe Skripte | Nicht vorhanden (alle Bibliotheken inline) |

Sicherheitsmeldungen: [SECURITY.md](SECURITY.md).

### Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

Aktuelle Tests laufen vollständig durch. Details zur Test-Architektur und neuen Test-Schichten: [CONTRIBUTING.md](CONTRIBUTING.md).

---

Vivodepot ist Architektur — keine Anwendung, keine Plattform, keine Cloud. Es ist die fehlende Schicht zwischen Bürger und Institution: einfach genug, um zu funktionieren; offen genug, um zu überleben; präzise genug, um Standard zu werden.
