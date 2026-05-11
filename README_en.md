# Vivodepot

A sovereign, offline-capable data layer between citizen and institution.

---

> **Status:** Vivodepot **beta.16** is online with the application-layer functionality — single-file HTML, AES-256-GCM encryption, offline capability, FHIR R4 base, structured forms. **Version 1.0** with care structure, transferable powers of attorney, and a redesigned user flow is in development. This page first describes the architecture as a whole; the quick-start and currently available functions are below under [„Vivodepot today (beta.16)"](#vivodepot-today-beta16).

---

## What this is

Throughout every life, data accumulates that others hold about us — health insurers, doctors, insurers, public authorities, banks, schools, employers. This data describes us, shapes decisions made about us, and outlasts us. We hold theoretical rights to it — access, correction, portability, erasure — but in practice these rights are hard to exercise, because the data is not technically or organizationally in our hands.

Vivodepot is an architecture that changes this. It turns rights into function: a simple, auditable, secure format in which a person can hold their data, receive it from institutions, pass it on to other institutions, and preserve it for future generations — without cloud dependency, without a platform, without trust in third parties.

Vivodepot is not another app. It is a standard layer for citizen-held data vis-à-vis institutions of all kinds.

## What this architecture carries

Vivodepot does not address the abstract problem of an isolated person managing their data. It addresses the problem of people who live in relationships and life trajectories — who must hold and pass on data for themselves, for relatives, for those in their care, in a system that rarely accommodates this reality at the structural level.

Some gaps only reveal themselves at life thresholds — the difficult ones and the welcome. At a marriage, at the birth of a child, at the purchase of a home, at the acceptance of an inheritance. At a difficult diagnosis, in a caregiving situation, at an unplanned hospital admission, in a guardianship case, after a death that leaves behind file boxes of unfamiliar documents. In such moments, what otherwise stays invisible becomes visible: where formal rights end and practical possibility begins, and how wide the gap between them really is.

Ordering one's own life, holding one's own data, passing it on or retrieving it — this is not only protection against the unforeseeable. It is a way of conducting one's own life.

Vivodepot carries these transitions at its core. The relatives mode, the care structure, the transferable powers of attorney are not auxiliary features but a precondition for data sovereignty to actually arrive in the everyday lives of families and life trajectories — and not remain in a concept paper.

## The core idea

A single file. Encrypted. On a storage medium of your choice. In the hands of the person to whom the data belongs.

This file — we call its individual entries Vivos — can hold health records, insurance documents, school certificates, banking documents, tax records, personal notes, contracts, powers of attorney, anything a person accumulates or is given over the course of a life. The file is structured according to open standards (full list in [Open Standards](#open-standards)), encrypted with AES-256-GCM, single-file, designed to function without internet access.

Institutions can read and write Vivodepot files when the person gives them the key. Without the key, they see nothing. With the key, they see only what the person grants.

That is the simple technical core. The hard work is not in the code — it is in the architectural decisions around the core that allow it to become a standard layer at all.

## Architectural principles

Vivodepot rests on six design principles that condition each other. They are not interchangeable — they define what Vivodepot is.

### Sovereignty with the person

Data belongs to the person it describes. Not to the institution that collected it, not to the platform that stores it, not to the vendor who provides the software. Sovereignty is not a feature you can add or omit — it is the precondition of every further decision.

### Single-file rather than distributed systems

A Vivodepot file is a self-contained object — not a database, not a server, not a cloud, not an API as prerequisite. It can sit on a USB stick, in a bank vault, on a private NAS, on encrypted cloud storage of your choice. This makes Vivodepot portable, vendor-independent, and survivable — even if the vendor that built the software no longer exists one day.

### Offline-capable as the default state

Vivodepot works without an internet connection. Synchronization, online features, cloud backups are optional and only ever decryptable with the person's private key. The file itself has no external dependencies. This is not nostalgia — it is resilience against outages, against overreach, against geopolitical change.

### Open standards rather than proprietary formats

Vivodepot invents no data formats. It builds on international specifications that institutions already operate and that remain readable over time. A full list is in [Open Standards](#open-standards).

### Readability for the person

A Vivodepot file must be readable by its holder with reasonable effort — not only through the Vivodepot software, but structurally. A person who, in ten years, wants their data back must be able to retrieve it without the Vivodepot vendor. The specification is open, the code is source-available.

### Compliance as a tool, not an obstacle

Vivodepot is built so that institutions can more easily meet their regulatory obligations — GDPR, EHDS, patient rights legislation, data portability — through Vivodepot, not bear additional burden. This is the bridge over which institutional adoption becomes realistic.

## What Vivodepot is not

Vivodepot is not a cloud solution. It is not a central platform. It is not a login system. It is not an identity wallet in the sense of the EU Digital Identity Wallet — it can coexist with one, imports from one, but does not replace and is not replaced by one. It is not a competitor to institutional databases — institutions continue to hold their own data. It is not a blockchain, not a decentralized database, not a new cryptographic construct.

It is an additional layer between person and institution, in which the person holds their own complete copy of the data relevant to them, securely and under their control.

## Identification and Interoperability

One of the core functions of Vivodepot is citizen-initiated identification: the institution does not pull identity data — the person actively presents it, in a format the institution can read.

### EUDIW integration

Vivodepot imports identity data from the EU Digital Identity Wallet (EUDIW) in SD-JWT format (Selective Disclosure JWT under eIDAS 2.0). This means: officially attested identity data — national ID, registered address, social security number, professional qualifications — can be transferred from the state-issued wallet into the personal depot and used as the basis for identification with institutions. The person chooses at each handover which fields to disclose.

### Identity anchor in health contexts

In the health domain, the FHIR Patient Resource serves as the identity anchor. It holds structured identifiers (health insurance number, hospital patient IDs, physician registration numbers) and is the connecting element between the person and their health data across different providers.

### Relationship coding and powers of attorney

Vivodepot codes relationships according to HL7 V3 RoleCode — the international standard for roles in health and care contexts. Who acts for whom (as authorised representative, as legal guardian, as heir) is thereby documented in a format that institutional systems can read. Powers of attorney are signed with JWS signatures (RFC 7515); the trust authority mechanism secures the authenticity of provider-supplied templates via W3C Verifiable Credentials certificates.

### Output formats for institutions

Institutions receive data in formats directly processable in their systems: FHIR R4 for health providers, FIM-JSON for public authorities, SD-JWT for EUDIW-compatible systems, structured JSON for all others. Integration does not run through an interface to Vivodepot — it runs through what the person actively hands over.

## Open Standards

Vivodepot uses exclusively open, internationally specified standards. No proprietary formats, no vendor lock-in constructs.

| Standard | Specification | Use in Vivodepot |
|---|---|---|
| FHIR R4 | HL7 FHIR Release 4 | Health data structure, export, import, IPS |
| IPS | ISO 27269 / HL7 FHIR | International Patient Summary export |
| SD-JWT | IETF / eIDAS 2.0 | EUDIW import, selective disclosure of identity data |
| eIDAS 2.0 | EU Regulation 910/2014 as amended 2024 | Framework for identifiability and wallet interoperability |
| JWS | RFC 7515 | Power-of-attorney signatures, template transfer mechanism |
| W3C Verifiable Credentials | W3C | Provider certificates (trust authority) |
| HL7 V3 RoleCode | HL7 | Relationship coding (powers of attorney, care, representation) |
| FIM-JSON | FIM standard Germany | Import/export for public authority contexts |
| AES-256-GCM | NIST FIPS 197 / SP 800-38D | Encryption of the depot file |
| PBKDF2-HMAC-SHA256 | NIST SP 800-132 | Key derivation from password |
| vCard | RFC 6350 | Contact export |
| RDF/Turtle | W3C | Solid Pod export |
| WCAG 2.2 | W3C | Accessibility |

Interoperability details and validation evidence: [INTEROPERABILITY.md](INTEROPERABILITY.md).

## What Vivodepot delivers for institutions

Institutions that process personal data face mounting regulatory pressure: GDPR access and erasure obligations, EHDS data portability, patient rights legislation, integration with EU Digital Identity. Meeting these obligations against rising data volumes and shrinking IT budgets is operationally hard.

Vivodepot reduces that load. Rather than building separate interfaces for each compliance requirement, institutions integrate Vivodepot once — and can hand data to the person it concerns, in a format that citizens can take with them, verify, and reuse. This is defensive compliance value: lower litigation risk, easier subject-access fulfilment, cleaner handovers across sector transitions.

## Why now

The regulatory and technical conditions for such a layer have only recently come together in Europe at the same time:

- The European Health Data Space (EHDS) has been in force since 2025 and requires Member States to grant citizens access to their health data in machine-readable form.
- The EU Digital Identity Wallet becomes mandatory from 2026/27 and creates a trusted authentication layer with which Vivodepot can interoperate.
- The Data Governance Act and Data Act have created legal frameworks in which citizen-centric data architectures are, for the first time, clearly placed.
- Structures such as the Sovereign Tech Fund (funding for critical open-source infrastructure) and the Centre for Digital Sovereignty (ZenDiS) with its OpenCode platform have established political and financial foundations for sovereign tech solutions in Germany.
- In Germany specifically, the Vergabebeschleunigungsgesetz (Public Procurement Acceleration Act), passed by the Bundestag on 23 April 2026 — subject to Bundesrat approval on 8 May 2026 and expected to take effect on 1 July 2026 — explicitly establishes digital sovereignty as a permissible qualitative award criterion in public IT procurement. The features named in the law include the use of interoperable and open IT systems, the traceability and control of data processing, data localisation, and legal, organisational, and technical immunity against unwanted access — properties that Vivodepot meets structurally.

Five years ago, Vivodepot would have been an isolated vision. Today, it is a connectable building block within a politically supported corridor.

## Contribution to the United Nations Sustainable Development Goals

Vivodepot is built for European legal contexts, but follows principles that are universally applicable — and addresses societal asymmetries that extend well beyond Germany.

**SDG 16 — Peace, Justice and Strong Institutions**

The primary connection is with Target 16.10: public access to information and protection of fundamental freedoms. The right to informational self-determination — a constitutional right in Germany since the Federal Constitutional Court's landmark ruling in 1983 (BVerfGE 65,1) — is in practice barely exercisable for most people, because their data is technically and organizationally held by institutions, not by the persons it describes. Vivodepot turns this right into an exercisable function: a standard layer through which citizens can hold, verify, and selectively share their data — without cloud dependency, without a platform, without trust in third parties.

**SDG 3 — Good Health and Well-Being**

The health domain is structurally among the most asymmetric: diagnoses, medication plans, care documentation, and advance directives are distributed across practices, hospitals, and insurers — and frequently inaccessible to the patients themselves. Vivodepot maps health data according to open standards (FHIR R4, IPS) and places it in the hands of the person: as a handover file for the emergency ward, as the basis for care home admission, as a long-term store for critical moments.

**SDG 10 — Reduced Inequalities**

Data sovereignty is in practice a matter of resources and digital literacy. Those who are familiar with digital systems, who can afford legal counsel, who face no cognitive or language barriers, can assert their rights more easily. Vivodepot addresses this structurally: through WCAG 2.2-compliant accessibility (touch targets, font scaling, high contrast, screen reader, dictation), through a care structure that technically maps delegated action for relatives and guardians, and through the principle that the software remains permanently free of charge for all individuals.

**Note on geographic scope**

Vivodepot is primarily developed for European legal contexts. The offline-first architecture — no server dependency, no cloud, no login — is however particularly valuable in regions with limited connectivity and in contexts where trust in digital infrastructure cannot be taken for granted. The project is explicitly open to adaptation for other jurisdictions and lived realities; the technical architecture is jurisdiction-independent. Two gaps are named explicitly in the project documentation: the lived realities of people with migration or refugee backgrounds, and the needs of people for whom data sovereignty in one's own hands must first be made possible through accompaniment, representation, or protected spaces.

## Privacy and Data Security

Vivodepot handles personal data structurally differently from server-based applications: data does not leave the device of the person using the application unless they actively release it.

**1. Privacy by Design and Privacy by Default**

Data protection is an architectural founding decision. Encryption happens locally before data is stored. No server receives data, no telemetry is collected, no external scripts are loaded. No cookies, no tracking, no user accounts.

**2. Data Minimization**

No mandatory fields, no minimum data requirement, no data collection by the software itself. Vivodepot stores only what the person actively enters.

**3. Purpose Limitation**

Transfers to institutions happen only through explicit action by the person. Every transfer is selective: the person chooses which fields to share, and when.

**4. Data Subject Rights**

The person using the application is technically the sole holder of their data. All data can be viewed, modified, exported, or fully removed at any time by deleting the file — without request, without waiting, without third-party involvement. Because no data is held by Vivodepot, no data access obligation arises for Vivodepot.

**5. Data Security**

Technical details, key derivation parameters, and security architecture: [SECURITY.md](SECURITY.md). Security vulnerabilities to [security@vivodepot.de](mailto:security@vivodepot.de).

**6. Lifecycle Management**

Open source under EUPL-1.2, complete source code publicly auditable. Privacy-relevant changes documented in [CHANGELOG.md](CHANGELOG.md). Because no user data is held on Vivodepot's servers, data migration, server shutdown, and third-party risks are structurally absent. Post-quantum-capable encryption schemes are planned for a future release.

## Economic approach

Vivodepot is not charitable — it is built to be structurally sustainable, because a data standard layer that is not maintained does not survive in a regulated environment.

The software is free software. Citizens, research institutions, non-profit organisations, and small actors use Vivodepot without license fees. Institutions that integrate Vivodepot into productive business operations — health insurers, insurers, federal states, hospital operators, commercial providers — conclude commercial license agreements that finance further development. After a transition period, each version is automatically converted to a full open-source license.

This construction combines three things that normally do not go together: maximum freedom for the persons whose data is held; sufficient commercial sustainability to maintain the architecture permanently; and a time-delayed open-source commitment that prevents the solution from ever becoming permanently proprietary.

Vivodepot as an application is **Open Source** under EUPL-1.2 — free for all, without restriction. The **template mechanism** (provider-supplied templates, companion schemas, trust authority substance) is licensed under BUSL-1.1 with automatic conversion to EUPL-1.2 after four years; institutional use above 1,000 personal data records requires a commercial license. Details: [LICENSE](LICENSE), [LICENSING.md](LICENSING.md), [vivodepot.de/lizenzierung](https://vivodepot.de/lizenzierung).

## Responsibility

Vivodepot is the responsibility of Carola Klessen. It emerged from decades of experience across different sectors, professionally and personally — and from concrete understanding of the reality this architecture carries. The advisory board is being established, with individuals from digital sovereignty, clinical care, standardisation, and civil society. Names will be published once appointments are concluded.

## Governance structure

Vivodepot is being set up in a form that combines commercial sustainability and long-term independence. Details of the corporate and governance structure will be published here once formally established.

The word mark "Vivodepot" has been applied for at the German Patent and Trade Mark Office, held privately by Carola Klessen. Details on trademark use in [TRADEMARK.md](TRADEMARK.md).

## Contributing

Vivodepot is a young, openly run project. Contributions are welcome — code, documentation, critical reviews, use case scenarios. Guidance on the contribution process and the current development phase is in [CONTRIBUTING.md](CONTRIBUTING.md).

Particularly sought is the adaptation of Vivodepot to other jurisdictions. Data sovereignty is a shared European concern, but the legal frameworks, the structures of powers of attorney and inheritance, the established data standards, and the everyday practices differ from country to country. A version built in Germany does not automatically reflect what is needed in France, in Switzerland, in the United Kingdom, in the Netherlands, or in the Nordic countries. Vivodepot is designed so that nationally sensible versions can emerge — carried by people who know the respective legal context and lived reality.

A second gap that should be named explicitly: the lived reality of people with migration, flight, or naturalization backgrounds. Asylum, toleration status, naturalization, residence permits, recognition of educational and professional qualifications from countries of origin — all of this produces its own, often especially fragmented data reality, in which the asymmetry between person and institution is particularly pronounced and in which trust in digital systems is rightly not self-evident. Vivodepot does not currently address this reality. A meaningful response requires knowledge of residence and asylum law, multilingual capability across the most common languages of immigrant communities, and above all a kind of trust that can only be built in cooperation with established actors in the field. Vivodepot is open to such cooperations.

A third gap concerns people for whom data sovereignty in one's own hands is not a precondition but something that must first be made possible — through accompaniment, through representation, through protected spaces. Those who have no safe place of storage, who depend cognitively or medically on representation, who live in contexts of violence, who cannot act independently because of digital skills gaps — for these life situations, a technical possibility alone is not enough. Vivodepot is open to cooperation with actors who build the accompanying structures — social associations, counselling services, guardianship and care institutions.

Anyone interested in strategic partnership or advisory board participation is invited to reach out directly. Vivodepot is open to co-stewardship on equal footing — by people who can carry the subject because they understand it from their own professional or personal life.

## Contact

- General: [kontakt@vivodepot.de](mailto:kontakt@vivodepot.de)
- Licensing: [lizenz@vivodepot.de](mailto:lizenz@vivodepot.de) · [LICENSE](LICENSE) · [LICENSING.md](LICENSING.md)
- Trademark: [marken@vivodepot.de](mailto:marken@vivodepot.de) · [TRADEMARK.md](TRADEMARK.md)
- Security reports: [security@vivodepot.de](mailto:security@vivodepot.de) · [SECURITY.md](SECURITY.md)
- Web: [vivodepot.de](https://vivodepot.de)
- Code: [github.com/carolaklessen/vivodepot](https://github.com/carolaklessen/vivodepot)

---

## Vivodepot today (beta.16)

While v1 is in development, beta.16 is publicly available. This version already carries part of the architecture above; the rest follows with v1.

### Status table

| Capability | beta.16 (online) | v1 (in development) |
|---|---|---|
| Single-file HTML, AES-256-GCM, offline, FHIR R4 base | ✓ | ✓ |
| Structured forms (personal data, health, contracts, etc.) | ✓ | extended |
| Multi-profile (four profiles in parallel) | ✓ | replaced by care structure |
| QR handover, share file, reading view | ✓ | ✓ |
| Template editor for institutions, FHIR PROM, FIM-JSON, Solid Pod export | ✓ | ✓ |
| Care structure (anchor person + sub-depots for those in care) | — | ✓ |
| Transferable powers of attorney with JWS signature and trust authority | — | ✓ |
| Occasion wizards (hospital, doctor, care grade, banking POA, inheritance) | — | ✓ |
| Routing gate for identity question (only when relatives access is configured) | — | ✓ |
| FHIR-IPS export, relationship coding, provider-supplied templates | partial | ✓ |
| CI/CD hardening with hash substitution, privacy enforcement (GDPR/CSP) | — | ✓ |

### Quick start (beta.16)

1. Download [`VIVODEPOT.html`](VIVODEPOT.html)
2. Open in Chrome or Firefox (double-click is enough)
3. Get started — no installation, no registration

**Online version:** [carolaklessen.github.io/vivodepot/](https://carolaklessen.github.io/vivodepot/)

### Functional scope of beta.16

The application covers 22 steps — personal data, persons of trust, finances, insurance, real estate, contracts and subscriptions, health, well-being and mind (PHQ-9, GAD-7, WHO-5), care, my will (testament & powers of attorney, BGB references 2023), my farewell, mementos, pets, digital legacy, assistants, emergency (BBK recommendations), data exchange (FHIR/FIM/EUDI/QR/Solid Pod), review dates, settings.

Exports: Word, PDF, emergency checklist, doctor's form (several variants), scenario PDFs, power-of-attorney/directive Word documents, vCard, QR stickers, share file (HTML, encrypted), QR handover (AES-256-GCM, PIN-protected, 24-hour validity, multi-part-capable), Solid Pod export (Turtle), FHIR export with PROM scores and GDPR consent.

Imports: EUDI Wallet (SD-JWT), FHIR R4, FIM-JSON, generic JSON.

For institutions (since beta.15/16): Companion-schema-v1.0 questionnaire templates plus an in-app template editor. FHIR-conformant export including a GDPR consent resource.

Accessibility: WCAG 2.2 touch targets (44 px), font-size A+ in three steps, high contrast, night mode, read-aloud, screen magnifier, dictation.

Detailed documentation: [DOCS.md](DOCS.md) · [INTEROPERABILITY.md](INTEROPERABILITY.md) · [QUICKSTART.md](QUICKSTART.md) · [FAQ.md](FAQ.md) · [SOVEREIGNTY.md](SOVEREIGNTY.md) · [CHANGELOG.md](CHANGELOG.md).

### Security in beta.16

| Property | Detail |
|---|---|
| Encryption | AES-256-GCM via Web Crypto API |
| Key derivation | PBKDF2-HMAC-SHA256, 200,000 iterations, cryptographically random salt |
| Salt storage | Embedded in the saved file (since beta.7) — decryptable on any device with the password |
| Share file | Own salt, own password |
| QR handover | Hash-fragment payload never reaches a server, PIN-protected, 24-hour expiry |
| Reading view | No storage, no server, no cookies, no tracking |
| Network requests | None — fully offline |
| Telemetry | None |
| External scripts | None (all libraries inline) |

Security reports: [SECURITY.md](SECURITY.md).

### Tests

```bash
python3 test_vivodepot.py VIVODEPOT.html
```

The tests pass in full. Notes on the test architecture and new test layers: [CONTRIBUTING.md](CONTRIBUTING.md).

---

Vivodepot is architecture — not an application, not a platform, not a cloud. It is the missing layer between citizen and institution: simple enough to work; open enough to outlast; precise enough to become a standard.
