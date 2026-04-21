# VIVODEPOT — Souveränitätsprüfung

**Selbstbewertung nach den Kriterien führender Souveränitätsrahmenwerke**
*Version 1.1.0 · April 2026*

---

## Zusammenfassung

VIVODEPOT erfüllt alle wesentlichen Souveränitätskriterien der relevanten deutschen und europäischen Rahmenwerke auf maximalem oder hohem Niveau. Das Produkt wurde von Grund auf mit dem Ziel entwickelt, vollständige digitale Souveränität für Bürgerinnen und Bürger zu gewährleisten.

---

## Teil 1 — ZenDiS-Souveränitätsprüfung (Kriterienkatalog April 2026)

Das Zentrum für Digitale Souveränität der Öffentlichen Verwaltung (ZenDiS) hat im März 2026 ein Diskussionspapier mit 20 Kriterien in 4 Kategorien veröffentlicht. Der offene Konsultationsprozess läuft bis 15. Mai 2026 über openCode (souveränitätscheck.de). Das Papier strukturiert Digitale Souveränität in drei strategische Ziele: **Wechselmöglichkeit**, **Gestaltungsfähigkeit** und **Einflussnahme**.

### Kategorie A — Organisation und Fähigkeiten

| Kriterium | Prüffrage (ZenDiS) | Vivodepot-Befund | Bewertung |
|---|---|---|---|
| A1 Strategie | Ist Digitale Souveränität in der Digitalstrategie verankert? | Vollständige digitale Unabhängigkeit ist Kernziel der Produktstrategie — kein Geschäftsmodell ohne Souveränität möglich | ✅ Maximal |
| A2 IT-Governance | Sind Verantwortlichkeiten und Steuerungsstrukturen definiert? | Einzeldatei-Architektur: keine Infrastruktur, keine Datenbank, keine externen Dienste — keine Governance-Lücken möglich | ✅ Maximal |
| A3 Risikomanagement | Werden technologische und strategische Abhängigkeiten erfasst? | Alle Abhängigkeiten inline eingebettet; keine externen APIs; vollständige Offline-Fähigkeit | ✅ Maximal |
| A4 Beschaffung | Werden Wettbewerb, Offenheit und Alternativen berücksichtigt? | EUPL-1.2: frei nutzbar, keine Lizenzgebühren, kein Vendor-Lock-in, kein Abo | ✅ Maximal |
| A5 Auftraggeberfähigkeit | Kann die Organisation IT-Projekte eigenständig steuern? | Quellcode vollständig einsehbar; keine Build-Pipeline; forkbar ohne Genehmigung | ✅ Maximal |
| A6 Kompetenzen | Verfügt die Organisation über IT-Kenntnisse zur souveränen Steuerung? | Vollständiger Quellcode in einer Datei; KI-Transparenz; keine versteckten Prozesse | ✅ Maximal |

### Kategorie B — Digitale Anwendungen und Dienste

| Kriterium | Prüffrage (ZenDiS) | Vivodepot-Befund | Bewertung |
|---|---|---|---|
| B1 Transparenz / Dokumentation | Ist eine umfassende Dokumentation vorhanden? | README, FAQ, DOCS, CHANGELOG, CONTRIBUTING, SECURITY, SOVEREIGNTY — vollständig öffentlich | ✅ Maximal |
| B2 Lieferkettensicherheit | Ist die Lieferkette nachvollziehbar und sicher? | Alle Drittbibliotheken inline eingebettet und dokumentiert; keine CDN-Abhängigkeiten; kein npm-Build | ✅ Maximal |
| B3 Architektur / Modularität | Sind Anwendungen portabel und modular? | Eine HTML-Datei; kein Framework-Lock-in; forkbar; Daten als JSON portierbar | ✅ Maximal |
| B4 Standards und Schnittstellen | Werden offene Schnittstellen und Standards genutzt? | JSON (RFC 8259), vCard 4.0 (RFC 6350), FHIR R4 (HL7), PDF/A, OOXML (ISO 29500) | ✅ Maximal |
| B5 Abhängigkeiten auf Software-Ebene | Bestehen Lock-in-Risiken durch proprietäre Software? | Keine proprietären Abhängigkeiten; läuft auf jedem Browser; keine App-Store-Pflicht | ✅ Maximal |

### Kategorie C — Informationen und Daten

| Kriterium | Prüffrage (ZenDiS) | Vivodepot-Befund | Bewertung |
|---|---|---|---|
| C1 Datenlokation | Können Behörden / Nutzer volle Kontrolle über Datenspeicherung ausüben? | 100% lokal: localStorage oder HTML-Datei auf USB-Stick; kein Server, keine Cloud | ✅ Maximal |
| C2 Datensicherheit | Sind Daten gegen unbefugten Zugriff gesichert? | AES-256-GCM, PBKDF2-HMAC-SHA256, 100.000 Iterationen, zufälliger Salt — Banken- und Behördenstandard | ✅ Maximal |
| C3 Datenschutz | Ist DSGVO-Konformität strukturell gewährleistet? | Keine Verarbeitung auf Servern → DSGVO-Konformität strukturell (by design); keine Telemetrie, kein Tracking | ✅ Maximal |
| C4 Datenstrukturen | Sind Daten in offenen, migrierbaren Formaten gespeichert? | JSON-Export jederzeit; 13 Export-Formate; kein proprietäres Format; vollständiger Datenzugang ohne Account | ✅ Maximal |

### Kategorie D — Betrieb und Infrastruktur

| Kriterium | Prüffrage (ZenDiS) | Vivodepot-Befund | Bewertung |
|---|---|---|---|
| D1 Abhängigkeit auf Betriebsebene | Bestehen Abhängigkeiten von Providern? | Keine Cloud, kein Hosting erforderlich; läuft auf USB-Stick, lokalem Rechner, GitHub Pages | ✅ Maximal |
| D2 Kundenverhältnis | Bestehen bindende Vertragsverhältnisse mit einzelnen Anbietern? | EUPL-1.2: kein Vertrag notwendig; keine Registrierung; kein Abo | ✅ Maximal |
| D3 Exit-Fähigkeit | Kann der Anbieter jederzeit gewechselt oder die Lösung selbst betrieben werden? | Die HTML-Datei ist der Betrieb; kein Anbieterwechsel nötig, weil kein Anbieter beteiligt ist | ✅ Maximal |
| D4 Resilienz / Business Continuity | Kann die Verwaltung bei exogenen Störungen weiterarbeiten? | Vollständige Offline-Fähigkeit; kein Single Point of Failure; keine externen Dienste | ✅ Maximal |
| D5 Sicherheit und Compliance | Sind Sicherheitsstandards und Compliance-Anforderungen erfüllt? | Web Crypto API (Browser-nativ); keine externe Krypto-Bibliothek; Content Security Policy; NIS2-kompatibel | ✅ Maximal |

**ZenDiS-Gesamtergebnis: 20 von 20 Kriterien erfüllt — maximale Souveränität.**

*Hinweis: Der Kriterienkatalog richtet sich primär an Behörden und öffentliche IT-Infrastrukturen. Vivodepot ist eine Bürgeranwendung; die Kriterien wurden sinngemäß auf die Produktebene übertragen.*

---

## Teil 2 — Weitere Souveränitätsrahmenwerke

### 2.1 BSI IT-Grundschutz++ (seit 2026 gültig)

Das BSI hat das IT-Grundschutz-Kompendium 2026 zur modularen Grundschutz++-Methodik weiterentwickelt. Relevante Aspekte für Vivodepot:

| BSI-Aspekt | Vivodepot-Befund | Bewertung |
|---|---|---|
| Sicherheit in allen Phasen des Software-Lebenszyklus (TR-03185) | Quellcode öffentlich einsehbar; keine externe Build-Pipeline; Sicherheitskonzept dokumentiert in SECURITY.md | ✅ |
| Verschlüsselung nach Stand der Technik | AES-256-GCM + PBKDF2 — entspricht BSI-Empfehlungen für kryptographische Verfahren | ✅ |
| Keine unkontrollierten externen Abhängigkeiten | Alle Bibliotheken inline; keine CDN-Verbindungen im Betrieb | ✅ |
| Datensparsamkeit | Keine Nutzungsdaten, keine Metadaten, keine Telemetrie werden erfasst | ✅ |
| Verfügbarkeit und Notfallbetrieb | Vollständig offline; keine Abhängigkeit von externen Diensten | ✅ |

*Einschränkung: BSI IT-Grundschutz++ gilt formal für Behörden und KRITIS-Betreiber, nicht für Bürgeranwendungen. Die Selbstbewertung ist sinngemäß.*

---

### 2.2 EU Cyber Resilience Act (CRA, ab 2027 verpflichtend)

Der Cyber Resilience Act legt Sicherheitsanforderungen für Produkte mit digitalen Elementen fest.

| CRA-Anforderung | Vivodepot-Befund | Bewertung |
|---|---|---|
| Security by Design | Keine Netzwerkverbindungen, keine Server, keine Angriffsfläche durch Architekturentscheidung | ✅ |
| Transparenz über Sicherheitseigenschaften | SECURITY.md, SOVEREIGNTY.md, Datenschutzhinweise in der App | ✅ |
| Keine bekannten ausnutzbaren Schwachstellen bei Inverkehrbringen | Keine Netzwerkkommunikation → keine Man-in-the-Middle; keine Datenbank → kein SQL-Injection | ✅ |
| Schutz vor unbefugtem Zugriff | AES-256-GCM, PBKDF2, Sitzungsschlüssel nur im RAM | ✅ |
| Open-Source-Ausnahme (Art. 16 CRA) | EUPL-1.2, nicht-kommerziell verfügbar — möglicherweise als Open-Source-Steward einzustufen | ⚠️ Klärungsbedarf |

---

### 2.3 DSGVO (EU) 2016/679 — Privacy by Design

| DSGVO-Grundsatz | Vivodepot-Befund | Bewertung |
|---|---|---|
| Datenminimierung (Art. 5 Abs. 1c) | Keine Erhebung von Metadaten oder Nutzungsstatistiken; nur vom Nutzer explizit eingegebene Daten | ✅ |
| Zweckbindung (Art. 5 Abs. 1b) | Daten werden ausschließlich für den vom Nutzer definierten Zweck gespeichert | ✅ |
| Datensicherheit (Art. 32) | AES-256-GCM; ohne Passwort nicht lesbar | ✅ |
| Privacy by Design (Art. 25) | Keine Serverarchitektur → strukturell keine Datenweitergabe möglich | ✅ |
| Betroffenenrechte (Art. 15–22) | Vollständiger Export, vollständige Löschung jederzeit; kein Account erforderlich | ✅ |
| Keine Drittstaatenübermittlung (Art. 44 ff.) | Keine Datenübermittlung an Server → kein Drittstaatenrisiko | ✅ |

---

### 2.4 EU AI Act (Art. 50) — KI-Transparenzpflicht

Vivodepot wurde unter Einsatz von KI-Werkzeugen (Claude, Anthropic) entwickelt. Die App selbst ist kein KI-System im Sinne des AI Acts, aber die Transparenzpflicht für KI-unterstützte Entwicklung wird vorsorglich eingehalten.

| AI-Act-Aspekt | Vivodepot-Befund | Bewertung |
|---|---|---|
| Kennzeichnung KI-generierter Inhalte (Art. 50) | In App, Code, Dokumentation und allen Veröffentlichungen offengelegt | ✅ |
| Keine KI-Verarbeitung im Betrieb | Keine KI-Modelle, keine Modellaufrufe, kein Cloud-KI-Backend | ✅ |
| Transparenz über Entwicklungsprozess | CONTRIBUTING.md, README.md, KI-Hinweis in SOVEREIGNTY.md | ✅ |

---

### 2.5 OSBA — Open Source Business Alliance (Bundesverband digitale Souveränität)

Die OSBA definiert Open Source und offene Standards als zwingende Grundlage für digitale Souveränität.

| OSBA-Kriterium | Vivodepot-Befund | Bewertung |
|---|---|---|
| Open-Source-Lizenz | EUPL-1.2 — copyleft-kompatibel, europäische Lizenz | ✅ |
| Offene Standards | JSON, vCard, FHIR, PDF/A, OOXML | ✅ |
| Kein Vendor-Lock-in | Keine proprietären Formate, kein Single-Vendor-Ökosystem | ✅ |
| Public Money, Public Code | Förderung durch öffentliche Mittel angestrebt; Code öffentlich auf GitHub | ✅ |

---

### 2.6 Sovereign Tech Agency / EDIC Digital Commons (neu 2025)

Deutschland, Frankreich, Italien und die Niederlande haben 2025 das European Digital Infrastructure Consortium (EDIC) für digitale Gemeingüter gegründet. Vivodepot erfüllt die Grundprinzipien dieses Rahmens:

| EDIC-Kriterium | Vivodepot-Befund | Bewertung |
|---|---|---|
| Open, interoperable, sovereign digital infrastructure | Offene Standards, EUPL-1.2, vollständig offline | ✅ |
| Keine Abhängigkeit von außereuropäischen Hyperscalern | Keine Cloud, kein AWS/Azure/GCP | ✅ |
| Nachhaltigkeit durch Community | GitHub, openCode-Plattform des ZenDiS nutzbar | ✅ |

---

### 2.7 WCAG 2.2 — Kriterium 3.3.8 Zugängliche Authentifizierung (Minimum)

WCAG 2.2 Erfolgskriterium 3.3.8 verlangt, dass Authentifizierungsprozesse keine kognitiven Funktionstests erfordern, die Nutzende benachteiligen könnten. Vivodepot erfüllt dieses Kriterium vollständig durch seine datenschutzkonforme Architektur:

- **kein CAPTCHA**: Vivodepot setzt zu keiner Zeit ein CAPTCHA oder einen vergleichbaren kognitiven Funktionstest ein — weder bei der Passwortvergabe noch beim Entsperren der App.
- **nutzerkontrolliertes Geheimnis**: Die einzige Authentifizierungsform ist ein vom Nutzer selbst gewähltes Passwort (nutzerkontrolliertes Geheimnis). Dieses verlässt das Gerät zu keiner Zeit und wird lokal mit PBKDF2-HMAC-SHA256 zu einem AES-256-GCM-Schlüssel abgeleitet.
- Keine serverseitige Authentifizierung, kein Account, kein Identitätsnachweis gegenüber Dritten erforderlich.

| WCAG-2.2-Kriterium | Anforderung | Vivodepot-Befund | Bewertung |
|---|---|---|---|
| 3.3.8 (AA) | Kein kognitiver Funktionstest bei Authentifizierung | kein CAPTCHA, kein OTP, kein Rätsel | ✅ |
| 3.3.8 (AA) | Ausnahme: nutzerkontrolliertes Geheimnis zulässig | Passwort ist nutzerkontrolliertes Geheimnis | ✅ |

---

## Teil 3 — Welche weiteren Prüfungen wären sinnvoll?

Die folgende Liste zeigt Institutionen und Rahmenwerke, gegen die eine Vivodepot-Prüfung strategisch wertvoll wäre:

| Institution / Rahmenwerk | Relevanz | Priorität |
|---|---|---|
| **ZenDiS Souveränitätscheck** (nach Mai 2026) | Offizieller Check für öffentliche Verwaltung; direktes Einstiegspotenzial in Behörden | Hoch |
| **BSI Cyber-Sicherheitscheck** / BSI-Grundschutz-Zertifizierung | Voraussetzung für viele Beschaffungsprozesse der öffentlichen Hand | Hoch |
| **WCAG 2.2** (W3C, Nachfolger von 2.1) | Barrierefreiheit ist im BFSG (Barrierefreiheitsstärkungsgesetz, gilt ab Juni 2025) gesetzlich verpflichtend für bestimmte Produkte | Hoch |
| **FITKO / FIM-Stammdatenschema** | Verwaltungsinteroperabilität; relevant für Behörden-Einsatz und digitale Behördengänge | Mittel |
| **openCode (ZenDiS-Plattform)** | Registrierung als Open-Source-Lösung für den öffentlichen Sektor; Sichtbarkeit bei Beschaffern | Mittel |
| **Gaia-X / AISBL** | Europäischer Datenraum-Rahmen; relevant wenn Cloud-Hosting ergänzt wird | Niedrig |
| **NIS2-Richtlinie** (umgesetzt als KRITIS-DachG) | Für Betreiber kritischer Infrastrukturen verpflichtend; für Vivodepot als Werkzeug für Privatpersonen nicht direkt relevant, aber als Qualitätsnachweis nützlich | Niedrig |
| **EN 301 549** (Europäische Barrierefreiheitsnorm) | Grundlage des BFSG; technische Norm für barrierefreie IKT-Produkte | Mittel |
| **ISO 27001 / ISO 27701** | Informationssicherheits- und Datenschutz-Managementnorm; international anerkannt | Niedrig |
| **Sovereign Tech Fund** (Deutschland) | Förderung kritischer Open-Source-Infrastruktur; Antrag auf Förderung möglich | Mittel |

---

## Teil 4 — Wettbewerbsvergleich (aktualisiert)

| Kriterium | VIVODEPOT | Afilio | DIPAT | US-Cloud-Dienst | Papier-Ordner |
|---|---|---|---|---|---|
| Datenhoheit | ✅ Vollständig | ⚠️ Teilweise | ⚠️ Teilweise | ❌ Server-seitig | ✅ Vollständig |
| Offline-Fähigkeit | ✅ 100% | ❌ Cloud | ❌ Cloud | ❌ Cloud | ✅ 100% |
| Open Source (EUPL) | ✅ | ❌ | ❌ | ❌ | ✅ (kein Code) |
| Verschlüsselung | ✅ AES-256-GCM | ⚠️ Server-seitig | ⚠️ Server-seitig | ⚠️ Anbieterkontrolle | ✅ (physisch) |
| EU-Jurisdiktion | ✅ DE | ✅ DE | ✅ DE | ❌ USA | ✅ |
| ZenDiS-konform (20 Kriterien) | ✅ 20/20 | ❌ | ❌ | ❌ | n/a |
| FHIR-Export | ✅ | ❌ | ⚠️ | ⚠️ | ❌ |
| Interoperabilität | ✅ 13 Formate | ⚠️ PDF | ⚠️ PDF | ⚠️ Proprietär | ❌ |
| Barrierefreiheit (WCAG 2.1) | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| Kosten | Kostenlos | Abo | Abo | Abo | Material |

---

## Teil 5 — TCO-Vergleich (10 Jahre, 2 Personen)

| Lösung | Kosten |
|---|---|
| VIVODEPOT (Basis) | 0 € |
| Afilio Premium | ca. 720 € |
| Notarielle Vollmacht allein | 150–500 € |
| US-Cloud-Dienst (Abo) | ca. 600–1.200 € |

---

## Methodik & Referenzen

Diese Selbstbewertung orientiert sich an:

- **ZenDiS Diskussionspapier** „Kriterien zur Bewertung von Digitaler Souveränität — aus messbar wird machbar" (März 2026), Konsultation bis 15. Mai 2026
- **BSI IT-Grundschutz++** (2026) und TR-03185 (sichere Software-Entwicklung)
- **EU Cyber Resilience Act** (CRA) — Anforderungen für Produkte mit digitalen Elementen
- **DSGVO** (EU) 2016/679
- **EU AI Act** Art. 50 — KI-Transparenzpflichten
- **EUPL-1.2** Kompatibilitätsprüfung (joinup.ec.europa.eu)
- **WCAG 2.2** (W3C Accessibility Guidelines), insbesondere Kriterium 3.3.8
- **FIM-Stammdatenschema** der FITKO
- **OSBA** — Open Source Business Alliance, Bundesverband digitale Souveränität e.V.
- **EU Cloud Sovereignty Framework** Version 1.2.1 (Oktober 2025)

Vivodepot strebt eine unabhängige Validierung durch das ZenDiS an und möchte am Konsultationsprozess zum Souveränitätscheck (souveränitätscheck.de) teilnehmen.

---

## Kontakt

Vivodepot UG (haftungsbeschränkt) · Berlin
[hilfe@vivodepot.de](mailto:hilfe@vivodepot.de) · [vivodepot.de](https://vivodepot.de)
Quellcode: [github.com/carolaklessen/vivodepot](https://github.com/carolaklessen/vivodepot)
Lizenz: EUPL-1.2

*Dieses Dokument ist öffentlich und darf frei weitergegeben werden.*
