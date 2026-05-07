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

This file — we call its individual entries Vivos — can hold health records, insurance documents, school certificates, banking documents, tax records, personal notes, contracts, powers of attorney, anything a person accumulates or is given over the course of a life. The file is structured according to open standards (FHIR R4 for medical data, additional standards by domain), encrypted with AES-256-GCM, single-file, designed to function without internet access.

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

### Standards rather than proprietary formats

Vivodepot builds on FHIR R4, established cryptographic methods (AES-256-GCM, with post-quantum-capable schemes to follow), common data formats. It invents nothing already well-served by existing work. This makes Vivodepot interoperable with what institutions already operate, and handover-capable for the future.

### Readability for the person

A Vivodepot file must be readable by its holder with reasonable effort — not only through the Vivodepot software, but structurally. A person who, in ten years, wants their data back must be able to retrieve it without the Vivodepot vendor. The specification is open, the code is source-available.

### Compliance as a tool, not an obstacle

Vivodepot is built so that institutions can more easily meet their regulatory obligations — GDPR, EHDS, patient rights legislation, data portability — through Vivodepot, not bear additional burden. This is the bridge over which institutional adoption becomes realistic.

## What Vivodepot is not

Vivodepot is not a cloud solution. It is not a central platform. It is not a login system. It is not an identity wallet in the sense of the EU Digital Identity Wallet (it can coexist with one, but does not replace and is not replaced). It is not a competitor to institutional databases — institutions continue to hold their own data. It is not a blockchain, not a decentralized database, not a new cryptographic construct.

It is an additional layer between person and institution, in which the person holds their own complete copy of the data relevant to them, securely and under their control.

## What Vivodepot delivers for institutions

Institutions that process personal data face mounting regulatory pressure: GDPR access and erasure obligations, EHDS data portability, patient rights legislation, integration with EU Digital Identity. Meeting these obligations against rising data volumes and shrinking IT budgets is operationally hard.

Vivodepot reduces that load. Rather than building separate interfaces for each compliance requirement, institutions integrate Vivodepot once — and can hand data to the person it concerns, in a format that citizens can take with them, verify, and reuse. This is defensive compliance value: lower litigation risk, easier subject-access fulfilment, cleaner handovers across sector transitions.

## Why now

The regulatory and technical conditions for such a layer have only recently come together in Europe at the same time:

- The European Health Data Space (EHDS) has been in force since 2025 and requires Member States to grant citizens access to their health data in machine-readable form.
- The EU Digital Identity Wallet becomes mandatory from 2026/27 and creates a trusted authentication layer with which Vivodepot can interoperate.
- The Data Governance Act and Data Act have created legal frameworks in which citizen-centric data architectures are, for the first time, clearly placed.
- Structures such as the Sovereign Tech Fund (funding for critical open-source infrastructure) and the Centre for Digital Sovereignty (ZenDiS) with its OpenCode platform have established political and financial foundations for sovereign tech solutions in Germany.
- FHIR R4 has become the broadly anchored international standard for medical data in Germany and the EU.
- In Germany specifically, the Vergabebeschleunigungsgesetz (Public Procurement Acceleration Act), passed by the Bundestag on 23 April 2026 — subject to Bundesrat approval on 8 May 2026 and expected to take effect on 1 July 2026 — explicitly establishes digital sovereignty as a permissible qualitative award criterion in public IT procurement. The features named in the law include the use of interoperable and open IT systems, the traceability and control of data processing, data localisation, and legal, organisational, and technical immunity against unwanted access — properties that Vivodepot meets structurally.

Five years ago, Vivodepot would have been an isolated vision. Today, it is a connectable building block within a politically supported corridor.

## Economic approach

Vivodepot is not a charitable project — it is built to be structurally sustainable, because a data standard layer that is not maintained will not survive a regulated environment.

The software is free software. Citizens, research institutions, non-profits, and small actors use Vivodepot without licence fees. Institutions that embed Vivodepot in their productive operations — health insurers, insurers, federal states, hospital operators, commercial providers — enter into commercial licence agreements that fund continued development. After a transition period, every version automatically converts to a fully open-source licence.

This construction combines three things that usually do not go together: maximum freedom for the people whose data is held; sufficient commercial viability to maintain the architecture over time; and a time-shifted open-source promise that ensures the solution never becomes permanently proprietary.

Details on the licensing approach are in [LICENSE](LICENSE), [LICENSING.md](LICENSING.md), and at [vivodepot.de/lizenzierung](https://vivodepot.de/lizenzierung).

## Responsibility

Vivodepot is led by Carola Klessen. It emerged from decades of experience across different sectors, professionally and personally — and from concrete understanding of the reality this architecture carries. The advisory board is being assembled, with figures from digital sovereignty, clinical care, standardisation, and citizen perspective. Names will be published once appointments are confirmed.

## Governance structure

Vivodepot is being set up in a form that combines commercial viability with long-term independence. Details about the corporate and governance structure will be published here as soon as the structure is formally in place.

The word mark „Vivodepot" has been filed for registration with the German Patent and Trade Mark Office (DPMA) and is held privately by Carola Klessen. Details on trademark use in [TRADEMARK.md](TRADEMARK.md).

## Contributing

Vivodepot is a young, openly run project. Contributions are welcome — code, documentation, critical reviews, application scenarios. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution process and the current development phase.

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
