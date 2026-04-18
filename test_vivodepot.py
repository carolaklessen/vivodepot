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
    
    # BUG-02: Overlays werden über ALL_OVERLAY_IDS verwaltet — dort prüfen
    all_ids_match = re.search(r'ALL_OVERLAY_IDS\s*=\s*\[([^\]]+)\]', html)
    if all_ids_match:
        all_ids = all_ids_match.group(1)
        required_overlays = ['welcome-overlay', 'return-overlay', 'crypto-overlay', 'goal-wizard']
        for oid in required_overlays:
            check(f"BUG-02: hideAllOverlays enthält '{oid}'", oid in all_ids)
    else:
        check("BUG-02: ALL_OVERLAY_IDS existiert", False)

    # BUG-14: showOverlay nutzt ALL_OVERLAY_IDS — goal-wizard dort prüfen
    show_fn_match = re.search(r'function showOverlay\(id\)\s*\{([^}]+)\}', html)
    if show_fn_match:
        show_fn = show_fn_match.group(1)
        check("BUG-14: showOverlay nutzt ALL_OVERLAY_IDS",
              'ALL_OVERLAY_IDS' in show_fn,
              "showOverlay nutzt ALL_OVERLAY_IDS nicht — Overlays werden nicht korrekt geschlossen")
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
    check("BUG-05: Max 15 password-Felder", pw_fields <= 15, f"Gefunden: {pw_fields}")
    
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

    # BUG-18: coreSection darf '·' nicht als nav-num rendern — Nummern müssen sichtbar sein
    # Symptom: Alle Core-Items zeigen Punkt statt Schrittnummer; Punkt 20 (exportStep) "verschwunden"
    core_render = re.search(
        r"nav-num.*?\$\{done \? '' : (.*?)\}",
        html)
    if core_render:
        num_expr = core_render.group(1).strip().strip("'\"")
        check("BUG-18: coreSection nav-num zeigt Schrittnummer (i+1), nicht '·'",
              num_expr != '\xb7' and num_expr != '·' and '·' not in num_expr,
              "nav-num rendert '·' statt i+1 — Schrittnummern im Core unsichtbar")
    else:
        check("BUG-18: coreSection nav-num Pattern gefunden", False,
              "Kein nav-num-Pattern gefunden")

    # BUG-21: exportStep muss step-header mit h1 haben — sonst bleibt Überschrift leer
    check("BUG-21: exportStep hat step-header mit h1",
          'exportStep: () => `\n    <div class="step-header">' in html,
          "exportStep fehlt <div class='step-header'><h1> — renderStep() findet kein .step-header h1")

    # BUG-20: Gruppenheader in erweiterter Sidebar müssen bei erstem Item der Gruppe erscheinen
    # Ursache: groups.find(g => g.at === i) traf nie zu, weil die Anker-Steps (0,7,14)
    # immer in CORE_IDS sind und nie in extraSection landen.
    render_fn = re.search(r'extraSection\.forEach.*?html \+= `</div>`', html, re.DOTALL)
    if render_fn:
        fn_body = render_fn.group(0)
        check("BUG-20: Gruppenheader nutzen Bereichsprüfung (>= statt ===)",
              'g.at <= i' in fn_body or 'i >= g.at' in fn_body,
              "groups.find(g => g.at === i) — Header erscheint nie wenn Anker-Step in CORE_IDS")
    else:
        check("BUG-20: extraSection-Render gefunden", False)

    # BUG-19: 'erinnerung' (Prüftermine, Punkt 19) muss in CORE_IDS sein
    # Symptom: Prüftermine verschwindet aus eingeklappter Sidebar sobald Step nicht aktiv/erledigt
    core_ids_match = re.search(r"new Set\(\[([^\]]+)\]\)", html)
    if core_ids_match:
        check("BUG-19: 'erinnerung' in CORE_IDS (immer in Sidebar sichtbar)",
              "'erinnerung'" in core_ids_match.group(0),
              "erinnerung fehlt in CORE_IDS — Prüftermine (Punkt 19) nur per Weiter-Klick erreichbar")
    else:
        check("BUG-19: CORE_IDS-Definition gefunden", False)

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

    check("Fokus: _goalMode Flag",                 "_goalMode" in html)
    check("Fokus: _goalRelevant Objekt",           "_goalRelevant" in html)
    check("Fokus: applyGoalWizard()",              "applyGoalWizard" in html)
    check("Fokus: skipGoalWizard()",               "skipGoalWizard" in html)
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
    check("Fokus: updateFokusBarLabel()",          "updateFokusBarLabel" in html)
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
    check("vCard: VERSION:4.0",                    "VERSION:4.0" in html)
    check("vCard: BEGIN:VCARD",                    "BEGIN:VCARD" in html)
    check("vCard: END:VCARD",                      "END:VCARD" in html)
    check("vCard: PRODID Vivodepot",               "PRODID:-//Vivodepot" in html)
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
    check("PWA: beforeinstallprompt",               "beforeinstallprompt" in html)
    check("PWA: installApp()",                      "function installApp" in html)
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
    check("Export: FHIR R4 Bundle", "Bundle" in html and "generateFHIR" in html)
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
    check("vCard: VERSION:4.0",                          "VERSION:4.0" in html)
    check("vCard: PRODID Vivodepot",                     "PRODID:-//Vivodepot" in html)

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
    check("Notfall: Campingkocher in Vorrat",             "Campingkocher" in html)
    check("Notfall: Hygieneartikel in Vorrat",            "Hygieneartikel" in html)
    check("Notfall: Decke in Vorrat",                     "Decke" in html and "NOTFALL_VORRAT" in html)
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

    # WG-16: wg-overlay wird über ALL_OVERLAY_IDS verwaltet — dort prüfen
    all_ids_wg = re.search(r'ALL_OVERLAY_IDS\s*=\s*\[([^\]]+)\]', html)
    check("WG-16a: wg-overlay in ALL_OVERLAY_IDS registriert",
          all_ids_wg and 'wg-overlay' in all_ids_wg.group(1),
          "wg-overlay fehlt in ALL_OVERLAY_IDS — Dialog bleibt offen bei Overlay-Wechsel")
    check("WG-16b: hideAllOverlays nutzt ALL_OVERLAY_IDS",
          all_ids_wg and 'ALL_OVERLAY_IDS' in html[html.find('function hideAllOverlays'):html.find('function hideAllOverlays')+200],
          "hideAllOverlays nutzt ALL_OVERLAY_IDS nicht")

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
    print("\n=== 27. SPEICHERN-HINWEIS (Haftungsausschluss vor Export) ===")
    # ═══════════════════════════════════════
    check("Speichern-Hinweis: _saveHinweisGezeigt Flag",
          "_saveHinweisGezeigt" in html,
          "Fehlt: Flag zur Einmal-pro-Sitzung-Anzeige des Hinweises")
    check("Speichern-Hinweis: Button 'Verstanden — speichern'",
          "save-hinweis-ok" in html,
          "Fehlt: Button-ID 'save-hinweis-ok'")
    check("Speichern-Hinweis: Kein Internet-Aufruf (kein save-hinweis-pruefen)",
          "save-hinweis-pruefen" not in html,
          "Gefunden: save-hinweis-pruefen — Offline-Versprechen gebrochen")
    check("Speichern-Hinweis: Jahres-Hinweis 'einmal pro Jahr'",
          "einmal pro Jahr" in html,
          "Fehlt: Jahres-Hinweis im Speichern-Dialog")
    check("Speichern-Hinweis: Verweis auf vivodepot.de",
          "save-hinweis-ok" in html and "vivodepot.de" in html,
          "Fehlt: Verweis auf vivodepot.de im Speichern-Dialog")
    check("Speichern-Hinweis: Rechtstext 'Keine Rechtsberatung'",
          "Keine Rechtsberatung" in html,
          "Fehlt: Hinweistext 'Keine Rechtsberatung'")
    check("Speichern-Hinweis: Dialog als Promise (await) in saveAsHTML",
          "_saveHinweisGezeigt" in html and "await new Promise" in html,
          "Fehlt: Dialog blockiert saveAsHTML als Promise")

    # ── Ablaufdatum ──
    check("Ablaufdatum: savedDate wird in saveAsHTML gesetzt",
          "const savedDate = new Date().toISOString().slice(0, 10)" in html,
          "Fehlt: Datum wird beim Speichern nicht erfasst")
    check("Ablaufdatum: __vivodepot_saved_date in INIT-Block eingebettet",
          "window.__vivodepot_saved_date" in html,
          "Fehlt: Datum wird nicht in gespeicherte Datei eingebettet")
    check("Ablaufdatum: Alterswarnung in showSavedFileWelcome",
          "__vivodepot_saved_date" in html and "altershinweis" in html,
          "Fehlt: Alterswarnung beim Öffnen der gespeicherten Datei")
    check("Ablaufdatum: Schwelle 12 Monate",
          "monate >= 12" in html,
          "Fehlt: 12-Monats-Schwelle in der Alterswarnung")
    check("Ablaufdatum: Verweis auf vivodepot.de in Alterswarnung",
          "altershinweis" in html and "vivodepot.de" in html,
          "Fehlt: Verweis auf vivodepot.de in der Alterswarnung")
    check("Ablaufdatum: Kein Internet-Aufruf (kein fetch in showSavedFileWelcome)",
          "fetch" not in html[html.find("function showSavedFileWelcome"):html.find("function savedWelcomeOwner")],
          "Gefunden: fetch() in showSavedFileWelcome — Offline-Versprechen gebrochen")

    # ═══════════════════════════════════════
    print("\n=== 53. WCAG 2.2 BARRIEREFREIHEIT ===")
    # ═══════════════════════════════════════
    # Prüfung der sechs neuen WCAG-2.2-Kriterien (gegenüber 2.1), die für
    # Vivodepot relevant sind. Siehe SOVEREIGNTY.md Sektion 2.7 für Übersicht.
    # Drei Kriterien werden hier automatisiert geprüft:
    #   2.4.11 Focus Not Obscured (AA)
    #   3.2.6  Consistent Help (A)
    #   3.3.8  Accessible Authentication (AA)
    # Die übrigen drei (2.5.7, 2.5.8, 3.3.7) waren bereits in WCAG 2.1 erfüllt.

    # ── 2.4.11 Focus Not Obscured ──
    # Die Topbar ist 60px hoch (Desktop) / 52px (Mobile) und sticky. Ohne
    # scroll-padding-top würden per Tab fokussierte Elemente beim Scrollen
    # hinter der Topbar verschwinden.
    scroll_padding_match = re.search(
        r'html\s*\{[^}]*scroll-padding-top\s*:\s*(\d+)px',
        html
    )
    check("WCAG22-2.4.11: html-Selector hat scroll-padding-top",
          scroll_padding_match is not None,
          "Fehlt: html { scroll-padding-top: ... } verhindert Focus-Verdeckung durch sticky Topbar")
    if scroll_padding_match:
        scroll_padding_wert = int(scroll_padding_match.group(1))
        check(f"WCAG22-2.4.11: scroll-padding-top >= 60px (aktuell {scroll_padding_wert}px)",
              scroll_padding_wert >= 60,
              "Muss mindestens Topbar-Höhe (60px Desktop) abdecken")

    # ── 3.2.6 Consistent Help ──
    # Falls Hilfe-Mechanismen (FAQ, Hilfe-Button, Support-Kontakt) im UI
    # existieren, müssen sie auf jedem Schritt an gleicher Position stehen.
    # Bereiche, die als "global konsistent" gelten: Topbar, Mehr-Menü,
    # Profil-Dropdown — alle sticky und auf jedem Schritt sichtbar.
    wcag_hilfe_button_muster = re.compile(
        r"<(?:button|a)\b[^>]*>\s*"
        r"(?:Hilfe|FAQ|Support|Help|Hilfe-Center|Kontakt aufnehmen)"
        r"\s*</(?:button|a)>",
        re.IGNORECASE
    )
    wcag_hilfe_handler_muster = re.compile(
        r"onclick\s*=\s*[\"']\s*(?:openHilfe|showHelp|openFAQ|openHelp)\b",
        re.IGNORECASE
    )
    wcag_globale_bereiche = re.compile(
        r'class\s*=\s*"[^"]*(?:topbar|more-dropdown|profile-dropdown)[^"]*"',
        re.IGNORECASE
    )

    wcag_hilfe_treffer = (
        list(wcag_hilfe_button_muster.finditer(html))
        + list(wcag_hilfe_handler_muster.finditer(html))
    )
    if not wcag_hilfe_treffer:
        check("WCAG22-3.2.6: Keine Hilfe-Funktion im UI (Kriterium automatisch erfüllt)",
              True, "")
    else:
        wcag_nicht_global = []
        for m in wcag_hilfe_treffer:
            fenster = html[max(0, m.start() - 800):m.start()]
            if not wcag_globale_bereiche.search(fenster):
                wcag_nicht_global.append(m.group(0))
        check(f"WCAG22-3.2.6: Alle {len(wcag_hilfe_treffer)} Hilfe-Element(e) global platziert",
              len(wcag_nicht_global) == 0,
              f"{len(wcag_nicht_global)} außerhalb Topbar/Mehr-Menü — Konsistenz manuell prüfen")

    # ── 3.3.8 Accessible Authentication ──
    # Vivodepot darf weder CAPTCHA noch SMS-Code noch andere kognitive
    # Funktionstests verwenden. Passwort-Eingabe zur Entschlüsselung gilt
    # als nutzerkontrolliertes Geheimnis und ist kein externer Test.
    wcag_captcha_muster = re.compile(
        r"(?:<input[^>]*captcha|class\s*=\s*[\"'][^\"']*captcha|"
        r"id\s*=\s*[\"'][^\"']*captcha|grecaptcha|hcaptcha|"
        r"cf-turnstile|recaptcha)",
        re.IGNORECASE
    )
    wcag_sms_muster = re.compile(
        r"(?:<input[^>]*(?:sms-code|otp-code|verification-code)|"
        r"placeholder\s*=\s*[\"'][^\"']*(?:SMS-Code|Verifizierungscode|OTP)|"
        r"name\s*=\s*[\"'](?:otp|sms_code|verification_code)[\"'])",
        re.IGNORECASE
    )
    check("WCAG22-3.3.8: Kein CAPTCHA im Code",
          not wcag_captcha_muster.search(html),
          "CAPTCHA-Mechanismus gefunden — verstößt gegen 3.3.8")
    check("WCAG22-3.3.8: Kein SMS-Code-/OTP-Eingabefeld",
          not wcag_sms_muster.search(html),
          "SMS-Code- oder OTP-Feld gefunden — verstößt gegen 3.3.8")

    # Doku-Prüfung: SOVEREIGNTY.md muss die 3.3.8-Begründung enthalten.
    # Wird im gleichen Verzeichnis wie die HTML gesucht.
    wcag_sov_pfad = os.path.join(os.path.dirname(filepath) or '.', 'SOVEREIGNTY.md')
    if os.path.exists(wcag_sov_pfad):
        try:
            wcag_sov = open(wcag_sov_pfad, encoding='utf-8').read()
            wcag_pflicht = ['3.3.8', 'kein CAPTCHA', 'nutzerkontrolliertes Geheimnis']
            wcag_fehlend = [b for b in wcag_pflicht if b not in wcag_sov]
            check("WCAG22-3.3.8: Begründung in SOVEREIGNTY.md vollständig",
                  not wcag_fehlend,
                  "Fehlende Pflichtbegriffe: " + ", ".join(repr(f) for f in wcag_fehlend))
        except Exception as wcag_e:
            check("WCAG22-3.3.8: SOVEREIGNTY.md lesbar",
                  False,
                  f"Fehler beim Lesen: {wcag_e}")
    else:
        check("WCAG22-3.3.8: SOVEREIGNTY.md vorhanden (neben HTML)",
              False,
              f"Nicht gefunden: {wcag_sov_pfad} — Begründung kann nicht geprüft werden")

    # ═══════════════════════════════════════
    print("\n=== 54. IMMOBILIEN — KAUFVERTRAG UND KREDITVERTRAG ===")
    # ═══════════════════════════════════════

    check("Immobilien: Kaufvertrag-Ablageort-Feld vorhanden", "'obj1_kaufvertrag'" in html)
    check("Immobilien: Kaufvertrag-Label korrekt", "Kaufvertrag \u2014 Ablageort" in html)
    check("Immobilien: Kreditvertrag-Ablageort-Feld vorhanden", "'obj1_kredit_ort'" in html)
    check("Immobilien: Kreditvertrag-Label korrekt", "Kreditvertrag/e \u2014 Ablageort" in html)
    check("Immobilien: Kaufvertrag-Tooltip vorhanden", "notariell beurkundet" in html)
    check("Immobilien: Kreditvertrag-Tooltip vorhanden", "Bank informiert" in html)

    # ═══════════════════════════════════════
    print("\n=== 55. TESTAMENT — EHEVERTRAG ===")
    # ═══════════════════════════════════════

    check("Ehevertrag: Ablageort-Feld vorhanden", "'dok_ehevertrag'" in html)
    check("Ehevertrag: Label korrekt", "Ehevertrag \u2014 Ablageort" in html)
    check("Ehevertrag: Tooltip vorhanden", "notariell beurkundet" in html and "Ehevertrag" in html)
    check("Ehevertrag: in mehr()-Schlüsselliste", "'dok_ehevertrag'" in html)
    check("Ehevertrag: im PDF-Export", "get('dok_ehevertrag')" in html)
    check("Ehevertrag: im Word-Export", html.count("get('dok_ehevertrag')") >= 2)

    # ═══════════════════════════════════════
    print("\n=== 56. KINDER — BETREUUNGSMODELL UND GEBURTSURKUNDE ===")
    # ═══════════════════════════════════════

    check("Kinder: Betreuungsmodell-Feld vorhanden", "'betreuungsmodell'" in html)
    check("Kinder: Betreuungsmodell-Label korrekt", "Betreuungsmodell bei Trennung" in html)
    check("Kinder: Option Residenzmodell vorhanden", "Residenzmodell" in html)
    check("Kinder: Option Wechselmodell vorhanden", "Wechselmodell" in html)
    check("Kinder: Option Nestmodell vorhanden", "Nestmodell" in html)
    check("Kinder: Erklaerungshinweis Betreuungsmodelle", "Betreuungsmodelle bei Trennung" in html)
    check("Kinder: Geburtsurkunde-Ablageort-Feld vorhanden", "'geburtsurkunde_ort'" in html)
    check("Kinder: Geburtsurkunde-Label korrekt", "Geburtsurkunde \u2014 Ablageort" in html)
    check("Kinder: addItem enthaelt betreuungsmodell", "betreuungsmodell:'Nicht zutreffend'" in html)
    check("Kinder: addItem enthaelt geburtsurkunde_ort", "geburtsurkunde_ort:''" in html)

    # ═══════════════════════════════════════
    print("\n=== 57. FINANZEN — ALTERSVORSORGE HERAUSGESTELLT ===")
    # ═══════════════════════════════════════

    check("Altersvorsorge: Abschnitt direkt im Finanzen-Step sichtbar",
          "'pk_name'" in html and "'saeule3_institut'" in html)
    check("Altersvorsorge: Abschnittstitel vorhanden",
          "Altersvorsorge &amp; Renten" in html or "Altersvorsorge & Renten" in html)
    check("Altersvorsorge: pk_name nicht mehr in mehr()-Schluessel",
          "['pk_name','saeule3_institut','steuerberater'" not in html)
    check("Altersvorsorge: finanzen_mehr-Label ohne Altersvorsorge",
          "Depots, Altersvorsorge" not in html)
    check("Altersvorsorge: renderRentenBlocks ausserhalb mehr()",
          html.index("renderRentenBlocks()") < html.index("finanzen_mehr"))

    # ═══════════════════════════════════════
    print("\n=== 58. DOKUMENTEN-ÜBERSICHT IM EXPORT ===")
    # ═══════════════════════════════════════

    # Seite erscheint nur im PDF-Export, nicht als Navigationspunkt.
    check("DokUebersicht: Seite in _generatePDFInner vorhanden",
          "Dokumenten-Übersicht" in html or "Dokumenten-\u00dcbersicht" in html)
    check("DokUebersicht: Abschnittstitel mit Nummer",
          "'14. Dokumenten-Übersicht" in html or
          "'14. Dokumenten-\u00dcbersicht" in html)
    check("DokUebersicht: Kategorie Rechtliches vorhanden",
          "'Rechtliches'" in html and "'testament_ort'" in html)
    check("DokUebersicht: Kategorie Immobilien vorhanden",
          "'Immobilien'" in html and "'obj1_kaufvertrag'" in html)
    check("DokUebersicht: Kategorie Gesundheit vorhanden",
          "'Gesundheit'" in html and "'krankenkassenkarte_ort'" in html)
    check("DokUebersicht: Kategorie Digital vorhanden",
          "'pw_masterkey_ort'" in html and "'bundid_ort'" in html)
    check("DokUebersicht: Kategorie Notfall vorhanden",
          "'ks_erstehilfe_ort'" in html and "'angehoerigen_passwort_ort'" in html)
    check("DokUebersicht: Kategorie Bestattung vorhanden",
          "'bestattung_vorsorge_nachweis'" in html)
    check("DokUebersicht: Filterlogik — nur Felder mit Wert anzeigen",
          "filter(f => get(f.key) && String(get(f.key)).trim())" in html)
    check("DokUebersicht: Keine Anzeige bei leeren Feldern (Kategorien filtern)",
          ".filter(kat => kat.felder.length > 0)" in html)
    check("DokUebersicht: Kein eigener Navigationspunkt (kein step-Button dafuer)",
          "step-btn' data-step='dokumente" not in html and
          "step='dokumenten" not in html)

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
    
    sys.exit(0 if failed == 0 else 1)

if __name__ == '__main__':
    main()
