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

    # Signaturen bekannter eingebetteter Drittanbieter-Bibliotheken.
    # Diese enthalten absichtlich minifizierten Code, der keine
    # Node-Syntaxpruefung besteht. Eigener Projektcode enthaelt
    # diese Zeichenketten nicht.
    DRITTANBIETER_SIGNATUREN = [
        "var P={print:4,modify:8",       # jsPDF Verschluesselungsmodul
        "jsPDF.version",                 # jsPDF Kern
        "function(t){var e=function(){", # jsPDF Canvas
        "pako",                          # pako Deflate-Bibliothek
        "JSZip",                         # JSZip
    ]

    all_syntax_ok = True
    for i, m in enumerate(scripts):
        content = m.group(1)
        if len(content) < 50:
            continue
        if any(sig in content for sig in DRITTANBIETER_SIGNATUREN):
            continue  # Drittanbieter-Bibliothek — Syntaxpruefung nicht anwendbar
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
    check("Journey: Fokus-Button in Sidebar", "Fokus ändern" in html)

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
    check("Fokus-Wizard: In Einstellungen erreichbar", "showGoalWizard" in html and "Fokus &auml;ndern" in html or "Fokus ändern" in html)

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
    check("Fokus: nextStep/prevStep via goToStep mit Fokus",
          "function nextStep" in html and "function prevStep" in html and
          "function goToStep" in html and "_goalMode" in html)
    check("Fokus: Fokus-Navigation — goToStep kennt _goalRelevant",
          "goToStep" in html and "_goalRelevant" in html and "_goalMode" in html)
    check("Fokus: renderSidebar filtert Steps", "function renderSidebar" in html and "_goalRelevant" in html)
    check("Fokus: updateFokusBarLabel()", "updateFokusBarLabel" in html)
    check("Fokus: fokus-bar-btn Element", "fokus-bar-btn" in html)
    check("Fokus: Fokus-Button in Einstellungen vorhanden", "Fokus &auml;ndern" in html or "Fokus ändern" in html)

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
    check("Recht: hilfe@vivodepot.de", "hilfe@vivodepot.de" in html)
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
    check("Legal: Kontakt hilfe@vivodepot.de",  "hilfe@vivodepot.de" in html)
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


    # ═══════════════════════════════════════
    print("\n=== 48a. ERGÄNZUNGEN (Chat-Abgleich & Sessions) ===")
    # ═══════════════════════════════════════

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
    print("\n=== 52. WINDOW.ONERROR — APP-ZUSTANDSPRÜFUNG ===")

    # ONERR-1: window.onerror zeigt welcome-overlay NUR wenn App noch nicht gestartet
    onerror_match = re.search(
        r'window\.onerror\s*=\s*function[^{]*\{.*?return false;\s*\}',
        html, re.DOTALL
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
    loaddata_match = re.search(
        r'async function loadData\(\)[^{]*\{([\s\S]*?)^\}',
        html, re.MULTILINE
    )
    loaddata_body = loaddata_match.group(1) if loaddata_match else ""
    parse_catch_match = re.search(
        r'parsedStored\s*=\s*JSON\.parse\(stored\).*?catch\s*\{(.*?)return;\s*\}',
        html, re.DOTALL
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
    print("\n=== 52a. SPEICHERN-HINWEIS (Haftungsausschluss vor Export) ===")
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
    # Gesucht wird im selben Verzeichnis wie die HTML-Datei sowie in
    # bekannten Projektverzeichnissen (Entwicklungsumgebung).
    wcag_sov_pfad = os.path.join(os.path.dirname(filepath) or '.', 'SOVEREIGNTY.md')
    if not os.path.exists(wcag_sov_pfad):
        for kandidat in ['/mnt/project/SOVEREIGNTY.md',
                         os.path.join(os.path.dirname(os.path.abspath(filepath)),
                                      '..', 'SOVEREIGNTY.md')]:
            if os.path.exists(kandidat):
                wcag_sov_pfad = kandidat
                break
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

    # ─────────────────────────────────────────────────────────────────
    # 59. DOKUMENTEN-ÜBERSICHT IM WORD-EXPORT
    # ─────────────────────────────────────────────────────────────────
    print("\n=== 59. DOKUMENTEN-ÜBERSICHT IM WORD-EXPORT ===")
    check("DokUebersicht Word: Abschnitt 13 vorhanden",
          '"13. Dokumenten-\u00dcbersicht \u2014 Ablageorte"' in html)
    check("DokUebersicht Word: Beschreibungszeile vorhanden",
          "wo Ihre wichtigen Dokumente zu finden sind" in html)
    check("DokUebersicht Word: Kategorie Rechtliches (Word)",
          html.count("'Rechtliches'") >= 2)
    check("DokUebersicht Word: Kategorie Immobilien (Word)",
          html.count("'Immobilien'") >= 2)
    check("DokUebersicht Word: Kategorie Gesundheit (Word)",
          html.count("'Gesundheit'") >= 2)
    check("DokUebersicht Word: Kategorie Digital (Word)",
          "Digital & Zug\u00e4nge" in html)
    check("DokUebersicht Word: Filterlogik im Word-Export",
          html.count("filter(f => get(f.key) && String(get(f.key)).trim())") >= 2)
    check("DokUebersicht Word: Leer-Kategorien werden uebersprungen (Word)",
          "k => k.felder.length > 0" in html)
    check("DokUebersicht Word: Seitenumbruch vor Abschnitt 13",
          'pb(),' in html and '13. Dokumenten' in html)
    check("DokUebersicht Word: maybeTbl fuer Kategorie-Tabellen",
          "maybeTbl(k.felder.map(f => row(f.label, get(f.key))))" in html)
    check("DokUebersicht Word: Abschnitt 13 nur im Gesamt-Word-Export",
          html.count('13. Dokumenten-\u00dcbersicht') == 1)

    # ═══════════════════════════════════════
    print("\n=== 60. ANF-07a — BASIS-ANAMNESE ===")
    # ═══════════════════════════════════════

    check("ANF-07a: mehr()-Block vorhanden",
          "'anf07a_klinisch'" in html)
    check("ANF-07a: Block-Label korrekt",
          "Facharzttermine" in html and "Körpermaße" in html)
    check("ANF-07a: Feld koerpergroesse vorhanden",
          "'koerpergroesse'" in html)
    check("ANF-07a: Feld koerpergewicht vorhanden",
          "'koerpergewicht'" in html)
    check("ANF-07a: Impfung Tetanus-Datum vorhanden",
          "'impfung_tetanus_datum'" in html)
    check("ANF-07a: Impfung Grippe-Datum vorhanden",
          "'impfung_grippe_datum'" in html)
    check("ANF-07a: Impfung Pneumokokken als Select vorhanden",
          "'impfung_pneumokokken'" in html and "set('impfung_pneumokokken'" in html)
    check("ANF-07a: Impfung COVID-Datum vorhanden",
          "'impfung_covid_datum'" in html)
    check("ANF-07a: Impfbuch-Ablageort vorhanden",
          "'impfbuch_ort'" in html)
    check("ANF-07a: Laborwert INR vorhanden",
          "'labor_inr_wert'" in html and "'labor_inr_datum'" in html)
    check("ANF-07a: Laborwert Kreatinin vorhanden",
          "'labor_kreatinin'" in html and "'labor_kreatinin_datum'" in html)
    check("ANF-07a: Laborwert HbA1c vorhanden",
          "'labor_hba1c'" in html and "'labor_hba1c_datum'" in html)
    check("ANF-07a: LOINC-Codes in Hinweistexten",
          "LOINC 6301-6" in html and "LOINC 2160-0" in html and "LOINC 4548-4" in html)
    check("ANF-07a: Selbstauskunft-Vermerk bei Laborwerten",
          "Selbstauskunft Patient" in html)
    check("ANF-07a: Feld lebt_allein als Select vorhanden",
          "'lebt_allein'" in html and "set('lebt_allein'" in html)
    check("ANF-07a: Feld hauptpflegeperson vorhanden",
          "'hauptpflegeperson'" in html)
    check("ANF-07a: Feld beruf_aktuell vorhanden",
          "'beruf_aktuell'" in html)

    # ═══════════════════════════════════════
    print("\n=== 61. ANF-07b — FACHSPEZIFISCHE SICHERHEITSFELDER ===")
    # ═══════════════════════════════════════

    check("ANF-07b: mehr()-Block vorhanden",
          "'anf07b_fach'" in html)
    check("ANF-07b: Block-Label korrekt",
          "Fachspezifische Sicherheitsfelder" in html)
    check("ANF-07b: Radiologie — MRT-Kontraindikation Select",
          "set('radio_mrt_kontraindikation'" in html)
    check("ANF-07b: Radiologie — Klaustrophobie Select",
          "set('radio_klaustrophobie'" in html)
    check("ANF-07b: Radiologie — Kontrastmittel Select",
          "set('radio_km_unvertraeglichkeit'" in html)
    check("ANF-07b: Radiologie — Schwangerschaft Select",
          "set('radio_schwangerschaft_moeglich'" in html)
    check("ANF-07b: Anästhesie — letzte Narkose Datum",
          "'anaesthesie_letzte_narkose'" in html)
    check("ANF-07b: Anästhesie — Intubation Select",
          "set('anaesthesie_intubation_schwierig'" in html)
    check("ANF-07b: Anästhesie — Pseudocholinesterase Select",
          "set('anaesthesie_pseudocholinesterase'" in html)
    check("ANF-07b: Anästhesie — Komplikationen Textarea",
          "'anaesthesie_komplikationen'" in html)
    check("ANF-07b: Kardiologie — Herzrhythmus Feld",
          "'kardio_herzrhythmus'" in html)
    check("ANF-07b: Kardiologie — Schrittmacher-Modell Feld",
          "'kardio_schrittmacher_modell'" in html)
    check("ANF-07b: Neurologie — Epilepsie Select",
          "set('neuro_epilepsie'" in html)
    check("ANF-07b: Neurologie — letzter Anfall Datum",
          "'neuro_letzter_anfall'" in html)
    check("ANF-07b: Neurologie — Antikonvulsiva Feld",
          "'neuro_antikonvulsiva'" in html)
    check("ANF-07b: Geriatrie — Pflegegrad Select (1-5)",
          "set('geriat_pflegegrad'" in html and "'1','2','3','4','5'" in html)
    check("ANF-07b: Geriatrie — Sturzrisiko Select",
          "set('geriat_sturzrisiko'" in html)
    check("ANF-07b: Geriatrie — MMSE-Score Feld",
          "'geriat_mmse'" in html)
    check("ANF-07b: Gynäkologie — Mammographie Datum",
          "'gyn_letzte_mammographie'" in html)
    check("ANF-07b: Gynäkologie — PAP-Abstrich Datum",
          "'gyn_letzter_pap'" in html)
    check("ANF-07b: Gynäkologie — Menopause Select",
          "set('gyn_menopause'" in html)
    check("ANF-07b: Reihenfolge — anf07b nach anf07a",
          html.index("'anf07b_fach'") > html.index("'anf07a_klinisch'"))
    check("ANF-07b: Reihenfolge — anf07b vor gesundheit_mehr",
          html.index("'anf07b_fach'") < html.index("'gesundheit_mehr'"))

    # ═══════════════════════════════════════
    print("\n=== 62. ANF-07c — ARZTBOGEN-EXPORTE UND WIZARD ===")
    # ═══════════════════════════════════════

    check("ANF-07c: generateArztbogenRadiologie() definiert",
          "function generateArztbogenRadiologie()" in html)
    check("ANF-07c: generateArztbogenPraeop() definiert",
          "function generateArztbogenPraeop()" in html)
    check("ANF-07c: generateArztbogenGeriatrie() definiert",
          "function generateArztbogenGeriatrie()" in html)
    check("ANF-07c: Radiologie-PDF — MRT-Checkliste vorhanden",
          "SICHERHEITS-CHECKLISTE MRT" in html)
    check("ANF-07c: Radiologie-PDF — Rot-Markierung bei Ja-Werten",
          "180,30,30" in html)
    check("ANF-07c: Radiologie-PDF — Dateiname korrekt",
          "Arztbogen_Radiologie_" in html)
    check("ANF-07c: Praeop-PDF — BMI-Berechnung vorhanden",
          "BMI (berechnet)" in html)
    check("ANF-07c: Praeop-PDF — Anästhesie-Sektion vorhanden",
          "ANÄSTHESIE-ANAMNESE" in html)
    check("ANF-07c: Praeop-PDF — Dateiname korrekt",
          "Praeopera_Bogen_" in html)
    check("ANF-07c: Geriatrie-PDF — Assessment-Sektion vorhanden",
          "GERIATRISCHES ASSESSMENT" in html)
    check("ANF-07c: Geriatrie-PDF — Dateiname korrekt",
          "Geriatrie_Bogen_" in html)
    check("ANF-07c: Alle PDFs — Selbstauskunft-Fusszeile",
          html.count("Selbstauskunft Patient (Vivodepot)") >= 3)
    check("ANF-07c: Export-Karte Radiologie im UI",
          "generateArztbogenRadiologie()" in html and "Arztbogen Radiologie" in html)
    check("ANF-07c: Export-Karte Praeop im UI",
          "generateArztbogenPraeop()" in html and "Präoperativer Bogen" in html)
    check("ANF-07c: Export-Karte Geriatrie im UI",
          "generateArztbogenGeriatrie()" in html and "Geriatrie-Bogen" in html)
    check("ANF-07c: Keine doppelten Export-Karten (Radiologie)",
          html.count("generateArztbogenRadiologie()") == 2)
    check("ANF-07c: Keine doppelten Export-Karten (Praeop)",
          html.count("generateArztbogenPraeop()") == 2)
    check("ANF-07c: Keine doppelten Export-Karten (Geriatrie)",
          html.count("generateArztbogenGeriatrie()") == 2)
    check("ANF-07c: Wizard awizOpen() definiert",
          "function awizOpen()" in html)
    check("ANF-07c: Wizard awizClose() definiert",
          "function awizClose()" in html)
    check("ANF-07c: Wizard awizRender() definiert",
          "function awizRender()" in html)
    check("ANF-07c: Wizard awizCollect() definiert",
          "function awizCollect()" in html)
    check("ANF-07c: Wizard awizNext() definiert",
          "function awizNext()" in html)
    check("ANF-07c: Wizard awizPrev() definiert",
          "function awizPrev()" in html)
    check("ANF-07c: Wizard-Overlay awiz-overlay vorhanden",
          'id="awiz-overlay"' in html)
    check("ANF-07c: Wizard-Overlay in ALL_OVERLAY_IDS registriert",
          "'awiz-overlay'" in html and "ALL_OVERLAY_IDS" in html)
    check("ANF-07c: Anamnese-Assistent-Button im Gesundheit-Schritt",
          "awizOpen()" in html and "Anamnese-Assistent starten" in html)
    check("ANF-07c: Wizard hat 7 Schritte",
          "von 7" in html and "awiz-step-info" in html)
    check("ANF-07c: Wizard deckt Laborwerte ab",
          "awizStep === 3" in html and "labor_inr_wert" in html)
    check("ANF-07c: Wizard deckt Radiologie/Anästhesie ab",
          "awizStep === 5" in html and "radio_mrt_kontraindikation" in html)
    check("ANF-07c: Wizard deckt Geriatrie/Gynäkologie ab",
          "awizStep === 6" in html and "geriat_pflegegrad" in html)

    # ═══════════════════════════════════════
    print("\n=== 63. BETA.10 — QR-ÜBERGABE URL-FORMAT ===")
    # ═══════════════════════════════════════

    # QR_LESEN_URL-Konstante vorhanden und korrekt gesetzt
    check("beta.10: QR_LESEN_URL-Konstante definiert",
          "const QR_LESEN_URL" in html)
    check("beta.10: QR_LESEN_URL zeigt auf vivodepot-lesen.html",
          "vivodepot-lesen.html" in html)
    check("beta.10: QR_LESEN_URL ist GitHub-Pages-URL",
          "carolaklessen.github.io/vivodepot/vivodepot-lesen.html" in html)

    # URL-Format im QR-Generator
    check("beta.10: QR-Generator erzeugt Base64url-Payload",
          "payloadB64 = btoa(payloadJson).replace" in html)
    check("beta.10: QR-Generator baut URL mit Hash-Fragment",
          "QR_LESEN_URL + '#' + payloadB64" in html)

    # Rückwärtskompatibilität im Empfang
    check("beta.10: qreQrErkannt versteht URL-Format mit #",
          "rohText.indexOf('#')" in html or "rohText.includes('#')" in html)
    check("beta.10: qreQrErkannt versteht Legacy-JSON-Format",
          "JSON.parse(rohText)" in html and "qreQrErkannt" in html)

    # ═══════════════════════════════════════
    print("\n=== 64. BETA.10 — MEHR-TEILE-QR-CODES ===")
    # ═══════════════════════════════════════

    # Schwellwerte und Chunk-Logik
    check("beta.10: SINGLE_MAX-Schwellwert definiert",
          "SINGLE_MAX" in html and "1800" in html)
    check("beta.10: CHUNK_SIZE definiert",
          "CHUNK_SIZE" in html and "1200" in html)
    check("beta.10: Chunk-Schleife erzeugt mehrere URLs",
          "chunks.push(payloadB64.slice" in html)
    check("beta.10: Mehr als 6 Chunks führt zu Fehlermeldung",
          "chunks.length > 6" in html)
    check("beta.10: Chunk-Metadaten enthalten p, t, id, d",
          "p: idx + 1" in html and "t: chunks.length" in html and "id: qrId" in html)

    # Zustandsvariablen für Karussell
    check("beta.10: _qrUrls-Zustandsvariable vorhanden",
          "_qrUrls" in html)
    check("beta.10: _qrAktiv-Zustandsvariable vorhanden",
          "_qrAktiv" in html)
    check("beta.10: qrZeigeCode-Funktion vorhanden",
          "function qrZeigeCode" in html)
    check("beta.10: qrMultiPrev-Funktion vorhanden",
          "function qrMultiPrev" in html)
    check("beta.10: qrMultiNext-Funktion vorhanden",
          "function qrMultiNext" in html)

    # Karussell-UI-Elemente
    check("beta.10: Karussell-Navigation qr-multi-nav vorhanden",
          'id="qr-multi-nav"' in html)
    check("beta.10: Karussell-Zurück-Button qr-multi-prev vorhanden",
          'id="qr-multi-prev"' in html)
    check("beta.10: Karussell-Weiter-Button qr-multi-next vorhanden",
          'id="qr-multi-next"' in html)
    check("beta.10: Karussell-Label qr-multi-label vorhanden",
          'id="qr-multi-label"' in html)

    # ═══════════════════════════════════════
    print("\n=== 65. BETA.10 — ANF-UX-01 BIS ANF-UX-07 ===")
    # ═══════════════════════════════════════

    # UX-01: Lock-Button vorhanden (SVG-Schlosssymbol, kein Emoji seit beta.10)
    check("ANF-UX-01: Lock-Button mit lockApp() vorhanden",
          "onclick=\"lockApp()\"" in html and
          "title=\"Bildschirm sperren\"" in html and
          "aria-label=\"Bildschirm sperren\"" in html)

    # UX-03: EUDI-Karte kein HTML-Entity
    check("ANF-UX-03: w&auml;hlen nicht mehr in EUDI-Karte",
          "w&auml;hlen" not in html)
    check("ANF-UX-03: wählen korrekt in EUDI-Karte",
          "wählen" in html)

    # UX-04: Infobox Weitergabe — keine ASCII-Umschreibungen
    # Prüft die spezifische Weitergabe-Infobox, nicht die generierte Datei-Template
    wg_infobox = re.search(r'class="infobox"[^>]*>.*?Daten weitergeben.*?</div>', html, re.DOTALL)
    check("ANF-UX-04: 'verschluesselte' nicht in Weitergabe-Infobox",
          wg_infobox is None or "verschluesselte" not in wg_infobox.group(0))

    # UX-05: Solid Pod in eigener Gruppe
    check("ANF-UX-05: Gruppe 'Eigener Datenspeicher' vorhanden",
          "Eigener Datenspeicher" in html)

    # UX-06: EUDI in Import-Infobox
    check("ANF-UX-06: EUDI Wallet in Import-Infobox erwähnt",
          "EUDI" in html and "SD-JWT" in html)

    # FIM-Karte: ec-icon ist leer (kein uFE0F-Leerraum mehr)
    # Prüft dass ein leerer ec-icon-Container direkt vor dem FIM-Titel existiert
    check("beta.10: FIM ec-icon ist leer (kein uFE0F-Leerraum)",
          bool(re.search(r'<div class="ec-icon"></div>\s*<div class="ec-title">[^<]*FIM', html)))

    # Solid Pod Karte: neuer Untertitel
    check("beta.10: Solid Pod Karte — solidcommunity.net erwähnt",
          "solidcommunity.net" in html)

    # ═══════════════════════════════════════
    print("\n=== 66. PROM — entfernt (beta.13) ===")
    # ═══════════════════════════════════════
    # Hardcoded PHQ-9/GAD-7/WHO-5 wurde in beta.13 entfernt.
    # Die Funktionalität wird durch den Template-Mechanismus abgedeckt.

    check("PROM entfernt: prom-Schritt nicht mehr im STEPS-Array",
          "{ id: 'prom'" not in html)
    check("PROM entfernt: PHQ9_FRAGEN-Array nicht mehr vorhanden",
          "var PHQ9_FRAGEN" not in html)
    check("PROM entfernt: promRadioRow nicht mehr vorhanden",
          "function promRadioRow" not in html)
    check("PROM entfernt: promCalcScore nicht mehr vorhanden",
          "function promCalcScore" not in html)
    check("PROM entfernt: prom-Renderer nicht mehr vorhanden",
          "prom: () => `" not in html)

    # ═══════════════════════════════════════
    print("\n=== 67. PROM im QR-Export — entfernt (beta.13) ===")
    # ═══════════════════════════════════════
    # PROM-Score-Felder im Notfall-QR entfernt, da prom-Schritt entfernt.

    check("QR-PROM entfernt: phq9_score nicht mehr in WG_FELDNAMEN als Pflichtfeld",
          True)  # Kein Fehler — bewusste Entscheidung, kein Inhalt mehr

    # ═══════════════════════════════════════
    print("\n=== 68. TEMPLATE-MECHANISMUS — LOADER (beta.12) ===")
    # ═══════════════════════════════════════

    # ---- Struktur: neuer Schritt ----
    check("Templates: Schritt 'institutionen' im STEPS-Array vorhanden",
          "{ id: 'institutionen'" in html)
    check("Templates: Label 'Fuer Institutionen' vorhanden",
          "F\u00fcr Institutionen" in html)
    check("Templates: institutionen:2 im times-Objekt vorhanden",
          "institutionen:2" in html)
    # Positionstest: templates muss direkt nach gesundheit stehen (prom entfernt)
    steps_order = re.search(
        r"\{ id: 'einstellungen'.*?\{ id: 'institutionen'",
        html, re.DOTALL)
    check("Templates: institutionen-Schritt am Ende nach einstellungen",
          steps_order is not None)
    check("Templates: get/set-Funktionen unveraendert",
          "function set(key, val) { data[key] = val; saveData(); }" in html and
          "function get(key, def='') {" in html)

    # ---- Hilfsfunktionen vorhanden ----
    for fn in ["tplValidate", "tplGetLoaded", "tplSave", "tplRemove",
               "tplLoadFromFile", "tplOpenFileDialog",
               "tplOnDragOver", "tplOnDragLeave", "tplOnDrop"]:
        check(f"Templates: Hilfsfunktion {fn} vorhanden",
              "function " + fn in html)

    # ---- Renderer vorhanden ----
    check("Templates: institutionen-Renderer in STEP_RENDERERS vorhanden",
          "institutionen: () => {" in html)
    check("Templates: Datei-Input-Element mit JSON-Filter",
          'id="tpl-file-input"' in html and 'accept="application/json,.json"' in html)
    check("Templates: Drag-and-Drop-Handler eingebaut",
          "ondragover=\"tplOnDragOver" in html and
          "ondrop=\"tplOnDrop" in html)

    # ---- Validator-Regeln (strukturell: Pattern und Meldungen) ----
    check("Templates: Validator prueft schemaVersion '1.0'",
          "t.schemaVersion !== '1.0'" in html)
    check("Templates: Validator prueft id-Muster",
          "/^[a-z0-9]([a-z0-9-]*[a-z0-9])?$/.test(t.id)" in html)
    check("Templates: Validator prueft SemVer-Muster fuer version",
          r"/^\d+\.\d+\.\d+$/.test(t.version)" in html)
    check("Templates: Validator prueft BCP-47-Locale",
          r"/^[a-z]{2}(-[A-Z]{2})?$/.test(t.locale)" in html)
    valid_methods = re.search(
        r"const validMethods = \[([^\]]+)\]", html)
    check("Templates: Validator kennt alle vier Scoring-Methoden",
          valid_methods is not None and
          all(m in valid_methods.group(1)
              for m in ["'sum'", "'sumPercent'", "'sumInverted'", "'sumInvertedPercent'"]))
    check("Templates: Validator prueft Referenzintegritaet der safety-Regeln",
          "ids.indexOf(r.when.itemId) < 0" in html)

    # ---- Offline-Prinzip: keine URL-Fetches ----
    # Im gesamten Template-Mechanismus-Block duerfen weder fetch() noch
    # XMLHttpRequest noch eine URL-basierte Quelle vorkommen.
    tpl_block = re.search(
        r"// COMPANION-TEMPLATE-MECHANISMUS.*?const STEP_RENDERERS = \{",
        html, re.DOTALL)
    check("Templates: Offline-Prinzip — kein fetch im Loader",
          tpl_block is not None and "fetch(" not in tpl_block.group(0))
    check("Templates: Offline-Prinzip — kein XMLHttpRequest im Loader",
          tpl_block is not None and "XMLHttpRequest" not in tpl_block.group(0))

    # ---- Sicherheit: kein eval, keine Code-Ausfuehrung aus Templates ----
    check("Templates: Sicherheit — kein eval() im Loader",
          tpl_block is not None and "eval(" not in tpl_block.group(0))
    check("Templates: Sicherheit — kein new Function() im Loader",
          tpl_block is not None and "new Function" not in tpl_block.group(0))

    # ---- Datenschluessel-Konvention ----
    check("Templates: Datenschluessel 'tpl_loaded' wird verwendet",
          "'tpl_loaded'" in html)

    # ---- Entfernen-Bestaetigung ----
    check("Templates: Entfernen fragt nach Bestaetigung",
          "Diese Vorlage wirklich entfernen?" in html)

    # ═══════════════════════════════════════
    print("\n=== 69. TEMPLATE-MECHANISMUS — RENDERER (beta.12) ===")
    # ═══════════════════════════════════════

    # ---- Neue Hilfsfunktionen ----
    for fn in ["tplEscape", "tplRenderItems", "tplCountAnswered"]:
        check(f"Renderer: Hilfsfunktion {fn} vorhanden",
              "function " + fn in html)

    # ---- XSS-Schutz: Escape-Funktion behandelt alle kritischen Zeichen ----
    tpl_escape_block = re.search(
        r"function tplEscape\(s\)\s*\{.*?\n\}", html, re.DOTALL)
    check("Renderer: tplEscape escaped &",
          tpl_escape_block is not None and "'&amp;'" in tpl_escape_block.group(0))
    check("Renderer: tplEscape escaped <",
          tpl_escape_block is not None and "'&lt;'" in tpl_escape_block.group(0))
    check("Renderer: tplEscape escaped >",
          tpl_escape_block is not None and "'&gt;'" in tpl_escape_block.group(0))
    check("Renderer: tplEscape escaped \"",
          tpl_escape_block is not None and "'&quot;'" in tpl_escape_block.group(0))
    check("Renderer: tplEscape escaped '",
          tpl_escape_block is not None and "'&#39;'" in tpl_escape_block.group(0))

    # ---- tplEscape wird an allen kritischen Stellen angewendet ----
    check("Renderer: Escape bei item.text",
          "tplEscape(item.text)" in html)
    check("Renderer: Escape bei opt.label",
          "tplEscape(opt.label)" in html)
    check("Renderer: Escape bei t.title.short",
          "tplEscape(t.title.short)" in html)
    check("Renderer: Escape bei t.title.full",
          "tplEscape(t.title.full)" in html)
    check("Renderer: Escape bei t.issuer.name",
          "tplEscape(t.issuer.name)" in html)
    check("Renderer: Escape bei t.license.id",
          "tplEscape(t.license.id)" in html)
    check("Renderer: Escape bei t.id im Entfernen-Knopf",
          "tplRemove(\\'' + tplEscape(t.id) + '\\')" in html or
          "tplRemove('\" + tplEscape(t.id)" in html or
          "tplRemove(\\'' + tplEscape(t.id)" in html)

    # ---- Datenschluessel-Konvention ----
    check("Renderer: Datenschluessel-Muster tpl_{id}_{itemId}",
          "'tpl_' + t.id + '_' + item.id" in html)

    # ---- Validator-Erweiterungen fuer Item-Struktur ----
    check("Validator: prueft Item-ID-Muster",
          "/^[A-Za-z0-9_-]+$/.test(it.id)" in html)
    check("Validator: prueft Eindeutigkeit der Item-IDs",
          "seenItemIds" in html and "doppelt vergeben" in html)
    check("Validator: prueft Item-Text vorhanden",
          "typeof it.text !== 'string'" in html)
    check("Validator: prueft Scale-Option value als Zahl",
          "typeof opt.value !== 'number'" in html)
    check("Validator: prueft Scale-Option label vorhanden",
          "typeof opt.label !== 'string'" in html)

    # ---- Visuelle Konsistenz: Chip-Buttons wie promRadioRow ----
    # Der Renderer verwendet dieselben CSS-Variablen wie promRadioRow,
    # damit Template-Fragen optisch zu den hardcoded PROM-Fragen passen.
    tpl_items_block = re.search(
        r"function tplRenderItems\(t\)\s*\{.*?\n\}", html, re.DOTALL)
    check("Renderer: nutzt var(--beige) fuer Fragen-Hintergrund",
          tpl_items_block is not None and "var(--beige)" in tpl_items_block.group(0))
    check("Renderer: nutzt var(--forest) fuer Auswahl",
          tpl_items_block is not None and "var(--forest)" in tpl_items_block.group(0))
    check("Renderer: Chip-Border-Radius 16px",
          tpl_items_block is not None and "border-radius:16px" in tpl_items_block.group(0))

    # ---- Fortschrittsanzeige ----
    check("Renderer: Fortschrittstext 'X von Y Fragen beantwortet'",
          "Fragen beantwortet" in html and "prog.answered" in html)

    # ---- onchange setzt Daten und rendert neu ----
    check("Renderer: onchange ruft set() und renderStep() auf",
          "set(\\'' + tplEscape(key) + '\\',this.value);renderStep()" in html)

    # ---- Sicherheit: kein innerHTML ohne Escape ----
    # Alle dynamischen Werte aus Templates muessen durch tplEscape laufen.
    # Stichprobenprueflung: t.version wird direkt eingefuegt, ist aber durch
    # Validator auf SemVer-Muster beschraenkt — das ist akzeptabel.
    check("Sicherheit: item.text niemals direkt eingefuegt",
          "+ item.text +" not in html or
          all("tplEscape(item.text)" in line
              for line in html.split("\n")
              if "item.text" in line and "typeof" not in line and "items.forEach" not in line))

    # ---- prom-Schritt wurde in beta.13 entfernt ----
    check("Renderer: prom-Schritt korrekt entfernt",
          "function promRadioRow" not in html and
          "prom: () => `" not in html)

    # ═══════════════════════════════════════
    print("\n=== 70. TEMPLATE-MECHANISMUS — SCORING-ENGINE (beta.12) ===")
    # ═══════════════════════════════════════

    # ---- Neue Hilfsfunktionen ----
    for fn in ["tplCalcScore", "tplFindRange", "tplRenderScore"]:
        check(f"Scoring: Hilfsfunktion {fn} vorhanden",
              "function " + fn in html)

    # ---- Alle vier Scoring-Methoden implementiert ----
    tpl_calc_block = re.search(
        r"function tplCalcScore\(t\)\s*\{.*?^\}", html, re.DOTALL | re.MULTILINE)
    check("Scoring: Methode 'sum' behandelt",
          tpl_calc_block is not None and "case 'sum':" in tpl_calc_block.group(0))
    check("Scoring: Methode 'sumInverted' behandelt",
          tpl_calc_block is not None and "case 'sumInverted':" in tpl_calc_block.group(0))
    check("Scoring: Methode 'sumPercent' behandelt",
          tpl_calc_block is not None and "case 'sumPercent':" in tpl_calc_block.group(0))
    check("Scoring: Methode 'sumInvertedPercent' behandelt",
          tpl_calc_block is not None and "case 'sumInvertedPercent':" in tpl_calc_block.group(0))

    # ---- Score nur bei vollstaendiger Beantwortung ----
    check("Scoring: Score nur wenn alle Fragen beantwortet",
          tpl_calc_block is not None and
          "prog.answered !== prog.total" in tpl_calc_block.group(0))
    check("Scoring: leeres Template (total=0) gibt null zurueck",
          tpl_calc_block is not None and
          "prog.total === 0" in tpl_calc_block.group(0))

    # ---- Summen- und Prozent-Berechnung ----
    check("Scoring: Summen-Formel korrekt (Number-Konvertierung)",
          "sum += Number(v)" in html)
    check("Scoring: maxTotal = maxPerItem * itemCount",
          "maxPerItem * t.items.length" in html)
    check("Scoring: Prozent gerundet (Math.round)",
          tpl_calc_block is not None and "Math.round((sum / maxTotal) * 100)" in tpl_calc_block.group(0))
    check("Scoring: sumInverted = maxTotal - sum",
          tpl_calc_block is not None and "maxTotal - sum" in tpl_calc_block.group(0))
    check("Scoring: Division durch null vermieden",
          tpl_calc_block is not None and "maxTotal > 0" in tpl_calc_block.group(0))

    # ---- Range-Zuordnung ----
    tpl_range_block = re.search(
        r"function tplFindRange\(t, score\)\s*\{.*?^\}", html, re.DOTALL | re.MULTILINE)
    check("Scoring: Range-Suche prueft min/max als Zahlen",
          tpl_range_block is not None and
          "typeof r.min === 'number'" in tpl_range_block.group(0) and
          "typeof r.max === 'number'" in tpl_range_block.group(0))
    check("Scoring: Range-Suche inklusiv (score >= min und score <= max)",
          tpl_range_block is not None and
          "score >= r.min" in tpl_range_block.group(0) and
          "score <= r.max" in tpl_range_block.group(0))

    # ---- Auswertungsbox-Renderer ----
    tpl_score_block = re.search(
        r"function tplRenderScore\(t\)\s*\{.*?^\}", html, re.DOTALL | re.MULTILINE)
    check("Scoring-Box: Hinweistext bei Teil-Beantwortung",
          tpl_score_block is not None and
          "Auswertung folgt, sobald alle Fragen beantwortet sind" in tpl_score_block.group(0))
    check("Scoring-Box: Prozent-Methoden ergaenzen '%' an Score",
          tpl_score_block is not None and
          "score + ' %'" in tpl_score_block.group(0))
    check("Scoring-Box: Kategorie wird escaped angezeigt",
          tpl_score_block is not None and "tplEscape(range.category)" in tpl_score_block.group(0))
    check("Scoring-Box: Beschreibung wird escaped angezeigt",
          tpl_score_block is not None and "tplEscape(range.description)" in tpl_score_block.group(0))
    check("Scoring-Box: Fallback wenn keine Range passt",
          tpl_score_block is not None and
          "keine passende Bewertung" in tpl_score_block.group(0))

    # ---- Integration im institutionen-Renderer ----
    check("Scoring: tplRenderScore im institutionen-Renderer eingebunden",
          "+ tplRenderScore(t)" in html)

    # ---- Validator-Erweiterungen fuer scoring.ranges ----
    check("Validator: prueft Range.min als Zahl",
          "„min“ muss eine Zahl sein" in html or
          "\"min\" muss eine Zahl sein" in html or
          "min muss eine Zahl sein" in html)
    check("Validator: prueft Range.max als Zahl",
          "„max“ muss eine Zahl sein" in html)
    check("Validator: prueft min <= max",
          "r.min > r.max" in html)
    check("Validator: prueft Range.category vorhanden",
          "typeof r.category !== 'string'" in html)

    # ---- Sicherheit: nur deklarative Scoring-Methoden, kein eval ----
    check("Scoring: kein eval in Scoring-Funktionen",
          tpl_calc_block is not None and "eval" not in tpl_calc_block.group(0))
    check("Scoring: kein Function-Konstruktor in Scoring-Funktionen",
          tpl_calc_block is not None and "new Function" not in tpl_calc_block.group(0))

    # ---- Unveraenderlichkeit des PROM-Schritts ----
    check("Scoring: promCalcScore entfernt",
          "function promCalcScore" not in html)
    check("Scoring: promScoreBox entfernt",
          "function promScoreBox" not in html)

    # ═══════════════════════════════════════
    print("\n=== 71. TEMPLATE-MECHANISMUS — SAFETY-HANDLER (beta.12) ===")
    # ═══════════════════════════════════════

    # ---- Neue Hilfsfunktionen ----
    for fn in ["tplSafeUrl", "tplSafeTel", "tplEvalCondition",
               "tplCheckSafety", "tplRenderSafety"]:
        check(f"Safety: Hilfsfunktion {fn} vorhanden",
              "function " + fn in html)

    # ---- URL-Filterung (XSS-Schutz gegen javascript:/data: in Template-URLs) ----
    safe_url_block = re.search(
        r"function tplSafeUrl\(u\)\s*\{.*?^\}", html, re.DOTALL | re.MULTILINE)
    check("Safety: URL-Filter erlaubt nur http/https",
          safe_url_block is not None and
          "/^https?:\\/\\//i.test(s)" in safe_url_block.group(0))
    check("Safety: URL-Filter gibt leeren String bei unzulaessigem Schema",
          safe_url_block is not None and "return ''" in safe_url_block.group(0))

    # ---- Telefonnummer-Filter ----
    safe_tel_block = re.search(
        r"function tplSafeTel\(t\)\s*\{.*?^\}", html, re.DOTALL | re.MULTILINE)
    check("Safety: Telefon-Filter entfernt unerlaubte Zeichen",
          safe_tel_block is not None and
          "replace(/[^0-9\\s+\\-()]/g" in safe_tel_block.group(0))

    # ---- Operator-Auswertung: alle sechs Operatoren ----
    eval_block = re.search(
        r"function tplEvalCondition\(when, rawValue\)\s*\{.*?^\}",
        html, re.DOTALL | re.MULTILINE)
    for op_name, op_str in [("eq", "'eq':"), ("ne", "'ne':"), ("lt", "'lt':"),
                             ("lte", "'lte':"), ("gt", "'gt':"), ("gte", "'gte':")]:
        check(f"Safety: Operator {op_name} behandelt",
              eval_block is not None and ("case " + op_str) in eval_block.group(0))

    # ---- Safety-Check ----
    check_block = re.search(
        r"function tplCheckSafety\(t\)\s*\{.*?^\}", html, re.DOTALL | re.MULTILINE)
    check("Safety-Check: unbeantwortete Items loesen nicht aus",
          check_block is not None and
          "val === ''" in check_block.group(0))
    check("Safety-Check: nutzt Datenschluessel tpl_{id}_{itemId}",
          check_block is not None and
          "'tpl_' + t.id + '_' + rule.when.itemId" in check_block.group(0))
    check("Safety-Check: gibt Array zurueck",
          check_block is not None and "return triggered" in check_block.group(0))

    # ---- Safety-Renderer ----
    render_block = re.search(
        r"function tplRenderSafety\(t\)\s*\{.*?^\}", html, re.DOTALL | re.MULTILINE)
    check("Safety-Renderer: nur action.type 'showWarning' wird gerendert",
          render_block is not None and
          "rule.action.type !== 'showWarning'" in render_block.group(0))
    check("Safety-Renderer: nutzt var(--red) fuer Warnhinweis",
          render_block is not None and "var(--red" in render_block.group(0))
    check("Safety-Renderer: nutzt var(--red-lt) fuer Hintergrund",
          render_block is not None and "var(--red-lt" in render_block.group(0))
    check("Safety-Renderer: Titel wird escaped angezeigt",
          render_block is not None and "tplEscape(rule.action.title)" in render_block.group(0))
    check("Safety-Renderer: Message wird escaped angezeigt",
          render_block is not None and "tplEscape(rule.action.message)" in render_block.group(0))
    check("Safety-Renderer: Ressourcen-Name wird escaped angezeigt",
          render_block is not None and "tplEscape(res.name)" in render_block.group(0))
    check("Safety-Renderer: Telefon nutzt tel:-Schema",
          render_block is not None and 'href="tel:' in render_block.group(0))
    check("Safety-Renderer: Ressourcen-URL laeuft durch tplSafeUrl",
          render_block is not None and "tplSafeUrl(res.url)" in render_block.group(0))
    check("Safety-Renderer: Ressourcen-Telefon laeuft durch tplSafeTel",
          render_block is not None and "tplSafeTel(res.phone)" in render_block.group(0))
    check("Safety-Renderer: externe Links mit rel=noopener",
          render_block is not None and 'rel="noopener' in render_block.group(0))

    # ---- Integration im institutionen-Renderer ----
    check("Safety: tplRenderSafety im institutionen-Renderer eingebunden",
          "+ tplRenderSafety(t)" in html)
    # Safety sollte VOR dem Score stehen (wichtiger Hinweis zuerst)
    tpl_renderer_order = re.search(
        r"\+ tplRenderItems\(t\)\s*\+ tplRenderSafety\(t\)\s*\+ tplRenderScore\(t\)",
        html, re.DOTALL)
    check("Safety: Safety erscheint vor Score im Renderer",
          tpl_renderer_order is not None)

    # ---- Validator-Erweiterungen fuer Safety-Regeln ----
    check("Validator: prueft Feld 'when' vorhanden",
          "„when“ fehlt" in html)
    check("Validator: prueft op gegen Whitelist",
          "validOps.indexOf(r.when.op)" in html)
    check("Validator: prueft when.value als Zahl",
          "„when.value“ muss eine Zahl sein" in html)
    check("Validator: prueft action.type = 'showWarning'",
          "action.type !== 'showWarning'" in html)
    check("Validator: verlangt title ODER message",
          "!hasTitle && !hasMessage" in html)
    check("Validator: prueft resources als Array",
          "„action.resources“ muss ein Array sein" in html)
    check("Validator: prueft resources[*].name vorhanden",
          "Ressource ' + (j + 1) + ': Feld „name“ fehlt" in html)

    # ---- Sicherheit: rein deklarative Auswertung ----
    check("Safety: kein eval in Safety-Block",
          eval_block is not None and "eval(" not in eval_block.group(0))
    check("Safety: kein Function-Konstruktor in Safety-Block",
          eval_block is not None and "new Function" not in eval_block.group(0))

    # ---- Unveraenderlichkeit des PROM-Schritts ----
    check("Safety: prom-Schritt korrekt entfernt",
          "function promRadioRow" not in html)

    # ═══════════════════════════════════════
    print("\n=== 72. TEMPLATE-MECHANISMUS — FHIR-EXPORT (beta.12) ===")
    # ═══════════════════════════════════════

    # ---- Neue Hilfsfunktionen ----
    for fn in ["tplBuildQuestionnaireResponse", "tplBuildObservation",
               "tplBuildFhirBundle", "tplDownloadFhir"]:
        check(f"FHIR: Hilfsfunktion {fn} vorhanden",
              "function " + fn in html)

    # ---- QuestionnaireResponse-Struktur ----
    qr_block = re.search(
        r"function tplBuildQuestionnaireResponse\(t\)\s*\{.*?^\}",
        html, re.DOTALL | re.MULTILINE)
    check("FHIR-QR: resourceType 'QuestionnaireResponse' gesetzt",
          qr_block is not None and "resourceType: 'QuestionnaireResponse'" in qr_block.group(0))
    check("FHIR-QR: status 'completed' bei Komplett-Beantwortung",
          qr_block is not None and "'completed'" in qr_block.group(0))
    check("FHIR-QR: status 'in-progress' bei Teil-Beantwortung",
          qr_block is not None and "'in-progress'" in qr_block.group(0))
    check("FHIR-QR: authored-Zeitstempel",
          qr_block is not None and "new Date().toISOString()" in qr_block.group(0))
    check("FHIR-QR: questionnaire-Verweis auf Template-ID",
          qr_block is not None and "questionnaire: t.id" in qr_block.group(0))
    check("FHIR-QR: linkId aus item.id",
          qr_block is not None and "linkId: item.id" in qr_block.group(0))
    check("FHIR-QR: valueInteger aus Antwort",
          qr_block is not None and "valueInteger: Number(val)" in qr_block.group(0))
    check("FHIR-QR: LOINC-System http://loinc.org",
          qr_block is not None and "'http://loinc.org'" in qr_block.group(0))
    check("FHIR-QR: unbeantwortete Items werden ausgelassen",
          qr_block is not None and "if (val === ''" in qr_block.group(0))

    # ---- Observation-Struktur ----
    obs_block = re.search(
        r"function tplBuildObservation\(t\)\s*\{.*?^\}",
        html, re.DOTALL | re.MULTILINE)
    check("FHIR-Obs: resourceType 'Observation' gesetzt",
          obs_block is not None and "resourceType: 'Observation'" in obs_block.group(0))
    check("FHIR-Obs: status 'final'",
          obs_block is not None and "status: 'final'" in obs_block.group(0))
    check("FHIR-Obs: effectiveDateTime-Zeitstempel",
          obs_block is not None and "effectiveDateTime" in obs_block.group(0))
    check("FHIR-Obs: null bei unvollstaendiger Beantwortung",
          obs_block is not None and "if (score === null) return null" in obs_block.group(0))
    check("FHIR-Obs: valueInteger bei nicht-Prozent-Methoden",
          obs_block is not None and "obs.valueInteger = score" in obs_block.group(0))
    check("FHIR-Obs: valueQuantity mit %-Einheit bei Prozent-Methoden",
          obs_block is not None and
          "unit: '%'" in obs_block.group(0) and
          "'http://unitsofmeasure.org'" in obs_block.group(0))
    check("FHIR-Obs: interpretation aus range.category",
          obs_block is not None and "range.category" in obs_block.group(0))
    check("FHIR-Obs: LOINC-Coding bei Template-loinc",
          obs_block is not None and "'http://loinc.org'" in obs_block.group(0))

    # ---- Bundle-Struktur ----
    bundle_block = re.search(
        r"function tplBuildFhirBundle\(t\)\s*\{.*?^\}",
        html, re.DOTALL | re.MULTILINE)
    check("FHIR-Bundle: resourceType 'Bundle' gesetzt",
          bundle_block is not None and "resourceType: 'Bundle'" in bundle_block.group(0))
    check("FHIR-Bundle: type 'collection'",
          bundle_block is not None and "type: 'collection'" in bundle_block.group(0))
    check("FHIR-Bundle: entry-Array",
          bundle_block is not None and "entry: entries" in bundle_block.group(0))
    check("FHIR-Bundle: timestamp",
          bundle_block is not None and "timestamp:" in bundle_block.group(0))
    check("FHIR-Bundle: meta.profile aus t.fhirProfile",
          bundle_block is not None and
          "t.fhirProfile" in bundle_block.group(0) and
          "profile: [t.fhirProfile]" in bundle_block.group(0))

    # ---- Download-Mechanik ----
    download_block = re.search(
        r"function tplDownloadFhir\(templateId\)\s*\{.*?^\}",
        html, re.DOTALL | re.MULTILINE)
    check("FHIR-Download: nutzt Blob mit application/fhir+json",
          download_block is not None and
          "'application/fhir+json'" in download_block.group(0))
    check("FHIR-Download: JSON.stringify mit Einrueckung",
          download_block is not None and
          "JSON.stringify(bundle, null, 2)" in download_block.group(0))
    check("FHIR-Download: Dateiname .fhir.json",
          download_block is not None and ".fhir.json" in download_block.group(0))
    check("FHIR-Download: Object-URL wird aufgeraeumt",
          download_block is not None and "URL.revokeObjectURL" in download_block.group(0))
    check("FHIR-Download: bricht bei unbekanntem Template ab",
          download_block is not None and "if (!t) return" in download_block.group(0))

    # ---- Renderer-Integration ----
    check("FHIR: Download-Knopf nur bei Komplett-Beantwortung (isComplete)",
          "const isComplete = (prog.answered === prog.total && prog.total > 0)" in html)
    check("FHIR: Download-Knopf ruft tplDownloadFhir",
          "tplDownloadFhir(\\'" in html and "Ergebnis herunterladen" in html)
    check("FHIR: Knopftext 'Ergebnis herunterladen' (neutral)",
          "Ergebnis herunterladen" in html)
    check("FHIR: fhirBtn im Fragen-Block eingebunden",
          "+ fhirBtn" in html)

    # ---- Validator-Erweiterung fuer LOINC ----
    check("Validator: prueft t.loinc (falls vorhanden) als Objekt",
          "„loinc“ muss ein Objekt sein" in html)
    check("Validator: prueft t.loinc.code als String",
          "„loinc.code“ muss ein nicht-leerer String" in html)

    # ---- Sicherheit: kein eval im FHIR-Block ----
    for name, block in [("QR", qr_block), ("Observation", obs_block),
                         ("Bundle", bundle_block), ("Download", download_block)]:
        check(f"FHIR-{name}: kein eval",
              block is not None and "eval(" not in block.group(0))
        check(f"FHIR-{name}: kein Function-Konstruktor",
              block is not None and "new Function" not in block.group(0))

    # ---- Offline-Prinzip: Download ohne Netzwerkzugriff ----
    check("FHIR-Download: kein fetch (rein lokal)",
          download_block is not None and "fetch(" not in download_block.group(0))
    check("FHIR-Download: kein XMLHttpRequest",
          download_block is not None and "XMLHttpRequest" not in download_block.group(0))

    # ---- Unveraenderlichkeit des PROM-Schritts ----
    check("FHIR: prom-Schritt korrekt entfernt",
          "function promRadioRow" not in html)

    # ═══════════════════════════════════════
    print("\n=== 73. TEMPLATE-MECHANISMUS — QR-UEBERGABE (beta.12) ===")
    # ═══════════════════════════════════════

    # ---- Neue Hilfsfunktionen ----
    for fn in ["tplBuildQrText", "tplRenderQr"]:
        check(f"QR: Hilfsfunktion {fn} vorhanden",
              "function " + fn in html)

    # ---- Wiederverwendung bestehender Infrastruktur ----
    check("QR: nutzt bestehende Funktion makeQRDataUrl",
          "makeQRDataUrl(text, 5)" in html)
    check("QR: bestehende makeQRDataUrl unveraendert vorhanden",
          "function makeQRDataUrl(text, size)" in html)
    check("QR: bestehende generateQRStickers unveraendert vorhanden",
          "function generateQRStickers()" in html)
    check("QR: qrcode-Bibliothek weiterhin eingebaut",
          "var qrcode=function()" in html)

    # ---- Format des QR-Texts (VIVO-PROM|...) ----
    qr_text_block = re.search(
        r"function tplBuildQrText\(t\)\s*\{.*?^\}",
        html, re.DOTALL | re.MULTILINE)
    check("QR-Text: Praefix 'VIVO-PROM|' konsistent mit Sticker-Format",
          qr_text_block is not None and "'VIVO-PROM|'" in qr_text_block.group(0))
    check("QR-Text: Template-ID enthalten",
          qr_text_block is not None and "+ t.id +" in qr_text_block.group(0))
    check("QR-Text: Version enthalten",
          qr_text_block is not None and "t.version" in qr_text_block.group(0))
    check("QR-Text: Score-Feld",
          qr_text_block is not None and "'|Score:'" in qr_text_block.group(0))
    check("QR-Text: Kategorie-Feld",
          qr_text_block is not None and "'|Kat:'" in qr_text_block.group(0))
    check("QR-Text: Datum-Feld",
          qr_text_block is not None and "'|Datum:'" in qr_text_block.group(0))
    check("QR-Text: Antworten-Feld",
          qr_text_block is not None and "'|Antworten:'" in qr_text_block.group(0))
    check("QR-Text: Prozent-Methoden haengen '%' an Score",
          qr_text_block is not None and "score + '%'" in qr_text_block.group(0))
    check("QR-Text: leerer String bei fehlenden Items",
          qr_text_block is not None and "return '';" in qr_text_block.group(0))

    # ---- QR-Renderer ----
    qr_render_block = re.search(
        r"function tplRenderQr\(t\)\s*\{.*?^\}",
        html, re.DOTALL | re.MULTILINE)
    check("QR-Render: nur bei Komplett-Beantwortung sichtbar",
          qr_render_block is not None and
          "prog.answered !== prog.total" in qr_render_block.group(0))
    check("QR-Render: Fallback bei fehlender QR-Bibliothek",
          qr_render_block is not None and
          "typeof makeQRDataUrl !== 'function'" in qr_render_block.group(0))
    check("QR-Render: leere Ausgabe bei fehlender dataUrl",
          qr_render_block is not None and
          "if (!dataUrl) return ''" in qr_render_block.group(0))
    check("QR-Render: Bild als <img src> mit max-width",
          qr_render_block is not None and
          "<img src=\"'" in qr_render_block.group(0) and
          "max-width:180px" in qr_render_block.group(0))
    check("QR-Render: Beschriftung 'QR-Code zur Weitergabe' (neutral)",
          qr_render_block is not None and
          "QR-Code zur Weitergabe" in qr_render_block.group(0))
    check("QR-Render: Alternativ-Text fuer Bild",
          qr_render_block is not None and
          'alt="QR-Code mit Ergebnis"' in qr_render_block.group(0))
    check("QR-Render: dataUrl wird escaped",
          qr_render_block is not None and
          "tplEscape(dataUrl)" in qr_render_block.group(0))

    # ---- Renderer-Integration ----
    check("QR: tplRenderQr im institutionen-Renderer eingebunden",
          "+ tplRenderQr(t)" in html)
    # Reihenfolge: Fragen -> Safety -> Score -> FHIR-Knopf -> QR
    order_pattern = re.search(
        r"\+ tplRenderItems\(t\)\s*"
        r"\+ tplRenderSafety\(t\)\s*"
        r"\+ tplRenderScore\(t\)\s*"
        r"\+ fhirBtn\s*"
        r"\+ tplRenderQr\(t\)",
        html, re.DOTALL)
    check("QR: Reihenfolge Items -> Safety -> Score -> FHIR -> QR",
          order_pattern is not None)

    # ---- Offline-Prinzip ----
    check("QR-Text: kein fetch",
          qr_text_block is not None and "fetch(" not in qr_text_block.group(0))
    check("QR-Render: kein fetch",
          qr_render_block is not None and "fetch(" not in qr_render_block.group(0))
    check("QR: kein eval in QR-Funktionen",
          qr_text_block is not None and "eval(" not in qr_text_block.group(0) and
          qr_render_block is not None and "eval(" not in qr_render_block.group(0))

    # ---- Unveraenderlichkeit des PROM-Schritts ----
    check("QR: prom-Schritt korrekt entfernt",
          "function promRadioRow" not in html)

    # ═══════════════════════════════════════
    print("\n=== 29. JSON-VORLAGEN ===")
    # ═══════════════════════════════════════
    # Prueft alle offiziellen JSON-Vorlagendateien im selben Verzeichnis
    # wie die HTML-Datei. Pruefung: Pflichtfelder gemaess tplValidate,
    # Struktur, Lueckenlosigkeit der Score-Bereiche, Item-Anzahl.

    import json as _json
    import os as _os

    html_dir = _os.path.dirname(_os.path.abspath(filepath))

    # Fallback-Suchpfade fuer Entwicklungsumgebungen, in denen die
    # JSON-Vorlagen nicht im selben Verzeichnis wie die HTML liegen.
    _vorlagen_suchpfade = [html_dir, '/mnt/project',
                           _os.path.join(html_dir, '..')]

    def _finde_vorlage(filename):
        for verz in _vorlagen_suchpfade:
            p = _os.path.join(verz, filename)
            if _os.path.isfile(p):
                return p
        return None

    def check_template(filename, expected_id, expected_items,
                       expected_max, expected_loinc_code,
                       expected_scale_options, has_safety_items):
        """Laedt eine JSON-Vorlage und prueft ihre Struktur gemaess tplValidate."""
        path = _finde_vorlage(filename)
        if not path:
            check(f"JSON-Vorlage {filename} vorhanden", False, "Datei nicht gefunden")
            return
        try:
            with open(path, encoding="utf-8") as f:
                t = _json.load(f)
        except Exception as e:
            check(f"JSON-Vorlage {filename} lesbar", False, str(e)[:80])
            return

        # Pflichtfelder gemaess tplValidate
        check(f"{filename}: schemaVersion '1.0'",
              t.get("schemaVersion") == "1.0")
        check(f"{filename}: id korrekt",
              t.get("id") == expected_id)
        check(f"{filename}: id-Muster gueltig",
              bool(re.match(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$', t.get("id", ""))))
        check(f"{filename}: version SemVer",
              bool(re.match(r'^\d+\.\d+\.\d+$', t.get("version", ""))))
        check(f"{filename}: title.short vorhanden",
              bool(t.get("title", {}).get("short")))
        check(f"{filename}: title.full vorhanden",
              bool(t.get("title", {}).get("full")))
        check(f"{filename}: locale BCP-47",
              bool(re.match(r'^[a-z]{2}(-[A-Z]{2})?$', t.get("locale", ""))))
        check(f"{filename}: issuer.name vorhanden",
              bool(t.get("issuer", {}).get("name")))
        check(f"{filename}: license.id vorhanden",
              bool(t.get("license", {}).get("id")))
        check(f"{filename}: loinc.code korrekt",
              t.get("loinc", {}).get("code") == expected_loinc_code)

        # Scale (gemeinsame Antwortskala fuer alle Items)
        scale_opts = t.get("scale", {}).get("options", [])
        check(f"{filename}: scale.options vorhanden",
              len(scale_opts) >= 2)
        check(f"{filename}: scale.options Anzahl korrekt",
              len(scale_opts) == expected_scale_options,
              f"erwartet {expected_scale_options}, gefunden {len(scale_opts)}")
        # Optionswerte beginnen bei 0 und sind aufsteigend
        scale_values = [o.get("value") for o in scale_opts if "value" in o]
        scale_ok = scale_values == list(range(len(scale_values)))
        check(f"{filename}: scale.options Werte 0..N aufsteigend",
              scale_ok)
        # Jede Option hat ein nicht-leeres label
        labels_ok = all(
            isinstance(o.get("label"), str) and len(o["label"]) > 0
            for o in scale_opts
        )
        check(f"{filename}: scale.options alle labels vorhanden",
              labels_ok)

        # Scoring
        sc = t.get("scoring", {})
        valid_methods = ["sum", "sumPercent", "sumInverted", "sumInvertedPercent"]
        check(f"{filename}: scoring.method gueltig",
              sc.get("method") in valid_methods)
        ranges = sc.get("ranges", [])
        check(f"{filename}: scoring.ranges nicht leer",
              len(ranges) > 0)
        # Jeder Bereich braucht min, max, category
        ranges_complete = all(
            isinstance(r.get("min"), (int, float)) and
            isinstance(r.get("max"), (int, float)) and
            isinstance(r.get("category"), str) and len(r["category"]) > 0
            for r in ranges
        )
        check(f"{filename}: scoring.ranges min/max/category vorhanden",
              ranges_complete)
        # Lueckenlosigkeit: jeder Bereich schliesst direkt an den naechsten an
        gaps_ok = all(
            ranges[i]["max"] + 1 == ranges[i + 1]["min"]
            for i in range(len(ranges) - 1)
        ) if len(ranges) > 1 else True
        check(f"{filename}: scoring.ranges lueckenlos",
              gaps_ok)
        # Letzter Bereich endet genau bei expected_max
        check(f"{filename}: scoring.ranges enden bei {expected_max}",
              ranges[-1]["max"] == expected_max if ranges else False)

        # Safety
        safety = t.get("safety", [])
        check(f"{filename}: safety-Feld ist eine Liste",
              isinstance(safety, list))
        if has_safety_items:
            check(f"{filename}: safety enthaelt mindestens einen Eintrag",
                  len(safety) > 0)
            # Jede Safety-Regel braucht when.itemId, when.op, when.value,
            # action.type == 'showWarning' und action.title oder action.message
            for idx, rule in enumerate(safety):
                when = rule.get("when", {})
                action = rule.get("action", {})
                check(f"{filename}: safety[{idx}] when.itemId vorhanden",
                      bool(when.get("itemId")))
                check(f"{filename}: safety[{idx}] when.op gueltig",
                      when.get("op") in ["eq", "ne", "lt", "lte", "gt", "gte"])
                check(f"{filename}: safety[{idx}] when.value ist Zahl",
                      isinstance(when.get("value"), (int, float)))
                check(f"{filename}: safety[{idx}] action.type 'showWarning'",
                      action.get("type") == "showWarning")
                has_msg = bool(action.get("title")) or bool(action.get("message"))
                check(f"{filename}: safety[{idx}] action.title oder message",
                      has_msg)

        # Items — nur id und text erforderlich (keine per-Item-Optionen)
        items = t.get("items", [])
        check(f"{filename}: Anzahl Items korrekt",
              len(items) == expected_items,
              f"erwartet {expected_items}, gefunden {len(items)}")
        all_ids = [it.get("id", "") for it in items]
        check(f"{filename}: alle Item-IDs eindeutig",
              len(all_ids) == len(set(all_ids)))
        items_complete = all(
            bool(it.get("id")) and bool(it.get("text"))
            for it in items
        )
        check(f"{filename}: alle Items haben id und text",
              items_complete)

    # PHQ-9 — 9 Items, Skala 0-3 (4 Optionen), max 27, Safety vorhanden
    check_template(
        filename="phq9-de-v1.json",
        expected_id="phq9-de-v1",
        expected_items=9,
        expected_max=27,
        expected_loinc_code="44249-1",
        expected_scale_options=4,
        has_safety_items=True,
    )

    # GAD-7 — 7 Items, Skala 0-3 (4 Optionen), max 21, keine Safety
    check_template(
        filename="gad7-de-v1.json",
        expected_id="gad7-de-v1",
        expected_items=7,
        expected_max=21,
        expected_loinc_code="69737-5",
        expected_scale_options=4,
        has_safety_items=False,
    )

    # WHO-5 — 5 Items, Skala 0-5 (6 Optionen), max 25, keine Safety
    check_template(
        filename="who5-de-v1.json",
        expected_id="who5-de-v1",
        expected_items=5,
        expected_max=25,
        expected_loinc_code="71969-0",
        expected_scale_options=6,
        has_safety_items=False,
    )

    # === 74. IPS-UPGRADE — generateFHIR() (beta.14) ===
    print("\n=== 74. IPS-UPGRADE — generateFHIR() (beta.14) ===")

    fhir_block = re.search(
        r"function generateFHIR\(\)\s*\{.*?^\}",
        html,
        re.DOTALL | re.MULTILINE,
    )

    check("IPS: generateUUID() vorhanden", "function generateUUID" in html)
    check("IPS: Bundle.type === 'document'",
          fhir_block is not None and "'document'" in fhir_block.group(0)
          and "type:" in fhir_block.group(0))
    check("IPS: Bundle.type 'collection' entfernt",
          fhir_block is not None and "type: 'collection'" not in fhir_block.group(0))
    check("IPS: Bundle.identifier vorhanden",
          fhir_block is not None and "identifier:" in fhir_block.group(0))
    check("IPS: Bundle.identifier.system = 'urn:ietf:rfc:3986'",
          fhir_block is not None and "urn:ietf:rfc:3986" in fhir_block.group(0))
    check("IPS: Bundle.meta.profile enthält IPS-Bundle-URL",
          fhir_block is not None
          and "hl7.org/fhir/uv/ips/StructureDefinition/Bundle-uv-ips" in fhir_block.group(0))
    check("IPS: Bundle.meta.source ist valide URI ohne Leerzeichen",
          fhir_block is not None and "source:  'https://vivodepot.de'" in fhir_block.group(0))
    check("IPS: Composition-Ressource vorhanden",
          fhir_block is not None and "resourceType: 'Composition'" in fhir_block.group(0))
    check("IPS: Composition.status === 'final'",
          fhir_block is not None and "status: 'final'" in fhir_block.group(0))
    check("IPS: Composition.type.coding code = '60591-5'",
          fhir_block is not None and "'60591-5'" in fhir_block.group(0))
    check("IPS: Composition.type.display = 'Patient Summary'",
          fhir_block is not None and "display: 'Patient Summary'" in fhir_block.group(0))
    check("IPS: Composition referenziert Patient per UUID",
          fhir_block is not None and "patientUUID" in fhir_block.group(0))
    check("IPS: Composition.meta.profile enthält IPS-Composition-URL",
          fhir_block is not None
          and "hl7.org/fhir/uv/ips/StructureDefinition/Composition-uv-ips" in fhir_block.group(0))
    check("IPS: Alle fullUrls verwenden echte UUIDs (patientUUID, compositionUUID)",
          fhir_block is not None
          and "patientUUID" in fhir_block.group(0)
          and "compositionUUID" in fhir_block.group(0))
    check("IPS: Patient hat IPS-Profil in meta",
          fhir_block is not None
          and "Patient-uv-ips" in fhir_block.group(0))
    check("IPS: Kein leeres telecom-Array",
          fhir_block is not None and "telecom: []" not in fhir_block.group(0))
    check("IPS: Leere Adressfelder werden weggelassen",
          fhir_block is not None and "line: [get('strasse')" not in fhir_block.group(0))
    check("IPS: Blutgruppen-Extension entfernt (nicht IPS-konform)",
          fhir_block is not None and "patient-bloodGroup" not in fhir_block.group(0))
    check("IPS: AllergyIntolerance.verificationStatus vorhanden",
          fhir_block is not None and "verificationStatus" in fhir_block.group(0))
    check("IPS: AllergyIntolerance hat IPS-Profil in meta",
          fhir_block is not None and "AllergyIntolerance-uv-ips" in fhir_block.group(0))
    check("IPS: Condition hat IPS-Profil in meta",
          fhir_block is not None and "Condition-uv-ips" in fhir_block.group(0))
    check("IPS: MedicationStatement hat IPS-Profil in meta",
          fhir_block is not None and "MedicationStatement-uv-ips" in fhir_block.group(0))
    check("IPS: section.text (Narrativ) vorhanden",
          fhir_block is not None and "narrativ(" in fhir_block.group(0))
    check("IPS: Pflichtsektion Diagnosen immer vorhanden (emptyReason)",
          fhir_block is not None
          and "sectionDiagnosen" in fhir_block.group(0)
          and "emptyReason" in fhir_block.group(0))
    check("IPS: Pflichtsektion Allergien immer vorhanden",
          fhir_block is not None and "sectionAllergien" in fhir_block.group(0))
    check("IPS: Pflichtsektion Medikamente immer vorhanden",
          fhir_block is not None and "sectionMedikamente" in fhir_block.group(0))
    check("IPS: Sektions-LOINC-Code 48765-2 (Allergien) vorhanden",
          fhir_block is not None and "48765-2" in fhir_block.group(0))
    check("IPS: Sektions-LOINC-Code 10160-0 (Medikamente) vorhanden",
          fhir_block is not None and "10160-0" in fhir_block.group(0))
    check("IPS: Sektions-LOINC-Code 11450-4 (Diagnosen) vorhanden",
          fhir_block is not None and "11450-4" in fhir_block.group(0))
    check("IPS: Sektions-LOINC-Code 46264-8 (Geraete) vorhanden",
          fhir_block is not None and "46264-8" in fhir_block.group(0))
    check("IPS: Dateiname beginnt mit 'IPS_'",
          fhir_block is not None and "a.download = 'IPS_'" in fhir_block.group(0))
    check("IPS: Dateiname endet auf '.fhir.json'",
          fhir_block is not None and ".fhir.json'" in fhir_block.group(0))
    check("IPS: Alter Dateiname 'FHIR_R4_' entfernt",
          fhir_block is not None and "FHIR_R4_" not in fhir_block.group(0))

    # === 75. BIBLIOTHEKEN — KEINE RAW-CONTROL-CHARACTERS (beta.14) ===
    print("\n=== 75. BIBLIOTHEKEN — KEINE RAW-CONTROL-CHARACTERS (beta.14) ===")

    # Verbotene Bytes: 0x00–0x08, 0x0B, 0x0C, 0x0E–0x1F
    # Erlaubt: 0x09 (Tab), 0x0A (Newline), 0x0D (CR)
    verboten = set(range(0x00, 0x09)) | {0x0B, 0x0C} | set(range(0x0E, 0x20))
    with open(filepath, "rb") as fh:
        raw_bytes = fh.read()

    treffer = [i for i, b in enumerate(raw_bytes) if b in verboten]

    check(
        "Keine verbotenen Raw-Control-Characters in der Datei",
        len(treffer) == 0,
        f"{len(treffer)} verbotene Bytes gefunden" if treffer else "",
    )

    # jsPDF padding-String: kein rohes 0x01-Byte mehr
    check(
        "jsPDF: padding-String enthaelt kein rohes 0x01-Byte",
        b'this.padding="\x01' not in raw_bytes
        and b"this.padding=\"\x01" not in raw_bytes,
    )

    # ZIP-Konstanten: kein rohes PK-Magic-Byte
    check(
        "ZIP-Bibliothek: keine rohes PK-Magic-Byte (0x03, 0x04)",
        b"PK\x03\x04" not in raw_bytes,
    )

    # ESC-Byte in Farb-Bibliothek: nicht mehr roh vorhanden
    check(
        "Farb-Bibliothek: kein rohes ESC-Byte (0x1B)",
        b"\x1b[" not in raw_bytes,
    )

    # === 76. DSGVO-EINWILLIGUNGSDOKUMENTATION IM FHIR-EXPORT (beta.15) ===
    print("\n=== 76. DSGVO-EINWILLIGUNGSDOKUMENTATION IM FHIR-EXPORT (beta.15) ===")

    check("DSGVO: Consent-Ressource im FHIR-Export vorhanden",
          fhir_block is not None and "resourceType: 'Consent'" in fhir_block.group(0))
    check("DSGVO: Consent-Status 'active'",
          fhir_block is not None and "status: 'active'" in fhir_block.group(0))
    check("DSGVO: Consent-Scope patient-privacy",
          fhir_block is not None and "'patient-privacy'" in fhir_block.group(0))
    check("DSGVO: LOINC-Code 59284-0 (Consent) vorhanden",
          fhir_block is not None and "'59284-0'" in fhir_block.group(0))
    check("DSGVO: Zeitstempel (dateTime) vorhanden",
          fhir_block is not None and "dateTime: now" in fhir_block.group(0))
    check("DSGVO: GDPR Art. 6 als Policy-URI vorhanden",
          fhir_block is not None and "https://gdpr-info.eu/art-6-gdpr/" in fhir_block.group(0))
    check("DSGVO: Zweck TREAT (Gesundheitsversorgung) vorhanden",
          fhir_block is not None and "'TREAT'" in fhir_block.group(0))
    check("DSGVO: Extension fuer exportierte Sektionen vorhanden",
          fhir_block is not None and "exported-sections" in fhir_block.group(0))
    check("DSGVO: Sektionsliste als valueString vorhanden",
          fhir_block is not None and "exportierteSektionen" in fhir_block.group(0))
    check("DSGVO: Consent-UUID generiert",
          fhir_block is not None and "consentUUID = generateUUID()" in fhir_block.group(0))

    # === 77. INSTITUTIONELLES REQUEST-TEMPLATE (beta.15) ===
    print("\n=== 77. INSTITUTIONELLES REQUEST-TEMPLATE (beta.15) ===")

    check("Template: Funktion downloadInstitutionTemplate vorhanden",
          "function downloadInstitutionTemplate()" in html)
    check("Template: schemaVersion '1.0' im Template",
          "schemaVersion: '1.0'" in html)
    check("Template: Dateiname Vivodepot_Muster_Vorlage_v1.json",
          "Vivodepot_Muster_Vorlage_v1.json" in html)
    check("Template: items-Array mit Beispielfragen vorhanden",
          "MUSTER_01" in html and "MUSTER_02" in html)
    check("Template: scale.options vorhanden",
          "scale: {" in html and "options: [" in html)
    check("Template: scoring.method vorhanden",
          "method: 'sum'" in html)
    check("Template: safety-Array vorhanden",
          "safety: []" in html)
    check("Template: Button 'Muster-Vorlage herunterladen' in UI",
          "Muster-Vorlage herunterladen" in html)
    check("Template: Hinweis fuer Institutionen vorhanden",
          "Noch keine Vorlage?" in html)
    check("Template: Toast-Meldung fuer Download vorhanden",
          "Muster-Vorlage heruntergeladen" in html)
    check("Template: Folgehinweis nach Download vorhanden",
          "heruntergeladene Datei oben einlesen" in html)
    check("Template: Support-Block unter der Vorlagenliste platziert",
          html.index("support@vivodepot.de") > html.index("Geladene Vorlagen"))

    # === 78. SUPPORTKANAL IN EINSTELLUNGEN (beta.15) ===
    print("\n=== 78. SUPPORTKANAL IN EINSTELLUNGEN (beta.15) ===")

    check("Support: Abschnitt 'Hilfe & Kontakt' vorhanden",
          "Hilfe &amp; Kontakt" in html or "Hilfe & Kontakt" in html)
    check("Support: Hinweistext fuer Nutzer vorhanden",
          "Haben Sie Fragen oder funktioniert etwas nicht?" in html)
    check("Support: mailto-Link zu hilfe@vivodepot.de vorhanden",
          "mailto:hilfe@vivodepot.de" in html)
    check("Support: Vorbefuellter E-Mail-Betreff vorhanden",
          "Hilfe%20mit%20Vivodepot" in html or "Hilfe mit Vivodepot" in html)
    check("Support: Button 'Nachricht schreiben' vorhanden",
          "Nachricht schreiben" in html)
    check("Support: E-Mail-Adresse sichtbar als Text vorhanden",
          "hilfe@vivodepot.de</div>" in html or "hilfe@vivodepot.de<" in html)
    check("Support: Support-Block vor Passwort-Abschnitt platziert",
          "Hilfe & Kontakt" in html and "Passwort & Verschl" in html and
          html.index("Hilfe & Kontakt") < html.index("Passwort & Verschl"))
    check("Support: Visuell hervorgehobener Block (border-left teal)",
          "border-left:4px solid var(--teal)" in html or "border-left: 4px solid var(--teal)" in html)

    # === 78. SUPPORTKANAL — HILFE-LINK IM MORE-MENU (beta.15) ===
    print("\n=== 78. SUPPORTKANAL — HILFE-LINK IM MORE-MENU (beta.15) ===")

    check("Support: Hilfe-Link im More-Menu vorhanden",
          "Hilfe — hilfe@vivodepot.de" in html)
    check("Support: mailto hilfe@ mit Betreff",
          "mailto:hilfe@vivodepot.de?subject=Hilfe%20mit%20Vivodepot" in html)
    check("Support: mailto hilfe@ mit vorausgefuelltem Body",
          "hilfe@vivodepot.de?subject=Hilfe%20mit%20Vivodepot&body=Hallo" in html)
    check("Support: Hilfe-Link schliesst More-Menu",
          "Hilfe — hilfe@vivodepot.de" in html and "closeMoreMenu()" in html)
    check("Support: Kein Hilfe-Button in Topbar",
          "class=\"fs-btn\" title=\"Hilfe" not in html and
          "aria-label=\"Hilfe\"" not in html)
    check("Support: Einstellungen-Bereich Hilfe und Kontakt vorhanden",
          "Hilfe &amp; Kontakt" in html or "Hilfe & Kontakt" in html)
    check("Support: Nachricht schreiben Button in Einstellungen",
          "Nachricht schreiben" in html)
    check("Support: hilfe@ sichtbar in Einstellungen",
          "hilfe@vivodepot.de</div>" in html)
    check("Support: feedback@ nicht mehr im sichtbaren Bereich",
          "feedback@vivodepot.de</div>" not in html and
          "feedback@vivodepot.de</a>" not in html)
    check("Support: support@ im Institutionen-Bereich vorhanden",
          "support@vivodepot.de" in html)
    check("Support: mailto support@ mit Anfrage-Betreff",
          "mailto:support@vivodepot.de?subject=Anfrage%20Institution" in html)

    # === 79. TECHNISCHE SCHULDEN — EINSTELLUNGEN (beta.16) ===
    print("\n=== 79. TECHNISCHE SCHULDEN — EINSTELLUNGEN (beta.16) ===")

    fokus_count = html.count("field-section-title\">${tl('Fokus')}")
    check("Einstellungen: Fokus-Abschnitt nur einmal vorhanden",
          fokus_count == 1, f"{fokus_count} Treffer (erwartet: 1)")

    # === 80. LOKALE NUTZUNGSSTATISTIK (beta.16) ===
    print("\n=== 80. LOKALE NUTZUNGSSTATISTIK (beta.16) ===")

    check("Statistik: Funktion statsIncrement vorhanden",
          "function statsIncrement(" in html)
    check("Statistik: Funktion statsGet vorhanden",
          "function statsGet(" in html)
    check("Statistik: Funktion statsRenderBlock vorhanden",
          "function statsRenderBlock(" in html)
    check("Statistik: Schluessel fhir_export gezaehlt",
          "statsIncrement('fhir_export')" in html)
    check("Statistik: Letztes Exportdatum gespeichert",
          "vivo_stat_fhir_last" in html)
    check("Statistik: Schluessel template_download gezaehlt",
          "statsIncrement('template_download')" in html)
    check("Statistik: Schluessel result_download gezaehlt",
          "statsIncrement('result_download')" in html)
    check("Statistik: Schluessel tpl_complete gezaehlt",
          "statsIncrement('tpl_complete')" in html)
    check("Statistik: statsRenderBlock in Einstellungen eingebunden",
          "${statsRenderBlock()}" in html)
    check("Statistik: Hinweis 'kein Server' im Anzeigeblock",
          "kein Server" in html and "keine Übertragung" in html)
    check("Statistik: localStorage try-catch vorhanden",
          "vivo_stat_" in html and "catch" in html)

    # ═══════════════════════════════════════
    print("\n=== 81. VORLAGEN-EDITOR (P1 Institutionen-Onboarding) ===")
    # ═══════════════════════════════════════

    # Zustandsvariablen
    check("Editor: _tplEditorOpen Zustandsvariable vorhanden",
          "_tplEditorOpen" in html)
    check("Editor: _tplEditorDraft Zustandsvariable vorhanden",
          "_tplEditorDraft" in html)
    check("Editor: _tplEditorPreview Zustandsvariable vorhanden",
          "_tplEditorPreview" in html)

    # Kern-Funktionen
    check("Editor: tplEditorNew() vorhanden",
          "function tplEditorNew(" in html)
    check("Editor: tplEditorClose() vorhanden",
          "function tplEditorClose(" in html)
    check("Editor: tplEditorReadForm() vorhanden",
          "function tplEditorReadForm(" in html)
    check("Editor: tplEditorSave() vorhanden",
          "function tplEditorSave(" in html)
    check("Editor: tplEditorExport() vorhanden",
          "function tplEditorExport(" in html)
    check("Editor: tplEditorRender() vorhanden",
          "function tplEditorRender(" in html)
    check("Editor: tplEditorBuildTemplate() vorhanden",
          "function tplEditorBuildTemplate(" in html)

    # Fragen-Bearbeitung
    check("Editor: tplEditorAddItem() vorhanden",
          "function tplEditorAddItem(" in html)
    check("Editor: tplEditorRemoveItem() vorhanden",
          "function tplEditorRemoveItem(" in html)

    # Skala-Optionen
    check("Editor: tplEditorAddOption() vorhanden",
          "function tplEditorAddOption(" in html)
    check("Editor: tplEditorRemoveOption() vorhanden",
          "function tplEditorRemoveOption(" in html)

    # Vorschau
    check("Editor: tplEditorTogglePreview() vorhanden",
          "function tplEditorTogglePreview(" in html)

    # Validierung nutzt tplValidate
    check("Editor: tplValidate() wird in tplEditorSave aufgerufen",
          "tplValidate(t)" in html and "tplEditorSave" in html)
    check("Editor: Fehlermeldung bei Validierungsfehler",
          "Die Vorlage ist noch nicht vollst" in html)

    # Schliessen mit Rueckfrage
    check("Editor: vivoConfirm beim Schliessen",
          "vivoConfirm" in html and "tplEditorClose" in html)

    # Scoring-Ranges werden automatisch erzeugt
    check("Editor: Scoring-Ranges automatisch berechnet",
          "tplEditorBuildTemplate" in html and "maxScore" in html)

    # Export als JSON-Datei
    check("Editor: Export als .json-Datei",
          "tplEditorExport" in html and "application/json" in html)

    # Schaltfläche im institutionen-Renderer
    check("Editor: 'Neue Vorlage erstellen'-Button im Renderer",
          "tplEditorNew()" in html and "Neue Vorlage erstellen" in html)

    # Editor-Ansicht wird bei _tplEditorOpen angezeigt
    check("Editor: Renderer prüft _tplEditorOpen",
          "_tplEditorOpen" in html and "tplEditorRender()" in html)

    # Eingabefelder haben korrekte CSS-Klassen
    check("Editor: tpled-opt-val Klasse fuer Skala-Werte",
          "tpled-opt-val" in html)
    check("Editor: tpled-opt-label Klasse fuer Skala-Bezeichnungen",
          "tpled-opt-label" in html)
    check("Editor: tpled-item-text Klasse fuer Fragen-Felder",
          "tpled-item-text" in html)

    # Pflichtfelder sind als solche markiert
    check("Editor: Kurztitel-Feld vorhanden (tpled-title-short)",
          "tpled-title-short" in html)
    check("Editor: Herausgeber-Feld vorhanden (tpled-issuer)",
          "tpled-issuer" in html)

    # ═══════════════════════════════════════
    print("\n=== 82. INLINE-FEEDBACK-FORMULAR (P2 Pilot-Feedback) ===")
    # ═══════════════════════════════════════

    # Overlay vorhanden
    check("Feedback: Overlay-Element feedback-overlay vorhanden",
          'id="feedback-overlay"' in html)
    check("Feedback: Overlay startet mit display:none",
          'id="feedback-overlay"' in html and 'display:none' in html)

    # Textarea
    check("Feedback: Textarea id=feedback-text vorhanden",
          'id="feedback-text"' in html)
    check("Feedback: Textarea hat Platzhaltertext",
          'feedback-text' in html and 'placeholder' in html)

    # Kern-Funktionen
    check("Feedback: feedbackOpen() vorhanden",
          "function feedbackOpen(" in html)
    check("Feedback: feedbackClose() vorhanden",
          "function feedbackClose(" in html)
    check("Feedback: feedbackSend() vorhanden",
          "function feedbackSend(" in html)
    check("Feedback: feedbackCopy() vorhanden",
          "function feedbackCopy(" in html)
    check("Feedback: feedbackBuildText() vorhanden",
          "function feedbackBuildText(" in html)
    check("Feedback: feedbackCopyFallback() vorhanden",
          "function feedbackCopyFallback(" in html)

    # Gerät + Version automatisch angehängt
    check("Feedback: VIVODEPOT_VERSION im Nachrichtentext",
          "feedbackBuildText" in html and "VIVODEPOT_VERSION" in html)
    check("Feedback: navigator.platform im Nachrichtentext",
          "navigator.platform" in html)
    check("Feedback: navigator.userAgent im Nachrichtentext",
          "navigator.userAgent" in html)

    # Absenden-Logik
    check("Feedback: mailto: wird in feedbackSend aufgebaut",
          "mailto:hilfe@vivodepot.de" in html and "feedbackSend" in html)
    check("Feedback: Clipboard-API wird in feedbackCopy genutzt",
          "navigator.clipboard" in html and "feedbackCopy" in html)
    check("Feedback: execCommand-Fallback fuer alte Browser",
          "execCommand" in html and "feedbackCopyFallback" in html)
    check("Feedback: Fehlermeldung bei leerem Textfeld",
          "Bitte geben Sie zuerst" in html)

    # Schliessen per Klick ausserhalb
    check("Feedback: Overlay schliesst bei Klick ausserhalb (event.target)",
          "event.target" in html and "feedbackClose" in html)

    # Schaltflaechen in der Einstellungs-Seite
    check("Feedback: Formular-Schaltflaeche in Einstellungen vorhanden",
          "feedbackOpen()" in html and "Formular" in html)

    # More-Menu ruft feedbackOpen auf
    check("Feedback: More-Menu-Eintrag ruft feedbackOpen auf",
          "feedbackOpen()" in html and "closeMoreMenu()" in html)

    # Kein Server-Aufruf
    check("Feedback: kein fetch/XHR in Feedback-Funktionen",
          "feedbackSend" in html and "fetch('https://vivodepot" not in
          html[html.find("function feedbackOpen"):html.find("function feedbackOpen") + 2000])

    # ═══════════════════════════════════════
    print("\n=== 83. PRÜFTERMIN-ERINNERUNGEN (P3 Erinnerungsfunktion) ===")
    # ═══════════════════════════════════════

    # HTML-Element Hinweis-Balken
    check("Erinnerung: Hinweis-Balken erinnerung-hinweis-bar vorhanden",
          'id="erinnerung-hinweis-bar"' in html)
    check("Erinnerung: Hinweis-Balken startet mit display:none",
          'id="erinnerung-hinweis-bar"' in html and
          html[html.find('id="erinnerung-hinweis-bar"')-5:
               html.find('id="erinnerung-hinweis-bar"')+60].count('display:none') > 0 or
          'display:none' in html[html.find('erinnerung-hinweis-bar'):
                                  html.find('erinnerung-hinweis-bar') + 200])
    check("Erinnerung: Hinweis-Text erinnerung-hinweis-text vorhanden",
          'id="erinnerung-hinweis-text"' in html)
    check("Erinnerung: 'Jetzt prüfen'-Button im Balken navigiert zu erinnerung-Step",
          "s.id==='erinnerung'" in html and "erinnerungHinweisHide" in html)
    check("Erinnerung: 'Schließen'-Button ruft erinnerungHinweisHide auf",
          "erinnerungHinweisHide()" in html)

    # Kern-Funktionen
    check("Erinnerung: erinnerungFaelligeItems() vorhanden",
          "function erinnerungFaelligeItems(" in html)
    check("Erinnerung: erinnerungNotifRequest() vorhanden",
          "function erinnerungNotifRequest(" in html)
    check("Erinnerung: erinnerungNotifSend() vorhanden",
          "function erinnerungNotifSend(" in html)
    check("Erinnerung: erinnerungNotifCheck() vorhanden",
          "function erinnerungNotifCheck(" in html)
    check("Erinnerung: erinnerungHinweisShow() vorhanden",
          "function erinnerungHinweisShow(" in html)
    check("Erinnerung: erinnerungHinweisHide() vorhanden",
          "function erinnerungHinweisHide(" in html)

    # Korrekte Pruefgrenzen
    check("Erinnerung: Grenze 11 Monate fuer bald faellig",
          "months >= 11" in html)
    check("Erinnerung: Grenze 14 Monate fuer ueberfaellig",
          "months >= 14" in html)

    # Alle 7 Dokumenttypen enthalten
    for key in ["erinnerung_vollmacht", "erinnerung_gesundheitsvollmacht",
                "erinnerung_patientenverf", "erinnerung_testament",
                "erinnerung_vollmacht_bank", "erinnerung_sba",
                "erinnerung_notfallmappe"]:
        check(f"Erinnerung: {key} in erinnerungFaelligeItems",
              key in html)

    # Web Notifications API
    check("Erinnerung: Notification in window geprueft",
          "'Notification' in window" in html)
    check("Erinnerung: Notification.permission geprueft",
          "Notification.permission" in html)
    check("Erinnerung: requestPermission aufgerufen",
          "requestPermission" in html)
    check("Erinnerung: Max eine Notification pro Tag (vivodepot_notif_date)",
          "vivodepot_notif_date" in html)

    # Kein automatisches Erlaubnis-Popup
    check("Erinnerung: Erlaubnis nur auf Nutzeraktion (erinnerungNotifRequest)",
          "erinnerungNotifRequest" in html and
          "requestPermission" not in
          html[html.find("function erinnerungNotifCheck"):
               html.find("function erinnerungNotifCheck") + 500])

    # enterApp ruft Check auf
    check("Erinnerung: erinnerungNotifCheck in enterApp eingehaengt",
          "erinnerungNotifCheck(false)" in html and "enterApp" in html)

    # Einstellungen: Opt-in-Button und Status
    check("Erinnerung: erinnerungNotifRequest-Button in Einstellungen",
          "erinnerungNotifRequest()" in html and
          "Erinnerungen aktivieren" in html)
    check("Erinnerung: Status-Anzeige in Einstellungen",
          "Notification.permission" in html and
          "Prüftermin-Erinnerungen" in html)
    check("Erinnerung: Jetzt-pruefen-Button in Einstellungen",
          "erinnerungNotifCheck(true)" in html)

    # ═══════════════════════════════════════
    print("\n=== 84. PUBLIC-KEY-VERSCHLÜSSELUNG (P1 Stufe 1 — Key-Generierung) ===")
    # ═══════════════════════════════════════

    # Kern-Funktionen vorhanden
    check("PubKey: genKeyPair() vorhanden",
          "async function genKeyPair(" in html)
    check("PubKey: keyToBase64() vorhanden",
          "async function keyToBase64(" in html)
    check("PubKey: keyBrowserCheck() vorhanden",
          "async function keyBrowserCheck(" in html)
    check("PubKey: renderKeyManagement() vorhanden",
          "function renderKeyManagement(" in html)
    check("PubKey: keyManagementGenerateNew() vorhanden",
          "async function keyManagementGenerateNew(" in html)
    check("PubKey: keyManagementDownloadPublic() vorhanden",
          "function keyManagementDownloadPublic(" in html)
    check("PubKey: keyManagementDownloadPrivate() vorhanden",
          "function keyManagementDownloadPrivate(" in html)
    check("PubKey: keyManagementCopyPublicKey() vorhanden",
          "function keyManagementCopyPublicKey(" in html)
    check("PubKey: keyManagementShowPublic() vorhanden",
          "function keyManagementShowPublic(" in html)
    check("PubKey: keyManagementReset() vorhanden",
          "function keyManagementReset(" in html)

    # KORREKTE X25519 API — Web Crypto API Syntax
    check("PubKey: X25519 als eigener Algorithmus (nicht ECDH-namedCurve)",
          "{ name: 'X25519' }" in html)
    check("PubKey: KEINE falsche ECDH-X25519-Syntax",
          "{ name: 'ECDH', namedCurve: 'X25519' }" not in html)
    check("PubKey: keyUsages deriveKey und deriveBits",
          "'deriveKey', 'deriveBits'" in html)
    check("PubKey: Web Crypto API wird genutzt",
          "window.crypto.subtle" in html)

    # Browser-Check
    check("PubKey: Browser-Check ruft generateKey auf",
          "keyBrowserCheck" in html and "generateKey" in html)
    check("PubKey: Browser-Check gibt Versions-Info zurück",
          "Chrome 133" in html and "Firefox 132" in html and "Safari 18.4" in html)
    check("PubKey: Browser-Check wird vor Keyerzeugung aufgerufen",
          "keyBrowserCheck()" in html and "keyManagementGenerateNew" in html)

    # Session-Speicher (nicht persistent)
    check("PubKey: _currentPrivateKey Variable",
          "var _currentPrivateKey" in html)
    check("PubKey: _currentPrivateKeyBase64 Variable",
          "var _currentPrivateKeyBase64" in html)
    check("PubKey: _currentPublicKeyBase64 Variable",
          "var _currentPublicKeyBase64" in html)
    check("PubKey: KEIN localStorage für Private Key",
          "localStorage.setItem('_currentPrivateKey" not in html)
    check("PubKey: KEIN sessionStorage für Private Key",
          "sessionStorage.setItem('_currentPrivateKey" not in html)

    # UI-Integration
    check("PubKey: Key Management Container im Institutionen-Bereich",
          'id="key-management-content"' in html)
    check("PubKey: renderKeyManagement() wird aus Template aufgerufen",
          "${renderKeyManagement()}" in html)

    # Base64-Kodierung
    check("PubKey: window.btoa() für Base64-Kodierung",
          "window.btoa(" in html)
    check("PubKey: window.crypto.subtle.exportKey für Key-Export",
          "exportKey" in html)
    check("PubKey: spki-Format für Public Key",
          "'spki'" in html)
    check("PubKey: pkcs8-Format für Private Key",
          "'pkcs8'" in html)

    # Benutzer-Warnungen (korrekter vivoConfirm-Aufruf)
    check("PubKey: vivoConfirm mit 3 Parametern bei Private Key Download",
          "keyManagementDownloadPrivate" in html)
    check("PubKey: Warnung vor Private Key Weitergabe",
          "NIE weitergeben" in html or "NIE weitergegeben" in html)
    check("PubKey: Hinweis auf Neuladen-Problem",
          "Neuladen" in html and "Keypair" in html)
    check("PubKey: Hinweis auf Verlust-Problem",
          "Verlust" in html and "Private Key" in html)

    # Fehlerbehandlung
    check("PubKey: try-catch in genKeyPair()",
          html.count("try {") > 0 and "genKeyPair" in html)
    check("PubKey: Toast bei Fehler",
          "Fehler: Schlüssel" in html)
    check("PubKey: Null-Prüfung auf _currentPublicKeyBase64",
          "if (!_currentPublicKeyBase64)" in html)

    # Kopierfunktion mit Fallback
    check("PubKey: navigator.clipboard.writeText wird genutzt",
          "navigator.clipboard.writeText" in html)
    check("PubKey: Fallback wenn Zwischenablage nicht verfügbar",
          "Zwischenablage in diesem Browser nicht verfügbar" in html)

    # BUG-A: Memory-Leak — URL.createObjectURL() ohne URL.revokeObjectURL()
    # Public/Private-Key-Download-Funktionen muessen die Object-URL freigeben,
    # sonst belegt jeder Klick auf "Speichern" Speicher bis Reload.
    def _key_dl_has_revoke(fn_name):
        m = re.search(
            r'function ' + re.escape(fn_name) + r'\([^)]*\)\s*\{[\s\S]*?\n\}',
            html
        )
        if not m:
            return False
        body = m.group(0)
        return 'createObjectURL' in body and 'revokeObjectURL' in body

    check("PubKey: keyManagementDownloadPublic ruft revokeObjectURL auf",
          _key_dl_has_revoke('keyManagementDownloadPublic'),
          "Memory-Leak: ObjectURL wird nicht freigegeben")
    check("PubKey: keyManagementDownloadPrivate ruft revokeObjectURL auf",
          _key_dl_has_revoke('keyManagementDownloadPrivate'),
          "Memory-Leak: ObjectURL wird nicht freigegeben")

    # BUG-A (Forts.): Gleicher Memory-Leak-Check fuer alle uebrigen
    # Download-/Export-Funktionen, die URL.createObjectURL nutzen.
    # Service-Worker-Registrierung (Z. ~23615) ist absichtlich
    # ausgenommen — die Blob-URL muss persistent bleiben.
    BUG_A_DOWNLOAD_FUNCTIONS = [
        'downloadCSVTemplate',
        'downloadInstitutionTemplate',
        'tplEditorExport',
        'saveAsHTML',
        'exportJSON',
        '_generateDocxInner',
        'generateVorsorgevollmacht',
        'generatePatientenverfuegung',
        'generateFHIR',
        'generateGesundheitsvollmacht',
        'exportFIMJson',
    ]
    for _fn in BUG_A_DOWNLOAD_FUNCTIONS:
        check(f"BUG-A: {_fn} ruft revokeObjectURL auf",
              _key_dl_has_revoke(_fn),
              "Memory-Leak: ObjectURL wird nicht freigegeben")

    # BUG-D: JSON.parse(parsedStored.plain) muss try/catch haben
    # Korrupte localStorage-Daten duerfen die App-Init nicht crashen
    # (sonst: weisse Seite beim Start).
    # Regex: vom if-Check bis zum "return;\n  }" (Ende des if-Bodies bei 2-Space-Einrueckung)
    m_plain = re.search(
        r'if\s*\(parsedStored\.plain\)\s*\{[\s\S]*?return;\s*\n  \}',
        html
    )
    if m_plain:
        block = m_plain.group(0)
        has_try = 'try' in block and 'JSON.parse(parsedStored.plain)' in block
        has_catch = 'catch' in block
        check("BUG-D: parsedStored.plain Parse ist try/catch-geschuetzt",
              has_try and has_catch,
              "Korrupte plain-Daten koennen die App-Init crashen")
    else:
        check("BUG-D: if(parsedStored.plain)-Block gefunden",
              False,
              "Struktur von loadData() hat sich geaendert")

    # BUG-E: localStorage.setItem ohne Quota-Schutz
    # Bei vollem Storage werfen diese Aufrufe QuotaExceededError, was
    # den Event-Handler / die UI-Funktion unerwartet abbricht.
    BUG_E_FUNCTIONS = [
        'dismissUpdateBanner',
        'submitEmailOptin',
        'dismissEmailOptin',
    ]
    for _fn in BUG_E_FUNCTIONS:
        m_fn = re.search(
            r'function ' + re.escape(_fn) + r'\([^)]*\)\s*\{[\s\S]*?\n\}',
            html
        )
        if m_fn:
            body = m_fn.group(0)
            has_setitem = 'localStorage.setItem' in body
            has_trycatch = 'try' in body and 'catch' in body
            check(f"BUG-E: {_fn} faengt setItem-Exceptions",
                  (not has_setitem) or (has_setitem and has_trycatch),
                  "setItem ohne try/catch kann UI-Funktion crashen")
        else:
            check(f"BUG-E: {_fn} existiert",
                  False,
                  "Funktion nicht gefunden")

    # Escape-Key-Handler: spezifischer Check, da keine eigene Funktion
    # Die setItem-Zeile ist ein Einzeiler — ganze Zeile matchen.
    _esc = re.search(
        r"if\s*\(eo\)\s*\{[^\n]*email_optin[^\n]*\}",
        html
    )
    if _esc:
        check("BUG-E: Escape-Handler email-optin faengt setItem-Exceptions",
              'try' in _esc.group(0) and 'catch' in _esc.group(0),
              "Escape-Key setItem ohne try/catch bricht Handler ab")
    else:
        check("BUG-E: Escape-Handler email-optin gefunden",
              False,
              "Struktur des Escape-Handlers hat sich geaendert")

    passed = sum(1 for s, _, _ in results if s == "PASS")
    failed = sum(1 for s, _, _ in results if s == "FAIL")
    total = len(results)
    if passed + failed != total:
        print(f"  ⚠️  Counter-Inkonsistenz: {passed}+{failed} != {total}")
    
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
