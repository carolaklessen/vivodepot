# Vivodepot — Standards-Substanz

*Stand: 13. Mai 2026 · Version 1.0 (Erstfassung) · Bezug: VIVODEPOT.html v1.0.0-beta.17*

Diese Datei dokumentiert alle offenen Standards, die Vivodepot abbildet — implementiert, in Roadmap verankert oder als regulatorischer Rahmen relevant. Sie ist die maßgebliche Substanz für die Aussage „über 30 offene Standards" auf den Webseiten und in Förderanträgen.

---

## Übersicht und Methodik

Vivodepot ist als Bürger-Daten-Container auf Interoperabilität mit institutionellen Systemen angelegt. Statt einer eigenen API oder eines proprietären Formats nutzt Vivodepot durchgängig anerkannte offene Standards für jede Datendomäne. Das schützt Bürgerinnen und Bürger vor Lock-in und ermöglicht Institutionen den Anschluss ohne Sonderaufwand.

**Implementations-Stand pro Standard:**

- **Implementiert** — in v1.0 (Mai/Juni 2026) im Code aktiv, getestet, durch automatisierte CI-Validierung gedeckt
- **Roadmap** — strategisch verankert in ADRs, Master-Briefing oder Verankerungs-Strategie, Implementation für 2026 oder 2027 geplant
- **Rahmen** — regulatorischer oder lizenzrechtlicher Anschluss, kein eigener Standard im Code

**Zählung für Webseiten-Aussage:** Sechs Implementations-Cluster (1–6) mit insgesamt 32 implementierten Standards. Cluster 7 und 8 sind regulatorische und lizenzrechtliche Rahmen, nicht im Standard-Count enthalten.

---

## Cluster 1 — Medizinische Codierungs-Systeme

Strukturierte Codierung für Gesundheitsdaten ist Voraussetzung für interoperablen Austausch mit Kliniken, Praxen und Krankenkassen. Vivodepot bildet die wichtigsten internationalen und deutschen Codierungs-Systeme pro Datendomäne ab. Die Codes sind als Vorschlagslisten (10 bis 15 häufigste Werte pro Bereich) im Code verankert; freitextliche Einträge sind möglich und werden später ärztlich codiert.

| Standard | Version | Quelle | Verwendung | Stand |
|---|---|---|---|---|
| **SNOMED-CT** | International Edition 2025 | IHTSDO (https://snomed.info/sct) | Allergien, Impfungen, Prozeduren, Devices | Implementiert |
| **ICD-10-GM** | 2024 | BfArM (https://www.bfarm.de/DE/Kodiersysteme/Klassifikationen/ICD/ICD-10-GM/) | Krankheiten und Diagnosen | Implementiert |
| **ATC** | aktuell | WHO Collaborating Centre for Drug Statistics Methodology (https://www.whocc.no/atc_ddd_index/) | Medikamenten-Wirkstoffe | Implementiert |
| **LOINC** | aktuell | Regenstrief Institute (https://loinc.org/) | IPS-Composition-Code 60591-5, Laborwerte | Implementiert |

---

## Cluster 2 — Gesundheitsdaten-Formate

FHIR R4 und das International Patient Summary (IPS) sind der HL7-Standard für interoperable Gesundheitsdaten in der EU. Vivodepot exportiert IPS-konforme FHIR-Bundles mit sechs Pflichtbereichen und importiert FHIR-R4-Daten aus EHDS-Quellen.

| Standard | Version | Quelle | Verwendung | Stand |
|---|---|---|---|---|
| **HL7 FHIR R4** | Release 4 | HL7 International (https://hl7.org/fhir/R4/) | Export und Import strukturierter Gesundheitsdaten | Implementiert |
| **International Patient Summary (IPS)** | v2.0.0 STU 2 (Oktober 2025) | HL7 (https://hl7.org/fhir/uv/ips/STU2/) | Patient Summary mit sechs Pflichtbereichen | Implementiert |
| **HL7 FHIR Provenance** | Release 4 | HL7 | Sub-Depot-Provenance, Audit-Substanz (ADR-063) | Implementiert |
| **HL7-V3-RoleCode** | v3 | HL7 Terminology (http://terminology.hl7.org/CodeSystem/v3-RoleCode) | Beziehungs-Codierung Anker zu Sub-Depot (16 Codes) | Implementiert |
| **HL7-V3-NullFlavor** | v3 | HL7 Terminology (http://terminology.hl7.org/CodeSystem/v3-NullFlavor) | OTH-Beziehung mit Freitext-Fallback | Implementiert |

Die sechs IPS-Pflichtbereiche sind in der Implementation als Konstante `IPS_PFLICHT_BEREICHE` verankert: Allergien (AllergyIntolerance), Medikation (MedicationStatement), Krankheiten (Condition), Impfungen (Immunization), Prozeduren (Procedure), Devices (Device plus DeviceUseStatement). Validierung erfolgt gegen den offiziellen HL7-Validator als CI-Schritt.

---

## Cluster 3 — Identität und Signaturen

Identitäts-Substanz, Verifiable Credentials und kryptographische Signaturen bilden die Vertrauens-Schicht zwischen Bürgerin, Institutionen und Vivodepot. Der Anschluss an eIDAS 2.0 plus EUDIW ist als Identitätsanker implementiert; die Trust-Authority-Architektur für Template-Übergaben nutzt JWS plus W3C Verifiable Credentials.

| Standard | Version | Quelle | Verwendung | Stand |
|---|---|---|---|---|
| **EUDIW (EU Digital Identity Wallet)** | eIDAS 2.0 ARF | EU-Kommission (https://digital-strategy.ec.europa.eu/en/policies/eudi-wallet) | Identitätsanker, PID-Import | Implementiert |
| **eIDAS 2.0** | Verordnung (EU) 2024/1183 | EU-Amtsblatt | Regulatorischer Rahmen für EUDIW | Rahmen + Implementiert |
| **SD-JWT** | IETF Draft | IETF OAuth WG (https://datatracker.ietf.org/doc/draft-ietf-oauth-selective-disclosure-jwt/) | Selective Disclosure JWT für EUDIW-PID-Import | Implementiert |
| **SD-JWT-VC** | OpenID Foundation Profile | OIDF (https://openid.net/specs/openid-4-verifiable-credentials-vc-data-model-1_0.html) | Verifiable Credentials im SD-JWT-Format | Implementiert |
| **W3C Verifiable Credentials** | v1.1 W3C Recommendation | W3C (https://www.w3.org/TR/vc-data-model/) | Provider-Zertifikate, Template-Anbieter-Trust | Implementiert (ADR-065) |
| **JWS RFC 7515** | IETF RFC 7515 | IETF | JSON Web Signature für Template-Übergaben | Implementiert (ADR-065) |
| **Ed25519** | RFC 8032 | IETF | Primärer Signatur-Algorithmus | Implementiert |
| **ES256** | RFC 7518 | IETF | Fallback-Signatur-Algorithmus (ECDSA mit P-256, SHA-256) | Implementiert |

---

## Cluster 4 — Verwaltung und Behörden

Bürgerinnen interagieren mit dutzenden Verwaltungs- und Behörden-Diensten. Vivodepot bildet die wichtigsten deutschen und europäischen Verwaltungs-Formate ab. FIM-JSON ist in v1.0 implementiert; weitere Verwaltungs-Anschlüsse sind in der Roadmap verankert.

| Standard | Version | Quelle | Verwendung | Stand |
|---|---|---|---|---|
| **FIM-JSON** | aktuell | Föderales Informationsmanagement (https://fimportal.de/) | Behördendaten-Export und -Import | Implementiert |
| **BundID** | aktuell | BMI (https://id.bund.de/) | Relying-Party-Anbindung für Pilotpartner-Szenarien | Roadmap (SPRIND-Sandbox Q3 2026) |
| **OOTS (Once-Only Technical System)** | EU SDG-Regulation | EU-Kommission (https://ec.europa.eu/single-market-economy/single-digital-gateway-and-technical-system) | EU-weite Once-Only-Anbindung | Roadmap (XDSC-Anschluss Q3/Q4 2026) |
| **XDSC** | Bremer Datenschutzcockpit-Standard | Senatsverwaltung Bremen | Datenschutz-Cockpit-Anschluss, OOTS-Bridge | Roadmap (Anbahnung Q3 2026) |
| **XMeld** | OSCI-XMeld | KoSIT (https://www.xrepository.de/) | Meldedaten-Import (Adressen, Familienstand) | Roadmap (v1.1) |
| **ELSTER** | aktuell | BMF (https://www.elster.de/) | Steuerdaten-Import, Bescheid-Format | Roadmap (v1.1) |
| **European Learning Model (ELM)** | EU-Edu-Standard | Europass / EU-Kommission | Bildungs- und Qualifikations-Nachweise | Roadmap (v1.1) |

---

## Cluster 5 — Bürger-zentrische Formate und Interoperabilität

Vivodepot exportiert nicht nur für Institutionen, sondern auch für Bürgerinnen und Bürger selbst — in Formaten, die mit Adressbüchern, persönlichen Datenspeichern und Office-Anwendungen kompatibel sind.

| Standard | Version | Quelle | Verwendung | Stand |
|---|---|---|---|---|
| **vCard** | 4.0 (RFC 6350) | IETF | Kontakte-Export und -Import (.vcf) | Implementiert |
| **CSV** | RFC 4180 | IETF | Kontakte-Import | Implementiert |
| **Turtle (RDF)** | W3C Recommendation 2014 | W3C (https://www.w3.org/TR/turtle/) | Solid-Pod-Export | Implementiert |
| **Schema.org** | aktuell | Schema.org (https://schema.org/) | RDF-Vokabular für Personen-Daten | Implementiert |
| **FOAF (Friend of a Friend)** | 0.99 | FOAF Project (http://xmlns.com/foaf/0.1/) | RDF-Vokabular für Beziehungen | Implementiert |
| **W3C vCard Ontology** | W3C Note | W3C (http://www.w3.org/2006/vcard/ns#) | RDF-Vokabular für Kontaktdaten | Implementiert |
| **RDFS** | W3C Recommendation | W3C | RDF Schema-Substanz | Implementiert |
| **XSD (XML Schema Datatypes)** | W3C Recommendation | W3C | Typisierung in RDF-Substanz | Implementiert |
| **Solid Protocol** | W3C Solid CG | W3C Solid Community Group (https://solidproject.org/) | Persönlicher Datenspeicher (Solid Pod) | Implementiert (Export) |

---

## Cluster 6 — Kryptographie und Sicherheit

Vivodepot ist eine offline-first Single-File-HTML-Anwendung mit lokaler Verschlüsselung. Sämtliche Krypto-Substanz folgt etablierten IETF- und NIST-Standards. Externe Verifikation erfolgt gegen RFC 5869 Test-Vektoren, NIST CAVP und Wycheproof (ADR-055).

| Standard | Version | Quelle | Verwendung | Stand |
|---|---|---|---|---|
| **AES-256-GCM** | NIST SP 800-38D | NIST | Verschlüsselung der Bürger-Daten | Implementiert |
| **PBKDF2** | RFC 8018 | IETF | Schlüssel-Ableitung aus Passwort (600.000 Iterationen) | Implementiert |
| **HKDF** | RFC 5869 | IETF | Sub-Schlüssel-Ableitung pro Sub-Depot | Implementiert |
| **SHA-256** | NIST FIPS 180-4 | NIST | Hash-Funktion für PBKDF2 und HKDF | Implementiert |
| **UUID v4** | RFC 4122 | IETF | FHIR-Resource-Identifikatoren, Bundle-IDs | Implementiert |

---

## Cluster 7 — Regulatorischer Rahmen *(nicht im Standard-Count)*

Diese regulatorischen Substanzen sind kein technischer Standard im engeren Sinn, sondern der Rechts- und Politik-Rahmen, in den Vivodepot eingebettet ist. Sie werden auf eu.html ausführlicher behandelt.

| Rahmen | Substanz | In-Kraft / Status | Vivodepot-Anschluss |
|---|---|---|---|
| **EHDS (European Health Data Space)** | Verordnung (EU) 2025/327 | In Kraft seit März 2025 | FHIR-R4/IPS-konformer Import aus EHDS-Quellen implementiert |
| **xShare Yellow Button** | EHDS-Exportinstrument | EOI eingereicht Mai 2026 | Vivodepot als Empfänger auf Bürger-Seite |
| **Vergabebeschleunigungsgesetz** | Deutsches Beschaffungsrecht | Verabschiedet 23. April 2026, in Kraft 1. Juli 2026 | Vivodepot erfüllt die drei Souveränitäts-Kriterien |
| **FiDA (Financial Data Access Regulation)** | EU-Finanzdaten-Verordnung | In Verhandlung (Trilog) | Roadmap-Anschluss für Finanzdaten-Bridge (v1.1) |
| **UN Global Digital Compact** | UN-Rahmenwerk Digitale Zusammenarbeit | Verabschiedet September 2024 | Vivodepot als Digital Public Good nominiert (DPGA GID0093612) |
| **DSGVO Art. 20** | Datenübertragbarkeit | In Kraft seit 2018 | Vivodepot ist das praktische Werkzeug für dieses Recht |

---

## Cluster 8 — Lizenz-Substanz *(nicht im Standard-Count)*

Lizenz-Substanz für die Vivodepot-Anwendung und den Template-Übergabe-Mechanismus. Vollständige Erläuterung in [LICENSING.md](LICENSING.md).

| Lizenz | Anwendungsbereich | Quelle |
|---|---|---|
| **EUPL-1.2** | Vivodepot-Anwendung, Hauptanwendung VIVODEPOT.html, alle Code-Dateien | EU-Kommission (https://joinup.ec.europa.eu/collection/eupl/) |
| **BUSL-1.1 → EUPL-1.2** | Template-Übergabe-Mechanismus und Trust-Authority-Architektur, mit automatischer Konversion zu EUPL-1.2 nach vier Jahren | MariaDB / Sentry (https://mariadb.com/bsl11/) |

---

## Konsolidierte Zählung

**Implementiert in v1.0 (Mai/Juni 2026):**

- Cluster 1 (Medizinische Codierungen): 4
- Cluster 2 (Gesundheitsdaten-Formate): 5
- Cluster 3 (Identität und Signaturen): 8
- Cluster 4 (Verwaltung — nur FIM-JSON): 1
- Cluster 5 (Bürger-zentrische Formate): 9
- Cluster 6 (Kryptographie): 5

**Summe Implementiert: 32 offene Standards in v1.0.**

**Roadmap (v1.1 bis 2027):**

- BundID, OOTS, XDSC, XMeld, ELSTER, ELM: 6 weitere Standards

**Summe inklusive Roadmap: 38 offene Standards.**

**Webseiten-Aussage:** „Über 30 offene Standards" — belegbar durch v1.0-Implementation allein.

---

## Verifikation und Audit

Alle implementierten Standards sind in der Codebasis nachweisbar:

- **FHIR R4 / IPS:** Validierung gegen HL7-FHIR-Validator als CI-Schritt
- **HL7-V3-RoleCode:** 16 Codes plus OTH, verifiziert gegen das offizielle HL7-V3-Code-System (drei Korrekturen während Implementation: ADOPT → CHLDADOPT, NIENE → NIENEPH, OTH System-Wechsel zu v3-NullFlavor)
- **AES-256-GCM, PBKDF2, HKDF:** Externe Verifikation gegen RFC 5869 Test-Vektoren, NIST CAVP, Wycheproof (ADR-055)
- **EUDIW SD-JWT:** Konform zur aktuellen eIDAS 2.0 ARF
- **W3C VC, JWS:** Konform zur W3C-Recommendation v1.1 (ADR-065)
- **Code-Belege:** VIVODEPOT.html enthält `IPS_PFLICHT_BEREICHE`, `IPS_CODES`, `BEZIEHUNGS_CODES`, sämtliche Krypto-Konstanten und alle Import-Export-Funktionen mit Bezug zur jeweiligen ADR

Vollständiger Code-Audit über das öffentliche Repository: [gitlab.opencode.de/oc000142426528/vivodepot](https://gitlab.opencode.de/oc000142426528/vivodepot)

---

## Pflege dieses Dokuments

Diese Datei wird bei jedem neuen Standard-Anschluss aktualisiert. Verantwortliche Pflege: Vivodepot GmbH (i.Gr.). Änderungs-Substanz wird in den ADRs unter `docs/adr/` dokumentiert.

Bei Fragen zu Standards-Implementation oder -Konformität: [eu@vivodepot.de](mailto:eu@vivodepot.de) oder direkt im Repository als Issue.
