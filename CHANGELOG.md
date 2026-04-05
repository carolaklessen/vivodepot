# Changelog

Alle wesentlichen Änderungen an VIVODEPOT werden in dieser Datei dokumentiert.
Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

## [1.0.0-beta] — 2026-04-05

### Erste öffentliche Beta-Version

#### Eingabe (18 Schritte)
- Persönliche Daten mit optionalem Profilfoto (Smart-Crop für Portraits)
- Vertrauenspersonen (Name, Rolle, Telefon, E-Mail, Aufgabe im Notfall)
- Zu informierende Personen (4 Zeitkategorien: Sofort / Erste Woche / 4 Wochen / Bei Bedarf)
- Finanzen (Konten, IBAN-Validierung nach Mod-97)
- Versicherungen
- Immobilien
- Testament & Vollmachten (inkl. Vollmachten für andere Personen)
- Verträge & Abonnements
- Gesundheit (Blutgruppe, Allergien, Medikamente, Befunde, Implantate, Organspende)
- Haustiere
- Pflege & Biografie (Pflegegrad, GdB, Kommunikation, Ernährung, Alltag)
- Digitales Erbe (Passwort-Manager, Krypto-Wallets, Legacy Contacts, Hardware-Wallets, Social Media)
- Persönliches & Briefe (Fotos-Ablageort, Krankenhaus- und Abschiedsbriefe)
- Bestattungswünsche (Art, Ort, Unternehmen, Musik, persönliche Botschaft)
- Fristen & Prüfung (Ampel-System für 5 Dokumente)

#### Assistenten (5 Wizards)
- Notfall-Gesundheitskarte (6 Schritte, druckbare Scheckkarte 85×54mm)
- Vorsorgevollmacht (6 Schritte, nach §§ 1814 ff. BGB)
- Patientenverfügung (6 Schritte, nach § 1827 BGB)
- Bestattungs-Assistent (8 Schritte)
- Haustier-Assistent (6 Schritte)

#### Exporte (11 Formate)
- Notfallmappe komplett (PDF + Word)
- Vorsorgevollmacht (Word, unterschriftsreif)
- Patientenverfügung (Word, unterschriftsreif)
- Krankenhaus-Einweisung (1-Seiten-PDF)
- Krisenplan — Im Todesfall (PDF)
- Haustier-Notfallkarte (PDF)
- Heimaufnahme-Paket (5-Seiten-PDF)
- Arbeitgeber-Notfallkarte (PDF)
- QR-Sticker Paket (3 laminierbare Sticker: Medizin, Haustier, Schlüssel)
- FHIR R4 JSON
- Fortschritts-Checkliste (HTML)

#### Sicherheit
- AES-256-GCM Verschlüsselung (Web Crypto API)
- Angehörigen-Weiche (Inhaber vs. Angehörige)
- Angehörigen-Passwort mit Abfrage
- Multi-Profil-System (bis 4 Profile, löschbar)

#### Benutzeroberfläche
- Zweisprachig (DE/EN, 140+ Übersetzungen)
- 3-stufige Schriftgröße (persistent)
- Geclusterte Navigation (5 Gruppen)
- Barrierefreie Tap-Targets (min. 44px)
- Topbar mit ⋮-Menü und Storage-Meter
- File System Access API (direktes Speichern auf USB-Stick)
- PWA / Service Worker für Offline-Nutzung
- Professionelles Logo und SVG-Favicon

#### Rechtlich
- EUPL-1.2 Lizenz
- Copyright © 2026 auf allen Exporten
- Aktuelle BGB-Referenzen (Betreuungsrechtsreform 2023)
- Links zu offiziellen Formularen und Registern
- KI-Transparenzhinweis (EU AI Act Art. 50) in App, Quellcode und Dokumentation
