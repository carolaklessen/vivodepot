# VIVODEPOT — Interoperabilität

*Version 1.0.0-beta.16 · April 2026*

---

## Grundprinzip

Vivodepot ist vollständig offline. Kein Server empfängt oder sendet Daten. Alle
Austauschvorgänge finden ausschließlich durch Dateien statt, die der Nutzer
selbst erzeugt und weitergibt — per Download, USB, E-Mail, QR-Code oder
Zwischenablage.

Interoperabilität bedeutet in Vivodepot daher: die Fähigkeit, strukturierte
Daten in etablierten offenen Standards zu erzeugen, die von anderen Systemen
ohne Konvertierungsaufwand gelesen werden können.

---

## Übersicht aller Austauschformate

### Export

| Format | Standard | Zielgruppe | Funktion | Dateiendung |
|---|---|---|---|---|
| FHIR R4 / IPS 2.0 | HL7, IPS, EU Base IG | Klinik, ePA, EHDS | `generateFHIR()` | `.fhir.json` |
| FHIR PROM | HL7 FHIR R4 | Institution (Fragebogen) | `tplDownloadFhir()` | `.fhir.json` |
| FIM-JSON | FIM, FITKO | Behörde, Verwaltungsportal | `exportFIMJson()` | `.json` |
| vCard 4.0 | RFC 6350 | Adressbuch, Smartphone | `exportVCard()` | `.vcf` |
| Solid / Turtle | RDF 1.1, Solid Protocol | Eigener Datenspeicher | `solidPodExport()` | `.ttl` |
| Weitergabe-Datei | Vivodepot-proprietär | Angehörige, Arzt, Institution | `wgErstellen()` | `.html` |
| QR-Übergabe | Vivodepot-proprietär | Institution (direkt, kein USB) | `qrErstellen()` | URL |
| Companion-Schema | Vivodepot-proprietär | Institution (Vorlage) | `tplEditorExport()` | `.json` |
| Vivodepot-JSON | Vivodepot-proprietär | Backup / Reimport | `exportJSON()` | `.json` |

### Import

| Format | Standard | Quelle | Funktion |
|---|---|---|---|
| FHIR R4 | HL7 FHIR R4 | ePA, Arztbrief, Medikationsplan | `importStructured(event,'fhir')` |
| FIM-JSON | FIM, FITKO | Verwaltungsportal, Bürgerportal | `importStructured(event,'fim')` |
| SD-JWT (EUDI) | EUDI Wallet | Europäischer digitaler Ausweis | `importEudiWallet()` |
| Allgemeines JSON | — | Beliebige JSON-Datei | `importStructured(event,'auto')` |
| Vivodepot-JSON | Vivodepot-proprietär | Früherer Vivodepot-Export | `importData()` |

---

## Export-Formate im Detail

### 1. FHIR R4 / International Patient Summary

**Standard:** HL7 FHIR R4 (4.0.1), IPS 2.0.0 (`hl7.fhir.uv.ips`),
HL7 Europe Base Implementation Guide (`hl7.fhir.eu.base 2.0.0-ballot`).

**Zielgruppe:** Krankenhäuser, Kliniken, niedergelassene Ärzte, ePA-Systeme,
alle EHDS-konformen Empfänger in der EU.

**Inhalt:**

| FHIR-Ressource | Inhalt aus Vivodepot |
|---|---|
| `Patient` | Name, Geburtsdatum, Adresse, Telefon, Nationalität |
| `MedicationStatement` | Medikamente, Dosierung |
| `AllergyIntolerance` | Allergien, Unverträglichkeiten |
| `Observation` | PROM-Scores (PHQ-9, GAD-7, WHO-5) mit LOINC-Codes |
| `QuestionnaireResponse` | Ausgefüllte Fragebögen mit LOINC-Fragebogen-Codes |
| `Composition` | IPS-Pflichtstruktur (Allergien, Medikamente, Diagnosen) |
| `Consent` | DSGVO-Einwilligungsnachweis (LOINC 59284-0, GDPR Art. 6) |

**LOINC-Codes:**

| Instrument | Fragebogen-Code | Score-Code |
|---|---|---|
| PHQ-9 | 44249-1 | 44261-6 |
| GAD-7 | 69737-5 | 70274-6 |
| WHO-5 | 71969-0 | 71969-0 |
| DSGVO-Consent | 59284-0 | — |

**Konformität:** Nachgewiesen. Zwei unabhängige Konformitätsberichte liegen vor:
- HL7 EU Base IG — 0 Fehler, 0 Warnungen (19. April 2026)
- IPS 2.0.0 — 0 Fehler, 0 Warnungen (20. April 2026)

**EHDS-Referenzierbarkeit:** Ja. Vivodepot ist die erste bekannte
Open-Source-Offline-Implementierung des EHDS Citizen User Journey mit
nachgewiesener HL7 EU Base IG Konformität.

**Dateiname:** `IPS_Nachname_JJJJ-MM-TT.fhir.json`

---

### 2. FHIR PROM (Fragebogen-Ergebnis)

**Standard:** HL7 FHIR R4 — `QuestionnaireResponse`, `Observation`, `Consent`.

**Zielgruppe:** Institutionen (Pflegeheime, Kliniken), die einen Companion-Schema-
Fragebogen bereitgestellt haben und das strukturierte Ergebnis empfangen.

**Inhalt:** Ausgefüllte Antworten, berechneter Score, DSGVO-Einwilligungsnachweis.
PGHD-Tag (`Patient-Generated Health Data`) im `meta.tag` — explizite EHDS-
Kategorie für patientengenerierte Daten.

**Besonderheit:** Dieser Export erfolgt immer im Kontext einer konkreten Vorlage
(Companion-Schema). Er ist inhaltlich spezifischer als der allgemeine FHIR-Export
und richtet sich ausschließlich an die Institution, die die Vorlage erstellt hat.

**Dateiname:** `{template-id}-{datum}.fhir.json`

---

### 3. FIM-JSON

**Standard:** Föderales Informationsmanagement (FIM), Stammdaten-Schema der
FITKO (Föderale IT-Kooperation). Maschinenlesbar, kompatibel mit deutschen
Verwaltungsportalen.

**Zielgruppe:** Behörden, Verwaltungsportale (z.B. Antragssysteme für
Pflegegeld, Grundsicherung, Schwerbehindertenausweis).

**Inhalt:** Stammdaten (`natuerlichePerson`): Name, Geburtsdatum, Adresse,
Kontakte. Kein Gesundheitsbezug.

**Hinweis:** FIM ist ein deutschsprachiger Verwaltungsstandard ohne
internationale Entsprechung. Empfänger außerhalb der deutschen Verwaltung
können dieses Format in der Regel nicht verarbeiten.

**Dateiname:** `Vivodepot_Behoerdendaten_Nachname_JJJJ-MM-TT.json`

---

### 4. vCard 4.0

**Standard:** RFC 6350 (vCard Format Specification, Version 4.0).

**Zielgruppe:** Adressbuch-Apps auf Smartphone und Computer, alle Anwendungen
mit vCard-Unterstützung.

**Inhalt:** Einzelner Kontakt oder alle Vertrauenspersonen. Felder: Name,
Telefon, E-Mail, Adresse, Beruf, Organisation.

**Dateiname:** `Kontaktname.vcf` (Einzelexport) oder `Vivodepot_Kontakte.vcf`
(Sammelexport).

---

### 5. Solid Pod / RDF Turtle

**Standard:** RDF 1.1 (W3C), Turtle-Serialisierung, Solid Protocol (W3C).
Präfixe: `vcard:` (W3C vCard Ontology), `schema:` (schema.org).

**Zielgruppe:** Persönlicher Solid Pod als souveräner Datenspeicher. Anbieter
z.B. solidcommunity.net.

**Inhalt:** Persönliche Stammdaten als Linked-Data-Graph. Maschinenlesbar und
semantisch verknüpfbar.

**Besonderheit:** Solid ist das einzige Austauschformat in Vivodepot, das auf
einen netzwerkfähigen Empfänger zielt. Der Export selbst erfolgt offline — der
Upload in den Pod liegt beim Nutzer.

**Dateiname:** `Vivodepot_SolidPod_Nachname_JJJJ-MM-TT.ttl`

---

### 6. Weitergabe-Datei

**Standard:** Vivodepot-proprietär. Kein externer Standard.

**Zielgruppe:** Angehörige, Hausarzt, Institution — Übermittlung per E-Mail
oder USB.

**Inhalt:** Gefilterter Datensatz nach Profil:

| Profil | Inhalt |
|---|---|
| Notfall | Notfallkontakte, Medikamente, Blutgruppe, Vollmacht-Status |
| Vollmacht | Bevollmächtigte, Vollmacht-Dokumente, Patientenverfügung |
| Familie | Persönliche Daten, Testament, Bestattungswünsche, Kontakte |
| Behörde | Stammdaten, Einkommensdaten, Versicherungen |

**Sicherheit:** AES-256-GCM, eigener Salt, separates Passwort (unabhängig vom
Hauptpasswort). Empfänger öffnet die Datei im Browser ohne Installation.

**Technisch:** Eigenständige HTML-Datei mit eingebetteten verschlüsselten Daten
und integriertem Entschlüsselungslogik.

---

### 7. QR-Übergabe

**Standard:** Vivodepot-proprietär. Kein externer Standard.

**Zielgruppe:** Direkte Übergabe in Institutionen, die keine USB-Geräte erlauben.
Empfänger scannt mit Smartphone-Kamera.

**Inhalt:** Identische Profile wie Weitergabe-Datei (Notfall, Vollmacht,
Familie, Behörde). Zusätzlich: PROM-Scores im Notfall-Profil.

**Sicherheit:** AES-256-GCM, PIN-geschützt, 24 Stunden Ablauf. Hash-Fragment-
URL: Payload erreicht keinen Server.

**Kapazität:** Bis zu 6 QR-Codes (Karussell). Bei größeren Datenmengen:
Weitergabe-Datei empfohlen.

---

### 8. Companion-Schema (Vorlagen-Definition)

**Standard:** Vivodepot Companion-Schema v1.0 — proprietär, öffentlich
dokumentiert.

**Zielgruppe:** Institutionen, die eigene Fragebögen erstellen und an Nutzer
bereitstellen. Kein Endnutzer-Format.

**Inhalt:** Fragebogen-Definition: Titel, Herausgeber, Fragen, Antwort-Skala,
Scoring-Regeln, Safety-Regeln, LOINC-Codes (optional).

**Schema-Pflichtfelder:** `schemaVersion`, `id`, `version`, `locale`, `title`,
`issuer`, `scale`, `items`, `scoring`, `license`.

---

### 9. Vivodepot-JSON (Backup)

**Standard:** Vivodepot-proprietär. Kein externer Standard.

**Zielgruppe:** Ausschließlich Vivodepot selbst (Backup und Restore).

**Inhalt:** Vollständiger interner Datensatz — alle Felder, alle Werte,
Rohdatenformat ohne Semantik.

**Wichtiger Hinweis:** Dieses Format ist kein Interoperabilitätsformat. Es ist
nicht für die Weitergabe an Dritte gedacht und kann von keiner anderen Anwendung
sinnvoll verarbeitet werden. Es dient ausschließlich der Datensicherung und dem
Geräte-Wechsel innerhalb von Vivodepot.

---

## Import-Formate im Detail

### FHIR R4

Einlesen von FHIR-Bundles aus ePA, Arztbriefen oder Medikationsplänen.
Automatische Felderkennung per `resourceType`. Vorschau vor dem Übernehmen.

### FIM-JSON

Einlesen von Stammdaten aus Verwaltungsportalen. Erkennung per
`natuerlichePerson`- oder `_meta`-Schlüssel. Vorschau vor dem Übernehmen.

### SD-JWT (EUDI Wallet)

Einlesen des europäischen digitalen Ausweises. Dekodierung des JWT-Payloads
(Base64url) ohne externe Bibliothek. Gemappte Felder: Name, Geburtsdatum,
Adresse, Staatsangehörigkeit. Vollständig offline.

### Allgemeines JSON

Automatische Felderkennung für beliebige JSON-Dateien. Kein Standardformat
erwartet — Vivodepot versucht bekannte Feldnamen zu erkennen und zuzuordnen.

### Vivodepot-JSON

Vollständiger Reimport des proprietären Backup-Formats. Überschreibt
vorhandene Daten nach Bestätigung.

---

## Konformitätsnachweise

| Standard | Status | Datum | Validator |
|---|---|---|---|
| HL7 EU Base IG 1.0 (`hl7.fhir.eu.base 2.0.0-ballot`) | KONFORM — 0 Fehler, 0 Warnungen | 19. April 2026 | HL7 FHIR Validator CLI (latest) |
| IPS 2.0.0 (`hl7.fhir.uv.ips 2.0.0`) | KONFORM — 0 Fehler, 0 Warnungen | 20. April 2026 | HL7 FHIR Validator CLI 6.9.6 |
| EHDS-referenzierbar | Ja (beide Berichte) | April 2026 | — |

Vollständige Berichte: `Vivodepot_HL7_Konformitaetsbericht_20260419.pdf` und
`Vivodepot_IPS_Konformitaetsbericht_20260420.pdf`.

---

## Identifizierte Lücken (v3-Anforderungen)

### L5 — Companion-Schema ist kein EUDIW-konformer VP Request (strategische Priorität)

**Hintergrund — Entscheidung aus der Produktroadmap v1–v3 (April 2026):**

Die Roadmap legt fest, dass der Austauschmechanismus zwischen Institution und
Bürger auf dem VP-Protokoll (Verifiable Presentation) aus dem EUDIW-Framework
basieren soll — dem EU-Standard für bürgergesteuerten Datenaustausch gemäß
Verordnung EU 2024/1183. Das ist kein proprietäres Format, sondern die von der
EU definierte Architektur: Institution sendet einen strukturierten VP Request
(welche Felder, welcher Zweck, welche Institution), Bürger prüft und gibt eine
verschlüsselte VP Response zurück.

**Was heute implementiert ist:**

Das Companion-Schema v1.0 übernimmt funktional eine ähnliche Aufgabe — eine
Institution definiert, welche Fragen gestellt werden, der Bürger füllt sie aus,
das Ergebnis geht als FHIR-Bundle zurück. Der Ausgang (FHIR QuestionnaireResponse
+ Observation) ist standardkonform. Der Eingang ist es nicht.

| Pfad | Standard | Status |
|---|---|---|
| Institution → Companion-Schema JSON | Proprietär (Vivodepot v1.0) | Implementiert |
| Institution → FHIR Questionnaire | HL7 FHIR R4 (offener Standard) | Nicht implementiert |
| Institution → EUDIW Presentation Request | EUDIW ARF / ISO 18013-5 | Nicht implementiert |
| Bürger → FHIR QuestionnaireResponse | HL7 FHIR R4 | Implementiert |
| Bürger → FHIR Observation (Score) | HL7 FHIR R4 | Implementiert |

**Was die Roadmap vorsieht:**

- **v1 (heute):** Companion-Schema als Platzhalter — bewusst akzeptiert.
  Das Risiko ist in der Roadmap als „niedrig (v1)" eingestuft, weil FHIR und
  FIM-JSON als Basis dienen und Vivodepot keine eigene Datenstruktur als neuen
  Standard durchsetzen will, sondern Kontext-Layer ist.

- **v2:** Einmalpasswort → Public-Key-Verschlüsselung (RSA-OAEP oder X25519).
  Noch kein vollständiger VP Request, aber kryptografisch sichere Remote-Übergabe.

- **v3:** Vollständige EUDIW-Kompatibilität. VP Requests aus EUDIW-Systemen
  werden erkannt und verarbeitet. Vivodepot antwortet als EUDIW-kompatibler
  Credential Holder.

**Konkrete Implementierungslücken heute:**

1. Kein strukturierter VP Request als Eingabeformat — Institution kann nicht
   maschinenlesbar mitteilen, welche Felder sie anfordert und zu welchem Zweck.
2. Keine kryptografische Signatur des Requests — Echtheit der anfragenden
   Institution ist nicht verifizierbar.
3. Companion-Schema hat keine Mapping-Schicht zu FHIR Questionnaire — eine
   spätere Migration müsste alle vorhandenen Templates konvertieren.
4. Kein Public-Key-Mechanismus — Remote-Übergabe ohne physischen Kontakt ist
   nicht sicher möglich (v1-Einschränkung, laut Roadmap bewusst).

**Anforderung v2:** Public-Key-Verschlüsselung der VP Response implementieren.
Institution erhält Schlüsselpaar, Public Key steckt im Request, nur die
Institution kann mit Private Key entschlüsseln. Transportkanal (E-Mail, QR,
Link) wird damit irrelevant.

**Anforderung v3:** FHIR Questionnaire als alternatives Eingabeformat neben
Companion-Schema akzeptieren. EUDIW Presentation Request erkennen und
verarbeiten. Companion-Schema auf FHIR Questionnaire mappen oder ablösen.

**Beziehung zu L3:** L3 (Companion-Schema nicht öffentlich spezifiziert) ist
ein Teilaspekt von L5. Wenn L5 gelöst wird — durch Migration zu FHIR
Questionnaire — wird L3 automatisch hinfällig, weil kein proprietäres Schema
mehr benötigt wird.

---

### L1 — Kein geführter Export-Dialog (hohe Priorität)

**Problem:** Der Nutzer muss wissen, welche der neun Export-Funktionen er für
welchen Zweck verwenden soll. Es gibt keinen Dialog, der fragt: Was soll
exportiert werden? Für wen? In welchem Format?

Die neun Exportpfade sind historisch gewachsen und über drei Bereiche der App
verteilt (Dokumente erstellen, Datenaustausch, Für Institutionen). Ein Nutzer
ohne technisches Vorwissen kann nicht entscheiden, ob er für den Hausarztbesuch
die Weitergabe-Datei, den FHIR-Export oder den QR-Code verwenden soll.

**Anforderung v3:** Geführter Export-Dialog mit den Leitfragen:
- Wer empfängt die Daten? (Arzt / Institution / Angehörige / Behörde / eigener Speicher)
- Wie sollen die Daten übermittelt werden? (Datei / QR-Code / direkte Übergabe)
- Das System empfiehlt dann das passende Format und öffnet den richtigen Export.

### L2 — Vivodepot-JSON ist kein Interoperabilitätsformat

**Problem:** `exportJSON()` erzeugt proprietäres Rohformat und ist als „Export"
im UI präsentiert. Nutzer könnten annehmen, dass diese Datei von anderen
Systemen lesbar ist — das ist nicht der Fall.

**Anforderung v3:** Funktion intern umbenennen oder klar als „Datensicherung"
kennzeichnen, getrennt von den Interoperabilitäts-Exporten.

### L3 — Companion-Schema v1.0 ist nicht öffentlich spezifiziert

**Problem:** Das Schema ist implementiert und funktioniert — aber es existiert
keine öffentlich zugängliche Spezifikation außerhalb des Codes. Institutionen,
die Vorlagen erstellen wollen, haben keine normative Referenz.

**Anforderung v3:** Schema-Spezifikation als separates Dokument oder
als JSON Schema (Draft 2020-12) veröffentlichen.

### L4 — Kein Roundtrip zwischen Vivodepot-Instanzen

**Problem:** FHIR-Export und FIM-Export können nicht vollständig reimportiert
werden — nur ein Teil der Felder wird beim Import erkannt. Ein vollständiger
datentreuer Austausch zwischen zwei Vivodepot-Instanzen ist nur über das
proprietäre JSON-Backup möglich.

**Anforderung v3:** Entweder Vivodepot-JSON formal spezifizieren (dann wäre
L2 gelöst) oder einen dedizierten Vivodepot-Übergabe-Export definieren, der
alle Felder in einem offenen, dokumentierten Format enthält.

---

## Offene Standardisierungsprozesse

| Prozess | Relevanz | Status |
|---|---|---|
| EHDS (European Health Data Space) | Direkter Bezug — FHIR-Export ist EHDS-referenzierbar | In Kraft, Umsetzung bis 2027 |
| ZenDiS Souveränitätscheck | Offene Standards als Kriterium — Vivodepot 20/20 | Konsultation läuft (bis Mai 2026) |
| ePA für alle (Gematik) | FHIR als Empfangsformat — Import aus ePA implementiert | Rollout 2025 |
| Solid Protocol (W3C) | Solid-Export implementiert | W3C-Spezifikation aktiv |
| EUDI Wallet Regulation (EU 2024/1183) | SD-JWT-Import implementiert; VP Request/Response als Zielarchitektur (L5) | In Kraft seit 2024 — EUDIW-Pflicht Ende 2026 |
| FHIR Questionnaire (HL7) | Ziel-Eingabeformat für Institution-zu-Bürger-Austausch (L5) | Spezifikation stabil, Implementierung offen |

---

*Vivodepot UG (haftungsbeschränkt) · Berlin · hilfe@vivodepot.de*
*EUPL-1.2 · Entwickelt mit KI-Unterstützung (EU AI Act Art. 50)*
