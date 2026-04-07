# 📘 Vivodepot — Dokumentation

**Alles Wichtige an einem Ort — für mich und meine Familie.**

Vivodepot ist eine browserbasierte Single-File-App für persönliche Vorsorge- und Nachlassdokumentation. Eine HTML-Datei, kein Internet, keine Installation, keine Cloud.

---

## Inhaltsverzeichnis

1. [Systemvoraussetzungen](#systemvoraussetzungen)
2. [Installation & Start](#installation--start)
3. [Die 19 Abschnitte im Detail](#die-18-abschnitte-im-detail)
4. [Datenschutz & Verschlüsselung](#datenschutz--verschlüsselung)
5. [Exporte & Dokumente](#exporte--dokumente)
6. [Assistenten (Wizards)](#assistenten-wizards)
7. [Barrierefreiheit](#barrierefreiheit)
8. [Notfall-Schnellzugriff](#notfall-schnellzugriff)
9. [Profile (Mehrere Personen)](#profile-mehrere-personen)
10. [Speichern & Backup](#speichern--backup)
11. [PWA & Offline-Nutzung](#pwa--offline-nutzung)
12. [Angehörigen-Modus](#angehörigen-modus)
13. [Technische Details](#technische-details)

---

## Systemvoraussetzungen

- Ein moderner Browser: Chrome, Firefox, Safari oder Edge
- JavaScript muss aktiviert sein
- Kein Internet erforderlich (alle Bibliotheken sind eingebettet)
- Empfohlen: Bildschirm ab 320px Breite (Smartphone aufwärts)

---

## Installation & Start

Es gibt keine Installation. Vivodepot ist eine einzelne HTML-Datei.

**Vom USB-Stick:** Doppelklicken Sie auf `index.html`.

**Aus dem Internet:** Laden Sie die Datei von [GitHub](https://github.com/carolaklessen/vivodepot) herunter und öffnen Sie sie lokal.

**Als App installieren (PWA):**
- **Android/Desktop:** Chrome zeigt einen „Installieren"-Banner → klicken
- **iPhone/iPad:** Safari → Teilen ⬆️ → „Zum Home-Bildschirm"
- PWA-Installation erfordert HTTPS (z.B. über GitHub Pages)

---

## Die 19 Abschnitte im Detail

### Meine Person

**1. Über mich** — Name, Geburtsdatum, Adresse, Kontaktdaten, Foto, Familienstand, Kinder. Das Minimum für den Einstieg. Pflichtfelder (Name) werden fürs Deckblatt benötigt.

**2. Vertrauenspersonen** — Die wichtigsten Kontakte im Notfall. Name, Telefon, E-Mail, Rolle (z.B. „Hauptkontaktperson"), Aufgabe (z.B. „hat Wohnungsschlüssel"). Unterstützt CSV- und vCard-Import.

**3. Wichtige Kontakte** — Ärzte, Anwälte, Steuerberater, Handwerker, Nachbarn — alle, die im Ernstfall informiert werden müssen.

### Absicherung & Finanzen

**4. Geld & Konten** — Bankkonten, Depots, Kreditkarten, Altersvorsorge, Rentenversicherungsnummer, Steuer-ID. Beliebig viele Konten und Depots, jeweils mit ▲▼-Buttons sortierbar.

**5. Versicherungen** — Alle Versicherungspolicen mit Gesellschaft, Policennummer und Ablageort.

**6. Wohnen & Eigentum** — Mietverträge, Immobilien, Grundbucheinträge.

**7. Verträge & Abos** — Laufende Verträge (Mobilfunk, Streaming, Strom, ADAC…) mit Kündigungsfrist und -weg. Jeder Vertrag hat eine Kategorie mit spezifischen Tipps (z.B. „ADAC-Mitgliedschaft kann übertragen werden").

**8. Mein Wille** — Testament, Vorsorgevollmacht, Patientenverfügung, Erben, Notar, Organspende, Sorgerechtsverfügung, Unterhaltsverpflichtungen. Enthält 5 Assistenten für geführte Eingabe.

### Gesundheit & Leben

**9. Meine Gesundheit** — Blutgruppe, Allergien, Erkrankungen, Medikamente, Implantate, Krankenversicherung (inkl. Familienversicherung), Voroperationen, Familienanamnese, Vorsorgeuntersuchungen, Zahnarzt, Bonusheft, Befunde (Ablageorte).

**10. Pflege & Lebenslauf** — Pflegegrad, Behinderung, Hilfsmittel, Pflegewünsche, Biografie, Bildung & Berufsleben (Schulabschluss, Ausbildung, Studium, Beruf, Arbeitgeber, Zeugnisse).

**11. Meine Tiere** — Name, Art, Betreuung, Tierarzt, Futter, besondere Hinweise.

### Persönliches & Wünsche

**12. Online & Zugänge** — Passwort-Manager, Cloud-Speicher, E-Mail-Konten, Soziale Netzwerke, Krypto-Wallets (inkl. Legacy Contact), BundID, ELEFAND, Geräte, Tresore, Schlüssel, Zugangscodes.

**13. Erinnerungsstücke & Briefe** — Fotos (physisch & digital), persönliche Gegenstände („Wer soll was bekommen?"), Haushalt/Spenden-Wünsche, persönliche Briefe für Szenarien (Krankenhaus, Todesfall).

**14. Mein Abschied** — Bestattungswünsche, Trauerfeier, Grabstein, Blumenschmuck, Musik, Nachrufe.

### Werkzeuge

**15. Assistenten** — 6 geführte Assistenten (Gesundheitskarte, Vorsorgevollmacht, Patientenverfügung, Gesundheitsvollmacht, Bestattung, Haustier). Außerdem: Passwort-Zugang für Angehörige.

**15b. Pflegekinder** (in Über mich — Familie): Pflegekinder mit Jugendamt-Kontakt, Art der Pflege, Vormund. Hinweis: Pflegekinder erben gesetzlich nicht — nur durch Testament oder Adoption.

**16. Meine Dateien** — Dokumente hochladen, benennen und nach Kategorie ablegen (Ausweise, Vollmachten, Befunde, Verträge, Fotos, Sonstiges). Beim Upload wird nach einem aussagekräftigen Namen gefragt. Jede Datei ist jederzeit wieder downloadbar.

**17. Prüftermine** — Erinnerungen an wichtige Fristen: Vollmacht, Patientenverfügung, Testament, Bankvollmacht, Vivodepot-Update. Ampelsystem (grün/gelb/rot).

**18. Einstellungen** — Passwort ändern oder entfernen, Darstellung (Schriftgröße, Kontrast, Nachtmodus, Bildschirmlupe), Profile verwalten, Daten exportieren/importieren, App-Informationen und Datenschutz.

**19. Dokumente erstellen** — Alle Exporte auf einen Blick (siehe unten).

---

## Datenschutz & Verschlüsselung

### Grundprinzip

Vivodepot speichert **keine Daten im Internet**. Es gibt keinen Server, keine Cloud, kein Benutzerkonto, kein Tracking, keine Cookies, kein Google Analytics.

Alle Daten bleiben:
- Im lokalen Browser-Speicher (localStorage), oder
- In der heruntergeladenen HTML-Datei auf Ihrem USB-Stick

### Verschlüsselung

- **Standard:** AES-256-GCM über die Web Crypto API
- **Schlüsselableitung:** PBKDF2 mit 100.000 Iterationen
- **Ohne Passwort** kann niemand die Daten lesen — auch nicht der Entwickler
- **iOS `file://`:** Falls `crypto.subtle` nicht verfügbar ist (z.B. auf iOS bei Dateien vom Stick), werden die Daten unverschlüsselt gespeichert — mit Warnhinweis

### Notfall-Daten

6 Felder werden **zusätzlich unverschlüsselt** gespeichert, damit der 🚨-Notfall-Button auch vor der Passworteingabe funktioniert: Name, Blutgruppe, Allergien, Erkrankungen, Medikamente, Notfallkontakt.

### Open Source

Der gesamte Quellcode ist öffentlich einsehbar auf [GitHub](https://github.com/carolaklessen/vivodepot). Lizenz: EUPL-1.2.

---

## Exporte & Dokumente

| Export | Format | Beschreibung |
|--------|--------|-------------|
| Haupt-PDF | PDF | Komplettes Vivodepot mit Deckblatt und allen Daten |
| Haupt-Word | DOCX | Bearbeitbares Word-Dokument |
| Checkliste | HTML | Was ist ausgefüllt, was fehlt? |
| Vorsorgevollmacht | DOCX | Rechtsgültiger Entwurf nach aktuellem BGB |
| Patientenverfügung | DOCX | Medizinische Wünsche nach aktuellem BGB |
| Heimaufnahme-Paket | PDF | 6 Seiten für Pflegeeinrichtungen |
| Arztbesuch-Bogen | PDF | Stammdaten für die Arztpraxis |
| Krankenhaus-Blatt | PDF | Notarzt- und Aufnahme-Daten |
| Todesfall-Krisenplan | PDF | Erste Schritte für Angehörige |
| Haustier-Notfallkarte | PDF | Versorgung bei Abwesenheit |
| Notfall-Tasche | PDF | Checkliste für Evakuierung/Krise |
| QR-Sticker | HTML | 3 laminierbare QR-Codes |
| Work-Life-Karte | HTML | Notfallkarte für den Arbeitgeber |
| FHIR R4 JSON | JSON | Medizindaten-Standard für Kliniken |

Alle Dokumente werden **lokal im Browser erzeugt** — keine Daten verlassen das Gerät.

---

## Assistenten (Wizards)

5 geführte Schritt-für-Schritt-Assistenten mit einfachen Fragen:

1. **Notfall-Gesundheitskarte** — 6 Schritte → druckbare Scheckkarte für die Geldbörse
2. **Vorsorgevollmacht** — 6 Schritte → füllt alle relevanten Felder aus
3. **Patientenverfügung** — 6 Schritte → Entscheidungen zu Lebenserhaltung
4. **Bestattungs-Assistent** — 8 Schritte → Bestattungsart, Feier, Musik
5. **Haustier-Assistent** — 6 Schritte → Tier, Futter, Betreuung, Tierarzt

Die Assistenten füllen automatisch die Felder im jeweiligen Abschnitt aus.

---

## Barrierefreiheit

| Funktion | Button | Beschreibung |
|----------|--------|-------------|
| Suche | 🔎 | Durchsucht alle Felder, Werte und Abschnitte |
| Schriftgröße | A⁺ | 3 Stufen (normal, groß, sehr groß) |
| Vorlesen | 🔊 | Liest die aktuelle Seite vor (Web Speech API, deutsch) |
| Hoher Kontrast | ◐ | Erhöhter Kontrast für bessere Lesbarkeit |
| Bildschirmlupe | 🔍 | 100% / 150% / 200% Zoom |
| Nachtmodus | 🌙 | Dunkler Hintergrund, augenschonend |
| Drucken | 🖨 | Browser-Druckdialog |
| Spracheingabe | 🎤 | Diktieren statt tippen (Chrome/Edge) |

Alle Einstellungen (Schriftgröße, Kontrast, Nachtmodus) werden gespeichert.

---

## Notfall-Schnellzugriff

Der rote **🚨-Button** unten rechts zeigt sofort:

- Blutgruppe
- Allergien
- Erkrankungen
- Medikamente (mit Dosierung)
- Notfallkontakt (mit Telefonnummer)
- Organspende-Wunsch

**Funktioniert auch ohne Passworteingabe** — die Notfall-Daten werden separat und unverschlüsselt gespeichert (wie die ICE-Funktion auf dem iPhone).

---

## Profile (Mehrere Personen)

Vivodepot unterstützt bis zu **4 Profile** in einer Datei — z.B. für Ehepartner oder pflegebedürftige Eltern.

- Klicken Sie auf den Profil-Button (👤) in der Topbar
- „Neues Profil" → eigener Datensatz, eigenes Passwort
- Profile sind vollständig getrennt — kein Zugriff zwischen den Profilen

---

## Speichern & Backup

### Automatisch

Die App speichert automatisch nach jeder Änderung im Browser-Speicher (localStorage).

### Manuell (empfohlen)

Klicken Sie auf **💾 Speichern** → die komplette App mit allen Daten wird als neue HTML-Datei heruntergeladen. Diese Datei ist Ihr Backup.

### Cloud-Backup

Ihre Vivodepot-Datei ist AES-256 verschlüsselt. Sie können eine Kopie sicher in Ihrer eigenen Cloud ablegen (iCloud, Google Drive, OneDrive). Ohne Ihr Passwort kann niemand die Datei lesen — auch nicht der Cloud-Anbieter.

### Daten exportieren/importieren

- **Menü ⋮ → Daten exportieren (JSON)** → Backup als JSON-Datei
- **Menü ⋮ → Daten importieren** → JSON oder HTML-Datei einlesen

---

## PWA & Offline-Nutzung

Vivodepot kann als Progressive Web App installiert werden:

- Alle 3 externen Bibliotheken (jsPDF, docx, QRCode) werden beim ersten Laden gecacht
- Danach funktioniert alles komplett offline
- Service Worker (Cache v2) aktualisiert sich automatisch

**Voraussetzung für PWA:** HTTPS (z.B. über GitHub Pages).

---

## Angehörigen-Modus

Beim Öffnen einer gespeicherten Datei erscheint die Frage „Wer öffnet dieses Vivodepot?" — Inhaberin oder Angehörige/r. Als Inhaberin ist der Modus auch über ⋮-Menü → „Angehörigen-Ansicht testen" erreichbar. Angehörige wählen ein Szenario:

- **Krankenhaus-Einweisung** → Allergien, Medikamente, Blutgruppe, Vollmachten, Hausarzt, laufende Behandlung, hochgeladene Befunde
- **Im Todesfall** → Testament, Bestattungswünsche, Kontakte, persönliche Botschaft, hochgeladene Vollmachten

Die Szenarien filtern die Daten auf das Wesentliche — Angehörige müssen nicht die ganze App durchsuchen.

---

## Technische Details

| Eigenschaft | Wert |
|-------------|------|
| Dateigröße | ~1 MB |
| Codezeilen | ~8.900 |
| Externe Abhängigkeiten | 3 CDN-Bibliotheken (gecacht) |
| Framework | Kein Framework — Vanilla HTML/CSS/JS |
| Verschlüsselung | AES-256-GCM, PBKDF2 |
| Lizenz | EUPL-1.2 |
| Browser-Support | Chrome 90+, Firefox 90+, Safari 15+, Edge 90+, DuckDuckGo, Android Chrome, iOS Safari |
| Mobile Features | Bottom-Nav, Share API, Camera Capture, Contacts API, Safe-area-insets, Keyboard-fix, Touch-optimiert |
| Fokus-Wizard | 4 Ziele mit echtem Field-Filtering, 8 FOCUSED_RENDERERS |
| Fokus-Rendering | 8 fokussierte Step-Varianten (FOCUSED_RENDERERS) pro Ziel |
| KI-Transparenz | Entwickelt mit KI-Unterstützung (EU AI Act Art. 50) |

### Verwendete Bibliotheken

- **jsPDF** (MIT) — PDF-Erzeugung
- **docx** (MIT) — Word-Dokument-Erzeugung
- **QRCode.js** (MIT) — QR-Code-Generierung

### localStorage-Keys

| Key | Inhalt |
|-----|--------|
| `vivodepot_v1_enc` | Verschlüsselte/unverschlüsselte Nutzerdaten |
| `vivodepot_v1_meta` | Kryptografisches Salt |
| `vivodepot_v1_enc_notfall` | Unverschlüsselte Notfall-Daten |
| `vivodepot_fontsize` | Schriftgröße-Einstellung |
| `vivodepot_contrast` | Kontrast-Modus |
| `vivodepot_darkmode` | Nachtmodus |
| `vivodepot_lang` | Sprache (de/en) |

---

*Version 1.0.0-beta · © 2026 Vivodepot · Lizenziert unter [EUPL-1.2](LICENSE)*
