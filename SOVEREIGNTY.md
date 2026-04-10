# VIVODEPOT — Souveränitätsprüfung

**Selbstbewertung nach den Kriterien des ZenDiS (Zentrum für Digitale Souveränität)**
*Version 1.0.0-beta.6 · April 2026*

---

## Zusammenfassung

VIVODEPOT erfüllt alle 8 Souveränitätskriterien des ZenDiS auf maximalem oder hohem Niveau. Das Produkt wurde von Grund auf mit dem Ziel entwickelt, vollständige digitale Souveränität für Bürgerinnen und Bürger zu gewährleisten.

| Kriterium | Bewertung | Kurzfazit |
|---|---|---|
| 1. Datenhoheit | ✅ Maximal | 100% lokale Speicherung, AES-256-GCM |
| 2. Wechselmöglichkeit | ✅ Maximal | JSON-Export, HTML-Export, kein Lock-in |
| 3. Transparenz | ✅ Maximal | EUPL-1.2, quelloffen, KI-Transparenz |
| 4. Jurisdiktion | ✅ Hoch | Deutsches Recht, EU-Datenschutz |
| 5. Verfügbarkeit | ✅ Maximal | Vollständig offline, keine Abhängigkeiten |
| 6. Sicherheit | ✅ Maximal | AES-256-GCM, PBKDF2, kein Netzwerk |
| 7. Interoperabilität | ✅ Hoch | JSON, vCard, PDF, DOCX, FHIR R4 |
| 8. Barrierefreiheit | ✅ Hoch | WCAG 2.1, Vorlesen, Kontrast, Lupe |

---

## 1. Datenhoheit

**Bewertung: ✅ Maximal**

**Prüffrage:** Wer kontrolliert die Daten des Nutzers?

**Befund:** Die nutzende Person hat vollständige und ausschließliche Kontrolle über ihre Daten.

- Alle Daten werden ausschließlich im `localStorage` des lokalen Browsers gespeichert
- Kein Server, keine Cloud, keine Datenbank empfängt jemals Nutzerdaten
- Keine Telemetrie, kein Analytics, keine Nutzungsstatistiken
- Die gespeicherte HTML-Datei ist eine vollständige Kopie aller Daten — keine Abhängigkeit von externen Diensten
- AES-256-GCM Verschlüsselung mit PBKDF2-Schlüsselableitung (100.000 Iterationen)
- Ohne das Passwort des Nutzers sind gespeicherte Daten nicht lesbar — auch nicht für Vivodepot

---

## 2. Wechselmöglichkeit (Portabilität)

**Bewertung: ✅ Maximal**

**Prüffrage:** Kann der Nutzer seine Daten jederzeit mitnehmen und zu einer anderen Lösung wechseln?

**Befund:** Vollständige Portabilität ohne Hürden.

**Export-Formate (13 Stück):**
- HTML-Datei (vollständige App mit eingebetteten Daten)
- JSON (maschinenlesbarer Rohdaten-Export)
- PDF (Notfallmappe, druckfertig)
- Word DOCX (bearbeitbar)
- Notfall-Blatt PDF
- Arztbogen PDF
- Szenario-PDFs (Krankenhaus, Todesfall, Notfall-Tasche)
- Vorsorgevollmacht DOCX
- Patientenverfügung DOCX
- Gesundheitsvollmacht DOCX
- QR-Aufkleber PDF
- vCard 4.0 (Kontaktexport)
- FHIR R4 JSON (Gesundheitsdaten, HL7-Standard)

Kein proprietäres Format, kein Export-Limit, kein Account erforderlich.

---

## 3. Transparenz

**Bewertung: ✅ Maximal**

**Prüffrage:** Ist das Produkt transparent hinsichtlich Funktionsweise, Quellcode und KI-Einsatz?

**Befund:** Vollständige Transparenz auf allen Ebenen.

- **Quelloffenheit:** EUPL-1.2 (Europäische Union Public Licence) — copyleft-kompatibel mit GPL und AGPL
- **Quellcode:** Vollständig einsehbar auf GitHub ([github.com/carolaklessen/vivodepot](https://github.com/carolaklessen/vivodepot))
- **Einzeldatei:** Der gesamte Quellcode ist in einer einzigen HTML-Datei — keine Build-Pipeline, kein versteckter Code
- **KI-Transparenz:** Entwickelt mit KI-Unterstützung (Claude, Anthropic) gemäß EU AI Act Art. 50 — in der App, im Code und in allen Dokumenten offengelegt
- **Bibliotheken:** Alle verwendeten Drittbibliotheken sind inline eingebettet und in ihrer Herkunft dokumentiert (jsPDF, docx.js, QR-Code-Generator)
- **Keine versteckten Funktionen:** Kein Tracking, kein Analytics, keine Werbung

---

## 4. Jurisdiktion

**Bewertung: ✅ Hoch**

**Prüffrage:** Welchem Recht unterliegt das Produkt? Gibt es Risiken durch außereuropäische Jurisdiction?

**Befund:** Deutsches Recht, kein US-Cloud-Risiko.

- Betreiber: Vivodepot UG (haftungsbeschränkt), Berlin — deutsches Gesellschaftsrecht
- Keine Datenübermittlung an Dritte → keine Drittstaaten-Jurisdiktion
- Keine US-Cloud-Dienste (kein AWS, Azure, Google Cloud)
- Keine Verarbeitung personenbezogener Daten auf Servern → DSGVO-Konformität strukturell gewährleistet
- Lizenz: EUPL-1.2 (europäische Open-Source-Lizenz, entwickelt für EU-Institutionen)
- Rechtliche Hinweise, Impressum und Datenschutzerklärung: vivodepot.de

*Einschränkung: Die zugrundeliegenden KI-Entwicklungswerkzeuge (Anthropic/Claude) sind US-amerikanisch. Der KI-Einsatz erfolgte ausschließlich während der Entwicklung — nicht im Betrieb der App.*

---

## 5. Verfügbarkeit & Betriebskontinuität

**Bewertung: ✅ Maximal**

**Prüffrage:** Ist das Produkt unabhängig von externen Diensten verfügbar?

**Befund:** Vollständige Offline-Fähigkeit — keine einzige externe Abhängigkeit im Betrieb.

- Alle Bibliotheken sind inline eingebettet (jsPDF 364 KB, docx.js 368 KB, QR-Code 20 KB)
- Keine Google Fonts — Systemschriften (Georgia, -apple-system) werden verwendet
- Keine CDN-Anfragen beim Öffnen oder Nutzen der App
- Keine API-Calls, keine Webhooks, keine Websockets
- Funktioniert im Flugmodus, auf USB-Sticks, auf Offline-Computern
- Service Worker für Browser-Cache (bei GitHub Pages Hosting)
- Kein Single Point of Failure: Wenn GitHub offline ist, funktionieren alle gespeicherten Kopien weiterhin

**Getestete Umgebungen:** Chrome, Firefox, Edge, Safari (Desktop + Mobile), DuckDuckGo (eingeschränkt)

---

## 6. Sicherheit

**Bewertung: ✅ Maximal**

**Prüffrage:** Wie ist das Produkt gegen Datenverlust und unbefugten Zugriff gesichert?

**Befund:** State-of-the-art Verschlüsselung, keine Angriffsfläche durch externe Verbindungen.

**Verschlüsselung:**
- Algorithmus: AES-256-GCM (authentifizierte Verschlüsselung)
- Schlüsselableitung: PBKDF2-HMAC-SHA256 mit 100.000 Iterationen und zufälligem Salt
- Implementierung: Web Crypto API (Browser-natives Krypto, keine externe Bibliothek)
- Kein Schlüssel verlässt das Gerät

**Angriffsfläche:**
- Keine Netzwerkkommunikation = keine Man-in-the-Middle-Angriffe
- Keine Server = kein Server-Hack
- Keine Datenbank = kein SQL-Injection
- Keine externe Skripte = kein Supply-Chain-Angriff
- Content Security Policy implementiert

**Passwortschutz:**
- Bis zu 5 Fehlversuche, dann Sperrung
- Kein Passwort-Reset (by design — nur der Nutzer kennt das Passwort)

---

## 7. Interoperabilität

**Bewertung: ✅ Hoch**

**Prüffrage:** Kann das Produkt mit anderen Systemen und Standards zusammenarbeiten?

**Befund:** Offene Standards, mehrere Importformate, Verwaltungsanbindung vorbereitet.

**Offene Exportstandards:**
- JSON (RFC 8259) — universell maschinenlesbar
- PDF/A — langzeitarchivierungsfähig
- OOXML (DOCX, ISO/IEC 29500) — Microsoft-kompatibel
- vCard 4.0 (RFC 6350) — Kontaktstandard
- FHIR R4 (HL7) — internationaler Gesundheitsdatenstandard

**Verwaltungsanbindung (vorbereitet):**
- BundID-Felder für digitale Behördengänge
- ELEFAND-Felder (Krisenvorsorgeliste Auswärtiges Amt)
- Strukturierte Behördendaten-Exporte (Kindergeld, Rentenversicherung, Pflegegrad)
- QR-Code-Export für institutionellen Einsatz

**Import:**
- JSON-Import (VIVODEPOT-Daten)
- HTML-Import (gespeicherte VIVODEPOT-Dateien)
- vCard-Import (Kontakte)
- CSV-Import (Kontaktlisten)

---

## 8. Barrierefreiheit

**Bewertung: ✅ Hoch**

**Prüffrage:** Ist das Produkt für Menschen mit Einschränkungen nutzbar?

**Befund:** Umfangreiche Barrierefreiheitsfunktionen implementiert — besonders für ältere Nutzende.

**Implementierte Funktionen:**
- **Schriftgröße:** 3 Stufen (normal, mittel, groß) — über Menü und Topbar
- **Hoher Kontrast:** CSS-Klasse mit verstärkten Farb- und Kontrastwerten
- **Nachtmodus:** Dunkles Farbschema für Augenschonung
- **Vorlesen:** Web Speech API — Seiteninhalte werden vorgelesen
- **Bildschirmlupe:** Vergrößerungs-Overlay für kleine Bildschirme
- **Diktat-Eingabe:** Sprach-zu-Text für Formulareingaben
- **Touch-Targets:** Mindestgröße 44×44px (WCAG 2.1 Erfolgskriterium 2.5.5)
- **ARIA-Labels:** Auf allen interaktiven Elementen
- **Fokus-Modus:** Zielgeführte Navigation (Notfall, Familie, Vorsorge)
- **Einstiegs-Wizard:** Schritt-für-Schritt-Führung beim ersten Start
- **Tastaturnavigation:** Vollständig bedienbar ohne Maus

**Sprachen:** Deutsch (primär), Englisch (experimentell)

---

## Wettbewerbsvergleich

| Kriterium | VIVODEPOT | Afilio | DIPAT | US-Cloud-Dienst | Papier-Ordner |
|---|---|---|---|---|---|
| Datenhoheit | ✅ Vollständig | ⚠️ Teilweise | ⚠️ Teilweise | ❌ Server-seitig | ✅ Vollständig |
| Offline-Fähigkeit | ✅ 100% | ❌ Cloud-abhängig | ❌ Cloud-abhängig | ❌ Cloud-abhängig | ✅ 100% |
| Open Source | ✅ EUPL-1.2 | ❌ Proprietär | ❌ Proprietär | ❌ Proprietär | ✅ (kein Code) |
| Verschlüsselung | ✅ AES-256-GCM | ⚠️ Server-seitig | ⚠️ Server-seitig | ⚠️ Anbieterkontrolle | ✅ (physisch) |
| EU-Jurisdiktion | ✅ DE | ✅ DE | ✅ DE | ❌ USA | ✅ |
| FHIR-Export | ✅ | ❌ | ⚠️ | ⚠️ | ❌ |
| Interoperabilität | ✅ 13 Formate | ⚠️ PDF | ⚠️ PDF | ⚠️ Proprietär | ❌ |
| Barrierefreiheit | ✅ WCAG 2.1 | ⚠️ Eingeschränkt | ⚠️ Eingeschränkt | ⚠️ Variiert | ❌ |
| Kosten | Kostenlos | Abo | Abo | Abo | Material |

---

## TCO-Vergleich (10 Jahre, 2 Personen)

| Lösung | Kosten |
|---|---|
| VIVODEPOT (Basis) | 0 € |
| Afilio Premium | ca. 720 € |
| Notarielle Vollmacht allein | 150–500 € |
| US-Cloud-Dienst (Abo) | ca. 600–1.200 € |

---

## Methodik & Referenzen

Diese Selbstbewertung orientiert sich an:
- ZenDiS Souveränitätskriterien für digitale Produkte
- BSI IT-Grundschutz (BSI-Standard 200-1)
- DSGVO (EU) 2016/679
- EUPL-1.2 Kompatibilitätsprüfung (joinup.ec.europa.eu)
- WCAG 2.1 (W3C Accessibility Guidelines)
- FIM-Stammdatenschema der FITKO

Vivodepot strebt eine unabhängige Validierung durch das ZenDiS an und möchte am Konsultationsprozess zum Souveränitätscheck teilnehmen.

---

## Kontakt

Vivodepot UG (haftungsbeschränkt) · Berlin
[feedback@vivodepot.de](mailto:feedback@vivodepot.de) · [vivodepot.de](https://vivodepot.de)
Quellcode: [github.com/carolaklessen/vivodepot](https://github.com/carolaklessen/vivodepot)
Lizenz: EUPL-1.2

*Dieses Dokument ist öffentlich und darf frei weitergegeben werden.*
