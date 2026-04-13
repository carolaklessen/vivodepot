# VIVODEPOT — Änderungsprotokoll

Alle wichtigen Änderungen werden in dieser Datei dokumentiert.

---

## [1.0.0-beta.8] — April 2026

### Neu

- **Weitergabe-Datei** — Nutzer können eine zweite, verschlüsselte HTML-Datei erstellen und an Dritte weitergeben: Angehörige, Ärzte, Notarinnen oder Behörden. Die Empfängerin öffnet die Datei im Browser, gibt ein separates Passwort ein und sieht ausschliesslich die Felder des gewählten Profils. Kein Server, keine Cloud, vollständig offline.

  Vier Profile stehen zur Wahl:

  | Profil | Enthaltene Felder | Typische Empfängerin |
  |---|---|---|
  | Notfall | Medikamente, Allergien, Blutgruppe, Hausarzt, Notfallkontakte, Patientenverfügung (Ablageort) | Krankenhaus, Rettungsdienst |
  | Vollmacht | Bevollmächtigte Person, Ablageorte, Patientenverfügung, Betreuer, Nachlassgericht | Notar, Sozialdienst |
  | Familie | Konten, Versicherungen, Verträge, Testament, Bestattungswunsch, persönliche Botschaft | Angehörige, Erben |
  | Behörde | Stammdaten, Steuer-ID, IBAN, KV-Nr., RV-Nr. | Ämter, Kassen, Rentenversicherung |

  Das Behörden-Profil enthält zusätzlich ein Dropdown mit 9 Optionen (Familienkasse, Elterngeldstelle, Pflegekasse, Deutsche Rentenversicherung, Einwohnermeldeamt, Krankenkassenwechsel, Finanzamt, Jobcenter u. a.).

  Der 3-Schritt-Dialog führt durch: Profil wählen → Passwort festlegen → Datei herunterladen und Begleittext kopieren.

  Ein Reminder erscheint, wenn die Weitergabe-Datei älter als 12 Monate ist (maximal einmal pro Woche, nicht blockierend).

### Behoben

- **Overlay-Konflikt (wg-overlay)** — Der Weitergabe-Dialog blieb offen, wenn ein anderer Dialog per Code geöffnet oder geschlossen wurde. Beide Dialoge überlagerten sich sichtbar auf dem Bildschirm. Fix: `wg-overlay` in `showOverlay()` und `hideAllOverlays()` eingetragen.

### Sicherheit

- Weitergabe-Datei verwendet eigenen Salt (`getRandomValues()`) und eigenes Passwort — vollständig unabhängig vom Hauptpasswort. Das Hauptpasswort kann die Weitergabe-Datei nicht entschlüsseln.
- Kein Netzwerkaufruf beim Erstellen oder Öffnen der Weitergabe-Datei.

### Tests

- 22 neue Tests: WG-01 bis WG-16b
- Gesamt: 877 Tests, 0 Fehler

---

## [1.0.0-beta.7] — April 2026

### Behoben

- **BUG-SALT: Verschlüsselung auf anderem Gerät schlägt fehl** — Der kryptographische Salt wurde bisher ausschließlich im `localStorage` des Ursprungsgeräts gespeichert. Beim Öffnen einer gespeicherten Datei auf einem anderen Browser oder Gerät fehlte der Salt, obwohl das Passwort korrekt war. Fix: `saveAsHTML()` bettet den Salt jetzt direkt in die gespeicherte HTML-Datei ein. Beim Öffnen wird er vor dem Entschlüsselungsversuch wiederhergestellt — ohne den bestehenden Salt zu überschreiben (idempotent).

### Verbessert

- `saveAsHTML()` — Salt-Einbettung in den INIT-Block (Option A)
- `initBlock`-Kommentar vereinheitlicht, damit der Regex auch beim erneuten Speichern greift

### Dokumentation

- **SOVEREIGNTY.md** vollständig überarbeitet: Prüfung gegen das neue ZenDiS-Diskussionspapier (März 2026, 20 Kriterien in 4 Kategorien), BSI IT-Grundschutz++, EU Cyber Resilience Act, DSGVO, EU AI Act, OSBA, Sovereign Tech Fund / EDIC Digital Commons; Tabelle empfohlener weiterer Prüfungen
- **README.md**, **DOCS.md**, **QUICKSTART.md**, **FAQ.md**, **SECURITY.md**, **CONTRIBUTING.md** auf Version 1.0.0-beta.7 aktualisiert

### Tests

- 4 neue Tests: BUG-SALT-01a, BUG-SALT-01b, BUG-SALT-01c, BUG-SALT-02
- Gesamt: 842 Tests, 0 Fehler

---

## [1.0.0-beta.6] — April 2026

### Neu

- **Offline-Vollständigkeit:** Alle Bibliotheken inline eingebettet (jsPDF, docx.js, QR-Code) — keine CDN-Abhängigkeit mehr
- **Google Fonts entfernt:** Systemschriften (Georgia, -apple-system) statt externe Ladeabhängigkeit
- **Notfall & Katastrophenschutz:** Vollständig überarbeiteter Schritt mit 6 klickbaren Ampelkarten (rot/gelb/grün), Evakuierungsplan, lokalen Kontakten, Notrufnummern-Grid, Notrufblatt-PDF
- **Barrierefreiheit im Menü:** Schriftgröße, Kontrast, Nachtmodus, Vorlesen, Lupe — direkt erreichbar
- **iOS-Speicher-Anleitung:** Automatischer Dialog mit Schritt-für-Schritt-Anleitung beim Speichern auf iPhone
- **iOS: .htm-Endung:** Auf iOS werden Dateien mit `.htm` statt `.html` gespeichert, um PocketBook-Konflikt zu umgehen
- **Scroll-Fix:** Navigation zu neuer Seite scrollt korrekt nach oben (auch auf Mobil)

### Verbessert

- `saveAsHTML()` INIT-Block-Regex korrigiert — gespeicherte Dateien enthielten vorher keine Daten
- `nextStep()`/`prevStep()` leiten über `goToStep()` für einheitlichen Code-Pfad
- PDF-Bibliothek-Nachlader mit automatischem Retry und Fallback-CDN
- `console.log` durch `console.error` ersetzt (Produktionsbereinigung)
- INIT-Kommentar-Reihenfolge korrigiert für korrekte Regex-Erkennung

### Behoben

- BUG-10: vCard-Code lag außerhalb `<script>`-Tags
- BUG-11: `mehr()`-Funktion wurde mit falschem Argument-Typ aufgerufen
- Emojis aus Abschnitts-Titeln in Notfall-Kategorie entfernt

---

## [1.0.0-beta.5] — März 2026

### Neu

- Fokus-System: Zielgeführte Navigation (Notfall, Familie, Vorsorge, Haustiere)
- Einstiegs-Wizard für neue Nutzer
- Multi-Profil-Unterstützung
- Angehörigen-Ansicht mit separatem Zugang
- Globale Suche in der Topbar
- Diktat-Eingabe (Web Speech API)
- Dokument-Upload (PDF, Bilder, HEIC) mit Kategorie-Verwaltung
- Gesundheitsvollmacht-Wizard und Word-Export
- Notfall-Tasche Szenario-PDF
- BundID- und ELEFAND-Felder
- Datenschutz-Modal

### Verbessert

- vivoConfirm ersetzt alle nativen `confirm()`-Dialoge
- PDF-Encoding-Fehler in Behördendaten-PDFs behoben
- Heimaufnahme/FHIR-Karten-Nesting behoben
- DuckDuckGo localStorage-Konflikt behoben

---

## [1.0.0-beta.4] — Februar 2026

### Neu

- Weiche beim Öffnen: Inhaberin oder Angehörige/r
- Angehörigen-Modus aus App heraus
- Fokus-Button in Sidebar
- 20 Schritte (statt 19)
- Einstellungen als eigener Schritt
- Logo transparent (Baum ohne Text)

### Verbessert

- User Journey komplett überarbeitet
- 253 Emojis aus Feldtiteln entfernt
- Alle nativen confirm() durch vivoConfirm ersetzt
- Tests: 89 auf 126 erweitert

---

## [1.0.0-beta.3] — Januar 2026

### Neu

- AES-256-GCM Verschlüsselung
- Passwortschutz mit PBKDF2
- `saveAsHTML()` — Datei mit eingebetteten Daten speichern
- vCard 4.0 Export
- FHIR R4 JSON Export
- QR-Code Aufkleber
- Arztbogen PDF
- Szenario-PDFs (Krankenhaus, Todesfall)
- Vorsorgevollmacht und Patientenverfügung Word
- Vorlesen (Web Speech API)
- Hoher Kontrast und Nachtmodus

---

## [1.0.0-beta.1] — Dezember 2025

Erste Version — vollständige Notfallmappe als PDF und Word, 17 Dateneingabe-Schritte, Wizard für Vollmachten und Haustier-Notfallplan.
