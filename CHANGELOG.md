# VIVODEPOT — Änderungsprotokoll

Alle wichtigen Änderungen werden in dieser Datei dokumentiert.

---

## [1.0.0-beta.9] — April 2026

### Neu

- **ANF-05 Solid Pod Export** — Export persönlicher Daten in einen Solid Pod im Turtle-Format (.ttl). Das Modal sp-overlay führt durch die Auswahl der Datenkategorien (Persönliche Angaben, Gesundheit, Finanzen, Vollmachten). Die Exportdatei folgt dem Linked-Data-Standard mit den Präfixen vcard: und schema:. EUPL-konform, vollständig offline.

  Neue Funktionen: solidPodOpen(), solidPodClose(), solidPodExport(), solidPodZeigStatus(), solidPodEsc().

- **Datenaustausch-Step** — Neuer Navigationsschritt „Datenaustausch" (zwischen Dokumente erstellen und Erinnerungen). Bündelt alle Import- und Export-Wege an einem Ort: FHIR-Import, FIM-Import, JSON-Import, EUDI-Wallet, Weitergabe-Datei, QR-Übergabe, QR-Empfang, Solid Pod. Import-Block aus dem Behördendaten-Tab und wg-Link-Zeilen aus dem Export-Tab wurden dorthin verschoben.

- **Strukturumstellung Sidebar** — 21 Schritte (bisher 20). Neue Sidebar-Gruppen: „Gesundheit & Abschluss" und „Besonderes". Alte Gruppen „Gesundheit & Leben" und „Persönliches & Wünsche" entfernt. Neue Schrittfolge endet mit: ... dokumente → datenaustausch → erinnerung → exportStep → einstellungen.

### Verbessert

- **Code-Optimierung** — Toter Code und Leerraum entfernt:
  - `_loadScript()` entfernt (CDN-Fallback, nie aufgerufen, −6 Zeilen)
  - `console.warn` für docx entfernt (−1 Zeile)
  - Leerkommentar `DATENSCHUTZ-MODAL` entfernt (−4 Zeilen)
  - Whitespace in Wizard-Overlays und Export-Tab bereinigt (−4 Zeilen)
  - `solidPodBaueVcard()` entfernt — toter Code mit Tippfehler (`zeilan.push` statt `zeilen.push`), der beim ersten Aufruf mit E-Mail-Adresse sofort gecrasht wäre (−11 Zeilen)
  - Gesamt: −26 Zeilen (22.157 → 22.131 Zeilen)

- **Test-Duplikate bereinigt** — 45 redundante Tests entfernt (Kopien aus den Sektionen 16, 19, 22, 31 und 33, die in späteren Sektionen doppelt geprüft wurden). Abdeckung bleibt identisch.

### Tests

- 43 neue Tests: ANF-05 Solid Pod (12), Datenaustausch-Step (11), Strukturumstellung (13), sonstige (7)
- 45 Duplikat-Tests entfernt
- Gesamt: 1093 Tests, 0 Fehler (vorher: 1050)

---

## [1.0.0-beta.8] — April 2026

### Neu

- **Weitergabe-Datei** — Eigenständige, verschlüsselte HTML-Datei mit gefiltertem Datensatz für Dritte. Vier Profile: Notfall, Vollmacht, Familie, Behörde. Behörden-Profil mit Dropdown (9 Optionen). Eigener Salt und eigenes Passwort — vollständig unabhängig vom Hauptpasswort. Reminder nach 12 Monaten.

- **QR-Übergabe (ANF-06)** — Drei Schritte: Auswahldialog mit PIN, AES-256-GCM-Verschlüsselung mit Zeitstempel iat und Ablauf exp (24 Stunden), Empfänger-Dialog mit jsQR v1.4.0 (256 KB, inline) und Kamerascan.

- **ANF-01 Einkommensdaten** — Felder brutto_monat, netto_monat, arbeitgeber, beruf_hauptberuf, letzter_arbeitgeber. PDF-Export: Elterngeld-Bogen.

- **ANF-02 Kind-Daten strukturiert** — renderKinderBlocks(), 5 Felder pro Kind, FIM-Export kinderListe. kinderMinderjaehrig (Legacy) unverändert erhalten.

- **ANF-03 EUDI-Wallet-Import** — SD-JWT-Import, 8 Felder gemappt.

- **ANF-04 FHIR-Import** — 6 Ressourcentypen: AllergyIntolerance, Condition (ICD-10), MedicationStatement, Observation (LOINC 8480-6), Immunization, CarePlan.

### Behoben

- BUG-05: wg-overlay und qre-overlay in showOverlay() und hideAllOverlays() eingetragen. Overlay-Limit auf 12 angehoben.

### Tests

- 208 neue Tests gegenüber beta.7
- Gesamt: 1050 Tests, 0 Fehler

---

## [1.0.0-beta.7] — April 2026

### Behoben

- **BUG-SALT** — `saveAsHTML()` bettet den Salt direkt in die gespeicherte HTML-Datei ein. Beim Öffnen auf einem anderen Gerät wird er idempotent wiederhergestellt.

### Dokumentation

- SOVEREIGNTY.md: ZenDiS-Diskussionspapier März 2026, BSI IT-Grundschutz++, EU Cyber Resilience Act

### Tests

- 4 neue Tests: BUG-SALT-01a bis BUG-SALT-02
- Gesamt: 842 Tests, 0 Fehler

---

## [1.0.0-beta.6] — April 2026

### Neu

- Offline-Vollständigkeit: Alle Bibliotheken inline eingebettet
- Notfall & Katastrophenschutz: 6 Ampelkarten, Evakuierungsplan, Notrufblatt-PDF
- Barrierefreiheit im Menü direkt erreichbar
- iOS-Speicher-Anleitung und .htm-Endung (PocketBook-Workaround)

### Behoben

- BUG-10: vCard-Code lag außerhalb `<script>`-Tags
- BUG-11: `mehr()`-Funktion mit falschem Argument-Typ

---

## [1.0.0-beta.5] — März 2026

Fokus-System, Einstiegs-Wizard, Multi-Profil-Unterstützung, Angehörigen-Ansicht, Diktat-Eingabe, Gesundheitsvollmacht-Wizard, Notfall-Tasche Szenario-PDF.

---

## [1.0.0-beta.4] — Februar 2026

Weiche beim Öffnen (Inhaberin / Angehörige/r), 20 Schritte, Einstellungen als eigener Schritt.

---

## [1.0.0-beta.3] — Januar 2026

AES-256-GCM Verschlüsselung, `saveAsHTML()`, vCard 4.0, FHIR R4, QR-Code Aufkleber, Arztbogen PDF, Vorsorgevollmacht Word, Vorlesen, Hoher Kontrast, Nachtmodus.

---

## [1.0.0-beta.1] — Dezember 2025

Erste Version — vollständige Notfallmappe als PDF und Word, 17 Dateneingabe-Schritte.
