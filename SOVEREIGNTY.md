# 🔒 Vivodepot — Selbstbewertung Digitale Souveränität

**Bewertung nach den Kriterien des Zentrums für Digitale Souveränität (ZenDiS)**

Stand: April 2026 · Version 1.0.0-beta · Vivodepot UG (haftungsbeschränkt)

---

## Zusammenfassung

Vivodepot ist ein persönlicher Vorsorge-Assistent, der als einzelne HTML-Datei lokal im Browser läuft — ohne Server, ohne Cloud, ohne Benutzerkonto. Die Anwendung speichert alle Daten ausschließlich auf dem Gerät des Nutzers, verschlüsselt sie mit AES-256-GCM und exportiert sie bei Bedarf als maschinenlesbares FIM-kompatibles JSON — mit QR-Code auf dem Datenblatt, scanbar durch Verwaltungssysteme.

**Ergebnis: Vivodepot erfüllt alle 8 Kriterien digitaler Souveränität auf höchstem Niveau.**

| Kriterium | Bewertung | Begründung |
|-----------|-----------|------------|
| Datenhoheit | ✅ Maximal | Kein Server. Daten existieren nur auf dem Gerät des Nutzers. |
| Wechselmöglichkeit | ✅ Maximal | 17 Export-Formate inkl. FIM-JSON. Kein Lock-in. |
| Transparenz | ✅ Maximal | Open Source (EUPL-1.2). Vollständig überprüfbarer Quellcode. |
| Herkunft & Jurisdiktion | ✅ Maximal | Deutsches Unternehmen. Keine US-Verbindung. Kein CLOUD Act. |
| Verfügbarkeit | ✅ Maximal | Funktioniert komplett offline. Keine Serverabhängigkeit. |
| Sicherheit | ✅ Maximal | AES-256-GCM. Kein Angriffspunkt, weil kein Server existiert. |
| Interoperabilität | ✅ Maximal | FHIR R4, FIM-JSON, PDF, DOCX, QR-Code, CSV, vCard. |
| Barrierefreiheit | ✅ Hoch | 10 Features: Vorlesen, Kontrast, Lupe, Nachtmodus, Spracheingabe. |

---

## 1. Datenhoheit

> *„Wer hat Zugriff auf die Daten des Nutzers?"*

**Bewertung: ✅ Maximal — ausschließlich der Nutzer selbst.**

Vivodepot speichert keine Daten auf einem Server. Es gibt keinen Server. Die Anwendung ist eine einzelne HTML-Datei (~450 KB), die lokal im Browser ausgeführt wird. Alle Nutzerdaten werden im localStorage des Browsers oder in der heruntergeladenen HTML-Datei gespeichert.

- Kein Benutzerkonto, keine Registrierung, keine E-Mail erforderlich
- Kein Tracking, keine Cookies, kein Google Analytics, keine Telemetrie
- Kein Anbieter — auch nicht Vivodepot — kann auf die Daten zugreifen
- Software funktioniert weiter, selbst wenn Vivodepot als Unternehmen nicht mehr existiert

---

## 2. Wechselmöglichkeit (kein Vendor Lock-in)

> *„Kann der Nutzer jederzeit seine Daten mitnehmen?"*

**Bewertung: ✅ Maximal — vollständige Datenportabilität in 17 Formaten.**

| Format | Beschreibung |
|--------|-------------|
| JSON | Alle Daten als strukturierte Datei — maschinenlesbar |
| FIM-JSON | Behördendaten nach FIM-Stammdatenschema — für Verwaltungsportale |
| HTML | Selbsttragende Datei mit eingebetteten Daten |
| PDF | Druckbares Gesamtdokument |
| DOCX (Word) | Bearbeitbares Dokument |
| FHIR R4 JSON | Internationaler Medizindaten-Standard (HL7) |
| CSV / vCard | Kontaktdaten-Import und -Export |
| QR-Code (Notfall) | Notfall-Informationen als scannbarer Code |
| QR-Code (Behörden) | Kerndaten als maschinenlesbares JSON auf Behördendatenblättern |
| Kindergeld-PDF | Datenblatt für die Familienkasse mit QR-Code |
| Arbeitsamt-PDF | Stammdaten für ALG-Antrag mit QR-Code |
| Pflegegrad-PDF | Gesundheitsdaten für die Pflegekasse mit QR-Code |

---

## 3. Transparenz

> *„Ist der Quellcode überprüfbar?"*

**Bewertung: ✅ Maximal — vollständig Open Source.**

- **Lizenz:** EUPL-1.2 (European Union Public Licence)
- **Quellcode:** Öffentlich auf [GitHub](https://github.com/carolaklessen/vivodepot)
- **Architektur:** Einzelne HTML-Datei, keine versteckten Abhängigkeiten
- **KI-Transparenz:** Konform mit EU AI Act Art. 50 — Entwicklung mit KI-Unterstützung dokumentiert
- **Externe Bibliotheken:** 3 Open-Source-Bibliotheken (jsPDF, docx, QRCode.js), alle MIT-lizenziert

Die EUPL-1.2 ist die einzige von der EU-Kommission herausgegebene, OSI-zertifizierte Open-Source-Lizenz. Sie ist in allen 23 EU-Amtssprachen rechtsverbindlich.

---

## 4. Herkunft & Jurisdiktion

> *„Unterliegt der Anbieter außereuropäischen Zugriffsgesetzen?"*

**Bewertung: ✅ Maximal — rein deutsches Unternehmen, keine US-Verbindung.**

| Prüfpunkt | Status |
|-----------|--------|
| Firmensitz | Deutschland |
| Rechtsform | UG (haftungsbeschränkt) nach deutschem Recht |
| US-Muttergesellschaft | Keine |
| US-Tochtergesellschaft | Keine |
| US-Investoren | Keine |
| Unterliegt dem CLOUD Act | **Nein** |
| Unterliegt FISA 702 | **Nein** |
| Server in den USA | **Es gibt keine Server** |

---

## 5. Verfügbarkeit & Resilienz

> *„Funktioniert die Anwendung auch bei Ausfall externer Dienste?"*

**Bewertung: ✅ Maximal — funktioniert komplett offline.**

| Szenario | Cloud-Anbieter | Vivodepot |
|----------|---------------|-----------|
| Internet-Ausfall | ❌ Kein Zugriff | ✅ Funktioniert |
| Server-Hack | ❌ Daten gefährdet | ✅ Kein Server vorhanden |
| Anbieter insolvent | ❌ Daten ggf. verloren | ✅ Software läuft weiter |
| CLOUD-Act-Anfrage | ⚠️ Herausgabepflicht | ✅ Nicht betroffen |

---

## 6. Sicherheit & Verschlüsselung

> *„Wie werden die Daten geschützt?"*

**Bewertung: ✅ Maximal — AES-256-GCM, kein Angriffspunkt.**

| Merkmal | Implementierung |
|---------|----------------|
| Verschlüsselung | AES-256-GCM (Web Crypto API) |
| Schlüsselableitung | PBKDF2, 100.000 Iterationen |
| Angriffsfläche | **Null** — kein Server, kein Netzwerk |
| Brute-Force-Schutz | 5 Versuche, dann gesperrt |
| Notfall-Zugriff | 6 Felder unverschlüsselt (wie iPhone ICE) |
| Passwort-Reset | **Nicht möglich** — by design |

---

## 7. Interoperabilität & Offene Standards

> *„Verwendet die Anwendung offene Standards?"*

**Bewertung: ✅ Maximal — inkl. FIM-kompatibler Verwaltungsbrücke.**

| Standard | Verwendung |
|----------|-----------|
| HTML5 | Anwendungsformat |
| JSON | Datenexport |
| FIM-JSON | Behördendaten (FITKO-Stammdatenschema) |
| PDF (ISO 32000) | Dokumentenexport |
| OOXML (ISO 29500) | Word-Export |
| FHIR R4 (HL7) | Medizindaten |
| vCard (RFC 6350) | Kontakte |
| QR-Code (ISO 18004) | Notfall- und Behördendaten |
| AES-256-GCM (NIST) | Verschlüsselung |
| EUPL-1.2 | Lizenz |

### FIM-JSON-Export (BürgerFIM)

Vivodepot exportiert Stammdaten als maschinenlesbares JSON mit 12 Kategorien:

```
natuerlichePerson    → Familienname, Vorname, Geburtsdatum, Familienstand
identifikation       → Steuer-ID, RV-Nr., Personalausweis, BundID
bankverbindung       → IBAN, BIC, Kreditinstitut, Kontoinhaber
krankenversicherung  → Art, Versichertennr., versichert über
familie              → Ehepartner, Kinder, Sorgerecht, Unterhalt
gesundheit           → Blutgruppe, Allergien, Erkrankungen, Medikamente
wohnsituation        → Wohnungstyp, Miete, Vermieter
beschaeftigung       → Arbeitgeber, Beruf
anschrift            → Straße, PLZ/Ort
kommunikation        → Telefon, Mobil, E-Mail
notfallkontakte      → Name, Telefon, Beziehung
_meta                → Version, Exportdatum, Formathinweis
```

### QR-Codes auf Behördendatenblättern

Die PDFs für Kindergeld, Arbeitsamt und Pflegegrad enthalten einen QR-Code mit Kerndaten als kompaktes JSON. Drei Nutzungsszenarien:

1. **Heute:** Bürger druckt PDF, bringt es mit. Sachbearbeiter hat alles auf einer Seite.
2. **Morgen:** Sachbearbeiter scannt QR → JSON wird ins Fachverfahren importiert.
3. **Langfristig:** Verwaltungsportal bietet „QR hochladen" → Formular automatisch vorgefüllt.

---

## 8. Barrierefreiheit

> *„Ist die Anwendung für alle Menschen zugänglich?"*

**Bewertung: ✅ Hoch — 10 Features + Einstiegs-Wizard.**

| Feature | Beschreibung |
|---------|-------------|
| Schriftgröße (A⁺) | 3 Stufen, persistent |
| Vorlesen (🔊) | Web Speech API, deutsche Stimme |
| Hoher Kontrast (◐) | Erhöhter Kontrast |
| Nachtmodus (🌙) | Dunkler Hintergrund |
| Bildschirmlupe (🔍) | 100% / 150% / 200% |
| Spracheingabe (🎤) | Diktieren statt tippen |
| Globale Suche (🔎) | Durchsucht alle Felder |
| Notfall-Button (🚨) | Ohne Passwort zugänglich |
| Einstiegs-Wizard (🎯) | Fokus-Modus reduziert Komplexität |
| Alt-Texte | Alle Bilder mit Beschreibung |

---

## Vergleich mit Wettbewerbern

| Kriterium | Vivodepot | Afilio | DIPAT | Papier-Ordner |
|-----------|-----------|--------|-------|---------------|
| Daten beim Nutzer | ✅ Nur lokal | ❌ Server | ❌ Server | ✅ Physisch |
| Kein CLOUD Act | ✅ | ⚠️ Unklar | ⚠️ Unklar | ✅ |
| Open Source | ✅ EUPL-1.2 | ❌ | ❌ | — |
| Offline-fähig | ✅ Komplett | ❌ | ❌ | ✅ |
| Kein Abo | ✅ Einmalig | ❌ 29-72€/J. | ❌ 30€/J. | ✅ |
| AES-256 lokal | ✅ | ⚠️ TLS | ⚠️ TLS | ❌ |
| FHIR R4 | ✅ | ❌ | ❌ | ❌ |
| FIM-JSON | ✅ | ❌ | ❌ | ❌ |
| QR-Code Behörden | ✅ | ❌ | ❌ | ❌ |
| Aktualisierbar | ✅ | ✅ | ✅ | ❌ |

### TCO (Total Cost of Ownership) — 2 Personen, 10 Jahre

| | Vivodepot (Duo) | Afilio (Familie) | DIPAT (2 Pers.) | Papier-Ordner |
|--|----------------|-----------------|----------------|---------------|
| Kosten | **79 €** | 720 € | 600 € | ~50 € |
| Ersparnis vs. Afilio | **641 €** | — | 120 € | 670 € |
| Offline | ✅ | ❌ | ❌ | ✅ |
| Maschinenlesbar | ✅ | ⚠️ | ⚠️ | ❌ |

---

## Methodik

Diese Selbstbewertung orientiert sich an:

- **ZenDiS-Kriterienkatalog** „Kriterien zur Bewertung von Digitaler Souveränität — aus messbar wird machbar" (2025)
- **Souveränitätscheck der Stadt München** (IT-Referat, TU München, 2025)
- **Bitkom-Bericht** „Digitale Souveränität 2025"
- **adesso Index Digitale Souveränität** (2025)
- **FIM-Stammdatenschema** der FITKO (Föderale IT-Kooperation)

Die Bewertung wurde intern durchgeführt. Vivodepot strebt eine unabhängige Validierung durch das ZenDiS an und möchte am Konsultationsprozess zum Souveränitätscheck teilnehmen.

---

## Kontakt

Vivodepot UG (haftungsbeschränkt)
E-Mail: feedback@vivodepot.de
Website: vivodepot.de
Quellcode: github.com/carolaklessen/vivodepot
Lizenz: EUPL-1.2

*Dieses Dokument ist öffentlich und darf frei weitergegeben werden.*
