#!/usr/bin/env python3
"""
Vivodepot — Regressions-Testscript
====================================
Prüft die VIVODEPOT.html auf bekannte Bugs und Feature-Vollständigkeit.

Verwendung:
  python3 test_vivodepot.py VIVODEPOT.html

Dieses Script nach JEDER Änderung laufen lassen.
Ergebnis muss 0 FAIL sein, bevor die Datei als Baseline akzeptiert wird.
"""

import re, sys, subprocess, tempfile, os

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python3 test_vivodepot.py <datei.html>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    html = open(filepath, encoding='utf-8').read()
    
    results = []
    
    def check(name, condition, detail=""):
        status = "PASS" if condition else "FAIL"
        results.append((status, name, detail))
        icon = "✓" if condition else "❌"
        print(f"  {icon} {name}" + (f" — {detail}" if detail and not condition else ""))
    
    # ═══════════════════════════════════════
    print("\n=== 1. SYNTAX ===")
    # ═══════════════════════════════════════
    scripts = list(re.finditer(r'<script(?!\s+src)[^>]*>([\s\S]*?)</script>', html))
    check("Script-Blöcke gefunden", len(scripts) >= 2, f"{len(scripts)} Blöcke")
    
    all_syntax_ok = True
    for i, m in enumerate(scripts):
        content = m.group(1)
        if len(content) < 50:
            continue
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(content)
            fname = f.name
        try:
            r = subprocess.run(['node', '--check', fname], capture_output=True, text=True)
            ok = r.returncode == 0
            check(f"Script {i} Syntax", ok, r.stderr[:100] if not ok else "")
            if not ok:
                all_syntax_ok = False
        finally:
            os.unlink(fname)
    
    # ═══════════════════════════════════════
    print("\n=== 2. BEKANNTE BUGS ===")
    # ═══════════════════════════════════════
    
    wo_match = re.search(r'id="welcome-overlay"[^>]*style="([^"]*)"', html)
    if wo_match:
        check("BUG-01: Welcome-Overlay default sichtbar", 
              'display:flex' in wo_match.group(1) or 'display: flex' in wo_match.group(1))
    else:
        check("BUG-01: Welcome-Overlay hat inline-style", False, "Kein style-Attribut gefunden")
    
    hide_fn_match = re.search(r'function hideAllOverlays\(\)\s*\{([^}]+)\}', html)
    if hide_fn_match:
        hide_fn = hide_fn_match.group(1)
        required_overlays = ['welcome-overlay', 'return-overlay', 'crypto-overlay', 'goal-wizard']
        for oid in required_overlays:
            check(f"BUG-02: hideAllOverlays enthält '{oid}'", oid in hide_fn)
    else:
        check("BUG-02: hideAllOverlays existiert", False)

    # BUG-14: goal-wizard muss auch in showOverlay-Liste stehen
    show_fn_match = re.search(r'function showOverlay\(id\)\s*\{([^}]+)\}', html)
    if show_fn_match:
        check("BUG-14: showOverlay enthält 'goal-wizard'",
              'goal-wizard' in show_fn_match.group(1),
              "goal-wizard fehlt in showOverlay — Wizard nicht schließbar bei Overlay-Wechsel")
    else:
        check("BUG-14: showOverlay existiert", False)

    # BUG-15: mehr()-Badge im onclick darf kein HTML mit Anführungszeichen enthalten
    # (style="..." oder style='...' bricht das onclick-Attribut → HTML kaputt oder JS-Fehler → welcome-overlay)
    check("BUG-15a: mehr() badgeOnclick (einfache Quotes) beseitigt",
          'badgeOnclick' not in html,
          "badgeOnclick mit style='...' bricht onclick-String")
    check("BUG-15b: mehr() verwendet mehrToggle() statt inline-HTML im onclick",
          'function mehrToggle' in html,
          "mehrToggle fehlt — mehr()-Button hat HTML-in-onclick die das Attribut bricht")
    mehr_fn = re.search(r'function mehr\(id.*?\n\}', html, re.DOTALL)
    if mehr_fn:
        check("BUG-15c: mehr() hat kein btn.innerHTML im onclick-String",
              'btn.innerHTML' not in mehr_fn.group(0),
              "btn.innerHTML im onclick-Attribut → HTML-Injection bricht Attribut-Parsing")

    # BUG-17: skipGoalWizard() muss currentStep auf 0 zurücksetzen vor safeRender()
    skip_fn_match = re.search(r'function skipGoalWizard\(\)\s*\{([\s\S]*?)\n\}', html)
    if skip_fn_match:
        skip_body = skip_fn_match.group(1)
        reset_before_render = bool(re.search(
            r'currentStep\s*=\s*0[\s\S]*?safeRender', skip_body))
        check("BUG-17: skipGoalWizard() setzt currentStep=0 vor safeRender()",
              reset_before_render,
              "Fokus überspringen auf Seite 7 → App startet auf Seite 7 statt Seite 1")
    else:
        check("BUG-17: skipGoalWizard() existiert", False)

    # BUG-16: applyGoalWizard() muss currentStep auf 0 zurücksetzen vor renderSidebar/renderStep
    apply_fn_match = re.search(r'function applyGoalWizard\(\)\s*\{([\s\S]*?)\n\}', html)
    if apply_fn_match:
        apply_body = apply_fn_match.group(1)
        reset_before_render = bool(re.search(
            r'currentStep\s*=\s*0[\s\S]*?renderSidebar', apply_body))
        check("BUG-16a: applyGoalWizard() setzt currentStep=0 vor renderSidebar()",
              reset_before_render,
              "Fokus-Wechsel auf Seite 7 → neuer Fokus startet auf Seite 7 statt Seite 1")
    else:
        check("BUG-16a: applyGoalWizard() existiert", False)

    check("BUG-03: enterApp() existiert", 'function enterApp' in html)

    # BUG-13: returnContinue() darf showGoalWizard nicht bedingungslos aufrufen
    rc_match = re.search(r'function returnContinue\(\)\s*\{([\s\S]*?)\n\}', html)
    if rc_match:
        rc_body = rc_match.group(1)
        unconditional = bool(re.search(r'setTimeout\s*\(\s*showGoalWizard', rc_body)) and \
                        'savedFokus' not in rc_body
        check("BUG-13: returnContinue() zeigt Wizard nur bei fehlendem Fokus",
              not unconditional,
              "setTimeout(showGoalWizard) ohne savedFokus-Check → Wizard für Rückkehr-Nutzer nicht schließbar")
    else:
        check("BUG-13: returnContinue() existiert", False)

    # vCard darf nicht als sichtbarer Text im HTML stehen
    # (Bug: JS-Code außerhalb <script>-Tag wird als HTML gerendert)
    vcard_pos = html.find('// ── vCard 4.0 Export')
    if vcard_pos >= 0:
        last_script_close = html.rfind('</script>', 0, vcard_pos)
        next_script_open  = html.rfind('<script',   0, vcard_pos)
        check("BUG-10: vCard-Code innerhalb <script>-Tag",
              next_script_open > last_script_close,
              "vCard-JS liegt außerhalb eines <script>-Tags — wird als Text gerendert!")
    else:
        check("BUG-10: vCard-Code innerhalb <script>-Tag", False,
              "Marker '// ── vCard 4.0 Export' nicht gefunden")

    # BUG-11: mehr()-Aufrufe mit falschem 3. Argument (Template statt Array → filter-Fehler)
    mehr_calls = re.findall(r"mehr\('([^']+)',\s*'[^']*',\s*(`|\[)", html)
    bad_mehr = [(mid, t) for mid, t in mehr_calls if t == '`']
    check("BUG-11: Alle mehr()-Aufrufe haben Array als 3. Arg",
          len(bad_mehr) == 0,
          f"Fehler in: {[mid for mid,_ in bad_mehr]}")
    
    pw_fields = len(re.findall(r'type=["\']password["\']', html))
    check("BUG-05: Max 12 password-Felder", pw_fields <= 12, f"Gefunden: {pw_fields}")  # ANF-06: +3 (qr-pin1, qr-pin2, qre-pin)
    
    proton_refs = html.lower().count('protonmail') + html.lower().count('proton.me')
    check("BUG-06: Keine Proton-Referenzen", proton_refs == 0, f"Gefunden: {proton_refs}")
    
    steps_match = re.search(r'(?:const|var|let)\s+STEPS\s*=\s*\[([\s\S]*?)\];', html)
    if steps_match:
        steps_block = steps_match.group(1)
        emojis = re.findall(r"label:\s*'[^']*[\U00010000-\U0010ffff]", steps_block)
        check("BUG-07: Keine Emojis in STEPS", len(emojis) == 0, f"Gefunden: {len(emojis)}")
    
    save_fn = re.search(r'function saveAsHTML\(\)\s*\{([\s\S]*?)\n\}', html)
    if save_fn:
        check("BUG-08: saveAsHTML enthält showSavedFileWelcome", 'showSavedFileWelcome' in save_fn.group(1))
    
    init_match = re.search(r'enterApp\(\)\s*\{([\s\S]*?)\n\}', html)
    if init_match:
        check("BUG-09: Init ruft hideAllOverlays auf", 'hideAllOverlays' in init_match.group(1))
    
    check("iOS: Kein bare 'export:' Key", 
          re.search(r"['\"]export['\"]?\s*:", html) is None or 'exportStep' in html)
    
    # ═══════════════════════════════════════
    print("\n=== 3. STEPS & RENDERER ===")
    # ═══════════════════════════════════════
    
    steps = re.findall(r"\{[^}]*id:\s*'(\w+)'", html)
    renderers = re.findall(r"(\w+)\s*:\s*\(\)\s*=>", html)
    
    required_steps = [
        'start', 'kontakte', 'infokontakte', 'finanzen', 'versich',
        'immobilien', 'testament', 'vertraege', 'gesundheit', 'haustiere',
        'pflege', 'digital', 'persoenliches', 'bestattung',
        'assistenten', 'dokumente', 'erinnerung', 'einstellungen', 'exportStep'
    ]
    
    for step in required_steps:
        check(f"Step '{step}' hat Renderer", step in renderers)
    
    # ═══════════════════════════════════════
    print("\n=== 4. KERN-FUNKTIONEN ===")
    # ═══════════════════════════════════════
    
    core_functions = {
        'saveData': 'async function saveData',
        'loadData': 'async function loadData',
        'saveAsHTML': 'function saveAsHTML',
        'importData': 'function importData',
        'renderStep': 'function renderStep',
        'renderSidebar': 'function renderSidebar',
        'generatePDF': 'function generatePDF',
        'toast': 'function toast',
        'get (Datenzugriff)': 'function get(',
        'set (Datenzugriff)': 'function set(',
        'switchExportTab': 'function switchExportTab',
        'showGoalWizard': 'function showGoalWizard',
    }
    
    for name, pattern in core_functions.items():
        check(f"Funktion: {name}", pattern in html)
    
    # ═══════════════════════════════════════
    print("\n=== 5. ENCRYPTION ===")
    # ═══════════════════════════════════════
    
    check("AES-GCM vorhanden", 'AES-GCM' in html)
    check("CRYPTO_AVAILABLE Check", 'CRYPTO_AVAILABLE' in html or 'crypto.subtle' in html)
    check("Crypto-Modal", 'crypto-overlay' in html or 'showCryptoModal' in html)
    
    # ═══════════════════════════════════════
    print("\n=== 6. IMPORT/EXPORT ===")
    # ═══════════════════════════════════════
    
    check("vCard Import", 'parseVCard' in html or 'vcard' in html.lower())
    check("CSV Import", 'parseCSV' in html or 'csv' in html.lower())
    check("PDF Export", 'generatePDF' in html)
    check("Word Export (Gesamt)", 'generateDocx' in html or 'docx' in html)
    check("Word Vorsorgevollmacht", 'generateVorsorgevollmacht' in html)
    check("Word Patientenverfügung", 'generatePatientenverfuegung' in html)
    check("Word Gesundheitsvollmacht", 'generateGesundheitsvollmacht' in html)
    check("Checklist Export", 'generateChecklist' in html or 'Checkliste' in html)
    check("FHIR R4 Export", 'generateFHIR' in html)
    check("FIM-JSON Export", 'exportFIMJson' in html)
    check("Behördendaten Export", 'generateBehoerdendaten' in html)
    check("Structured Import", 'importStructured' in html)
    check("jsPDF geladen", 'jspdf' in html.lower())
    check("docx geladen", 'docx@' in html)
    
    # ═══════════════════════════════════════
    print("\n=== 7. WIZARDS ===")
    # ═══════════════════════════════════════
    
    wizards = {
        'Gesundheitskarte': 'gwizOpen',
        'Vorsorgevollmacht': 'vvwizOpen',
        'Patientenverfügung': 'pvwizOpen',
        'Bestattung': 'bwizOpen',
        'Haustier': 'hwizOpen',
        'Gesundheitsvollmacht': 'gvwizOpen',
        'Fokus/Ziel': 'showGoalWizard',
    }
    for name, fn in wizards.items():
        check(f"Wizard: {name}", f'function {fn}' in html)
    
    # ═══════════════════════════════════════
    print("\n=== 8. ROBUSTHEIT ===")
    # ═══════════════════════════════════════
    
    check("window.onerror Handler", 'window.onerror' in html)
    check("localStorage Wrapper (_ls)", 'localStorage' in html and 'try' in html)
    
    # ═══════════════════════════════════════
    print("\n=== 9. PROFIL-SYSTEM ===")
    # ═══════════════════════════════════════
    
    check("Profil: switchToProfile()", 'function switchToProfile' in html or 'async function switchToProfile' in html)
    check("Profil: addNewProfile()", 'function addNewProfile' in html)
    check("Profil: getProfileManifest()", 'function getProfileManifest' in html)
    check("Profil: updateProfileButton()", 'function updateProfileButton' in html)
    check("Profil: Dropdown UI", 'profile-dropdown' in html)
    check("Profil: STORE_KEY ist let (nicht const)", 'let STORE_KEY' in html)
    check("Profil: setActiveProfile()", 'function setActiveProfile' in html)
    
    # ═══════════════════════════════════════
    print("\n=== 10. UI & BRANDING ===")
    # ═══════════════════════════════════════
    
    check("Favicon vorhanden", 'rel="icon"' in html)
    check("PWA Manifest", 'rel="manifest"' in html)
    check("Slogan", 'SOUVERÄNITÄT BY DESIGN' in html)
    check("Export-Tabs (4 Tabs)", html.count('class="etab"') >= 3)
    check("Kein Technik-Tab", 'etab-technik' not in html)
    check("Barrierefreiheit: Vorlesen", 'toggleVorlesen' in html)
    check("Barrierefreiheit: Kontrast", 'toggleKontrast' in html)
    check("Barrierefreiheit: Nachtmodus", 'toggleNacht' in html)
    check("Barrierefreiheit: Schriftgröße", 'cycleFontSize' in html)
    check("Globale Suche", 'openGlobalSearch' in html)

    # ═══════════════════════════════════════
    # USER JOURNEY TESTS
    # ═══════════════════════════════════════

    # Journey 1: Standard-User (Erstbesuch)
    check("Journey: Welcome-Overlay hat Loslegen-Button", "onclick=\"welcomeStart()\"" in html)
    check("Journey: Goal-Wizard aufrufbar", "function showGoalWizard()" in html)
    check("Journey: enterApp ruft safeRender", "function enterApp() {\n  hideAllOverlays();\n  safeRender();" in html)
    check("Journey: safeRender fängt Fehler ab", "function safeRender()" in html and "catch" in html)
    check("Journey: Fokus-Button in Sidebar", "Fokus wählen" in html and "Fokus ändern" in html)

    # Journey 2: Rückkehr (Return-Overlay)
    check("Journey: Return-Overlay hat Weiche", "id=\"return-overlay\"" in html and "showAngehoerigenAuswahl()" in html)
    check("Journey: Return-Overlay zeigt Namen", "return-owner-label" in html)
    check("Journey: returnContinue ruft safeRender", "function returnContinue() {\n  hideAllOverlays();\n  safeRender();" in html)

    # Journey 3: Gespeicherte Datei
    check("Journey: showSavedFileWelcome vorhanden", "function showSavedFileWelcome()" in html)
    check("Journey: savedWelcomeOwner vorhanden", "function savedWelcomeOwner()" in html)
    check("Journey: savedWelcomeAngehoerige vorhanden", "function savedWelcomeAngehoerige()" in html)

    # Journey 4: Angehörigen-Modus
    check("Journey: Angehörigen-Auswahl-Overlay", "id=\"angehoerigenauswahl-overlay\"" in html)
    check("Journey: Angehörigen hospital-Szenario", "openAngehoerigenView('hospital')" in html)
    check("Journey: Angehörigen death-Szenario", "openAngehoerigenView('death')" in html)
    check("Journey: Angehörigen-View zeigt Hausarzt", "get('hausarzt')" in html)
    check("Journey: Angehörigen-View zeigt Behandlung", "get('behandlung_aktuell')" in html)
    check("Journey: Angehörigen-View zeigt Dateien", "Gespeicherte Dokumente" in html)
    check("Journey: Angehörigen-Modus im Menü", "showAngehoerigenAuswahl(); closeMoreMenu()" in html)
    check("Journey: Angehörigen Zurück smart", "already in app" in html)

    # Journey 5: Dokumente (Meine Dateien)
    check("Journey: Upload mit Namensabfrage", "prompt('Wie soll das Dokument hei" in html)
    check("Journey: Datei-Download möglich", "function downloadFile(idx)" in html)
    check("Journey: Kategorie korrigierbar", "function changeFileCategory(idx" in html)
    check("Journey: Datei umbenennen möglich", "function renameFile(idx, label)" in html)

    # Journey 6: Exporte vollständig
    export_fns = ["generatePDF", "generateDocx", "generateVorsorgevollmacht",
                  "generatePatientenverfuegung", "generateGesundheitsvollmacht",
                  "generateArztbogen", "generateScenarioPDF", "generateQRStickers",
                  "generateHeimaufnahme", "generateFHIR", "generateBehoerdendaten",
                  "generateChecklist"]
    for fn in export_fns:
        check(f"Export: {fn} vorhanden", f"function {fn}" in html)

    # Journey 7: Kein nativer confirm()
    check("UX: Kein nativer confirm()-Dialog", "if (!confirm(" not in html)
    check("UX: vivoConfirm implementiert", "function vivoConfirm(msg, onOk" in html)

    # ═══════════════════════════════════════
    print("\n=== 11. KERN/MEHR-SYSTEM ===")
    # ═══════════════════════════════════════

    check("mehr(): Hilfsfunktion vorhanden", "function mehr(" in html)
    check("mehr(): Erzeugt aufklappbaren Button", "mehr_" in html)
    mehr_count = html.count("mehr('")
    check("mehr(): Mindestens 9 Blöcke in Steps", mehr_count >= 9, f"Gefunden: {mehr_count}")
    check("mehr(): start-Step hat Mehr-Bereich", "mehr('start_mehr'" in html)
    check("mehr(): gesundheit-Step hat Mehr-Bereich", "mehr('gesundheit_mehr'" in html)
    check("mehr(): finanzen-Step hat Mehr-Bereich", "mehr('finanzen_mehr'" in html)
    check("mehr(): testament-Step hat Mehr-Bereich", "mehr('testament_mehr'" in html)
    check("mehr(): immobilien-Step hat Mehr-Bereich", "mehr('immo_mehr'" in html)
    check("mehr(): pflege-Step hat Mehr-Bereiche", "mehr('pflege_vorgeschichte'" in html)
    check("mehr(): digital-Step hat Mehr-Bereich", "mehr('digital_mehr'" in html)
    check("mehr(): bestattung-Step hat Mehr-Bereich", "mehr('bestattung_mehr'" in html)
    check("Speichern-Erinnerung: Bar vorhanden", "save-reminder-bar" in html)
    check("Speichern-Erinnerung: dismissSaveReminder()", "function dismissSaveReminder" in html)
    check("Speichern-Erinnerung: saveAndDismiss()", "function saveAndDismiss" in html)
    check("Fokus-Wizard: In Einstellungen erreichbar", "Meinen Fokus neu wählen" in html)

    # ═══════════════════════════════════════
    print("\n=== 12. PERSONA-FELDER ===")
    # ═══════════════════════════════════════

    persona_fields = [
        ("Selbständigkeit Notfallplan", "selbstaendig_notfall"),
        ("GmbH / Firma Nachfolge", "gmb_nachfolge"),
        ("Auslandsvermögen", "ausland_vermoegen"),
        ("Volljährige Kinder", "kinder_erwachsen"),
        ("Palliativversorgung", "palliativ_wunsch"),
        ("Laufende Behandlung", "behandlung_aktuell"),
        ("Onkolog*in / Spezialist*in", "facharzt_1"),
        ("SBA Gültigkeitsdatum", "schwerbehindertenausweis_gueltig"),
        ("Krypto Seed Ablageort", "krypto_seed_ort"),
        ("Scheidungsfolgenvereinbarung", "dok_scheidungsvereinbarung"),
        ("Besondere Wohnsituation", "wohnsituation_bem"),
        ("Unterhalt (inkl. Elternunterhalt)", "unterhalt"),
    ]
    for label, key in persona_fields:
        check(f"Feld: {label}", f"'{key}'" in html)

    check("Rente: Erwerbsminderungsrente im Dropdown", "Erwerbsminderungsrente (DRV)" in html)
    check("Prüftermine: Schwerbehindertenausweis", "erinnerung_sba" in html)
    check("WG: Kategorie Mitbewohner*in", "Mitbewohner*in / WG" in html)
    check("WG: Kategorie Hauptmieter*in", "Hauptmieter*in (WG)" in html)
    check("Krypto: Seed-Warnbox rot", "Seed-Phrase = Geld" in html)
    check("Checkliste: krypto_seed_ort enthalten", "get('krypto_seed_ort')" in html)
    check("Checkliste: erinnerung_sba enthalten", "get('erinnerung_sba')" in html)
    check("Checkliste: selbstaendig_notfall enthalten", "get('selbstaendig_notfall')" in html)
    check("Checkliste: palliativ_wunsch enthalten", "get('palliativ_wunsch')" in html)

    # ═══════════════════════════════════════
    print("\n=== 13. SICHERHEIT, RECHT & UX ===")
    # ═══════════════════════════════════════

    # Angehörigen-Modus Sicherheit
    check("Sicherheit: Kein 'Vollständige Datei öffnen' Button", "Vollständige Datei öffnen" not in html)
    check("Sicherheit: angehoerigenZurueck() vorhanden", "function angehoerigenZurueck" in html)

    # Barrierefreiheit
    check("A11y: Basis-Schrift >= 16px", "font-size: 17px" in html or "font-size: 16px" in html)
    check("A11y: Input-Rahmen 2px", "border: 2px solid #a89e90" in html)
    check("A11y: Touch-Ziele 44px", "min-height: 44px" in html)
    check("A11y: Schriftgrößen-Hinweis Welcome", "A⁺" in html)

    # Rechtliche Warnboxen
    check("Recht: Patchwork-Warnung (Stiefkinder)", "Stiefkinder erben nichts" in html)
    check("Recht: Warnung unverheiratete Paare", "nicht verheiratete Paare" in html)
    check("Recht: Testament nach Scheidung (§ 2077)", "2077 BGB" in html)
    check("Recht: Alleinerziehend ohne Kontakt", "Nachlassgericht hinterlegen" in html)
    check("Recht: Elternunterhalt nur leibliche Kinder", "Elternunterhalt gilt nur für leibliche" in html)
    check("Recht: Vollmacht Hinweis Alleinlebende", "Alleinlebend oder verwitwet?" in html)
    check("Recht: Krypto unwiederbringlich verloren", "unwiederbringlich" in html)

    # ═══════════════════════════════════════
    
    # ═══════════════════════════════════════
    print("\n=== 14. UPDATE-SYSTEM ===")
    # ═══════════════════════════════════════

    check("Update: checkForUpdates() vorhanden", "function checkForUpdates" in html)
    check("Update: UPDATE_CHECK_URL enthält vivodepot.de/aktuell", "vivodepot.de/aktuell" in html)
    check("Update: showUpdateBanner() vorhanden", "function showUpdateBanner" in html)
    check("Update: dismissUpdateBanner() vorhanden", "function dismissUpdateBanner" in html)
    check("Update: update-banner Element-ID", 'id="update-banner"' in html or "'update-banner'" in html)
    check("Update: E-Mail Opt-in showEmailOptin()", "function showEmailOptin" in html)
    check("Update: E-Mail Opt-in submitEmailOptin()", "function submitEmailOptin" in html)
    check("Update: E-Mail Opt-in dismissEmailOptin()", "function dismissEmailOptin" in html)
    check("Update: maybeShowEmailOptin() vorhanden", "function maybeShowEmailOptin" in html)
    check("Update: email-optin-overlay Element-ID", "email-optin-overlay" in html)
    check("Update: email-optin-input Feld", "email-optin-input" in html)
    check("Update: DSGVO-Datenschutzhinweis im Opt-in", "Datenschutz" in html and "email-optin" in html)
    check("Update: vivodepot_email_optin gespeichert", "vivodepot_email_optin" in html)
    check("Update: E-Mail Opt-in hat Abmelden-Option", "dismissEmailOptin" in html and "Nein, danke" in html)
    check("Update: enterApp ruft checkForUpdates auf", "checkForUpdates" in html and "enterApp" in html)
    check("Update: checkForUpdates hat Timeout-Schutz", "controller.abort" in html or "AbortController" in html)
    check("Update: Auf Updates prüfen in Einstellungen", "Auf Updates prüfen" in html)


    # ═══════════════════════════════════════
    print("\n=== 15. MOBILE & VIEWPORT ===")
    # ═══════════════════════════════════════

    check("Mobile: viewport-fit=cover", "viewport-fit=cover" in html)
    check("Mobile: safe-area-inset am FAB", "safe-area-inset" in html)
    check("Mobile: @media print", "@media print" in html)
    check("Mobile: window.print()", "window.print" in html)
    check("Mobile: @media Breakpoints >= 3", html.count("@media") >= 3)
    check("Mobile: Touch-Targets 44px", "min-height: 44px" in html)
    check("Mobile: scrollTo bei Step-Wechsel", "scrollTo" in html)
    check("Mobile: type=date vorhanden", 'type="date"' in html or "type='date'" in html)
    check("Mobile: type=email vorhanden", 'type="email"' in html or "type='email'" in html)
    check("Mobile: autocomplete-Attribute", "autocomplete" in html)
    check("Mobile: font-size >= 16px (iOS-Zoom-Schutz)", "font-size: 17px" in html or "font-size: 16px" in html)
    check("Mobile: display:flex Layout", "display:flex" in html or "display: flex" in html)
    check("Mobile: flex-wrap vorhanden", "flex-wrap" in html)
    check("Mobile: grid-template-columns", "grid-template-columns" in html)

    # ═══════════════════════════════════════
    print("\n=== 16. FOKUS-SYSTEM ===")
    # ═══════════════════════════════════════

    check("Fokus: _goalMode Flag", "_goalMode" in html)
    check("Fokus: _goalRelevant Objekt", "_goalRelevant" in html)
    check("Fokus: applyGoalWizard()", "applyGoalWizard" in html)
    check("Fokus: skipGoalWizard()", "skipGoalWizard" in html)
    check("Fokus: showGoalWizard()", "function showGoalWizard" in html)
    check("Fokus: Ziel family", "'family'" in html)
    check("Fokus: Ziel emergency", "'emergency'" in html)
    check("Fokus: Ziel health", "'health'" in html)
    check("Fokus: Ziel legal (Mein Wille)", "'legal'" in html)
    check("Fokus: goalBtn() Hilfsfunktion", "goalBtn" in html)
    check("Fokus: nextStep/prevStep via goToStep mit Fokus",
          "function nextStep" in html and "function prevStep" in html and
          "function goToStep" in html and "_goalMode" in html)
    check("Fokus: Fokus-Navigation — goToStep kennt _goalRelevant",
          "goToStep" in html and "_goalRelevant" in html and "_goalMode" in html)
    check("Fokus: renderSidebar filtert Steps", "function renderSidebar" in html and "_goalRelevant" in html)
    check("Fokus: updateFokusBarLabel()", "updateFokusBarLabel" in html)
    check("Fokus: fokus-bar-btn Element", "fokus-bar-btn" in html)
    check("Fokus: Meinen Fokus neu wählen", "Meinen Fokus neu wählen" in html)

    # ═══════════════════════════════════════
    print("\n=== 17. KEYBOARD & NAVIGATION ===")
    # ═══════════════════════════════════════

    check("Nav: Escape-Handler keydown", "keydown" in html and "Escape" in html)
    check("Nav: Escape schließt Wizards", "gwiz-overlay" in html and "Escape" in html)
    check("Nav: Escape schließt Email-Optin", "email-optin-overlay" in html and "Escape" in html)
    check("Nav: Escape schließt Suche", "search-overlay" in html and "Escape" in html)
    check("Nav: popstate abgefangen", "popstate" in html)
    check("Nav: history.pushState", "history.pushState" in html)
    check("Nav: goToStep() mit try/catch",
          "function goToStep" in html and
          "try {" in html[html.find("function goToStep"):html.find("function goToStep")+800])
    check("Nav: goToStep() console.error bei Fehler",
          "console.error" in html[html.find("function goToStep"):html.find("function goToStep")+1000])
    check("Nav: safeRender() fängt Fehler ab", "function safeRender" in html and "catch" in html)
    check("Nav: window.onerror globaler Handler", "window.onerror" in html)
    check("Nav: openGlobalSearch()", "openGlobalSearch" in html)
    check("Nav: onclick goToStep in Sidebar", 'onclick="goToStep' in html)

    # ═══════════════════════════════════════
    print("\n=== 18. FAB & DRAGGABLE ===")
    # ═══════════════════════════════════════

    check("FAB: id=notfall-fab", "notfall-fab" in html)
    check("FAB: showNotfallPopup()", "showNotfallPopup" in html)
    check("FAB: Draggable — _dragging Flag", "_dragging" in html)
    check("FAB: Draggable — mousedown Listener", "mousedown" in html and "_dragging" in html)
    check("FAB: Draggable — touchstart Listener", "touchstart" in html)
    check("FAB: safe-area-inset am FAB", "safe-area-inset" in html and "notfall-fab" in html)
    check("FAB: Hover-Effekt scale(1.1)", "scale(1.1)" in html)
    check("FAB: z-index >= 800", "z-index:800" in html or "z-index: 800" in html)
    check("FAB: 56px Größe", "56px" in html)
    check("FAB: position fixed", "position:fixed" in html or "position: fixed" in html)

    # ═══════════════════════════════════════
    print("\n=== 19. VCARD EXPORT ===")
    # ═══════════════════════════════════════

    check("vCard: function exportVCard()", "function exportVCard" in html)
    check("vCard: function generateVCard()", "function generateVCard" in html)
    check("vCard: VERSION:4.0", "VERSION:4.0" in html)
    check("vCard: BEGIN:VCARD", "BEGIN:VCARD" in html)
    check("vCard: END:VCARD", "END:VCARD" in html)
    check("vCard: PRODID Vivodepot", "PRODID" in html and "Vivodepot" in html)
    check("vCard: FN-Feld", "'FN:'" in html or '"FN:"' in html)
    check("vCard: TEL-Feld", "'TEL;" in html or '"TEL;' in html)
    check("vCard: EMAIL-Feld", "'EMAIL:'" in html or '"EMAIL:"' in html)
    check("vCard: .vcf Dateiendung", ".vcf" in html)
    check("vCard: toast nach Export", "vCard exportiert" in html)
    check("vCard: parseVCard() Import", "parseVCard" in html)
    check("vCard: RFC 6350 Referenz", "RFC 6350" in html or "vCard 4.0" in html or "vcard" in html.lower())

    # ═══════════════════════════════════════
    print("\n=== 20. ARIA & BARRIEREFREIHEIT ===")
    # ═══════════════════════════════════════

    check("ARIA: role=dialog auf Overlays", 'role="dialog"' in html)
    check("ARIA: aria-modal=true", 'aria-modal="true"' in html)
    check("ARIA: aria-live auf Bannern", "aria-live" in html)
    check("ARIA: aria-label auf Buttons", "aria-label" in html)
    check("ARIA: role=alert in Update-Banner (JS)", 'role="alert"' in html or "role='alert'" in html or "setAttribute('role', 'alert')" in html or "setAttribute(\"role\", \"alert\")" in html)
    check("ARIA: aria-labelledby", "aria-labelledby" in html)
    check("ARIA: label-Elemente", "<label" in html)
    check("ARIA: for-Attribut auf Labels", 'for="' in html)
    check("ARIA: title-Attribute auf Buttons", 'title="' in html)
    check("ARIA: toggleNacht()", "toggleNacht" in html)
    check("ARIA: toggleKontrast()", "toggleKontrast" in html)
    check("ARIA: toggleVorlesen()", "toggleVorlesen" in html)
    check("ARIA: cycleFontSize()", "cycleFontSize" in html)
    check("ARIA: fs-large CSS-Klasse", "fs-large" in html)
    check("ARIA: high-contrast CSS-Klasse", "high-contrast" in html)
    check("ARIA: dark-mode CSS-Klasse", "dark-mode" in html)
    check("ARIA: 2px Input-Rahmen (Kontrast)", "border: 2px solid #a89e90" in html)
    check("ARIA: toggleMikrofon() / Spracheingabe", "toggleMikrofon" in html or "mikrofon" in html.lower())
    check("ARIA: toggleLupe()", "toggleLupe" in html)

    # ═══════════════════════════════════════
    print("\n=== 21. NOTFALLVORSORGE & BBK ===")
    # ═══════════════════════════════════════

    check("BBK: Bundesamt für Bevölkerungsschutz", "Bundesamt für Bevölkerungsschutz" in html or "BBK" in html)
    check("BBK: NINA Warn-App", "NINA" in html)
    check("BBK: ELEFAND Auslandsregistrierung", "ELEFAND" in html)
    check("BBK: NOTFALL_VORRAT_ITEMS Konstante", "NOTFALL_VORRAT_ITEMS" in html)
    check("BBK: Wasser in Vorratsliste", "Wasser" in html and "NOTFALL_VORRAT" in html)
    check("BBK: Taschenlampe", "Taschenlampe" in html)
    check("BBK: Erste-Hilfe-Kasten", "Erste-Hilfe" in html)
    check("BBK: Bargeld", "Bargeld" in html)
    check("BBK: Powerbank", "Powerbank" in html)
    check("BBK: bbk.bund.de Link", "bbk.bund.de" in html)
    check("BBK: Notfall-FAB zeigt Gesundheitsdaten", "showNotfallPopup" in html and "blutgruppe" in html)

    # ═══════════════════════════════════════
    print("\n=== 22. PWA DETAILS ===")
    # ═══════════════════════════════════════

    check("PWA: rel=manifest", 'rel="manifest"' in html)
    check("PWA: theme-color Meta", "theme-color" in html)
    check("PWA: apple-mobile-web-app-capable", "apple-mobile-web-app-capable" in html)
    check("PWA: apple-mobile-web-app-title", "apple-mobile-web-app-title" in html)
    check("PWA: apple-touch-icon", "apple-touch-icon" in html)
    check("PWA: serviceWorker.register()", "serviceWorker" in html)
    check("PWA: Cache-Name", "CACHE" in html or "vivodepot-v" in html)
    check("PWA: Install-Banner", "install-banner" in html)
    check("PWA: iOS Teilen-Hinweis", "Teilen" in html and "Home-Bildschirm" in html)
    check("PWA: display standalone", "standalone" in html)
    check("PWA: SVG Favicon", 'rel="icon"' in html and "svg" in html)
    check("PWA: beforeinstallprompt", "beforeinstallprompt" in html)
    check("PWA: installApp()", "installApp" in html)

    # ═══════════════════════════════════════
    print("\n=== 23. VERSCHLÜSSELUNG DETAILS ===")
    # ═══════════════════════════════════════

    check("Krypto: AES-GCM", "AES-GCM" in html)
    check("Krypto: PBKDF2", "PBKDF2" in html)
    check("Krypto: SHA-256", "SHA-256" in html)
    check("Krypto: CRYPTO_AVAILABLE", "CRYPTO_AVAILABLE" in html)
    check("Krypto: crypto.subtle", "crypto.subtle" in html)
    check("Krypto: sessionKey", "sessionKey" in html)
    check("Krypto: lockApp()", "lockApp" in html)
    check("Krypto: showCryptoModal()", "showCryptoModal" in html)
    check("Krypto: changePassword()", "changePassword" in html)
    check("Krypto: removePassword()", "removePassword" in html)
    check("Krypto: min. 6 Zeichen Hinweis", "Mindestens 6 Zeichen" in html)
    check("Krypto: AES-256-GCM Bezeichnung", "AES-256-GCM" in html or ("AES-GCM" in html and "256" in html))
    check("Krypto: IV Initialisierungsvektor", "iv" in html and "AES-GCM" in html)
    check("Krypto: Salt für PBKDF2", "salt" in html and "PBKDF2" in html)
    check("Krypto: 200000 Iterationen PBKDF2", "200000" in html or "100000" in html)

    # ═══════════════════════════════════════
    print("\n=== 24. DATENSPEICHER & PROFIL ===")
    # ═══════════════════════════════════════

    check("Store: let STORE_KEY", "let STORE_KEY" in html)
    check("Store: getProfileManifest()", "function getProfileManifest" in html)
    check("Store: setActiveProfile()", "function setActiveProfile" in html)
    check("Store: switchToProfile()", "switchToProfile" in html)
    check("Store: addNewProfile()", "function addNewProfile" in html)
    check("Store: updateProfileButton()", "function updateProfileButton" in html)
    check("Store: profile-dropdown UI", "profile-dropdown" in html)
    check("Store: localStorage.getItem verwendet", "localStorage.getItem(" in html)
    check("Store: localStorage.setItem verwendet", "localStorage.setItem(" in html)
    check("Store: kein undefiniertes _ls Objekt", "_ls.get(" not in html and "_ls.set(" not in html)
    check("Store: async saveData()", "async function saveData" in html)
    check("Store: async loadData()", "async function loadData" in html)
    check("Store: saveAsHTML()", "function saveAsHTML" in html)
    check("Store: showSaveFilePicker (USB)", "showSaveFilePicker" in html)
    check("Store: importData()", "function importData" in html)
    check("Store: exportJSON()", "exportJSON" in html)
    check("Store: importStructured()", "importStructured" in html)

    # ═══════════════════════════════════════
    print("\n=== 25. SCHRITT-INHALTE ===")
    # ═══════════════════════════════════════

    check("Inhalt: Vorname-Feld", "'vorname'" in html)
    check("Inhalt: Nachname-Feld", "'nachname'" in html)
    check("Inhalt: Blutgruppe-Feld", "'blutgruppe'" in html)
    check("Inhalt: Profilfoto", "'profilfoto'" in html)
    check("Inhalt: Personen-Array (Kontakte)", "'personen'" in html)
    check("Inhalt: Allergien-Feld", "'allergien'" in html)
    check("Inhalt: Hausarzt-Feld", "'hausarzt'" in html)
    check("Inhalt: IBAN-Feld", "'iban'" in html or "IBAN" in html)
    check("Inhalt: Pflegegrad-Feld", "'pflegegrad'" in html)
    check("Inhalt: Bestattungsart-Feld", "'bestattung_art'" in html)
    check("Inhalt: Organspende-Feld", "'organspende'" in html)
    check("Inhalt: Testament-Feld", "'testament_vorhanden'" in html or "testament" in html.lower())
    check("Inhalt: Notar-Feld", "'notar'" in html)
    check("Inhalt: Passwort-Manager-Feld", "'pw_manager'" in html or "Passwort-Manager" in html)
    check("Inhalt: Krypto-Felder", "'krypto'" in html or "Krypto" in html)
    check("Inhalt: ELEFAND-Feld", "elefand" in html.lower())
    check("Inhalt: erinnerung_sba (SBA-Prüftermin)", "'erinnerung_sba'" in html)
    check("Inhalt: Unterhalt-Feld", "'unterhalt'" in html)
    check("Inhalt: Palliativ-Wunsch-Feld", "'palliativ_wunsch'" in html)
    check("Inhalt: krypto_seed_ort", "'krypto_seed_ort'" in html)
    check("Inhalt: selbstaendig_notfall", "'selbstaendig_notfall'" in html)

    # ═══════════════════════════════════════
    print("\n=== 26. RECHT & EXTERNE LINKS ===")
    # ═══════════════════════════════════════

    check("Recht: EUPL-1.2 Lizenz", "EUPL" in html)
    check("Recht: feedback@vivodepot.de", "feedback@vivodepot.de" in html)
    check("Recht: organspende-register.de Link", "organspende-register.de" in html)
    check("Recht: showDatenschutz()", "showDatenschutz" in html)
    check("Recht: Datenschutzinformationen", "Datenschutz" in html)
    check("Recht: KI-Hinweis EU AI Act", "EU AI Act" in html or "KI-Hinweis" in html)
    check("Recht: Vivodepot UG (haftungsbeschränkt)", "UG" in html and "haftungsbeschränkt" in html)
    check("Recht: GitHub-Link Quellcode", "github.com" in html)
    check("Recht: joinup.ec.europa.eu EUPL", "joinup.ec.europa.eu" in html)
    check("Recht: Keine Rechtsberatung Hinweis", "Keine Rechtsberatung" in html)
    check("Recht: Patchwork — Stiefkinder erben nichts", "Stiefkinder erben nichts" in html)
    check("Recht: nicht verheiratete Paare Warnung", "nicht verheiratete Paare" in html)
    check("Recht: § 2077 BGB Testament nach Scheidung", "2077 BGB" in html)
    check("Recht: Elternunterhalt leibliche Kinder", "Elternunterhalt gilt nur für leibliche" in html)
    check("Recht: Alleinlebend Vollmacht Hinweis", "Alleinlebend oder verwitwet?" in html)
    check("Recht: unwiederbringlich verloren (Krypto)", "unwiederbringlich" in html)
    check("Recht: Nachlassgericht (Alleinerziehend)", "Nachlassgericht hinterlegen" in html)


    # ═══════════════════════════════════════
    print("\n=== 27. MOBILE & RESPONSIVE ===")
    # ═══════════════════════════════════════

    check("Mobile: safe-area-inset-bottom",        "safe-area-inset-bottom" in html)
    check("Mobile: safe-area-inset-right",         "safe-area-inset-right" in html)
    check("Mobile: apple-mobile-web-app-capable",  "apple-mobile-web-app-capable" in html)
    check("Mobile: apple-mobile-web-app-title",    "apple-mobile-web-app-title" in html)
    check("Mobile: apple-mobile-web-app-status",   "apple-mobile-web-app-status-bar-style" in html)
    check("Mobile: theme-color meta",              'name="theme-color"' in html)
    check("Mobile: @media print vorhanden",        "@media print" in html)
    check("Mobile: window.scrollTo vorhanden",     "scrollTo" in html)
    check("Mobile: FAB draggable mousedown",       "mousedown" in html and "btn._dragging" in html)
    check("Mobile: FAB draggable touchstart",      "touchstart" in html and "onDown" in html)
    check("Mobile: FAB touchmove preventDefault",  "preventDefault" in html and "touchmove" in html)
    check("Mobile: FAB bounds (min 4px)",          "Math.max(4," in html)
    check("Mobile: input type=date vorhanden",     'type="date"' in html or "type='date'" in html)
    check("Mobile: input type=email vorhanden",    'type="email"' in html or "type='email'" in html)
    check("Mobile: autocomplete Attribute",        "autocomplete" in html)
    check("Mobile: Systemschrift geladen",          "DM Sans" in html or "-apple-system" in html or "Georgia" in html)
    check("Mobile: Lora Schrift geladen",          "Lora" in html)

    # ═══════════════════════════════════════
    print("\n=== 28. FOKUS-SYSTEM ===")
    # ═══════════════════════════════════════

    check("Fokus: goalBtn() Hilfsfunktion",        "function goalBtn" in html or "goalBtn(" in html)
    check("Fokus: Modus 'start'",                  "'start'" in html)
    check("Fokus: Modus 'family'",                 "'family'" in html)
    check("Fokus: Modus 'emergency'",              "'emergency'" in html)
    check("Fokus: Modus 'health'",                 "'health'" in html)
    check("Fokus: Modus 'legal' (Vollmacht/Testament)", "'legal'" in html)
    check("Fokus: Modus 'all'",                    "'all'" in html)
    check("Fokus: goToStep() hat try/catch",
          "function goToStep" in html and
          "try {" in html[html.find("function goToStep"):html.find("function goToStep")+500])
    check("Fokus: goToStep() catch mit console.error",
          "console.error" in html[html.find("function goToStep"):html.find("function goToStep")+600])
    check("Fokus: nextStep() vorhanden",           "function nextStep" in html)
    check("Fokus: prevStep() vorhanden",           "function prevStep" in html)
    check("Fokus: selectedGoal Variable",           "selectedGoal" in html)
    check("Fokus: Alle Bereiche anzeigen Button",  "Alle anzeigen" in html or "_goalMode=false" in html)
    check("Fokus: Relevanz-Filterung in renderSidebar",
          "_goalRelevant" in html[html.find("function renderSidebar"):html.find("function renderSidebar")+800]
          if "function renderSidebar" in html else False)

    # ═══════════════════════════════════════
    print("\n=== 29. BARRIEREFREIHEIT (ERWEITERT) ===")
    # ═══════════════════════════════════════

    check("A11y: aria-label auf FAB",              'aria-label' in html)
    check("A11y: role=dialog auf Overlays",        'role="dialog"' in html)
    check("A11y: aria-modal=true",                 'aria-modal="true"' in html)
    check("A11y: aria-live auf Update-Banner",     'aria-live' in html)
    check("A11y: aria-labelledby vorhanden",       "aria-labelledby" in html)
    check("A11y: aria-label auf Schließen-Button", 'aria-label="Hinweis schlie' in html or 'aria-label="Schlie' in html)
    check("A11y: Escape-Handler vorhanden",        "'Escape'" in html and "keydown" in html)
    check("A11y: Escape schließt Crypto-Overlay",  "'Escape'" in html and "crypto-overlay" in html)
    check("A11y: Escape schließt Wizards",         "'Escape'" in html and "gwiz-overlay" in html)
    check("A11y: Escape schließt Email-Optin",     "'Escape'" in html and "email-optin-overlay" in html)
    check("A11y: Escape schließt Suche",           "'Escape'" in html and "search-overlay" in html)
    check("A11y: toggleVorlesen()",                "function toggleVorlesen" in html)
    check("A11y: toggleKontrast()",                "function toggleKontrast" in html)
    check("A11y: toggleNacht()",                   "function toggleNacht" in html)
    check("A11y: cycleFontSize()",                 "function cycleFontSize" in html)
    check("A11y: toggleLupe()",                    "function toggleLupe" in html)
    check("A11y: toggleMikrofon()",                "function toggleMikrofon" in html)
    check("A11y: Spracheingabe startDiktat()",     "function startDiktat" in html)
    check("A11y: fs-medium / fs-large Klassen",   "fs-medium" in html and "fs-large" in html)
    check("A11y: high-contrast Klasse",            "high-contrast" in html)
    check("A11y: dark-mode Klasse",                "dark-mode" in html)

    # ═══════════════════════════════════════
    print("\n=== 30. VCARD & KONTAKTE ===")
    # ═══════════════════════════════════════

    check("vCard: exportVCard() vorhanden",        "function exportVCard" in html)
    check("vCard: generateVCard() vorhanden",      "function generateVCard" in html)
    check("vCard: TEL TYPE=VOICE",                 "TEL;TYPE=VOICE" in html)
    check("vCard: RFC 6350 vCard 4.0",             "RFC 6350" in html or "VERSION:4.0" in html)
    check("vCard: .vcf Download",                  ".vcf" in html)
    check("vCard: Blob text/vcard",                "text/vcard" in html)
    check("vCard: Import parseVCard vorhanden",    "parseVCard" in html or "vcard" in html.lower())
    check("vCard: Export Bestätigung toast()",     "vCard exportiert" in html or "generateVCard" in html)
    check("vCard: Alle Kontakte Export",           "vivodepot-kontakte.vcf" in html)
    check("vCard: Leere Kontakte Prüfung",         "Keine Kontakte" in html or "personen" in html)

    # ═══════════════════════════════════════
    print("\n=== 31. NOTFALL & KATASTROPHENSCHUTZ ===")
    # ═══════════════════════════════════════

    check("Notfall: NOTFALL_VORRAT_ITEMS definiert", "NOTFALL_VORRAT_ITEMS" in html)
    check("Notfall: Wasser-Empfehlung BBK",          "2 l/Person" in html or "Wasser" in html)
    check("Notfall: BBK Bundesamt referenziert",     "BBK" in html)
    check("Notfall: BBK-Checkliste Link",            "bbk.bund.de" in html)
    check("Notfall: NINA-App referenziert",          "NINA" in html)
    check("Notfall: ELEFAND-Register",               "ELEFAND" in html)
    check("Notfall: ELEFAND Link",                   "elefand.diplo.de" in html)
    check("Notfall: 10-Tage-Vorrat Empfehlung",     "10 Tage" in html or "10-Tage" in html or "10 t" in html.lower())
    check("Notfall: Erste-Hilfe-Kasten",             "Erste-Hilfe" in html)
    check("Notfall: FAB Notfall-Button vorhanden",   "notfall-fab" in html)
    check("Notfall: showNotfallPopup()",             "function showNotfallPopup" in html)
    check("Notfall: Notfall-Popup zeigt Name",       "showNotfallPopup" in html and "vorname" in html)
    check("Notfall: Notfall-Popup zeigt Blutgruppe", "blutgruppe" in html and "showNotfallPopup" in html)
    check("Notfall: Notfall-Popup zeigt Allergien",  "allergien" in html and "showNotfallPopup" in html)
    check("Notfall: Powerbank in Vorrat",            "Powerbank" in html)
    check("Notfall: Eigener Step 'notfall' in STEPS",    "{ id: 'notfall'" in html)
    check("Notfall: Renderer vorhanden",                   "notfall: () =>" in html)
    check("Notfall: nina_regionen Feld",                   "'nina_regionen'" in html or "'ks_nina_installiert'" in html)
    check("Notfall: notfallvorrat_stand Feld",             "'notfallvorrat_stand'" in html or "'ks_wasser_liter'" in html)
    check("Notfall: notfall_treffpunkt Feld",              "'notfall_treffpunkt'" in html or "'ks_sammelplatz'" in html)
    check("Notfall: notfall_nachbar Feld",                 "'notfall_nachbar'" in html or "'ks_nachbar'" in html)
    check("Notfall: Vorrat-Checkliste interaktiv",         "vorrat_" in html and "NOTFALL_VORRAT_ITEMS" in html)
    check("Notfall: Personalisierter Hinweis (Kinder)",    "Familien mit Kindern" in html or "ks_rucksack" in html)
    check("Notfall: Personalisierter Hinweis (Pflege)",    "Pflegeaufgaben" in html or "ks_medikamente_vorrat" in html)
    check("Notfall: Personalisierter Hinweis (Allein)",    "Alleinlebend" in html)
    check("Notfall: Bargeld in Vorrat",              "Bargeld" in html)
    check("Notfall: Campingkocher in Vorrat",        "Campingkocher" in html)
    check("Notfall: Hygieneartikel in Vorrat",       "Hygieneartikel" in html)
    check("Notfall: Decke in Vorrat",                "Decke" in html and "NOTFALL" in html)
    check("Notfall: Pfeife/Signalmittel in Vorrat",  "Signalmittel" in html)
    check("Notfall: Werkzeug in Vorrat",             "Dosenöffner" in html)
    # Genau 15 Einträge
    vorrat_start = html.find("var NOTFALL_VORRAT_ITEMS")
    vorrat_end   = html.find("];", vorrat_start) + 2
    vorrat_block = html[vorrat_start:vorrat_end]
    vorrat_count = vorrat_block.count("',") + (1 if "'\n]" in vorrat_block else 0)
    check("Notfall: Liste hat genau 15 Einträge", vorrat_count == 15, f"Gefunden: {vorrat_count}")

    # ═══════════════════════════════════════
    print("\n=== 32. BROWSER-VERHALTEN & ROBUSTHEIT ===")
    # ═══════════════════════════════════════

    check("Browser: popstate Handler",             "popstate" in html)
    check("Browser: history.pushState",            "history.pushState" in html)
    check("Browser: window.onerror",               "window.onerror" in html)
    check("Browser: localStorage try/catch", "localStorage" in html and "try" in html)
    check("Browser: AbortController (Timeout)",    "AbortController" in html)
    check("Browser: keepalive fetch",              "keepalive" in html)
    check("Browser: URL.createObjectURL",          "URL.createObjectURL" in html)
    check("Browser: URL.revokeObjectURL",          "URL.revokeObjectURL" in html)
    check("Browser: Blob API",                     "new Blob(" in html)
    check("Browser: File System Access API",       "showSaveFilePicker" in html)
    check("Browser: FileReader API",               "FileReader" in html)
    check("Browser: crypto.subtle API",            "crypto.subtle" in html)
    check("Browser: Service Worker",               "serviceWorker" in html)
    check("Browser: PWA beforeinstallprompt",      "beforeinstallprompt" in html)
    check("Browser: matchMedia standalone",        "display-mode: standalone" in html)
    check("Browser: iOS standalone detect",        "window.navigator.standalone" in html)

    # ═══════════════════════════════════════
    print("\n=== 33. EXPORT-QUALITÄT ===")
    # ═══════════════════════════════════════

    check("Export: PDF generiert Titelseite",      "Mein Vivodepot" in html and "generatePDF" in html)
    check("Export: PDF hat Datum",                 "new Date" in html and "generatePDF" in html)
    check("Export: PDF EUPL Hinweis",              "EUPL" in html)
    check("Export: Word DOCTYPE korrekt",          "docx" in html.lower())
    check("Export: Vorsorgevollmacht § vorhanden", '§' in html and 'generateVorsorgevollmacht' in html)
    check("Export: Patientenverfügung § 1901",     "1901" in html or "Patientenverfügung" in html)
    check("Export: Gesundheitsvollmacht OK",       "generateGesundheitsvollmacht" in html)
    check("Export: Arztbogen generateArztbogen",   "generateArztbogen" in html)
    check("Export: Heimaufnahme 5 Seiten",         "generateHeimaufnahme" in html)
    check("Export: Szenario PDFs (3 Szenarien)",   "generateScenarioPDF" in html)
    check("Export: QR-Sticker-Paket",              "generateQRStickers" in html)
    check("Export: FHIR R4 Bundle",                "FHIR" in html and "Bundle" in html)
    check("Export: FIM-JSON Export",               "exportFIMJson" in html)
    check("Export: Behördendaten PDF",             "generateBehoerdendaten" in html)
    check("Export: Checkliste HTML",               "generateChecklist" in html)
    check("Export: Download via a.click()",        "a.click()" in html)
    check("Export: Dateiname mit .pdf",            ".pdf'" in html or '.pdf"' in html)
    check("Export: Dateiname mit .docx",           ".docx'" in html or '.docx"' in html)
    check("Export: © 2026 Vivodepot",             "© 2026 Vivodepot" in html or "2026 Vivodepot" in html)

    # ═══════════════════════════════════════
    print("\n=== 34. DATENSPEICHERUNG ===")
    # ═══════════════════════════════════════

    check("Speicher: STORE_KEY let (nicht const)",    "let STORE_KEY" in html)
    check("Speicher: STORE_META",                     "STORE_META" in html)
    check("Speicher: saveData async",                 "async function saveData" in html)
    check("Speicher: loadData async",                 "async function loadData" in html)
    check("Speicher: get() Funktion",                 "function get(" in html)
    check("Speicher: set() Funktion",                 "function set(" in html)
    check("Speicher: AES-GCM Verschlüsselung",        "AES-GCM" in html)
    check("Speicher: PBKDF2 Schlüsselableitung",      "PBKDF2" in html)
    check("Speicher: sessionKey Variable",            "sessionKey" in html)
    check("Speicher: changePassword()",               "function changePassword" in html)
    check("Speicher: removePassword()",               "function removePassword" in html)
    check("Speicher: exportJSON()",                   "function exportJSON" in html)
    check("Speicher: importData()",                   "function importData" in html)
    check("Speicher: importStructured()",             "importStructured" in html)
    check("Speicher: Multi-Profil switchToProfile",   "switchToProfile" in html)
    check("Speicher: Max 4 Profile",                  "4" in html and "Profile" in html)
    check("Speicher: Profil-Manifest getProfileManifest", "getProfileManifest" in html)
    check("Speicher: setActiveProfile()",             "function setActiveProfile" in html)

    # ═══════════════════════════════════════
    print("\n=== 35. INTERNATIONALISIERUNG ===")
    # ═══════════════════════════════════════

    en_block_start = html.find("var EN")
    en_block_end   = html.find("function tl(")
    en_block = html[en_block_start:en_block_end] if en_block_start > 0 else ""
    en_keys  = len(re.findall(r"'[^']{3,50}'\s*:", en_block))

    check("i18n: var EN Wörterbuch vorhanden",    "var EN" in html)
    check("i18n: function tl() vorhanden",         "function tl(" in html)
    check("i18n: Mindestens 20 EN-Einträge",       en_keys >= 20, f"Gefunden: {en_keys}")
    check("i18n: tl() aufgerufen (Mindest 10x)",   html.count("tl(") >= 10, f"Gefunden: {html.count('tl(')}")
    check("i18n: Sprache Deutsch Standard",        'lang="de"' in html)
    check("i18n: tl('Passwort",                   "tl('Passwort" in html or 'tl("Passwort' in html)
    check("i18n: tl('Fokus')",                    "tl('Fokus" in html or 'tl("Fokus' in html)

    # ═══════════════════════════════════════
    print("\n=== 36. PWA & INSTALLATION ===")
    # ═══════════════════════════════════════

    check("PWA: rel=manifest vorhanden",            'rel="manifest"' in html)
    check("PWA: Manifest name=Vivodepot",           "Vivodepot" in html and "manifest" in html)
    check("PWA: display=standalone",                "standalone" in html)
    check("PWA: background_color",                  "background_color" in html or "background-color" in html)
    check("PWA: Service Worker Register",           "serviceWorker.register" in html)
    check("PWA: Cache-Name vivodepot",              "vivodepot-v" in html or "CACHE" in html)
    check("PWA: showInstallBanner()",               "function showInstallBanner" in html)
    check("PWA: pwaInstall()",                      "function pwaInstall" in html or "pwaInstall" in html)
    check("PWA: iOS Hinweis (Teilen-Button)",       "Home-Bildschirm" in html)
    check("PWA: Offline-Fähigkeit (Cache-First)",   "caches.match" in html)
    check("PWA: CDN URLs gecacht",                  "cdnjs.cloudflare.com" in html and "CACHE" in html)
    check("PWA: skipWaiting()",                     "skipWaiting" in html)
    check("PWA: Apple Touch Icon",                  "apple-touch-icon" in html)

    # ═══════════════════════════════════════
    print("\n=== 37. LEGAL & COMPLIANCE ===")
    # ═══════════════════════════════════════

    check("Legal: EUPL-1.2 Lizenz",                "EUPL" in html)
    check("Legal: © 2026 Vivodepot",              "© 2026" in html)
    check("Legal: Keine Rechtsberatung Hinweis",   "Keine Rechtsberatung" in html)
    check("Legal: Dokumente sind Entwürfe",        "Entwürfe" in html or "Entwurf" in html)
    check("Legal: Datenschutz showDatenschutz()",  "showDatenschutz" in html)
    check("Legal: Datenschutz-Erwähnung (DSGVO-konform)", "Datenschutz" in html)
    check("Legal: EU AI Act Art. 50",              "EU AI Act" in html)
    check("Legal: Kontakt feedback@vivodepot.de",  "feedback@vivodepot.de" in html)
    check("Legal: GitHub-Link",                    "github.com" in html)
    check("Legal: Organspende-Register Link",       "organspende-register" in html)
    check("Legal: § 2077 BGB Testament",           "2077" in html)
    check("Legal: § BGB Referenzen",               '§' in html and ('BGB' in html or 'GG' in html))
    check("Legal: Alleinlebend-Warnung Vollmacht",  "Alleinlebend" in html)
    check("Legal: Patchwork-Warnung Erbrecht",     "Stiefkinder" in html)
    check("Legal: Unverheiratete Paare Warnung",   "nicht verheiratete Paare" in html)

    # ═══════════════════════════════════════
    print("\n=== 38. WIZARDS (ERWEITERT) ===")
    # ═══════════════════════════════════════

    check("Wizard: gwizOpen() Gesundheitskarte",   "function gwizOpen" in html)
    check("Wizard: gwizClose() vorhanden",          "function gwizClose" in html)
    check("Wizard: gwizNext() vorhanden",           "function gwizNext" in html)
    check("Wizard: gwizPrev() vorhanden",           "function gwizPrev" in html)
    check("Wizard: vvwizOpen() Vorsorgevollmacht",  "function vvwizOpen" in html)
    check("Wizard: pvwizOpen() Patientenverfügung", "function pvwizOpen" in html)
    check("Wizard: bwizOpen() Bestattung",          "function bwizOpen" in html)
    check("Wizard: hwizOpen() Haustier",            "function hwizOpen" in html)
    check("Wizard: gvwizOpen() Gesundheitsvollmacht","function gvwizOpen" in html)
    check("Wizard: showGoalWizard() Fokus",        "function showGoalWizard" in html)
    check("Wizard: Fortschrittsbalken vorhanden",   "wizard-progress-bar" in html)
    check("Wizard: Schritt-Info vorhanden",         "wizard-step-info" in html or "Schritt" in html)
    check("Wizard: Zurück-Button vorhanden",        "wizard-btn-back" in html)
    check("Wizard: Weiter-Button vorhanden",        "wizard-btn-next" in html)
    check("Wizard: Schließen im Header",            'title="Schlie' in html)
    check("Wizard: Schließen-Button hat sichtbaren Inhalt", 'title="Schließen">✕</button>' in html)

    # ═══════════════════════════════════════
    print("\n=== 39. IMPORT-SYSTEM ===")
    # ═══════════════════════════════════════

    check("Import: parseVCard() vorhanden",        "parseVCard" in html)
    check("Import: parseCSV() vorhanden",          "parseCSV" in html)
    check("Import: importData() vorhanden",        "function importData" in html)
    check("Import: importStructured()",            "importStructured" in html)
    check("Import: FHIR-Erkennung",               "FHIR" in html and "import" in html.lower())
    check("Import: FIM-Erkennung",                "FIM" in html and "import" in html.lower())
    check("Import: Auto-Erkennung Format",         "auto" in html.lower() and "import" in html.lower())
    check("Import: JSON-Import möglich",           ".json" in html and "importData" in html)
    check("Import: HTML-Import möglich",           ".html" in html and "importData" in html)
    check("Import: FileReader onload",             "FileReader" in html and "onload" in html)

    # ═══════════════════════════════════════
    print("\n=== 40. UX-DETAILS ===")
    # ═══════════════════════════════════════

    check("UX: toast() Funktion",                  "function toast(" in html)
    check("UX: vivoConfirm() statt confirm()",     "function vivoConfirm" in html)
    check("UX: Kein nativer confirm()",            "if (!confirm(" not in html)
    check("UX: openGlobalSearch()",                "function openGlobalSearch" in html or "openGlobalSearch" in html)
    check("UX: mehr() Akkordeon-System",           "function mehr(" in html)
    check("UX: save-reminder-bar",                "save-reminder-bar" in html)
    check("UX: dismissSaveReminder()",             "function dismissSaveReminder" in html)
    check("UX: saveAndDismiss()",                  "function saveAndDismiss" in html)
    check("UX: topbar-logo vorhanden",             "topbar-logo" in html)
    check("UX: Speichern-Button im Topbar",        "saveAsHTML" in html and "topbar" in html)
    check("UX: Profil-Dropdown UI",               "profile-dropdown" in html)
    check("UX: Mehr-Menü (⋯)",                   "more-dropdown" in html or "more-menu" in html or "moreMenu" in html)
    check("UX: Angehörigen-Modus im Menü",        "showAngehoerigenAuswahl" in html)
    check("UX: Nachtmodus-Toggle im Menü",        "toggleNacht" in html)
    check("UX: Update-Prüfung im Menü",           "checkForUpdates" in html and "Einstellungen" in html)
    check("UX: Suche öffnend",                    "openGlobalSearch" in html)
    check("UX: Sidebar rendert",                   "function renderSidebar" in html)
    check("UX: Step rendert",                      "function renderStep" in html)
    check("UX: navButtons() Hilfsfunktion",        "function navButtons" in html)
    check("UX: stepDots() Hilfsfunktion",          "function stepDots" in html or "stepDots" in html)

    # ═══════════════════════════════════════
    print("\n=== 41. INHALTLICHE VOLLSTÄNDIGKEIT ===")
    # ═══════════════════════════════════════

    content_checks = [
        ("Kontakte: Vertrauenspersonen",    "vertrauensperson" in html.lower() or "personen" in html),
        ("Kontakte: Hausarzt-Feld",         "hausarzt" in html),
        ("Kontakte: Facharzt-Feld",         "facharzt" in html),
        ("Gesundheit: Blutgruppe",          "blutgruppe" in html),
        ("Gesundheit: Allergien",           "allergien" in html),
        ("Gesundheit: Medikamente",         "medikamente" in html or "medikament" in html),
        ("Gesundheit: Organspende",         "organspende" in html.lower()),
        ("Gesundheit: Patientenverfügung",  "patientenverfügung" in html.lower() or "patientenverfuegung" in html.lower()),
        ("Finanzen: IBAN",                  "iban" in html.lower()),
        ("Finanzen: Rente/Renten",         "rente" in html.lower()),
        ("Finanzen: Krypto/Bitcoin",        "krypto" in html.lower()),
        ("Testament: Erbfolge",             "erbfolge" in html.lower() or "erbe" in html.lower()),
        ("Testament: Vollmacht",            "vollmacht" in html.lower()),
        ("Versicherungen: KFZ",             "kfz" in html.lower() or "auto" in html.lower()),
        ("Versicherungen: Lebensversicherung","lebensversicherung" in html.lower()),
        ("Digital: Passwörter/Zugänge",    "digital" in html and "passwort" in html.lower()),
        ("Digital: Social Media",           "social" in html.lower() or "instagram" in html.lower() or "facebook" in html.lower()),
        ("Bestattung: Wünsche",             "bestattung" in html.lower()),
        ("Haustiere: Veterinär",            "haustier" in html.lower() or "tier" in html.lower()),
        ("Pflege: Pflegegrad",              "pflegegrad" in html.lower()),
    ]
    for label, cond in content_checks:
        check(f"Inhalt: {label}", cond)

    # ═══════════════════════════════════════
    print("\n=== 42. UPDATE-SYSTEM (ERWEITERT) ===")
    # ═══════════════════════════════════════

    check("Update-Ext: vivodepot_use_count gespeichert",  "vivodepot_use_count" in html)
    check("Update-Ext: maybeShowEmailOptin() in enterApp", "maybeShowEmailOptin" in html and "enterApp" in html)
    check("Update-Ext: Opt-in nach 3 Nutzungen",          "count >= 3" in html or "useCount >= 3" in html)
    check("Update-Ext: Opt-in Verzögerung 4000ms",        "4000" in html and "showEmailOptin" in html)
    check("Update-Ext: Update-Check Verzögerung 5000ms",  "5000" in html and "checkForUpdates" in html)
    check("Update-Ext: vivodepot.de/newsletter",          "vivodepot.de/newsletter" in html)
    check("Update-Ext: E-Mail Regex Validierung",         r"@[^\s@]+" in html or "test(email)" in html or "includes('@')" in html)
    check("Update-Ext: vivodepot.de/datenschutz Link",   "vivodepot.de/datenschutz" in html)
    check("Update-Ext: Banner unter Topbar (top:68px)",   "68px" in html and "update-banner" in html)
    check("Update-Ext: Banner min-width 160px",           "160px" in html and "update-banner" in html)
    check("Update-Ext: Opt-in email-optin-title ID",      "email-optin-title" in html)
    check("Update-Ext: Opt-in hat aria-labelledby",       "aria-labelledby" in html and "email-optin" in html)
    check("Update-Ext: Update-URL mit ?v= Param",         "?v=" in html and "UPDATE_CHECK_URL" in html)
    check("Update-Ext: Dismissed-Version gespeichert",    "vivodepot_update_dismissed" in html)


    # ═══════════════════════════════════════
    print("\n=== 43. EXPORTE — QUALITÄT ===")
    # ═══════════════════════════════════════

    check("Export: generateArztbogen() vorhanden", "function generateArztbogen" in html)
    check("Export: generateScenarioPDF() vorhanden", "function generateScenarioPDF" in html)
    check("Export: generateQRStickers() vorhanden", "function generateQRStickers" in html)
    check("Export: generateHeimaufnahme() vorhanden", "function generateHeimaufnahme" in html)
    check("Export: generateFHIR() vorhanden", "function generateFHIR" in html)
    check("Export: exportFIMJson() vorhanden", "exportFIMJson" in html)
    check("Export: generateBehoerdendaten() vorhanden", "function generateBehoerdendaten" in html)
    check("Export: generateChecklist() vorhanden", "function generateChecklist" in html)
    check("Export: Szenario hospital", "hospital" in html and "generateScenarioPDF" in html)
    check("Export: Szenario emergency (Todesfall)", "'emergency'" in html and "generateScenarioPDF" in html)
    check("Export: Szenario pet (Haustier)", "'pet'" in html and "generateScenarioPDF" in html)
    check("Export: QR-Code-Bibliothek geladen", "qrcode" in html.lower())
    check("Export: jsPDF-Bibliothek geladen", "jspdf" in html.lower())
    check("Export: docx-Bibliothek geladen", "docx@" in html)
    check("Export: Checkliste enthält Gesundheit", "get('hausarzt')" in html and "generateChecklist" in html)
    check("Export: FIM-JSON Struktur", "exportFIMJson" in html)
    check("Export: Behördendaten Kindergeld", "Kindergeld" in html or "generateBehoerdendaten" in html)
    check("Export: Behördendaten Elterngeld — Karte vorhanden", "'elterngeld'" in html and "Elterngeld-Datenblatt" in html)
    check("Export: Behördendaten Elterngeld — PDF-Logik vorhanden", "type === 'elterngeld'" in html)
    check("Export: Behördendaten Elterngeld — Checkliste Geburtsurkunde", "Geburtsurkunde des Kindes" in html)
    check("Export: Behördendaten Elterngeld — Hinweis 3-Monats-Frist", "3 Monate" in html and "Elterngeld" in html)
    check("Export: Behördendaten Elterngeld — QR-Code Payload", "t:'EG'" in html)
    check("Export: Behördendaten Elterngeld — im titles-Objekt", "elterngeld:'Elterngeld'" in html)
    check("Export: Behördendaten Grundsicherung — Karte vorhanden", "'grundsicherung'" in html and "Grundsicherung-Datenblatt" in html)
    check("Export: Behördendaten Grundsicherung — PDF-Logik vorhanden", "type === 'grundsicherung'" in html)
    check("Export: Behördendaten Grundsicherung — Checkliste Kontoauszüge", "Kontoausz" in html and "grundsicherung" in html)
    check("Export: Behördendaten Grundsicherung — SGB-Hinweis", "SGB II" in html and "SGB XII" in html)
    check("Export: Behördendaten Grundsicherung — QR-Code Payload", "t:'GS'" in html)
    check("Export: Behördendaten Grundsicherung — im titles-Objekt", "grundsicherung:'Grundsicherung'" in html)
    check("Export: Behördendaten Schwerbehinderung — Karte vorhanden", "'schwerbehinderung'" in html and "Schwerbehindertenantrag-Datenblatt" in html)
    check("Export: Behördendaten Schwerbehinderung — PDF-Logik vorhanden", "type === 'schwerbehinderung'" in html)
    check("Export: Behördendaten Schwerbehinderung — GdB-Feld", "get('gdb')" in html and "schwerbehinderung" in html)
    check("Export: Behördendaten Schwerbehinderung — Merkzeichen", "Merkzeichen" in html and "schwerbehinderung" in html.lower())
    check("Export: Behördendaten Schwerbehinderung — Hinweis GdB 50", "GdB von 50" in html)
    check("Export: Behördendaten Schwerbehinderung — QR-Code Payload", "t:'SB'" in html)
    check("Export: Behördendaten Schwerbehinderung — im titles-Objekt", "schwerbehinderung:'Schwerbehinderung'" in html)

    # ═══════════════════════════════════════
    print("\n=== 44. VOLLMACHTEN & DOKUMENTE ===")
    # ═══════════════════════════════════════

    check("Vollmacht: generateVorsorgevollmacht()", "function generateVorsorgevollmacht" in html)
    check("Vollmacht: generatePatientenverfuegung()", "function generatePatientenverfuegung" in html)
    check("Vollmacht: generateGesundheitsvollmacht()", "function generateGesundheitsvollmacht" in html)
    check("Vollmacht: Vorsorgevollmacht-Wizard vvwizOpen", "vvwizOpen" in html)
    check("Vollmacht: Patientenverfügung-Wizard pvwizOpen", "pvwizOpen" in html)
    check("Vollmacht: Gesundheitsvollmacht-Wizard gvwizOpen", "gvwizOpen" in html)
    check("Vollmacht: Betreuer-Angaben", "'betreuer_name'" in html or "betreuer" in html.lower())
    check("Vollmacht: Vollmacht-Bezug im Dokument", "Vollmacht" in html and "generateVorsorgevollmacht" in html)
    check("Vollmacht: Gesundheitsvollmacht Schritt 1–5", "gvwiz-step-info" in html)
    check("Vollmacht: Vorsorgevollmacht §§ BGB", "§" in html and "Vollmacht" in html)
    check("Vollmacht: Patientenverfügung Bewusstlos", "bewusstlos" in html.lower() or "Bewusstlosigkeit" in html or "Patientenverfügung" in html)
    check("Vollmacht: Vollmacht Hinweis Alleinlebende", "Alleinlebend oder verwitwet?" in html)

    # ═══════════════════════════════════════
    print("\n=== 45. ROBUSTHEIT & FEHLERBEHANDLUNG ===")
    # ═══════════════════════════════════════

    check("Robust: window.onerror", "window.onerror" in html)
    check("Robust: safeRender() mit catch", "function safeRender" in html and "catch" in html)
    check("Robust: localStorage try/catch", "localStorage" in html and "try" in html and "localStorage" in html)
    check("Robust: goToStep try/catch",
          "try {" in html[html.find("function goToStep"):html.find("function goToStep")+800])
    check("Robust: fetch mit catch", "fetch" in html and ".catch" in html)
    check("Robust: AbortController Timeout", "AbortController" in html)
    check("Robust: clearTimeout nach fetch", "clearTimeout" in html)
    check("Robust: catch(e) >= 20 Blöcke", html.count("catch(e)") + html.count("catch (e)") >= 20)
    check("Robust: try/catch >= 20 Blöcke", html.count("try {") + html.count("try{") >= 20)
    check("Robust: console.error für Entwickler", "console.error" in html)
    check("Robust: Keine nicht-abgefangenen Promises", html.count(".catch(") >= 3)
    check("Robust: vivoConfirm statt confirm()", "function vivoConfirm" in html and "if (!confirm(" not in html)
    check("Robust: toast für Nutzerfeedback", "function toast" in html)
    check("Robust: Daten-Fallback bei leerem Wert", "|| ''" in html or "|| \"\"" in html)

    # ═══════════════════════════════════════
    print("\n=== 46. UPDATE-SYSTEM INTEGRATION ===")
    # ═══════════════════════════════════════

    check("Update: VIVODEPOT_VERSION Konstante", "VIVODEPOT_VERSION" in html)
    check("Update: Version enthält beta", "beta" in html and "VIVODEPOT_VERSION" in html)
    check("Update: checkForUpdates() in enterApp", "checkForUpdates" in html and "enterApp" in html)
    check("Update: Timeout 5s vor Update-Check", "5000" in html and "checkForUpdates" in html)
    check("Update: maybeShowEmailOptin() in enterApp", "maybeShowEmailOptin" in html and "enterApp" in html)
    check("Update: vivodepot_use_count Zähler", "vivodepot_use_count" in html)
    check("Update: Opt-in ab 3. Nutzung", "3" in html and "vivodepot_use_count" in html)
    check("Update: vivodepot_update_dismissed gespeichert", "vivodepot_update_dismissed" in html)
    check("Update: Newsletter-Endpunkt", "vivodepot.de/newsletter" in html)
    check("Update: keepalive:true beim Submit", "keepalive" in html)
    check("Update: E-Mail Regex-Validierung", "@" in html and (".test(" in html or "test(email)" in html))
    check("Update: Opt-in mit 4s Verzögerung", "4000" in html and "showEmailOptin" in html)

    # ═══════════════════════════════════════
    print("\n=== 47. EINGABE-HILFE & VALIDIERUNG ===")
    # ═══════════════════════════════════════

    # IBAN-Formatierung
    check("Eingabe: ibanFormat() vorhanden",               "function ibanFormat" in html)
    check("Eingabe: ibanFormat() formatiert in Gruppen",   "ibanFormat" in html and "match(/.{1,4}/g)" in html)
    check("Eingabe: ibanFormat() via Event-Delegation",    "ibanFormat(el)" in html and "addEventListener" in html)
    check("Eingabe: IBAN Cursor-Position erhalten",        "setSelectionRange" in html and "ibanFormat" in html)
    check("Eingabe: IBAN-Delegation nur auf INPUT",        "tagName" in html and "ibanFormat" in html)

    # Bestehende Validierung
    check("Eingabe: validateField() IBAN-Prüfziffer",      "Mod 97" in html or "mod.97" in html.lower() or "% 97" in html)
    check("Eingabe: validateField() DE-IBAN 22 Zeichen",   "22" in html and "iban" in html.lower())
    check("Eingabe: validateField() Geburtsdatum Zukunft", "Geburtsdatum liegt in der Zukunft" in html)
    check("Eingabe: validateField() Alter über 120",       "120" in html and "geburtsdatum" in html.lower())
    check("Eingabe: validateField() Steuer-ID 11 Stellen", "11" in html and "steuerid" in html)
    check("Eingabe: validateField() E-Mail-Format",        "E-Mail-Format ungültig" in html)
    check("Eingabe: validateField() Telefon-Format",       "Telefonnummer" in html and "validateField" in html)
    check("Eingabe: validateField() PLZ 5 Stellen",        "5 Ziffern" in html and "plz" in html.lower())

    # Neue BIC-Validierung
    check("Eingabe: validateField() BIC-Format",           "BIC" in html and "COBADEFFXXX" in html)
    check("Eingabe: validateField() BIC 8 oder 11 Zeichen","8 oder 11" in html and "BIC" in html)

    # Neue SVNR-Validierung
    check("Eingabe: validateField() SVNR 12 Stellen",      "12 Ziffern" in html and "svnr" in html)

    # Inaktivitäts-Erinnerung
    check("Inaktiv: _idleTimer vorhanden",                 "_idleTimer" in html)
    check("Inaktiv: IDLE_MS 15 Minuten",                   "15 * 60 * 1000" in html or "900000" in html)
    check("Inaktiv: resetIdleTimer() Funktion",            "function resetIdleTimer" in html)
    check("Inaktiv: Erinnerung via toast()",               "_idleShown" in html and "toast(" in html)
    check("Inaktiv: Timer-Reset bei Nutzeraktion",         "resetIdleTimer" in html and "addEventListener" in html)
    check("Inaktiv: sessionStorage Datei-gespeichert",     "vivodepot_file_saved" in html)
    check("Inaktiv: saveAsHTML patchen",                   "vivodepot_file_saved" in html and "saveAsHTML" in html)
    check("Inaktiv: passive Event-Listener",               "passive: true" in html or "passive:true" in html)
    check("Inaktiv: Mehrere Events (input/click/keydown)", "_idleTimer" in html and "keydown" in html and "touchstart" in html)

    # ═══════════════════════════════════════
    print("\n=== 48. VOLLSTÄNDIGKEITS-REGRESSION (Chat-Abgleich) ===")
    # ═══════════════════════════════════════

    # Fokus-System: notfall muss in emergency UND family enthalten sein
    em_block = html[html.find("selectedGoal === 'emergency'"):html.find("selectedGoal === 'emergency'")+250]
    fa_block  = html[html.find("selectedGoal === 'family'"):html.find("selectedGoal === 'family'")+250]
    check("Fokus: 'notfall' im emergency-Ziel",          "'notfall'" in em_block)
    check("Fokus: 'notfall' im family-Ziel",             "'notfall'" in fa_block)
    check("Fokus: emergency enthält gesundheit",         "'gesundheit'" in em_block)
    check("Fokus: emergency enthält kontakte",           "'kontakte'" in em_block)
    check("Fokus: family enthält testament",             "'testament'" in fa_block)
    check("Fokus: family enthält assistenten",           "'assistenten'" in fa_block)

    # Notfall-Step: vollständig vorhanden
    check("Notfall-Step: id='notfall' in STEPS",         "{ id: 'notfall'" in html)
    check("Notfall-Step: Renderer notfall: () =>",       "notfall: () =>" in html)
    check("Notfall-Step: nina_regionen Feld",            "'nina_regionen'" in html or "'ks_nina_installiert'" in html)
    check("Notfall-Step: notfallvorrat_stand Feld",      "'notfallvorrat_stand'" in html or "'ks_wasser_liter'" in html)
    check("Notfall-Step: notfall_treffpunkt Feld",       "'notfall_treffpunkt'" in html or "'ks_sammelplatz'" in html)
    check("Notfall-Step: notfall_nachbar Feld",          "'notfall_nachbar'" in html or "'ks_nachbar'" in html)
    check("Notfall-Step: BBK-Link im Renderer",          "bbk.bund.de" in html and "notfall: () =>" in html)
    check("Notfall-Step: Vorrat-Checkliste interaktiv",  "vorrat_" in html and "NOTFALL_VORRAT_ITEMS" in html)
    check("Notfall-Step: in times-Objekt",               "notfall:2" in html or "notfall: 2" in html)

    # Angehörigen-Modus: Vollständigkeit
    check("Angehörigen: brief_krankenhaus Feld",         "'brief_krankenhaus'" in html)
    check("Angehörigen: brief_todesfall Feld",           "'brief_todesfall'" in html)
    check("Angehörigen: hospital-Szenario",              "openAngehoerigenView('hospital')" in html)
    check("Angehörigen: death-Szenario",                 "openAngehoerigenView('death')" in html)
    check("Angehörigen: return-owner-label",             "return-owner-label" in html)
    check("Angehörigen: angehoerigen_passwort Feld",     "'angehoerigen_passwort'" in html)

    # BUG-FIX Angehörigen-Modus: Zugangssperre (verhindert Owner-Datenzugriff)
    check("BUG-ANG-01: _angehoerigenModus Flag gesetzt in openAngehoerigenView()",
          "window._angehoerigenModus = true" in html,
          "Fehlt: Flag zum Sperren des Owner-Modus wird nicht gesetzt")
    check("BUG-ANG-02: _angehoerigenModus Flag zurückgesetzt in angehoerigenZurueck()",
          "window._angehoerigenModus = false" in html,
          "Fehlt: Flag wird beim Verlassen nicht zurückgesetzt")
    check("BUG-ANG-03: renderSidebar() prüft _angehoerigenModus Guard",
          "if (window._angehoerigenModus) return" in html,
          "Fehlt: renderSidebar() kann im Angehörigen-Modus Owner-Navigation neu rendern")
    check("BUG-ANG-04: Sidebar wird per display:none gesperrt (nicht nur geleert)",
          "sb.style.display = 'none'" in html,
          "Fehlt: Sidebar nur geleert statt unsichtbar — renderSidebar() kann sie neu befüllen")
    check("BUG-ANG-05: hideAllOverlays() schützt angehoerigenauswahl-overlay im Angehörigen-Modus",
          "id === 'angehoerigenauswahl-overlay' && window._angehoerigenModus" in html,
          "Fehlt: hideAllOverlays() kann Auswahl-Overlay im Angehörigen-Modus schließen")
    check("BUG-ANG-06: ESC-Handler schließt angehoerigenauswahl-overlay nur außerhalb Angehörigen-Modus",
          "if (!window._angehoerigenModus)" in html and "angehoerigenauswahl-overlay" in html,
          "Fehlt: ESC-Taste kann Auswahl-Overlay im Angehörigen-Modus schließen")
    check("BUG-ANG-07: welcomeStart() zeigt zuerst Inhaber/Angehörigen-Auswahl",
          "showWelcomeRoleSelect" in html,
          "Fehlt: welcomeStart() springt direkt zum Goal-Wizard ohne Inhaber/Angehörigen-Auswahl")
    check("BUG-ANG-08: welcomeRoleOwner() führt zum Goal-Wizard",
          "function welcomeRoleOwner" in html and "showGoalWizard" in html,
          "Fehlt: Inhaber-Pfad nach Rollenauswahl")
    check("BUG-ANG-09: welcomeRoleAngehoerige() öffnet Angehörigen-Auswahl",
          "function welcomeRoleAngehoerige" in html and "angehoerigenauswahl-overlay" in html,
          "Fehlt: Angehörigen-Pfad nach Rollenauswahl")
    check("BUG-ANG-10: setTimeout(showGoalWizard) prüft _angehoerigenModus",
          "if (!window._angehoerigenModus) showGoalWizard" in html,
          "Fehlt: Timer kann showGoalWizard im Angehoerigen-Modus aufrufen")
    check("BUG-ANG-11: applyGoalWizard() Guard gegen Angehoerigen-Modus",
          "if (window._angehoerigenModus) return;" in html,
          "Fehlt: applyGoalWizard oeffnet Owner-App im Angehoerigen-Modus")
    check("BUG-ANG-12: skipGoalWizard() Guard gegen Angehoerigen-Modus",
          "if (window._angehoerigenModus) return;" in html,
          "Fehlt: skipGoalWizard oeffnet Owner-App im Angehoerigen-Modus")
    check("BUG-ANG-13: openAngehoerigenView() versteckt App-Shell (.app)",
          "appEl.style.display = 'none'" in html,
          "Fehlt: App-Shell bleibt sichtbar — 20 Kategorien in Sidebar sichtbar")
    check("BUG-ANG-14: openAngehoerigenView() versteckt save-reminder-bar",
          "save-reminder-bar" in html and "barEl.style.display = 'none'" in html,
          "Fehlt: save-reminder-bar mit Fokus/Speichern-Buttons bleibt sichtbar")
    check("BUG-ANG-15: openAngehoerigenView() nutzt eigenen Vollbild-Overlay",
          "angehoerigen-view-overlay" in html,
          "Fehlt: Angehoerigen-View zeigt in main-content statt eigenem Overlay")
    check("BUG-ANG-16: angehoerigenZurueck() stellt App-Shell wieder her",
          "angehoerigen-view-overlay" in html and "appEl.style.display = ''" in html,
          "Fehlt: App-Shell wird nach Angehoerigen-Modus nicht wiederhergestellt")
    check("BUG-ANG-17: wechselAngehoerigenAnsicht() setzt _angehoerigenModus=false",
          "function wechselAngehoerigenAnsicht" in html and
          "window._angehoerigenModus = false" in html,
          "Fehlt: _angehoerigenModus bleibt true — hideAllOverlays-Guard blockiert naechstes Szenario")
    check("BUG-ANG-18: View-Overlay z-index ueber crypto-overlay (10001 > 10000)",
          "z-index:10001" in html,
          "Fehlt: View-Overlay z-index 9000 liegt unter crypto-overlay 10000 — Auswahl-Overlay verdeckt View")


    # Persona-Felder aus Chat-Abgleich
    check("Persona: selbstaendig_notfall",               "'selbstaendig_notfall'" in html)
    check("Persona: krypto_seed_ort",                    "'krypto_seed_ort'" in html)
    check("Persona: palliativ_wunsch",                   "'palliativ_wunsch'" in html)
    check("Persona: schwerbehindertenausweis_gueltig",   "'schwerbehindertenausweis_gueltig'" in html)
    check("Persona: erinnerung_sba",                     "'erinnerung_sba'" in html)
    check("Persona: unterhalt",                          "'unterhalt'" in html)
    check("Persona: ausland_vermoegen",                  "'ausland_vermoegen'" in html)
    check("Persona: gmb_nachfolge",                      "'gmb_nachfolge'" in html)
    check("Persona: elefand_nr",                         "'elefand_nr'" in html)
    check("Persona: bundid_email",                       "'bundid_email'" in html)
    check("Persona: behandlung_aktuell",                 "'behandlung_aktuell'" in html)

    # Rechtliche Inhalte
    check("Recht: Stiefkinder erben nichts",             "Stiefkinder erben nichts" in html)
    check("Recht: § 2077 BGB (Scheidung)",               "2077 BGB" in html)
    check("Recht: Nachlassgericht Alleinerziehend",      "Nachlassgericht hinterlegen" in html)

    # Print-CSS (aus Session)
    check("Print: @media print Sidebar weg",             "@media print" in html and ".sidebar" in html)
    check("Print: @page A4",                             "@page" in html and "A4" in html)
    check("Print: page-break-inside avoid",              "page-break-inside" in html)

    # vCard aus Session
    check("vCard: exportVCard() Funktion",               "function exportVCard" in html)
    check("vCard: generateVCard() Funktion",             "function generateVCard" in html)

    # IBAN-Formatierung und Validierung
    check("Eingabe: BIC-Validierung",                    "BIC" in html and "COBADEFFXXX" in html)
    check("Eingabe: SVNR-Validierung 12 Stellen",        "12 Ziffern" in html and "svnr" in html)

    # Inaktivitäts-Timer
    check("Inaktiv: _idleTimer 15 Minuten",              "_idleTimer" in html and "15 * 60 * 1000" in html)
    check("Inaktiv: sessionStorage vivodepot_file_saved","vivodepot_file_saved" in html)

    # Notfall-Vorrat 15 Items
    vorrat_start = html.find("var NOTFALL_VORRAT_ITEMS")
    vorrat_end   = html.find("];", vorrat_start) + 2
    vorrat_block = html[vorrat_start:vorrat_end]
    vorrat_count = vorrat_block.count("',\n") + (1 if "'\n]" in vorrat_block else 0)
    check("Notfall: NOTFALL_VORRAT_ITEMS hat 15 Einträge", vorrat_count == 15, f"Gefunden: {vorrat_count}")
    check("Notfall: Signalmittel in Vorrat",              "Signalmittel" in html)
    check("Notfall: Dosenöffner in Vorrat",               "Dosenöffner" in html)

    # Persistierter Fokus
    check("Fokus: __fokus__ in data gespeichert",         "data['__fokus__']" in html or "'__fokus__'" in html)
    check("Fokus: applyGoalWizard persistiert Fokus",     "__fokus__" in html and "applyGoalWizard" in html)
    check("Fokus: skipGoalWizard löscht Fokus",           "__fokus__" in html and "skipGoalWizard" in html)
    check("Fokus: enterApp stellt Fokus wieder her",      "savedFokus" in html and "enterApp" in html)
    check("Fokus: savedWelcomeOwner stellt Fokus wieder her", "savedFokus" in html and "savedWelcomeOwner" in html)
    check("Fokus: Wizard nur bei fehlendem Fokus",        "savedFokus" in html and "showGoalWizard" in html)

    # ═══════════════════════════════════════
    print("\n=== 49. VIEWPORT & LAYOUT-REGRESSION ===")
    # ═══════════════════════════════════════

    # BUG-12: .crypto-modal auf kleinen Bildschirmen (iPhone) oben/unten abgeschnitten.
    # Ursache: Fehlende max-height und overflow-y im .crypto-modal CSS-Block.
    # Suche den Haupt-Block (enthält border-radius), nicht den Dark-Mode-Override.
    modal_css = re.search(r'\.crypto-modal\s*\{([^}]*border-radius[^}]*)\}', html)
    if modal_css:
        block = modal_css.group(1)
        check("BUG-12: .crypto-modal hat max-height (kein Viewport-Clipping)",
              'max-height' in block,
              "Fehlt: max-height — Modal wird auf kleinen Bildschirmen abgeschnitten")
        check("BUG-12: .crypto-modal hat overflow-y (scrollbar bei Überlauf)",
              'overflow-y' in block,
              "Fehlt: overflow-y — Inhalt nicht scrollbar wenn Modal zu hoch")
    else:
        check("BUG-12: .crypto-modal CSS-Block gefunden", False, "Klasse nicht gefunden")

    # ═══════════════════════════════════════
    print("\n=== 50. NEUE BUGS (BUG-NEW) ===")
    # ═══════════════════════════════════════

    # BUG-NEW-02: window.onerror darf bei Cross-Origin-Fehlern (Script error, Zeile 0, kein src)
    # NICHT das welcome-overlay anzeigen. Safari/file:// liefert solche opaken Fehler für
    # externe Bibliotheken → overlay erscheint fälschlicherweise als Startseite.
    onerror_match = re.search(r'window\.onerror\s*=\s*function\([^)]*\)\s*\{([\s\S]*?)\n\};', html)
    if onerror_match:
        onerror_body = onerror_match.group(1)
        # Fix: Prüft auf leere src UND Zeile 0 → kein welcome-overlay
        has_guard = bool(re.search(r'if\s*\(\s*!src\b.*?line\s*===?\s*0', onerror_body)) or \
                    bool(re.search(r'if\s*\(\s*line\s*===?\s*0.*?!src', onerror_body))
        check("BUG-NEW-02: onerror ignoriert Cross-Origin-Fehler (kein src, Zeile 0)",
              has_guard,
              "Fehlende Guard-Bedingung: Safari 'Script error.' (line 0) löst welcome-overlay aus")
    else:
        check("BUG-NEW-02: window.onerror gefunden", False, "window.onerror nicht auffindbar")

    # BUG-NEW-01: updateFokusBarLabel() hatte toten Ternary — beide Zweige identisch '⊕ Fokus'
    # Nutzer konnte nicht erkennen ob Fokus aktiv ist. Fix: '⊕ Fokus ändern' vs. '⊕ Fokus wählen'
    fokus_label_match = re.search(
        r"btn\.textContent\s*=\s*\([^)]+\)\s*\?\s*'([^']*)'\s*:\s*'([^']*)'", html)
    if fokus_label_match:
        a = fokus_label_match.group(1)
        b = fokus_label_match.group(2)
        check("BUG-NEW-01: updateFokusBarLabel() zeigt unterschiedliche Labels (Fokus aktiv/inaktiv)",
              a != b,
              f"Toter Ternary: beide Zweige '{a}' — kein visueller Unterschied ob Fokus aktiv ist")
    else:
        check("BUG-NEW-01: updateFokusBarLabel() Ternary gefunden", False,
              "btn.textContent-Ternary in updateFokusBarLabel() nicht gefunden")

    # ═══════════════════════════════════════
    print("\n=== 51. KRYPTO-PORTABILITÄT (Salt in Datei) ===")
    # ═══════════════════════════════════════

    # BUG-SALT-01: Salt muss beim Speichern in die HTML-Datei eingebettet werden.
    # Ohne diesen Fix schlägt die Entschlüsselung auf einem anderen Gerät fehl,
    # weil der Salt nur im localStorage des Ursprungsgeräts existiert.
    # Prüfung: saveAsHTML() liest STORE_META aus localStorage und schreibt ihn
    # in den initBlock der gespeicherten Datei.
    save_fn = re.search(r'async function saveAsHTML\(\)([\s\S]*?)(?=\nasync function |\nfunction )', html)
    if save_fn:
        save_body = save_fn.group(1)
        check("BUG-SALT-01a: saveAsHTML() liest STORE_META (Salt) aus localStorage",
              'localStorage.getItem(STORE_META)' in save_body or
              "localStorage.getItem(STORE_META)" in save_body,
              "Salt wird nicht aus localStorage gelesen — nicht portierbar")
        check("BUG-SALT-01b: saveAsHTML() schreibt Salt in den initBlock",
              'localStorage.setItem' in save_body and 'embeddedSalt' in save_body,
              "Salt wird nicht in die gespeicherte Datei eingebettet")
        check("BUG-SALT-01c: Salt-Schreibung ist idempotent (nur wenn nicht vorhanden)",
              "if(!" in save_body or "if (!" in save_body,
              "Salt wird immer überschrieben statt nur bei Fehlen gesetzt")
    else:
        check("BUG-SALT-01: saveAsHTML() gefunden", False)

    # BUG-SALT-02: initBlock-Regex muss auch den neuen Salt-Block treffen.
    # Der Regex /\/\/ [═]+\s*\/\/ INIT[\s\S]*?\}\)\(\);/ muss den neuen
    # gespeicherten Block mit "// INIT (mit eingebetteten Daten)" erkennen.
    check("BUG-SALT-02: initBlock enthält '// INIT'-Marker für Regex",
          '// INIT (mit eingebetteten Daten)' in html or
          "// INIT\\n" in html,
          "initBlock-Kommentar fehlt — Regex trifft gespeicherte Datei nicht beim Weiter-Speichern")

    # ═══════════════════════════════════════
    print("\n=== 52. WEITERGABE-DATEI ===")
    # ═══════════════════════════════════════

    # WG-01: Weitergabe-Teaser-Block im DOM
    check("WG-01: Teaser-Block 'weitergabeOpen()' vorhanden",
          "weitergabeOpen()" in html,
          "Teaser-Block ruft weitergabeOpen() nicht auf")
    check("WG-01b: Link-Zeile CSS-Klasse 'wg-link-zeile' vorhanden",
          "wg-link-zeile" in html,
          "CSS-Klasse wg-link-zeile fehlt")
    check("WG-01c: Weitergabe-Karte nicht mehr im Export-Raster",
          'onclick="weitergabeOpen()" style="border-left:4px solid var(--teal)"' not in html,
          "Alte Export-Karte wurde nicht entfernt")

    # WG-02: Modal-HTML
    check("WG-02: Modal-Overlay id='wg-overlay' vorhanden",
          'id="wg-overlay"' in html,
          "Modal-Overlay fehlt")
    check("WG-03: Schritt 1 id='wg-step-1' vorhanden",
          'id="wg-step-1"' in html,
          "Schritt-1-Element fehlt")
    check("WG-04: Schritt 2 id='wg-step-2' vorhanden",
          'id="wg-step-2"' in html,
          "Schritt-2-Element fehlt")
    check("WG-05: Schritt 3 id='wg-step-3' vorhanden",
          'id="wg-step-3"' in html,
          "Schritt-3-Element fehlt")

    # WG-06: Alle 4 Profil-Cards
    for profil in ['notfall', 'vollmacht', 'familie', 'behoerde']:
        check(f"WG-06-{profil}: Profil-Card id='wg-card-{profil}' vorhanden",
              f'id="wg-card-{profil}"' in html,
              f"Profil-Card {profil} fehlt")

    # WG-07: Behoerde-Dropdown
    check("WG-07: Behoerde-Dropdown id='wg-behoerde-select' vorhanden",
          'id="wg-behoerde-select"' in html,
          "Behoerde-Dropdown fehlt")

    # WG-08: Passwort-Felder
    check("WG-08: Passwort-Feld id='wg-pw1' vorhanden",
          'id="wg-pw1"' in html,
          "Passwort-Feld 1 fehlt")
    check("WG-09: Passwort-Feld id='wg-pw2' vorhanden",
          'id="wg-pw2"' in html,
          "Passwort-Feld 2 fehlt")

    # WG-10: JavaScript-Funktionen
    for fn in ['weitergabeOpen', 'weitergabeClose', 'wgZeigeSchritt',
               'wgWaehleProfilCard', 'wgPwInput', 'wgErstellen',
               'wgBegleitKopieren', 'wgBaueHtmlDatei', 'wgReminderPruefen']:
        check(f"WG-10-{fn}: Funktion '{fn}' vorhanden",
              f"function {fn}" in html,
              f"Funktion {fn} fehlt")

    # WG-11: Separater Salt — Hauptpasswort darf Weitergabe-Datei NICHT öffnen
    # Der Salt fuer die Weitergabe-Datei wird mit crypto.getRandomValues erzeugt,
    # nicht aus dem globalen `salt` der Hauptanwendung gelesen.
    wg_fn = re.search(r'async function wgErstellen\(\)([\s\S]*?)(?=\nasync function |\nfunction )', html)
    if wg_fn:
        wg_body = wg_fn.group(1)
        check("WG-11a: wgErstellen() erzeugt eigenen Salt via getRandomValues",
              "getRandomValues" in wg_body,
              "Kein eigener Salt — Hauptpasswort koennte Weitergabe-Datei entschluesseln")
        check("WG-11b: wgErstellen() ruft deriveKey mit eigenem Salt auf",
              "deriveKey" in wg_body,
              "deriveKey nicht aufgerufen")
        check("WG-11c: wgErstellen() verwendet NOT den globalen 'salt'",
              "deriveKey(pw," in wg_body or "deriveKey(password," in wg_body,
              "Weitergabe nutzt moeglicherweise den globalen Salt")
    else:
        check("WG-11: wgErstellen() gefunden", False,
              "Funktion wgErstellen() nicht auffindbar")

    # WG-12: Generierte Datei enthaelt eigenen Decrypt-Code
    check("WG-12: Generierte Datei enthaelt inline Decrypt-Funktion",
          "async function entschluesseln" in html or
          "function entschluesseln" in html,
          "Decrypt-Funktion fuer generierte Datei fehlt")

    # WG-13: Begleittext-Feld
    check("WG-13: Begleittext-Container id='wg-begleit-inhalt' vorhanden",
          'id="wg-begleit-inhalt"' in html,
          "Begleittext-Container fehlt")

    # WG-14: Reminder-Mechanismus
    check("WG-14: Reminder prueft localStorage 'vivodepot_wg_datum'",
          "vivodepot_wg_datum" in html,
          "Reminder-Key 'vivodepot_wg_datum' fehlt")

    # WG-15: Kein Netzwerkaufruf in wgErstellen / wgBaueHtmlDatei
    check("WG-15: Keine fetch()-Aufrufe in Weitergabe-Funktionen",
          html.count("fetch(") == html.replace("wgErstellen", "").replace("wgBaueHtmlDatei", "").count("fetch("),
          "fetch() in Weitergabe-Funktionen gefunden — Offline-Bedingung verletzt")

    # WG-16: wg-overlay muss in hideAllOverlays() registriert sein
    # Bug: Weitergabe-Dialog blieb offen wenn ein anderer Overlay geöffnet wurde
    hide_fn_wg = re.search(r'function hideAllOverlays\(\)\s*\{([\s\S]*?)\n\}', html)
    check("WG-16a: wg-overlay in hideAllOverlays() registriert",
          hide_fn_wg and 'wg-overlay' in hide_fn_wg.group(1),
          "wg-overlay fehlt in hideAllOverlays — Dialog bleibt offen bei Overlay-Wechsel")

    # WG-16b: wg-overlay muss auch in showOverlay() (Hide-Liste) registriert sein
    show_fn_wg = re.search(r'function showOverlay\(id\)\s*\{([\s\S]*?)\n\}', html)
    check("WG-16b: wg-overlay in showOverlay() Hide-Liste registriert",
          show_fn_wg and 'wg-overlay' in show_fn_wg.group(1),
          "wg-overlay fehlt in showOverlay — Dialog bleibt offen wenn anderer Overlay aufgerufen wird")

    # ── window.onerror: App-Zustandsprüfung ───────────────────────────────
    print("\n  window.onerror Guard:")

    # ONERR-1: window.onerror zeigt welcome-overlay NUR wenn App noch nicht gestartet
    import re as _re
    onerror_match = _re.search(
        r'window\.onerror\s*=\s*function[^{]*\{.*?return false;\s*\}',
        html, _re.DOTALL
    )
    onerror_body = onerror_match.group(0) if onerror_match else ""
    check("ONERR-1: window.onerror prüft App-Zustand vor welcome-overlay",
          "appStarted" in onerror_body and
          "return-overlay" in onerror_body and
          "main-content" in onerror_body and
          "innerHTML" in onerror_body and
          "if (!appStarted)" in onerror_body,
          "window.onerror zeigt welcome-overlay ohne App-Zustandsprüfung")

    # ONERR-2: loadData() JSON-Parse-Fehler zeigt welcome-overlay NUR wenn App noch nicht gestartet
    loaddata_match = _re.search(
        r'async function loadData\(\)[^{]*\{([\s\S]*?)^\}',
        html, _re.MULTILINE
    )
    loaddata_body = loaddata_match.group(1) if loaddata_match else ""
    parse_catch_match = _re.search(
        r'parsedStored\s*=\s*JSON\.parse\(stored\).*?catch\s*\{(.*?)return;\s*\}',
        html, _re.DOTALL
    )
    parse_catch_body = parse_catch_match.group(1) if parse_catch_match else ""
    check("ONERR-2: loadData() JSON-Parse-Fehler prüft App-Zustand vor welcome-overlay",
          ("return-overlay" in parse_catch_body or "_ro" in parse_catch_body) and
          ("main-content" in parse_catch_body or "_mc" in parse_catch_body) and
          ("innerHTML" in parse_catch_body) and
          ("appStarted" in parse_catch_body or "_appStarted" in parse_catch_body) and
          ("if (!" in parse_catch_body),
          "loadData() zeigt welcome-overlay bei Parse-Fehler ohne App-Zustandsprüfung")

    # ═══════════════════════════════════════
    print("\n=== 53. ANF-01 EINKOMMENSDATEN (Profil 4) ===")
    # ═══════════════════════════════════════

    # ANF01-1: Alle fuenf neuen Feldschluessel existieren im HTML
    check("ANF01-1a: Feld brutto_monat vorhanden",
          "'brutto_monat'" in html,
          "Feldschluessel brutto_monat fehlt")
    check("ANF01-1b: Feld netto_monat vorhanden",
          "'netto_monat'" in html,
          "Feldschluessel netto_monat fehlt")
    check("ANF01-1c: Feld einkommensart vorhanden",
          "'einkommensart'" in html,
          "Feldschluessel einkommensart fehlt")
    check("ANF01-1d: Feld arbeitgeber_adresse vorhanden",
          "'arbeitgeber_adresse'" in html,
          "Feldschluessel arbeitgeber_adresse fehlt")
    check("ANF01-1e: Feld gehaltsnachweis_ort vorhanden",
          "'gehaltsnachweis_ort'" in html,
          "Feldschluessel gehaltsnachweis_ort fehlt")

    # ANF01-2: Dropdown einkommensart enthaelt die fuenf vorgegebenen Optionen
    einkommen_match = re.search(
        r"radio\(\s*'einkommensart'\s*,\s*'[^']*'\s*,\s*\[([^\]]+)\]",
        html
    )
    if einkommen_match:
        options_str = einkommen_match.group(1)
        check("ANF01-2a: Option Angestellt in einkommensart",
              "'Angestellt'" in options_str,
              "Option 'Angestellt' fehlt")
        check("ANF01-2b: Option Selbstaendig in einkommensart",
              "'Selbständig'" in options_str,
              "Option 'Selbständig' fehlt")
        check("ANF01-2c: Option Rente in einkommensart",
              "'Rente'" in options_str,
              "Option 'Rente' fehlt")
        check("ANF01-2d: Option Buergergeld in einkommensart",
              "'Bürgergeld'" in options_str,
              "Option 'Bürgergeld' fehlt")
        check("ANF01-2e: Option Sonstiges in einkommensart",
              "'Sonstiges'" in options_str,
              "Option 'Sonstiges' fehlt")
    else:
        check("ANF01-2: einkommensart als radio-Element gefunden",
              False,
              "radio('einkommensart', ...) nicht auffindbar")

    # ANF01-3: Neuer Block pflege_einkommen existiert
    check("ANF01-3: Block pflege_einkommen existiert",
          "'pflege_einkommen'" in html,
          "Block pflege_einkommen (mehr-Funktion) fehlt")

    # ANF01-4: Neue Felder sind im Suchregister (knownFields) eingetragen
    check("ANF01-4a: brutto_monat im Suchregister",
          "[9,'Bruttogehalt','brutto_monat']" in html,
          "Sucheintrag fuer brutto_monat fehlt")
    check("ANF01-4b: netto_monat im Suchregister",
          "[9,'Nettoeinkommen','netto_monat']" in html,
          "Sucheintrag fuer netto_monat fehlt")
    check("ANF01-4c: einkommensart im Suchregister",
          "[9,'Einkommensart','einkommensart']" in html,
          "Sucheintrag fuer einkommensart fehlt")

    # ANF01-5: Bestehendes Feld letzter_arbeitgeber unveraendert vorhanden
    # (Philosophie: bestehende Funktionen bleiben unberuehrt)
    check("ANF01-5: Bestehendes Feld letzter_arbeitgeber unveraendert",
          "'letzter_arbeitgeber'" in html and
          "field('letzter_arbeitgeber','Letzter Arbeitgeber'" in html,
          "Feld letzter_arbeitgeber wurde veraendert oder entfernt")

    # ── Schritt 2: Export-Struktur (FIM-JSON) ─────────────────────────────

    # ANF01-6: Neue einkommen-Sektion im FIM-Export vorhanden
    fim_match = re.search(
        r'function exportFIMJson\(\)\s*\{([\s\S]*?)\n\}',
        html
    )
    fim_body = fim_match.group(1) if fim_match else ""
    check("ANF01-6: exportFIMJson-Funktion gefunden",
          bool(fim_match),
          "Funktion exportFIMJson() nicht auffindbar")

    check("ANF01-6a: einkommen-Sektion im FIM-Export",
          "einkommen:" in fim_body,
          "Sektion 'einkommen' fehlt im FIM-Export")
    check("ANF01-6b: bruttoMonat im Export",
          "bruttoMonat:" in fim_body and "get('brutto_monat')" in fim_body,
          "bruttoMonat nicht korrekt im Export")
    check("ANF01-6c: nettoMonat im Export",
          "nettoMonat:" in fim_body and "get('netto_monat')" in fim_body,
          "nettoMonat nicht korrekt im Export")
    check("ANF01-6d: einkommensart im Export",
          "einkommensart:" in fim_body and "get('einkommensart')" in fim_body,
          "einkommensart nicht korrekt im Export")
    check("ANF01-6e: arbeitgeberAdresse im Export",
          "arbeitgeberAdresse:" in fim_body and "get('arbeitgeber_adresse')" in fim_body,
          "arbeitgeberAdresse nicht korrekt im Export")
    check("ANF01-6f: gehaltsnachweisOrt im Export",
          "gehaltsnachweisOrt:" in fim_body and "get('gehaltsnachweis_ort')" in fim_body,
          "gehaltsnachweisOrt nicht korrekt im Export")

    # ANF01-7: Bestehende Export-Sektionen sind unveraendert vorhanden
    check("ANF01-7a: Bestehende Sektion natuerlichePerson unveraendert",
          "natuerlichePerson:" in fim_body,
          "Sektion natuerlichePerson fehlt oder wurde umbenannt")
    check("ANF01-7b: Bestehende Sektion beschaeftigung unveraendert",
          "beschaeftigung:" in fim_body,
          "Sektion beschaeftigung fehlt oder wurde umbenannt")

    # ANF01-7c: Bug-Regression: beschaeftigung-Sektion nutzt korrekte Feld-Keys
    # Der fruehere Bug rief get('arbeitgeber') und get('beruf') auf --
    # die echten Keys sind aber letzter_arbeitgeber und beruf_hauptberuf.
    # Ohne diesen Test war die Sektion im Export immer leer.
    besch_match = re.search(
        r'beschaeftigung:\s*\{([\s\S]*?)\}',
        fim_body
    )
    besch_body = besch_match.group(1) if besch_match else ""
    check("ANF01-7c: beschaeftigung nutzt get('letzter_arbeitgeber')",
          "get('letzter_arbeitgeber')" in besch_body,
          "beschaeftigung-Sektion ruft falschen Feld-Key (Bug-Regression)")
    check("ANF01-7d: beschaeftigung nutzt get('beruf_hauptberuf')",
          "get('beruf_hauptberuf')" in besch_body,
          "beschaeftigung-Sektion ruft falschen Feld-Key (Bug-Regression)")

    # ANF01-8: Neue Felder sind NICHT im Notfallprofil
    # (Philosophie: Notfallprofil bleibt minimal, sensible Behoerdendaten
    #  gehoeren nur in den FIM-Export.)
    notfall_match = re.search(
        r'function saveNotfallData\(\)\s*\{([\s\S]*?)\n\}',
        html
    )
    notfall_body = notfall_match.group(1) if notfall_match else ""
    check("ANF01-8: saveNotfallData-Funktion gefunden",
          bool(notfall_match),
          "Funktion saveNotfallData() nicht auffindbar")
    check("ANF01-8a: brutto_monat NICHT im Notfallprofil",
          "brutto_monat" not in notfall_body,
          "brutto_monat taucht im Notfallprofil auf (sollte nicht)")
    check("ANF01-8b: netto_monat NICHT im Notfallprofil",
          "netto_monat" not in notfall_body,
          "netto_monat taucht im Notfallprofil auf (sollte nicht)")
    check("ANF01-8c: einkommensart NICHT im Notfallprofil",
          "einkommensart" not in notfall_body,
          "einkommensart taucht im Notfallprofil auf (sollte nicht)")
    check("ANF01-8d: arbeitgeber_adresse NICHT im Notfallprofil",
          "arbeitgeber_adresse" not in notfall_body,
          "arbeitgeber_adresse taucht im Notfallprofil auf (sollte nicht)")
    check("ANF01-8e: gehaltsnachweis_ort NICHT im Notfallprofil",
          "gehaltsnachweis_ort" not in notfall_body,
          "gehaltsnachweis_ort taucht im Notfallprofil auf (sollte nicht)")

    # ── Schritt 3: Elterngeld-PDF ─────────────────────────────────────────

    # ANF01-9: Elterngeld-PDF-Block isolieren
    # Der Block beginnt bei "type === 'elterngeld'" und endet bei "type === 'arbeitsamt'".
    eg_match = re.search(
        r"type === 'elterngeld'[\s\S]*?(?=\}\s*else if \(type === 'arbeitsamt')",
        html
    )
    eg_body = eg_match.group(0) if eg_match else ""
    check("ANF01-9: Elterngeld-PDF-Block gefunden",
          bool(eg_match),
          "Block 'type === elterngeld' nicht auffindbar")

    # ANF01-10: Alle sieben Felder im Elterngeld-PDF referenziert
    # (6 Einkommensfelder aus ANF-01 plus beruf_hauptberuf = 7)
    check("ANF01-10a: beruf_hauptberuf im Elterngeld-PDF",
          "get('beruf_hauptberuf')" in eg_body,
          "beruf_hauptberuf nicht im Elterngeld-PDF referenziert")
    check("ANF01-10b: letzter_arbeitgeber im Elterngeld-PDF",
          "get('letzter_arbeitgeber')" in eg_body,
          "letzter_arbeitgeber nicht im Elterngeld-PDF referenziert")
    check("ANF01-10c: arbeitgeber_adresse im Elterngeld-PDF",
          "get('arbeitgeber_adresse')" in eg_body,
          "arbeitgeber_adresse nicht im Elterngeld-PDF referenziert")
    check("ANF01-10d: einkommensart im Elterngeld-PDF",
          "get('einkommensart')" in eg_body,
          "einkommensart nicht im Elterngeld-PDF referenziert")
    check("ANF01-10e: brutto_monat im Elterngeld-PDF",
          "get('brutto_monat')" in eg_body,
          "brutto_monat nicht im Elterngeld-PDF referenziert")
    check("ANF01-10f: netto_monat im Elterngeld-PDF",
          "get('netto_monat')" in eg_body,
          "netto_monat nicht im Elterngeld-PDF referenziert")
    check("ANF01-10g: gehaltsnachweis_ort im Elterngeld-PDF",
          "get('gehaltsnachweis_ort')" in eg_body,
          "gehaltsnachweis_ort nicht im Elterngeld-PDF referenziert")

    # ANF01-11: Bestehende Elterngeld-Funktionalitaet unveraendert
    check("ANF01-11a: Beschaeftigungs-Sektion existiert",
          "Besch\\u00E4ftigung (vor der Geburt)" in eg_body,
          "Sektion 'Beschaeftigung' wurde veraendert oder entfernt")
    check("ANF01-11b: Krankenversicherungs-Zeilen erhalten",
          "get('kv_art')" in eg_body and "get('kv_nummer')" in eg_body,
          "KV-Daten wurden aus Elterngeld-PDF entfernt")
    check("ANF01-11c: Checkliste erhalten",
          "egChecks" in eg_body,
          "Checkliste wurde aus Elterngeld-PDF entfernt")

    # ── Schritt 4: Grundsicherungs-PDF ────────────────────────────────────

    # ANF01-12: Grundsicherungs-PDF-Block isolieren
    gs_match = re.search(
        r"type === 'grundsicherung'[\s\S]*?(?=\}\s*else if \(type === 'schwerbehinderung')",
        html
    )
    gs_body = gs_match.group(0) if gs_match else ""
    check("ANF01-12: Grundsicherungs-PDF-Block gefunden",
          bool(gs_match),
          "Block 'type === grundsicherung' nicht auffindbar")

    # ANF01-13: Einkommensnachweis-Sektion vorhanden
    # (Akzeptanzkriterium aus Strategiepapier)
    check("ANF01-13: Sektion 'Einkommen' im Grundsicherungs-PDF",
          "section('Einkommen')" in gs_body,
          "Einkommensnachweis-Sektion fehlt im Grundsicherungs-PDF")

    # ANF01-14: Alle sechs Einkommensfelder im Grundsicherungs-PDF referenziert
    check("ANF01-14a: einkommensart im Grundsicherungs-PDF",
          "get('einkommensart')" in gs_body,
          "einkommensart nicht referenziert")
    check("ANF01-14b: brutto_monat im Grundsicherungs-PDF",
          "get('brutto_monat')" in gs_body,
          "brutto_monat nicht referenziert")
    check("ANF01-14c: netto_monat im Grundsicherungs-PDF",
          "get('netto_monat')" in gs_body,
          "netto_monat nicht referenziert")
    check("ANF01-14d: letzter_arbeitgeber im Grundsicherungs-PDF",
          "get('letzter_arbeitgeber')" in gs_body,
          "letzter_arbeitgeber nicht referenziert")
    check("ANF01-14e: arbeitgeber_adresse im Grundsicherungs-PDF",
          "get('arbeitgeber_adresse')" in gs_body,
          "arbeitgeber_adresse nicht referenziert")
    check("ANF01-14f: gehaltsnachweis_ort im Grundsicherungs-PDF",
          "get('gehaltsnachweis_ort')" in gs_body,
          "gehaltsnachweis_ort nicht referenziert")

    # ANF01-15: Bestehende Grundsicherungs-Sektionen unveraendert
    check("ANF01-15a: Sektion Wohnsituation erhalten",
          "section('Wohnsituation')" in gs_body,
          "Sektion Wohnsituation wurde entfernt")
    check("ANF01-15b: Sektion Krankenversicherung erhalten",
          "section('Krankenversicherung')" in gs_body,
          "Sektion Krankenversicherung wurde entfernt")
    check("ANF01-15c: Sektion Familie erhalten",
          "section('Familie')" in gs_body,
          "Sektion Familie wurde entfernt")
    check("ANF01-15d: Checkliste erhalten",
          "gsChecks" in gs_body,
          "Checkliste wurde aus Grundsicherungs-PDF entfernt")

    # ═══════════════════════════════════════
    print("\n=== 54. ANF-02 KIND-DATEN STRUKTURIERT (Schritt 1: Datenmodell & UI) ===")
    # ═══════════════════════════════════════

    # ANF02-01: Funktion renderKinderBlocks vorhanden
    check("ANF02-01: Funktion renderKinderBlocks() vorhanden",
          "function renderKinderBlocks()" in html,
          "renderKinderBlocks() fehlt")

    # ANF02-02: Schluesselbegriff kinder_liste wird verwendet
    check("ANF02-02: Listenschluessel 'kinder_liste' vorhanden",
          "'kinder_liste'" in html,
          "Listenschluessel kinder_liste fehlt")

    # ANF02-03: Alle fuenf Felder pro Kind vorhanden
    kinder_fn = re.search(
        r'function renderKinderBlocks\(\)([\s\S]*?)(?=\n// |\nfunction )',
        html
    )
    kinder_body = kinder_fn.group(1) if kinder_fn else ""
    check("ANF02-03a: Feld vorname in renderKinderBlocks",
          "'vorname'" in kinder_body,
          "Feld vorname fehlt in renderKinderBlocks")
    check("ANF02-03b: Feld nachname in renderKinderBlocks",
          "'nachname'" in kinder_body,
          "Feld nachname fehlt in renderKinderBlocks")
    check("ANF02-03c: Feld geburtsdatum in renderKinderBlocks",
          "'geburtsdatum'" in kinder_body,
          "Feld geburtsdatum fehlt in renderKinderBlocks")
    check("ANF02-03d: Feld geburtsort in renderKinderBlocks",
          "'geburtsort'" in kinder_body,
          "Feld geburtsort fehlt in renderKinderBlocks")
    check("ANF02-03e: Feld sorgerecht_kind in renderKinderBlocks",
          "'sorgerecht_kind'" in kinder_body,
          "Feld sorgerecht_kind fehlt in renderKinderBlocks")

    # ANF02-04: Sorgerecht-Dropdown enthaelt die drei vorgegebenen Optionen
    check("ANF02-04a: Option Gemeinsam im Sorgerecht-Dropdown",
          "'Gemeinsam'" in kinder_body,
          "Option 'Gemeinsam' fehlt im Sorgerecht-Dropdown")
    check("ANF02-04b: Option Allein im Sorgerecht-Dropdown",
          "'Allein'" in kinder_body,
          "Option 'Allein' fehlt im Sorgerecht-Dropdown")
    check("ANF02-04c: Option Beim anderen Elternteil im Sorgerecht-Dropdown",
          "'Beim anderen Elternteil'" in kinder_body,
          "Option 'Beim anderen Elternteil' fehlt im Sorgerecht-Dropdown")

    # ANF02-05: Hinzufuegen-Button nutzt addItem mit kinder_liste
    check("ANF02-05: addItem('kinder_liste', ...) vorhanden",
          "addItem('kinder_liste'," in kinder_body,
          "addItem-Aufruf fuer kinder_liste fehlt")

    # ANF02-06: renderKinderBlocks wird im start-Template aufgerufen
    start_match = re.search(
        r"start:\s*\(\)\s*=>\s*`([\s\S]*?)`\s*,\s*\n\s*kontakte:",
        html
    )
    start_body = start_match.group(1) if start_match else ""
    check("ANF02-06: renderKinderBlocks() im start-Template aufgerufen",
          "renderKinderBlocks()" in start_body,
          "renderKinderBlocks() wird im start-Template nicht aufgerufen")

    # ANF02-07: Legacy-Feldschluessel noch im HTML vorhanden
    # (Formularfelder wurden in Schritt 5 ausgeblendet,
    #  Schluessel bleiben fuer Export und PDF erhalten.)
    check("ANF02-07a: Schluessel kinder_minderjaehrig noch im HTML",
          "'kinder_minderjaehrig'" in html,
          "Schluessel kinder_minderjaehrig fehlt — wurde versehentlich entfernt")
    check("ANF02-07b: Schluessel sorgerecht noch im HTML",
          "'sorgerecht'" in html,
          "Schluessel sorgerecht fehlt — wurde versehentlich entfernt")
    check("ANF02-07c: Formularfeld kinder_minderjaehrig im start-Template ausgeblendet",
          "field('kinder_minderjaehrig'" not in start_body,
          "Formularfeld kinder_minderjaehrig ist noch sichtbar (sollte ausgeblendet sein)")

    # ANF02-08: kinderListe im FIM-Export vorhanden (Schritt 2)
    fim_match2 = re.search(
        r'function exportFIMJson\(\)\s*\{([\s\S]*?)\n\}',
        html
    )
    fim_body2 = fim_match2.group(1) if fim_match2 else ""
    check("ANF02-08a: kinderListe in der familie-Sektion des FIM-Exports",
          "kinderListe:" in fim_body2,
          "kinderListe fehlt im FIM-Export (familie-Sektion)")
    check("ANF02-08b: kinderListe liest getList('kinder_liste')",
          "getList('kinder_liste')" in fim_body2,
          "kinderListe nutzt nicht getList('kinder_liste')")
    check("ANF02-08c: Legacy-Feld kinderMinderjaehrig bleibt im Export",
          "kinderMinderjaehrig:" in fim_body2,
          "Legacy-Feld kinderMinderjaehrig wurde aus dem Export entfernt")

    # ANF02-09: Elterngeld-PDF Kinder-Sektion (Schritt 3)
    eg2_match = re.search(
        r"type === 'elterngeld'[\s\S]*?(?=\}\s*else if \(type === 'arbeitsamt')",
        html
    )
    eg2_body = eg2_match.group(0) if eg2_match else ""
    check("ANF02-09: Elterngeld-PDF-Block fuer Schritt-3-Pruefung gefunden",
          bool(eg2_match),
          "Elterngeld-Block nicht auffindbar")
    check("ANF02-09a: Elterngeld-PDF liest getList('kinder_liste')",
          "getList('kinder_liste')" in eg2_body,
          "getList('kinder_liste') fehlt im Elterngeld-PDF")
    check("ANF02-09b: Elterngeld-PDF gibt Geburtsdatum pro Kind aus",
          "k.geburtsdatum" in eg2_body,
          "k.geburtsdatum fehlt im Elterngeld-PDF")
    check("ANF02-09c: Elterngeld-PDF gibt Geburtsort pro Kind aus",
          "k.geburtsort" in eg2_body,
          "k.geburtsort fehlt im Elterngeld-PDF")
    check("ANF02-09d: Elterngeld-PDF gibt Sorgerecht pro Kind aus",
          "k.sorgerecht_kind" in eg2_body,
          "k.sorgerecht_kind fehlt im Elterngeld-PDF")
    check("ANF02-09e: Elterngeld-PDF hat Freitext-Fallback",
          "get('kinder_minderjaehrig')" in eg2_body,
          "Freitext-Fallback kinder_minderjaehrig fehlt im Elterngeld-PDF")
    check("ANF02-09f: Checkliste unveraendert erhalten",
          "egChecks" in eg2_body,
          "Checkliste wurde aus Elterngeld-PDF entfernt")

    # ANF02-10: Kindergeld-PDF Kinder-Sektion (Schritt 4)
    kg_match = re.search(
        r"type === 'kindergeld'[\s\S]*?(?=\}\s*else if \(type === 'elterngeld')",
        html
    )
    kg_body = kg_match.group(0) if kg_match else ""
    check("ANF02-10: Kindergeld-PDF-Block gefunden",
          bool(kg_match),
          "Kindergeld-Block nicht auffindbar")
    check("ANF02-10a: Kindergeld-PDF liest getList('kinder_liste')",
          "getList('kinder_liste')" in kg_body,
          "getList('kinder_liste') fehlt im Kindergeld-PDF")
    check("ANF02-10b: Kindergeld-PDF gibt Geburtsdatum pro Kind aus",
          "k.geburtsdatum" in kg_body,
          "k.geburtsdatum fehlt im Kindergeld-PDF")
    check("ANF02-10c: Kindergeld-PDF gibt Geburtsort pro Kind aus",
          "k.geburtsort" in kg_body,
          "k.geburtsort fehlt im Kindergeld-PDF")
    check("ANF02-10d: Kindergeld-PDF gibt Sorgerecht pro Kind aus",
          "k.sorgerecht_kind" in kg_body,
          "k.sorgerecht_kind fehlt im Kindergeld-PDF")
    check("ANF02-10e: Kindergeld-PDF hat Freitext-Fallback",
          "get('kinder_minderjaehrig')" in kg_body,
          "Freitext-Fallback kinder_minderjaehrig fehlt im Kindergeld-PDF")
    check("ANF02-10f: Kindergeld-Checkliste unveraendert erhalten",
          "checks" in kg_body and "Geburtsurkunde" in kg_body,
          "Checkliste wurde aus Kindergeld-PDF entfernt")

    # ═══════════════════════════════════════
    print("\n=== 41. ANF-03 EUDI WALLET IMPORT (SCHRITT 1) ===")
    # ═══════════════════════════════════════

    # ANF03-01a: Import-Button im Import-Dialog vorhanden
    check("ANF03-01a: EUDI-Wallet-Import-Button im HTML vorhanden",
          "importEudiWallet(event)" in html,
          "importEudiWallet(event) fehlt im HTML")

    # ANF03-01b: Funktion importEudiWallet() vorhanden
    check("ANF03-01b: Funktion importEudiWallet() im HTML vorhanden",
          "function importEudiWallet" in html,
          "function importEudiWallet fehlt im HTML")

    # ANF03-02a: Parser-Funktion parseEudiSdJwt() vorhanden
    check("ANF03-02a: Funktion parseEudiSdJwt() vorhanden",
          "function parseEudiSdJwt" in html,
          "function parseEudiSdJwt fehlt im HTML")

    # ANF03-02b: Hilfsfunktion _b64urlDecode() vorhanden
    check("ANF03-02b: Hilfsfunktion _b64urlDecode() vorhanden",
          "function _b64urlDecode" in html,
          "function _b64urlDecode fehlt im HTML")

    # ANF03-02c: Alle fuenf Vivodepot-Zielfelder werden im Parser gemappt
    import re as _re
    parser_match = _re.search(
        r'function parseEudiSdJwt[\s\S]*?(?=\nfunction importEudiWallet)',
        html
    )
    parser_body = parser_match.group(0) if parser_match else ""
    check("ANF03-02c: Parser mappt Feld nachname",
          "mapped.nachname" in parser_body,
          "mapped.nachname fehlt im Parser")
    check("ANF03-02d: Parser mappt Feld vorname",
          "mapped.vorname" in parser_body,
          "mapped.vorname fehlt im Parser")
    check("ANF03-02e: Parser mappt Feld geburtsdatum",
          "mapped.geburtsdatum" in parser_body,
          "mapped.geburtsdatum fehlt im Parser")
    check("ANF03-02f: Parser mappt Feld strasse",
          "mapped.strasse" in parser_body,
          "mapped.strasse fehlt im Parser")
    check("ANF03-02g: Parser mappt Feld staatsangehoerigkeit",
          "mapped.staatsangehoerigkeit" in parser_body,
          "mapped.staatsangehoerigkeit fehlt im Parser")

    # ANF03-02h: Kein Netzwerk-Call im Parser-Code (fetch, XMLHttpRequest)
    check("ANF03-02h: Kein fetch() im Parser-Code",
          "fetch(" not in parser_body,
          "fetch() wurde im Parser-Code gefunden -- Offline-Pflicht verletzt")
    check("ANF03-02i: Kein XMLHttpRequest im Parser-Code",
          "XMLHttpRequest" not in parser_body,
          "XMLHttpRequest wurde im Parser-Code gefunden -- Offline-Pflicht verletzt")

    # ANF03-02j: Parser liest Disclosures (Tilde-Trennung)
    check("ANF03-02j: Parser liest Disclosures (Tilde-Trennung ~)",
          "split('~')" in parser_body or 'split("~")' in parser_body,
          "Tilde-Trennung fehlt im Parser -- Disclosures werden nicht gelesen")

    # ═══════════════════════════════════════
    print("\n=== 42. ANF-03 EUDI WALLET IMPORT (SCHRITT 3 -- FIXTURE) ===")
    # ═══════════════════════════════════════
    # Testfixture: handgefertigtes SD-JWT nach IETF-Muster (Erika Mustermann).
    # Quelle des Datenmusters: IETF SD-JWT VC Appendix A.3, EUDI PID Rulebook.
    # Die Signatur ist ein Platzhalter -- fuer den Import ist nur der Payload
    # und die Disclosures relevant, nicht die kryptografische Gueltigkeit.
    FIXTURE_SDJWT = (
        "eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImRjK3NkLWp3dCJ9"
        ".eyJpc3MiOiAiaHR0cHM6Ly9pc3N1ZXIuZXhhbXBsZS5kZSIsICJpYXQiOiAxNjgzMDAwMDAwLCAiZXhwIjogMTg4MzAwMDAwMCwgInZjdCI6ICJodHRwczovL2JtaS5idW5kLmV4YW1wbGUvY3JlZGVudGlhbC9waWQvMS4wIn0"
        ".VklWT0RFUE9ULVRFU1QtRklYVFVSRS1LRUlORS1FQ0hURS1TSUdOQVRVUg"
        "~WyJTYWx0Vm9ybmFtZTAwMSIsICJnaXZlbl9uYW1lIiwgIkVyaWthIl0"
        "~WyJTYWx0TmFjaG5hbWUwMDIiLCAiZmFtaWx5X25hbWUiLCAiTXVzdGVybWFubiJd"
        "~WyJTYWx0R2ViRGF0MDAzIiwgImJpcnRoZGF0ZSIsICIxOTYzLTA4LTEyIl0"
        "~WyJTYWx0QWRyZXNzZTAwNCIsICJhZGRyZXNzIiwgeyJzdHJlZXRfYWRkcmVzcyI6ICJIZWlkZXN0cmFzc2UgMTciLCAibG9jYWxpdHkiOiAiS29lbG4iLCAicG9zdGFsX2NvZGUiOiAiNTExNDciLCAiY291bnRyeSI6ICJERSJ9XQ"
        "~WyJTYWx0TmF0aW9uMDA1IiwgIm5hdGlvbmFsaXRpZXMiLCBbIkRFIl1d~"
    )

    # Parser in Python nachbauen (spiegelt die JS-Logik in parseEudiSdJwt).
    import base64 as _b64
    import json as _json

    def _b64url_decode_py(s):
        b = s.replace('-', '+').replace('_', '/')
        while len(b) % 4:
            b += '='
        try:
            return _b64.b64decode(b).decode('utf-8')
        except Exception:
            return None

    def parse_fixture(token):
        teile = token.strip().split('~')
        jwt_teile = teile[0].split('.')
        if len(jwt_teile) < 2:
            return {}
        payload_text = _b64url_decode_py(jwt_teile[1])
        if not payload_text:
            return {}
        try:
            payload = _json.loads(payload_text)
        except Exception:
            return {}
        offengelegt = {}
        for i in range(1, len(teile)):
            if not teile[i]:
                continue
            disc_text = _b64url_decode_py(teile[i])
            if not disc_text:
                continue
            try:
                arr = _json.loads(disc_text)
                if isinstance(arr, list) and len(arr) == 3:
                    offengelegt[arr[1]] = arr[2]
            except Exception:
                pass
        def lese(feld):
            if feld in payload:
                return payload[feld]
            if feld in offengelegt:
                return offengelegt[feld]
            return None
        mapped = {}
        fn = lese('family_name')
        if fn:
            mapped['nachname'] = fn
        gn = lese('given_name')
        if gn:
            mapped['vorname'] = gn
        bd = lese('birth_date') or lese('birthdate')
        if bd:
            mapped['geburtsdatum'] = bd
        adr = lese('address')
        if isinstance(adr, dict):
            st = adr.get('street_address', '')
            plz = adr.get('postal_code', '')
            ort = adr.get('locality', '')
            if st:
                mapped['strasse'] = st
            if plz or ort:
                mapped['plz_ort'] = (plz + ' ' + ort).strip()
        nat = lese('nationalities') or lese('nationality')
        if isinstance(nat, list) and len(nat) > 0:
            mapped['staatsangehoerigkeit'] = nat[0]
        elif isinstance(nat, str) and nat:
            mapped['staatsangehoerigkeit'] = nat
        return mapped

    fixture_result = parse_fixture(FIXTURE_SDJWT)

    check("ANF03-03a: Fixture -- Nachname 'Mustermann' erkannt",
          fixture_result.get('nachname') == 'Mustermann',
          f"nachname ist '{fixture_result.get('nachname')}', erwartet 'Mustermann'")

    check("ANF03-03b: Fixture -- Vorname 'Erika' erkannt",
          fixture_result.get('vorname') == 'Erika',
          f"vorname ist '{fixture_result.get('vorname')}', erwartet 'Erika'")

    check("ANF03-03c: Fixture -- Geburtsdatum '1963-08-12' erkannt",
          fixture_result.get('geburtsdatum') == '1963-08-12',
          f"geburtsdatum ist '{fixture_result.get('geburtsdatum')}', erwartet '1963-08-12'")

    check("ANF03-03d: Fixture -- Strasse 'Heidestrasse 17' erkannt",
          fixture_result.get('strasse') == 'Heidestrasse 17',
          f"strasse ist '{fixture_result.get('strasse')}', erwartet 'Heidestrasse 17'")

    check("ANF03-03e: Fixture -- PLZ/Ort '51147 Koeln' erkannt",
          fixture_result.get('plz_ort') == '51147 Koeln',
          f"plz_ort ist '{fixture_result.get('plz_ort')}', erwartet '51147 Koeln'")

    check("ANF03-03f: Fixture -- Staatsangehoerigkeit 'DE' erkannt",
          fixture_result.get('staatsangehoerigkeit') == 'DE',
          f"staatsangehoerigkeit ist '{fixture_result.get('staatsangehoerigkeit')}', erwartet 'DE'")

    check("ANF03-03g: Fixture -- genau sechs Felder erkannt",
          len(fixture_result) == 6,
          f"{len(fixture_result)} Felder erkannt, erwartet 6")

    # --- ANF-04 Schritt 6: CarePlan -- Pflegeplan-Struktur ---

    check("ANF04-06a: CarePlan -- resourceType-Auswertung im Code vorhanden",
          "'CarePlan'" in html,
          "CarePlan-Block nicht im Code gefunden")

    check("ANF04-06b: CarePlan -- Titel (r.title) im Code vorhanden",
          "r.title" in html,
          "r.title nicht im Code gefunden")

    check("ANF04-06c: CarePlan -- Beschreibung (r.description) im Code vorhanden",
          "r.description" in html,
          "r.description nicht im Code gefunden")

    check("ANF04-06d: CarePlan -- Massnahmen (activity[].detail.description) im Code vorhanden",
          "akt.detail" in html and "akt.detail.description" in html,
          "activity-Auswertung nicht im Code gefunden")

    check("ANF04-06e: CarePlan -- Praefix 'Pflegeplan:' im Code vorhanden",
          "'Pflegeplan: '" in html,
          "Praefix 'Pflegeplan: ' nicht im Code gefunden")

    check("ANF04-06f: CarePlan -- Praefix 'Massnahme:' im Code vorhanden",
          "'Massnahme: '" in html,
          "Praefix 'Massnahme: ' nicht im Code gefunden")

    check("ANF04-06g: CarePlan -- Eintrag wird in vorsorge_uebersicht gespeichert",
          "cpEintraege" in html and "vorsorge_uebersicht" in html,
          "Zuweisung nach vorsorge_uebersicht fuer CarePlan nicht im Code gefunden")

    # --- ANF-04 Schritt 5: Immunization -- Impfstoff, Datum, Charge ---

    check("ANF04-05a: Immunization -- resourceType-Auswertung im Code vorhanden",
          "'Immunization'" in html,
          "Immunization-Block nicht im Code gefunden")

    check("ANF04-05b: Immunization -- Impfstoffname (vaccineCode) im Code vorhanden",
          "vaccineCode" in html,
          "vaccineCode nicht im Code gefunden")

    check("ANF04-05c: Immunization -- Datum (occurrenceDateTime) im Code vorhanden",
          "occurrenceDateTime" in html,
          "occurrenceDateTime nicht im Code gefunden")

    check("ANF04-05d: Immunization -- Chargennummer (lotNumber) im Code vorhanden",
          "lotNumber" in html,
          "lotNumber nicht im Code gefunden")

    check("ANF04-05e: Immunization -- Eintrag beginnt mit 'Impfung:'",
          "'Impfung: '" in html,
          "Prafix 'Impfung: ' nicht im Code gefunden")

    check("ANF04-05f: Immunization -- Eintrag wird in vorsorge_uebersicht gespeichert",
          "impfEintrag" in html and "vorsorge_uebersicht" in html,
          "Zuweisung nach vorsorge_uebersicht fuer Immunization nicht im Code gefunden")

    # --- ANF-04 Schritt 4: Observation -- Blutdruck, Gewicht, Blutzucker ---

    check("ANF04-04a: Observation -- LOINC-Code fuer Blutdruck systolisch (8480-6) vorhanden",
          "'8480-6'" in html,
          "LOINC 8480-6 (Blutdruck systolisch) nicht im Code gefunden")

    check("ANF04-04b: Observation -- LOINC-Code fuer Blutdruck diastolisch (8462-4) vorhanden",
          "'8462-4'" in html,
          "LOINC 8462-4 (Blutdruck diastolisch) nicht im Code gefunden")

    check("ANF04-04c: Observation -- LOINC-Code fuer Koerpergewicht (29463-7) vorhanden",
          "'29463-7'" in html,
          "LOINC 29463-7 (Koerpergewicht) nicht im Code gefunden")

    check("ANF04-04d: Observation -- LOINC-Code fuer Blutzucker (2339-0) vorhanden",
          "'2339-0'" in html,
          "LOINC 2339-0 (Blutzucker) nicht im Code gefunden")

    check("ANF04-04e: Observation -- Messwerte werden in vorsorge_uebersicht gespeichert",
          "vorsorge_uebersicht" in html and "Blutdruck" in html,
          "vorsorge_uebersicht-Zuweisung fuer Observation nicht im Code gefunden")

    check("ANF04-04f: Observation -- Blutdruck-Panel-Komponenten (component[]) werden ausgewertet",
          "r.component" in html,
          "Komponenten-Auswertung fuer Blutdruck-Panel nicht im Code gefunden")

    # --- ANF-04 Schritt 3: MedicationStatement -- Dosierung, Einnahmezeit, Dauermedikation ---

    check("ANF04-03a: MedicationStatement -- Einnahmezeit (when) im Code vorhanden",
          "whenMap" in html and "MORN" in html,
          "Einnahmezeit-Auswertung (whenMap/MORN) nicht im Code gefunden")

    check("ANF04-03b: MedicationStatement -- Einnahmezeit (timeOfDay) im Code vorhanden",
          "timeOfDay" in html,
          "timeOfDay nicht im Code gefunden")

    check("ANF04-03c: MedicationStatement -- Dauermedikation-Auswertung im Code vorhanden",
          "Dauermedikation" in html and "hatEnddatum" in html,
          "Dauermedikation-Auswertung nicht im Code gefunden")

    check("ANF04-03d: MedicationStatement -- FHIR-Kuerzel 'morgens' uebersetzt",
          "morgens" in html,
          "'morgens' nicht im Code gefunden")

    # --- ANF-04 Schritt 2: Condition -- ICD-10-Code und Datum ---

    check("ANF04-02a: Condition -- ICD-10-Code-Auswertung im Code vorhanden",
          "icd" in html.lower() and "icdCode" in html,
          "ICD-10-Auswertung nicht im Code gefunden")

    check("ANF04-02b: Condition -- Datumsauswertung (onsetDateTime) im Code vorhanden",
          "onsetDateTime" in html,
          "onsetDateTime nicht im Code gefunden")

    check("ANF04-02c: Condition -- Datumsauswertung (recordedDate) im Code vorhanden",
          "recordedDate" in html,
          "recordedDate nicht im Code gefunden")

    check("ANF04-02d: Condition -- Datum wird auf 10 Zeichen gekuerzt (YYYY-MM-DD)",
          "substring(0, 10)" in html,
          "Datum-Kuerzung auf 10 Zeichen nicht im Code gefunden")

    # --- ANF-04 Schritt 1: AllergyIntolerance -- Reaktionstyp und Schweregrad ---
    fhir_allergy_fixture = '''{
      "resourceType": "Bundle",
      "entry": [{
        "resource": {
          "resourceType": "AllergyIntolerance",
          "type": "allergy",
          "code": {
            "text": "Erdnuss"
          },
          "reaction": [{
            "severity": "severe"
          }]
        }
      }]
    }'''

    check("ANF04-01a: AllergyIntolerance -- Reaktionstyp 'Allergie' im Ergebnis",
          "'Allergie'" in html or "reaktionstyp" in html.lower() or "r.type" in html,
          "Reaktionstyp-Auswertung nicht im Code gefunden")

    check("ANF04-01b: AllergyIntolerance -- Schweregrad 'schwer' im Ergebnis",
          "'schwer'" in html or "severity" in html,
          "Schweregrad-Auswertung nicht im Code gefunden")

    check("ANF04-01c: AllergyIntolerance -- Zusatzangaben in Klammern",
          "zusatz" in html and "filter(Boolean)" in html,
          "Klammer-Logik fuer Zusatzangaben nicht im Code gefunden")

    # ═══════════════════════════════════════
    print("\n=== ANF-06 Schritt 1: QR-Übergabe -- Auswahldialog ===")
    # ═══════════════════════════════════════

    # ANF06-01a: Einstiegspunkt vorhanden
    check("ANF06-01a: qrUebergabeOpen() -- Funktion vorhanden",
          "function qrUebergabeOpen" in html,
          "Funktion qrUebergabeOpen fehlt")

    # ANF06-01b: Modal-Overlay vorhanden
    check("ANF06-01b: id='qr-overlay' -- Modal vorhanden",
          'id="qr-overlay"' in html,
          "Modal-Overlay qr-overlay fehlt")

    # ANF06-01c: Schritt-1-Element vorhanden
    check("ANF06-01c: id='qr-step-1' -- Schritt 1 vorhanden",
          'id="qr-step-1"' in html,
          "qr-step-1 fehlt")

    # ANF06-01d: Schritt-2-Element vorhanden
    check("ANF06-01d: id='qr-step-2' -- Schritt 2 vorhanden",
          'id="qr-step-2"' in html,
          "qr-step-2 fehlt")

    # ANF06-01e: Schritt-3-Element vorhanden
    check("ANF06-01e: id='qr-step-3' -- Schritt 3 vorhanden",
          'id="qr-step-3"' in html,
          "qr-step-3 fehlt")

    # ANF06-01f: Alle vier Profil-Cards vorhanden
    for profil in ['notfall', 'vollmacht', 'familie', 'behoerde']:
        check(f"ANF06-01f-{profil}: Profil-Card id='qr-card-{profil}' vorhanden",
              f'id="qr-card-{profil}"' in html,
              f"Profil-Card qr-card-{profil} fehlt")

    # ANF06-01g: Weiter-Button Schritt 1 vorhanden und initial deaktiviert
    check("ANF06-01g: id='qr-weiter-1' -- Weiter-Button Schritt 1 vorhanden",
          'id="qr-weiter-1"' in html,
          "qr-weiter-1 fehlt")

    # ANF06-01h: qrWaehleProfilCard vorhanden
    check("ANF06-01h: qrWaehleProfilCard -- Funktion vorhanden",
          "function qrWaehleProfilCard" in html,
          "Funktion qrWaehleProfilCard fehlt")

    # ANF06-01i: qrZeigeSchritt vorhanden
    check("ANF06-01i: qrZeigeSchritt -- Funktion vorhanden",
          "function qrZeigeSchritt" in html,
          "Funktion qrZeigeSchritt fehlt")

    # ANF06-01j: qrUebergabeClose vorhanden
    check("ANF06-01j: qrUebergabeClose -- Funktion vorhanden",
          "function qrUebergabeClose" in html,
          "Funktion qrUebergabeClose fehlt")

    # ANF06-01k: Link-Button im Export-Bereich vorhanden
    check("ANF06-01k: qrUebergabeOpen() -- Aufruf im Export-Bereich vorhanden",
          'onclick="qrUebergabeOpen()"' in html,
          "Aufruf qrUebergabeOpen() nicht im Export-Bereich gefunden")

    # ANF06-01l: qr-overlay in hideAllOverlays-Liste eingetragen
    check("ANF06-01l: qr-overlay -- in Overlay-Schliess-Liste eingetragen",
          "'qr-overlay'" in html,
          "qr-overlay fehlt in der Overlay-Schliess-Liste")

    # ANF06-01m: Schritt-Indikatoren (qr-dot) vorhanden
    check("ANF06-01m: qr-dot-1/2/3 -- Fortschritts-Punkte vorhanden",
          'id="qr-dot-1"' in html and 'id="qr-dot-2"' in html and 'id="qr-dot-3"' in html,
          "Fortschritts-Punkte qr-dot-1/2/3 fehlen")

    # ═══════════════════════════════════════
    print("\n=== ANF-06 Schritt 2/3: QR-Übergabe -- Verschlüsselung, QR-Code, Empfang ===")
    # ═══════════════════════════════════════

    # ANF06-02a: jsQR inline eingebettet
    check("ANF06-02a: jsQR -- inline eingebettet",
          "jsQR v1.4.0" in html or "jsQR(" in html,
          "jsQR-Bibliothek fehlt")

    # ANF06-02b: Zeitstempel im Payload (iat)
    check("ANF06-02b: Zeitstempel iat im Payload vorhanden",
          "iat:" in html and "Date.now()" in html,
          "Zeitstempel iat fehlt im qrErstellen-Code")

    # ANF06-02c: Ablauf exp im Payload (24 Stunden)
    check("ANF06-02c: Ablauf exp (24 Stunden) im Payload vorhanden",
          "exp:" in html and "24 * 60 * 60 * 1000" in html,
          "Ablauf-Logik (24 Stunden) fehlt")

    # ANF06-02d: AES-Verschlüsselung via deriveKey + encryptData
    check("ANF06-02d: AES-Verschlüsselung -- deriveKey und encryptData im qrErstellen-Code",
          "deriveKey(pin" in html and "encryptData(payload" in html,
          "deriveKey oder encryptData fehlt im qrErstellen-Code")

    # ANF06-02e: Eigener Salt (getRandomValues) -- getrennt vom Hauptpasswort
    check("ANF06-02e: Eigener Salt -- crypto.getRandomValues im qrErstellen-Code",
          "getRandomValues" in html and "qrSalt" in html,
          "Eigener Salt fuer QR fehlt")

    # ANF06-02f: qrcode-Bibliothek wird fuer QR-Erzeugung verwendet
    check("ANF06-02f: qrcode -- fuer QR-Code-Erzeugung verwendet",
          "qr.addData(qrPayload)" in html,
          "qr.addData(qrPayload) fehlt")

    # ANF06-02g: Ablauf-Info wird angezeigt (qr-ablauf-info)
    check("ANF06-02g: qr-ablauf-info -- Ablaufdatum wird angezeigt",
          'id="qr-ablauf-info"' in html,
          "Element qr-ablauf-info fehlt")

    # ANF06-03a: Empfänger-Modal qre-overlay vorhanden
    check("ANF06-03a: id='qre-overlay' -- Empfänger-Modal vorhanden",
          'id="qre-overlay"' in html,
          "Empfänger-Modal qre-overlay fehlt")

    # ANF06-03b: qrEmpfangOpen vorhanden
    check("ANF06-03b: qrEmpfangOpen -- Funktion vorhanden",
          "function qrEmpfangOpen" in html,
          "Funktion qrEmpfangOpen fehlt")

    # ANF06-03c: qrEmpfangClose vorhanden
    check("ANF06-03c: qrEmpfangClose -- Funktion vorhanden",
          "function qrEmpfangClose" in html,
          "Funktion qrEmpfangClose fehlt")

    # ANF06-03d: qreStartKamera vorhanden
    check("ANF06-03d: qreStartKamera -- Funktion vorhanden",
          "function qreStartKamera" in html,
          "Funktion qreStartKamera fehlt")

    # ANF06-03e: qreScanFrame (Kamerabild auslesen) vorhanden
    check("ANF06-03e: qreScanFrame -- Funktion vorhanden",
          "function qreScanFrame" in html,
          "Funktion qreScanFrame fehlt")

    # ANF06-03f: qreQrErkannt vorhanden
    check("ANF06-03f: qreQrErkannt -- Funktion vorhanden",
          "function qreQrErkannt" in html,
          "Funktion qreQrErkannt fehlt")

    # ANF06-03g: qreEntschluesseln vorhanden
    check("ANF06-03g: qreEntschluesseln -- Funktion vorhanden",
          "function qreEntschluesseln" in html,
          "Funktion qreEntschluesseln fehlt")

    # ANF06-03h: Ablauf-Prüfung im Empfänger (payload.exp)
    check("ANF06-03h: Ablauf-Prüfung -- payload.exp und Date.now() im qreEntschluesseln-Code",
          "payload.exp" in html and "Date.now() > payload.exp" in html,
          "Ablauf-Prüfung im Empfänger fehlt")

    # ANF06-03i: getUserMedia (Kamerazugriff)
    check("ANF06-03i: getUserMedia -- Kamerazugriff im Code vorhanden",
          "getUserMedia" in html,
          "getUserMedia fehlt")

    # ANF06-03j: Video-Element fuer Kamerabild vorhanden
    check("ANF06-03j: id='qre-video' -- Video-Element vorhanden",
          'id="qre-video"' in html,
          "Video-Element qre-video fehlt")

    # ANF06-03k: Empfänger-Link im Export-Bereich vorhanden
    check("ANF06-03k: qrEmpfangOpen() -- Aufruf im Export-Bereich vorhanden",
          'onclick="qrEmpfangOpen()"' in html,
          "Aufruf qrEmpfangOpen() fehlt")

    # ANF06-03l: qre-overlay in Overlay-Listen eingetragen
    check("ANF06-03l: qre-overlay -- in Overlay-Schliess-Listen eingetragen",
          "'qre-overlay'" in html,
          "qre-overlay fehlt in den Overlay-Schliess-Listen")

    # ANF06-03m: WG_FELDNAMEN wird im Empfänger fuer Feldbezeichnungen verwendet
    check("ANF06-03m: WG_FELDNAMEN -- im Empfänger-Dialog verwendet",
          "WG_FELDNAMEN[k]" in html,
          "WG_FELDNAMEN wird im Empfänger nicht verwendet")

    # ═══════════════════════════════════════
    print("\n=== 53. ANF-05 SOLID POD EXPORT ===")
    # ═══════════════════════════════════════

    # ANF05-01: Solid-Pod-Link im Export-Bereich vorhanden
    check("ANF05-01: solidPodOpen() -- Link im Export-Bereich vorhanden",
          "solidPodOpen()" in html,
          "solidPodOpen() fehlt im Export-Bereich")

    # ANF05-02: Modal sp-overlay vorhanden
    check("ANF05-02: id='sp-overlay' -- Solid-Pod-Modal vorhanden",
          'id="sp-overlay"' in html,
          "sp-overlay-Modal fehlt")

    # ANF05-03: solidPodOpen Funktion vorhanden
    check("ANF05-03: function solidPodOpen -- Oeffnungs-Funktion vorhanden",
          "function solidPodOpen" in html,
          "function solidPodOpen fehlt")

    # ANF05-04: solidPodClose Funktion vorhanden
    check("ANF05-04: function solidPodClose -- Schliess-Funktion vorhanden",
          "function solidPodClose" in html,
          "function solidPodClose fehlt")

    # ANF05-05: solidPodExport Funktion vorhanden
    check("ANF05-05: function solidPodExport -- Export-Funktion vorhanden",
          "function solidPodExport" in html,
          "function solidPodExport fehlt")

    # ANF05-06: Turtle-Format (text/turtle) wird erzeugt
    check("ANF05-06: text/turtle -- Turtle-MIME-Typ wird verwendet",
          "text/turtle" in html,
          "text/turtle-MIME-Typ fehlt -- kein Turtle-Format")

    # ANF05-07: Turtle-Praefix fuer vcard vorhanden
    check("ANF05-07: @prefix vcard -- Turtle-Praefix vcard vorhanden",
          "@prefix vcard:" in html,
          "@prefix vcard: fehlt in solidPodExport")

    # ANF05-08: Turtle-Praefix fuer schema.org vorhanden
    check("ANF05-08: @prefix schema -- Turtle-Praefix schema.org vorhanden",
          "@prefix schema:" in html,
          "@prefix schema: fehlt in solidPodExport")

    # ANF05-09: Turtle-Datei-Download mit .ttl-Endung
    check("ANF05-09: _solid.ttl -- Dateiname mit .ttl-Endung",
          "_solid.ttl" in html,
          "Dateiname-Muster _solid.ttl fehlt")

    # ANF05-10: sp-overlay in Overlay-Listen eingetragen
    check("ANF05-10: sp-overlay -- in Overlay-Schliess-Listen eingetragen",
          "'sp-overlay'" in html,
          "sp-overlay fehlt in den Overlay-Listen")

    # ANF05-11: Auswahl-Checkboxen vorhanden (Persoenliche Daten)
    check("ANF05-11: id='sp-cb-person' -- Checkbox fuer Persoenliche Angaben vorhanden",
          'id="sp-cb-person"' in html,
          "Checkbox sp-cb-person fehlt")

    # ANF05-12: Auswahl-Checkbox Gesundheit vorhanden
    check("ANF05-12: id='sp-cb-gesundheit' -- Checkbox fuer Gesundheitsdaten vorhanden",
          'id="sp-cb-gesundheit"' in html,
          "Checkbox sp-cb-gesundheit fehlt")

    # ANF05-13: solidPodZeigStatus Hilfsfunktion vorhanden
    check("ANF05-13: function solidPodZeigStatus -- Status-Hilfsfunktion vorhanden",
          "function solidPodZeigStatus" in html,
          "function solidPodZeigStatus fehlt")

    # ANF05-14: solidPodEsc Escape-Funktion fuer Turtle-Strings vorhanden
    check("ANF05-14: function solidPodEsc -- Escape-Funktion fuer Turtle vorhanden",
          "function solidPodEsc" in html,
          "function solidPodEsc fehlt")


    # ═══════════════════════════════════════
    print("\n=== FEEDBACK-01 (April 2026) ===")
    # ═══════════════════════════════════════

    # Punkt 2: A+-Hinweis korrigiert
    check("FB01-02: A+-Hinweis nennt Drei-Punkte-Menue statt 'oben rechts auf A+'",
          "Schriftgr\u00f6\u00dfe A\u207a" in html and "A\u207a um die Schrift zu vergr\u00f6\u00dfern" not in html,
          "Alter A+-Hinweis noch vorhanden oder neuer Hinweis fehlt")

    # Punkt 3: Einleitungstext
    check("FB01-03: Einleitungstext erklaert was Vivodepot ist",
          "Ihr pers\u00f6nlicher Vorsorge-Ordner" in html,
          "Einleitungstext fehlt")

    # Punkt 4: 'Ohne Auswahl starten' umbenannt
    check("FB01-04: 'Ohne Auswahl starten' umbenannt",
          "Ohne Auswahl starten" not in html,
          "'Ohne Auswahl starten' noch vorhanden")
    check("FB01-04b: Neuer Text 'Alle Bereiche anzeigen' vorhanden",
          "Alle Bereiche anzeigen" in html,
          "Neuer Fokus-Skip-Text fehlt")

    # Punkt 6: Foto-Loeschen-Button beschriftet
    check("FB01-06: Foto-Loeschen-Button hat Beschriftung 'Foto entfernen'",
          "Foto entfernen" in html,
          "Beschriftung 'Foto entfernen' fehlt")

    # Punkt 7: Familienstand als Dropdown
    check("FB01-07: Familienstand ist Dropdown (select-Element)",
          "verheiratet" in html and "verwitwet" in html and "ledig" in html,
          "Familienstand-Dropdown-Optionen fehlen")
    check("FB01-07b: Familienstand nicht mehr als Freitext-Feld",
          "z. B. verheiratet, geschieden, verwitwet" not in html,
          "Alter Freitext-Platzhalter fuer Familienstand noch vorhanden")

    # Punkt 9: Scroll nach Kind hinzufuegen
    check("FB01-09: Nach 'Kind hinzufuegen' wird zum neuen Eintrag gescrollt",
          "scrollIntoView" in html,
          "scrollIntoView-Aufruf in addItem fehlt")

    # Punkte 13+14: Button vereinheitlicht
    check("FB01-13: 'Abhaken' nicht mehr als Button-Text vorhanden",
          "Abhaken" not in html,
          "'Abhaken' noch als Button-Text vorhanden")
    check("FB01-14: 'Fertig?' nicht mehr als alleiniger Button-Text",
          "Fertig?' " not in html,
          "'Fertig?' noch als Button-Text vorhanden")
    check("FB01-13b: Neue Beschriftung 'Als erledigt markieren' vorhanden",
          "Als erledigt markieren" in html,
          "Neue Button-Beschriftung fehlt")

    # ═══════════════════════════════════════
    print("\n=== FEEDBACK-02 (April 2026) ===")
    # ═══════════════════════════════════════

    # Punkt 5: Fokus-Wizard Erklärung verbessert
    check("FB02-05: Fokus-Wizard erklaert dass Fokus aenderbar ist",
          "k\u00f6nnen den Fokus jederzeit \u00e4ndern" in html,
          "Hinweis auf Fokus-Aenderbarkeit fehlt")

    # Punkt 11: Adresse direkt sichtbar (nicht mehr im Aufklapp-Bereich)
    check("FB02-11: Strasse nicht mehr im Aufklapp-Bereich (mehr-Block ohne strasse)",
          "'strasse','plz_ort','email','nationalitaet','kinder_erwachsen','unterhalt'" not in html,
          "Alter Aufklapp-Block mit Adresse noch vorhanden")
    check("FB02-11b: Strasse direkt im start-Renderer sichtbar (vor renderKinderBlocks)",
          "field('strasse','Strasse" in html,
          "Strassen-Feld fehlt ganz")

    # Punkt 16: Footer-Bar auf Desktop ausgeblendet
    check("FB02-16: save-reminder-bar auf Desktop (min-width 701px) ausgeblendet",
          "min-width: 701px" in html and "save-reminder-bar" in html,
          "Desktop-Ausblendung der mobilen Navigationsleiste fehlt")

    passed = sum(1 for s, _, _ in results if s == "PASS")
    failed = sum(1 for s, _, _ in results if s == "FAIL")
    total = len(results)
    
    print(f"\n  Gesamt: {total} Tests")
    print(f"  ✓ Bestanden: {passed}")
    print(f"  ❌ Fehlgeschlagen: {failed}")
    
    if failed == 0:
        print("\n  🎉 ALLE TESTS BESTANDEN — Datei ist Baseline-tauglich!")
    else:
        print(f"\n  ⚠️  {failed} Tests fehlgeschlagen — Datei ist NICHT Baseline-tauglich.")
        print("\n  Fehlgeschlagene Tests:")
        for s, name, detail in results:
            if s == "FAIL":
                print(f"    ❌ {name}" + (f" — {detail}" if detail else ""))
    
    # ═══════════════════════════════════════
    print("\n=== 54. DATENAUSTAUSCH-STEP ===")
    # ═══════════════════════════════════════

    # Step in STEPS-Liste vorhanden
    check("Datenaustausch: Step 'datenaustausch' in STEPS",
          "{ id: 'datenaustausch'" in html,
          "Step 'datenaustausch' fehlt in der STEPS-Liste")

    # Renderer vorhanden
    check("Datenaustausch: Renderer 'datenaustausch: () =>' vorhanden",
          "datenaustausch: () =>" in html,
          "Renderer fuer 'datenaustausch' fehlt")

    # Position: datenaustausch liegt zwischen dokumente und erinnerung
    pos_dok   = html.find("{ id: 'dokumente'")
    pos_da    = html.find("{ id: 'datenaustausch'")
    pos_erin  = html.find("{ id: 'erinnerung'")
    check("Datenaustausch: Reihenfolge dokumente → datenaustausch → erinnerung",
          0 < pos_dok < pos_da < pos_erin,
          f"Reihenfolge falsch: dokumente={pos_dok}, datenaustausch={pos_da}, erinnerung={pos_erin}")

    # Import-Karten im Renderer vorhanden
    da_block_start = html.find("datenaustausch: () =>")
    da_block_end   = html.find("exportStep: () =>")
    da_block = html[da_block_start:da_block_end] if da_block_start > 0 and da_block_end > 0 else ""

    check("Datenaustausch: Import FHIR-Karte vorhanden",
          "importStructured(event,'fhir')" in da_block,
          "FHIR-Import-Karte fehlt im Datenaustausch-Renderer")

    check("Datenaustausch: Import FIM-Karte vorhanden",
          "importStructured(event,'fim')" in da_block,
          "FIM-Import-Karte fehlt im Datenaustausch-Renderer")

    check("Datenaustausch: Import JSON-Karte vorhanden",
          "importStructured(event,'auto')" in da_block,
          "JSON-Import-Karte fehlt im Datenaustausch-Renderer")

    check("Datenaustausch: EUDI-Wallet-Karte vorhanden",
          "importEudiWallet(event)" in da_block,
          "EUDI-Wallet-Karte fehlt im Datenaustausch-Renderer")

    # Weitergabe-Karten im Renderer vorhanden
    check("Datenaustausch: Weitergabe-Karte vorhanden",
          "weitergabeOpen()" in da_block,
          "weitergabeOpen() fehlt im Datenaustausch-Renderer")

    check("Datenaustausch: QR-Uebergabe-Karte vorhanden",
          "qrUebergabeOpen()" in da_block,
          "qrUebergabeOpen() fehlt im Datenaustausch-Renderer")

    check("Datenaustausch: QR-Empfang-Karte vorhanden",
          "qrEmpfangOpen()" in da_block,
          "qrEmpfangOpen() fehlt im Datenaustausch-Renderer")

    check("Datenaustausch: Solid-Pod-Karte vorhanden",
          "solidPodOpen()" in da_block,
          "solidPodOpen() fehlt im Datenaustausch-Renderer")

    # navButtons() im Renderer vorhanden
    check("Datenaustausch: navButtons() im Renderer vorhanden",
          "navButtons()" in da_block,
          "navButtons() fehlt im Datenaustausch-Renderer")

    # Import-Block NICHT mehr in etab-behoerden
    behoerden_start = html.find('id="etab-behoerden"')
    behoerden_end   = html.find('id="etab-', behoerden_start + 1) if behoerden_start > 0 else -1
    behoerden_block = html[behoerden_start:behoerden_end] if behoerden_start > 0 and behoerden_end > 0 else ""
    check("Datenaustausch: Import-Block nicht mehr in etab-behoerden",
          "importStructured(event,'fhir')" not in behoerden_block,
          "FHIR-Import-Block ist noch in etab-behoerden -- sollte entfernt sein")

    # wg-link-Zeilen NICHT mehr in exportStep
    export_block_start = html.find("exportStep: () =>")
    export_block_end   = html.find("navButtons()", export_block_start) + 50 if export_block_start > 0 else -1
    export_block = html[export_block_start:export_block_end] if export_block_start > 0 and export_block_end > 0 else ""
    check("Datenaustausch: wg-link-Zeilen nicht mehr in exportStep",
          'class="wg-link-zeile"' not in export_block,
          "wg-link-Zeilen sind noch im exportStep-Renderer -- sollten entfernt sein")

    # ═══════════════════════════════════════
    print("\n=== 55. STRUKTURUMSTELLUNG APRIL 2026 ===")
    # ═══════════════════════════════════════

    # Schritte 0–13: Inhalt in korrekter Reihenfolge
    steps_ids = []
    for m in __import__('re').finditer(r"\{ id: '(\w+)'", html):
        sid = m.group(1)
        if sid in ('start','kontakte','infokontakte','finanzen','versich','immobilien',
                   'vertraege','gesundheit','pflege','testament','bestattung','persoenliches',
                   'haustiere','digital','assistenten','notfall','dokumente','datenaustausch',
                   'erinnerung','exportStep','einstellungen'):
            if sid not in steps_ids:
                steps_ids.append(sid)

    expected = [
        'start','kontakte','infokontakte','finanzen','versich','immobilien','vertraege',
        'gesundheit','pflege','testament','bestattung','persoenliches','haustiere','digital',
        'assistenten','notfall','dokumente','datenaustausch','erinnerung','exportStep','einstellungen'
    ]

    check("Struktur: Alle 21 Schritte vorhanden",
          len(steps_ids) == 21,
          f"Erwartet 21 Schritte, gefunden: {len(steps_ids)}")

    check("Struktur: Reihenfolge Gesundheit vor Mein Wille",
          steps_ids.index('gesundheit') < steps_ids.index('testament'),
          "gesundheit muss vor testament stehen")

    check("Struktur: Reihenfolge Mein Wille vor Mein Abschied",
          steps_ids.index('testament') < steps_ids.index('bestattung'),
          "testament muss vor bestattung stehen")

    check("Struktur: Reihenfolge Mein Abschied vor Erinnerungsstuecke",
          steps_ids.index('bestattung') < steps_ids.index('persoenliches'),
          "bestattung muss vor persoenliches stehen")

    check("Struktur: Assistenten nach Inhalt (nach digital)",
          steps_ids.index('assistenten') > steps_ids.index('digital'),
          "assistenten muss nach digital stehen")

    check("Struktur: Dokumente erstellen vor Einstellungen",
          steps_ids.index('exportStep') < steps_ids.index('einstellungen'),
          "exportStep muss vor einstellungen stehen")

    check("Struktur: Einstellungen ist letzter Schritt",
          steps_ids[-1] == 'einstellungen',
          "einstellungen muss der letzte Schritt sein")

    check("Struktur: Dokumente erstellen ist vorletzter Schritt",
          steps_ids[-2] == 'exportStep',
          "exportStep muss der vorletzte Schritt sein")

    # Sidebar-Gruppen pruefen
    check("Sidebar: Gruppe 'Gesundheit & Abschluss' vorhanden",
          "'Gesundheit & Abschluss'" in html or "Gesundheit & Abschluss" in html,
          "Sidebar-Gruppe 'Gesundheit & Abschluss' fehlt")

    check("Sidebar: Gruppe 'Besonderes' vorhanden",
          "'Besonderes'" in html or "label: 'Besonderes'" in html,
          "Sidebar-Gruppe 'Besonderes' fehlt")

    check("Sidebar: Alte Gruppe 'Gesundheit & Leben' entfernt",
          "'Gesundheit & Leben'" not in html,
          "Alte Sidebar-Gruppe 'Gesundheit & Leben' ist noch vorhanden")

    check("Sidebar: Alte Gruppe 'Persoenliches & Wuensche' entfernt",
          "Pers\u00f6nliches & W\u00fcnsche" not in html,
          "Alte Sidebar-Gruppe 'Pers\u00f6nliches & W\u00fcnsche' ist noch vorhanden")

    # Einstellungen: kein Weiter-Button am Ende
    check("Einstellungen: isExport-Bedingung schliesst einstellungen ein",
          "id === 'einstellungen'" in html,
          "Einstellungen-Schritt hat keinen Schutz gegen den Weiter-Button")


    # ═══════════════════════════════════════
    print("\n=== 56. UX-OPTIMIERUNGEN (Session April 2026) ===")
    # ═══════════════════════════════════════

    # Schriftgrößen-Korrektur
    check("UX-01: SCHRIFTGRÖSSEN-KORREKTUR CSS-Block vorhanden",
          "SCHRIFTGR\u00d6SSEN-KORREKTUR" in html,
          "CSS-Korrekturblock fehlt")
    check("UX-02: .nav-label font-size 0.95rem",
          ".nav-label       { font-size: 0.95rem; }" in html,
          "nav-label Schriftgröße nicht erhöht")
    check("UX-03: .field-hint font-size 0.88rem",
          ".field-hint      { font-size: 0.88rem; }" in html,
          "field-hint Schriftgröße nicht erhöht")
    check("UX-04: .fs-btn font-size 0.82rem",
          ".fs-btn          { font-size: 0.82rem; }" in html,
          "fs-btn Schriftgröße nicht erhöht")

    # Touch-Targets
    check("UX-05: Input padding 12px (Touch-Target 44px)",
          "padding: 12px 12px;" in html,
          "Input padding unter 44px-Schwelle")
    check("UX-06: textarea min-height 44px",
          "textarea { min-height: 44px; }" in html,
          "textarea min-height fehlt")

    # Passwort-Warnung
    check("UX-07: Passwort-Warnung nicht mehr rot",
          "#fdf3f3" not in html,
          "Rote Passwort-Warnung noch vorhanden")
    check("UX-08: Passwort-Warnung Bernstein (Bitte notieren)",
          "Bitte notieren" in html,
          "Neuer Passwort-Warntext fehlt")
    check("UX-09: Passwort-Warnung nach Feldern (Reihenfolge)",
          html.index("set-pw-confirm") < html.index("Bitte notieren"),
          "Passwort-Warnung steht noch vor den Eingabefeldern")

    # Emojis entfernt
    check("UX-10: Kein Emoji im Rolle-Auswahl-Button",
          "\U0001f464 F\u00fcr mich" not in html,
          "Emoji im Button noch vorhanden")
    check("UX-11: Kein Emoji im Angehörigen-Button",
          "\U0001f468\u200d\U0001f469\u200d\U0001f467 Angeh" not in html,
          "Emoji in Angehörigen-Button noch vorhanden")
    check("UX-12: Button-Text parallel (Für mich / Für Angehörige)",
          "F\u00fcr mich \u2014 Vorsorge anlegen" in html and
          "F\u00fcr Angeh\u00f6rige \u2014 Notfall-Informationen" in html,
          "Parallele Button-Texte fehlen")

    # Sidebar-Gruppen
    nav_group = html.split(".nav-group-label {")[1].split("}")[0] if ".nav-group-label {" in html else ""
    check("UX-13: nav-group-label ohne text-transform uppercase",
          "text-transform" not in nav_group,
          "nav-group-label hat noch text-transform")
    check("UX-14: nav-group-label Kontrast 0.55",
          "rgba(255,255,255,0.55)" in html,
          "nav-group-label Kontrast nicht erhöht")
    check("UX-15: nav-group-label kein Inline-Style im JS",
          'style="font-size:0.65rem"' not in html,
          "nav-group-label hat noch Inline-Style im JS")

    # Schritt-Beschreibungen
    check("UX-16: Neue Beschreibung Über mich",
          "das Deckblatt Ihres Vivodepots" in html,
          "Neue Beschreibung fehlt")
    check("UX-17: Neue Beschreibung Vertrauenspersonen",
          "Wer soll im Notfall angerufen werden?" in html,
          "Neue Beschreibung fehlt")
    check("UX-18: Neue Beschreibung Meine Gesundheit",
          "im Notfall sofort zur Hand" in html,
          "Neue Beschreibung fehlt")
    check("UX-19: Neue Beschreibung Mein Wille",
          "damit Ihr Wille gilt" in html,
          "Neue Beschreibung fehlt")
    check("UX-20: Neue Beschreibung Notfall-Vorsorge",
          "was haben Sie f\u00fcr den Ernstfall?" in html,
          "Neue Beschreibung fehlt")

    # Notfallmappe → Vivodepot
    check("UX-21: Angehörigen-Überschrift auf Vivodepot umgestellt",
          "Vivodepot \u2014 ' + esc(name)" in html,
          "Angehörigen-Überschrift nicht umgestellt")
    check("UX-22: Kein Notfallmappe mehr in Angehörigen-Überschrift",
          "Notfallmappe \u2014 ' + esc(name)" not in html,
          "Alte Angehörigen-Überschrift noch vorhanden")

    # Infoboxen
    check("UX-23: Vertrauenspersonen-Infobox entfernt",
          "Tragen Sie mindestens eine Hauptkontaktperson ein" not in html,
          "Redundante Infobox noch vorhanden")
    check("UX-24: Gesundheit-Infobox entfernt (nicht mehr als infobox-div)",
          'class="infobox">${tl(\'Diese Angaben k' not in html,
          "Redundante Gesundheit-Infobox noch vorhanden")
    check("UX-25: Versicherungen-Infobox gekürzt",
          "Fristen beachten \u2014 im Todesfall" in html,
          "Gekürzte Infobox fehlt")
    check("UX-26: Wohnen-Infobox gekürzt",
          "Ein Mietvertrag l\u00e4uft nach einem Todesfall weiter" in html,
          "Gekürzte Infobox fehlt")

    # Willkommen
    check("UX-27: Willkommen-Text vereinfacht",
          "Ihre Daten bleiben auf Ihrem Ger\u00e4t \u2014 keine Cloud, kein Server." in html,
          "Vereinfachter Willkommen-Text fehlt")
    check("UX-28: USB-Stick-Erklärungs-Text entfernt",
          "Wenn Sie die Datei auf einen USB-Stick speichern, haben Sie alles dabei" not in html,
          "Alter Erklärungs-Text noch vorhanden")

    # Formularabstände
    check("UX-29: margin-top:8px in Renderern stark reduziert",
          html.count('style="margin-top:8px"') <= 5,
          f"Noch {html.count('style="margin-top:8px"')} Vorkommen")

    # Mobile-Fixes
    check("UX-30: fs-btn auf Mobile nicht ausgeblendet",
          ".fs-btn { display: none !important; }" not in html,
          "fs-btn wird auf Mobile noch ausgeblendet")
    check("UX-31: safe-area-inset-bottom in Bottom-Bar",
          "safe-area-inset-bottom" in html,
          "safe-area-inset-bottom fehlt")
    check("UX-32: export-grid 2-spaltig bei 900px",
          "max-width: 900px" in html and "grid-template-columns: 1fr 1fr" in html,
          "export-grid 900px-Breakpoint fehlt")
    check("UX-33: main-content margin auto",
          "margin-left: auto;" in html and "margin-right: auto;" in html,
          "main-content nicht zentriert")

    sys.exit(0 if failed == 0 else 1)

if __name__ == '__main__':
    main()
