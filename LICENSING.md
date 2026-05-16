# Vivodepot — Lizenzpolitik

*Stand: Mai 2026 · Fassung 1.1 (Zwei-Schichten-Klarstellung)*

Diese Seite erklärt das Lizenzmodell von Vivodepot in einfacher Sprache. Verbindlich ist der Lizenztext in [LICENSE](LICENSE).

---

## Vivodepot — frei für Bürger, fair für Institutionen

Vivodepot ist eine souveräne, offline-fähige Architektur für Bürger-Datenhaltung. Sie wurde gebaut, damit Menschen ihre Daten gegenüber Institutionen souverän verwalten können. Diese Mission verlangt eine Lizenzpolitik, die zwei Dinge gleichzeitig sicherstellt: maximale Freiheit für Bürger, Forscher und Communities — und eine wirtschaftliche Tragfähigkeit, die Vivodepot dauerhaft existieren lässt.

## Zwei Schichten, zwei Lizenzen

Vivodepot besteht aus zwei Code-Schichten mit unterschiedlichen Aufgaben — und entsprechend unterschiedlichen Lizenzen:

### Schicht 1 — App-Code unter EUPL-1.2 (Open Source)

Die Vivodepot-Anwendung als Ganzes ist Open Source unter der **European Union Public Licence v1.2 (EUPL-1.2)**. Das schließt die Hauptanwendung `VIVODEPOT.html`, die Leseansicht `vivodepot-lesen.html`, die Test-Suite und alle weiteren Code-Dateien des Repositories ein.

Was das bedeutet:

- Bürger:innen, Forschungseinrichtungen, gemeinnützige Organisationen, Behörden, Unternehmen — alle dürfen die Anwendung sofort und ohne Lizenzgebühren nutzen, kopieren, verändern, weitergeben und kommerziell einsetzen.
- Beiträge zur Anwendung (Pull Requests, Bug-Fixes, Übersetzungen) werden ebenfalls unter EUPL-1.2 veröffentlicht.
- Die EUPL-1.2 ist reziprok — abgeleitete Werke müssen wieder unter EUPL-1.2 (oder einer kompatiblen Lizenz) verfügbar sein. Das ist methodisch konsequent zum Werkzeug-Charakter.

### Schicht 2 — Template-Mechanismus unter BUSL-1.1 (kommerziell, mit Konversion)

Der Template-Mechanismus von Vivodepot — also die Vorlagen, die anbieter-mitgebrachten Companion-Schemata, der zugehörige Übergabe- und Trust-Authority-Mechanismus — ist unter der **Business Source License 1.1 (BUSL-1.1)** lizenziert. Vier Jahre nach Veröffentlichung jeder einzelnen Version konvertiert diese Schicht automatisch zu EUPL-1.2.

Was das bedeutet:

- Bürger:innen, Forschungseinrichtungen, gemeinnützige Organisationen und kleine Akteure dürfen den Template-Mechanismus frei nutzen.
- Institutionen, die Vivodepot in einem produktiven Umfeld einsetzen, in dem die personenbezogenen Daten von **mehr als 1.000 Personen** verarbeitet werden, benötigen für die Template-Schicht eine kommerzielle Lizenz.
- Vier Jahre nach Veröffentlichung wird jede Version dieser Schicht automatisch EUPL-1.2 — also vollständig frei, auch für große Institutionen.

## Was Vivodepot für Sie kostet

| Wer Sie sind | App-Code (EUPL-1.2) | Template-Mechanismus (BUSL-1.1 → EUPL-1.2) |
|---|---|---|
| Bürgerin oder Bürger | frei | frei |
| Forschungseinrichtung, Hochschule | frei | frei |
| Gemeinnützige Organisation, kleine NGO | frei | frei |
| Institution mit weniger als 1.000 Personen-Datensätzen | frei | frei |
| Institution mit mehr als 1.000 Personen-Datensätzen | frei (EUPL-1.2) | **kommerzielle Lizenz erforderlich** |

Wenn Sie als Krankenkasse, Versicherer, Bundesland, Krankenhausträger oder gewerblicher Dienstleister Vivodepot in Ihren Geschäftsbetrieb einbauen wollen, sprechen Sie uns an — wir gestalten Lizenzen fair und passend zu Ihrer Größe.

## Warum dieses Modell

Eine Bürger-Datensouveränitäts-Plattform muss zwei Dingen gerecht werden, die in normalen Software-Geschäftsmodellen nicht zusammenpassen: sie muss frei sein, weil Souveränität nicht hinter einer Bezahlschranke leben kann. Und sie muss tragen, weil eine Software, die nicht weiterentwickelt wird, in einem regulierten Umfeld wie der Patientendatenverarbeitung nicht überlebt.

Die Trennung in zwei Schichten löst diesen Konflikt:

- **App-Code unter EUPL-1.2** — Werkzeug. Frei für alle, sofort. Maximale Verbreitung, maximale Freiheit. Das Werkzeug muss bei den Menschen ankommen, die es brauchen.
- **Template-Mechanismus unter BUSL-1.1** — Plattform. Über sie werden anbieter-gebrachte Vorlagen verteilt und kryptographisch signiert; sie trägt die institutionelle Trust-Schicht. Hier finanzieren Institutionen, die Vivodepot strukturell einsetzen, die Weiterentwicklung. Nach vier Jahren wird auch diese Schicht frei.

So entsteht ein Modell, das maximale Freiheit für Personen mit ausreichender Tragfähigkeit für eine dauerhaft gepflegte Architektur verbindet — plus ein zeitversetztes Open-Source-Versprechen, das verhindert, dass irgendein Teil dauerhaft proprietär bleibt.

## Was nach vier Jahren passiert

Vier Jahre nach Veröffentlichung einer Version wird der Template-Mechanismus dieser Version — und nur dieser — automatisch EUPL-1.2. Beispiel: Vivodepot beta.16, veröffentlicht im Mai 2026, wird im Mai 2030 vollständig EUPL-1.2 (App-Code ist es bereits jetzt). Während ältere Versionen sukzessive frei werden, bleibt die jeweils aktuelle Versionsfront der Template-Schicht BUSL-1.1 — solange das Geschäftsmodell sie trägt.

**Eine Zusage, die wir geben:** Wenn Vivodepot Standardschicht-Status erreicht oder in eine gemeinnützige Trägerstruktur überführt wird, behalten wir uns vor, das Lizenzmodell der Template-Schicht aktiv auf eine vollständige Open-Source-Lizenz umzustellen — auch früher als die Vier-Jahres-Frist. Wir versprechen, dass Vivodepot nie restriktiver wird. Es kann nur freier werden.

## Was das technisch heißt

**App-Code:**

- Lizenz: EUPL-1.2
- Reziprozität: abgeleitete Werke unter EUPL-1.2 (oder kompatibler Lizenz)
- Keine Schwelle, keine kommerzielle Einschränkung

**Template-Mechanismus, pro Version:**

- Lizenz heute: Business Source License 1.1 (BUSL-1.1)
- Use Limitation: produktiver Einsatz durch Organisationen mit mehr als 1.000 personenbezogenen Datensätzen erfordert eine kommerzielle Lizenz; privater, gemeinnütziger, akademischer und Forschungs-Einsatz ist frei
- Change Date: Veröffentlichungsdatum + 4 Jahre (pro Version individuell)
- Change License: EUPL-1.2

Nach dem Change Date verliert die BUSL-Einschränkung ihre Wirkung, und die Template-Schicht der jeweiligen Version steht ohne weitere Bedingungen unter EUPL-1.2.

## Kontakt für Lizenzfragen

Lizenzgespräche, Anfragen zur kommerziellen Nutzung der Template-Schicht, Klärungen zur 1.000-Personen-Schwelle: **[lizenz@vivodepot.de](mailto:lizenz@vivodepot.de)** oder **[legal@vivodepot.de](mailto:legal@vivodepot.de)**.
