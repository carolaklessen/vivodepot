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
        required_overlays = ['welcome-overlay', 'return-overlay', 'crypto-overlay']
        for oid in required_overlays:
            check(f"BUG-02: hideAllOverlays enthält '{oid}'", oid in hide_fn)
    else:
        check("BUG-02: hideAllOverlays existiert", False)
    
    check("BUG-03: enterApp() existiert", 'function enterApp' in html)
    
    pw_fields = len(re.findall(r'type=["\']password["\']', html))
    check("BUG-05: Max 7 password-Felder", pw_fields <= 7, f"Gefunden: {pw_fields}")
    
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
    check("Journey: enterApp ruft safeRender", "function enterApp" in html and "safeRender" in html)
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
    print("\n=== 11. FOKUS-WIZARD (beta.4) ===")
    # ═══════════════════════════════════════
    check("Fokus: FOCUSED_RENDERERS definiert", "const FOCUSED_RENDERERS = {" in html)
    check("Fokus: health_start Renderer", "health_start:" in html)
    check("Fokus: health_gesundheit Renderer", "health_gesundheit:" in html)
    check("Fokus: emergency_start Renderer", "emergency_start:" in html)
    check("Fokus: emergency_kontakte Renderer", "emergency_kontakte:" in html)
    check("Fokus: emergency_gesundheit Renderer", "emergency_gesundheit:" in html)
    check("Fokus: legal_start Renderer", "legal_start:" in html)
    check("Fokus: family_start Renderer", "family_start:" in html)
    check("Fokus: family_kontakte Renderer", "family_kontakte:" in html)
    check("Fokus: renderStep nutzt FOCUSED_RENDERERS", "FOCUSED_RENDERERS[focusKey]" in html)
    check("Fokus: _activeGoal wird gesetzt", "window._activeGoal = selectedGoal" in html)
    check("Fokus: _activeGoal wird geleert", "window._activeGoal = null" in html)
    check("Fokus: nextStep überspringt irrelevante", "_goalRelevant[STEPS[next].id]" in html)
    check("Fokus: prevStep überspringt irrelevante", "_goalRelevant[STEPS[prev].id]" in html)
    check("Fokus: startet bei Schritt 0", "currentStep = 0;" in html)

    # ═══════════════════════════════════════
    print("\n=== 12. MOBILE (beta.4) ===")
    # ═══════════════════════════════════════
    check("Mobile: Bottom-Nav vorhanden", 'class="mobile-nav"' in html)
    check("Mobile: mobileNavUpdate()", "function mobileNavUpdate" in html)
    check("Mobile: Safe-area-inset Bottom-Nav", "safe-area-inset-bottom" in html)
    check("Mobile: Viewport-fit cover", "viewport-fit=cover" in html)
    check("Mobile: Font-size 16px (kein Auto-Zoom)", "font-size: 16px !important" in html)
    check("Mobile: Touch-action manipulation", "touch-action: manipulation" in html)
    check("Mobile: Tap-highlight entfernt", "tap-highlight-color: transparent" in html)
    check("Mobile: Share API", "async function shareApp" in html)
    check("Mobile: Kamera capture", 'capture="environment"' in html)
    check("Mobile: Telefonbuch-Import", "async function importFromPhone" in html)
    check("Mobile: Keyboard-fix visualViewport", "visualViewport" in html)
    check("Mobile: Notfall-Button über Nav", "74px" in html)

    # ═══════════════════════════════════════
    print("\n=== 13. UX & FELDER (beta.4) ===")
    # ═══════════════════════════════════════
    check("UX: Pflegekinder-Felder vorhanden", "field('pflegekinder'" in html)
    check("UX: feedback@vivodepot.de", "feedback@vivodepot.de" in html)
    check("UX: Telefonbuch-Anleitung bei fehlendem API", "Direkter Telefonbuch-Zugriff" in html)
    check("UX: PWA-Logo 512x512", "512x512" in html)
    check("UX: SVG Favicon (DuckDuckGo-kompatibel)", "image/svg+xml" in html)
    check("UX: Fokus-Wizard im More-Menu", "showGoalWizard(); closeMoreMenu()" in html)
    check("UX: Fokus-Wizard in Mobile Bottom-Nav", 'showGoalWizard()' in html and 'mobile-nav-center' in html)

    # Export-Fokus
    check("Fokus: health_exportStep", 'health_exportStep:' in html)
    check("Fokus: emergency_exportStep", 'emergency_exportStep:' in html)
    check("Fokus: legal_exportStep", 'legal_exportStep:' in html)
    check("Fokus: family_exportStep", 'family_exportStep:' in html)
    check("Fokus: health_dokumente", 'health_dokumente:' in html)
    check("Fokus: emergency_dokumente", 'emergency_dokumente:' in html)
    check("Fokus: legal_assistenten", 'legal_assistenten:' in html)
    check("Fokus: family_assistenten", 'family_assistenten:' in html)
    check("Fokus: renderUploadedFilesByCategories", 'renderUploadedFilesByCategories' in html)
    check("Fokus: mobileNavNext ruft nextStep auf", "function mobileNavNext" in html and "nextStep()" in html.split("function mobileNavNext")[1][:30])
    check("Fokus: mobileNavPrev ruft prevStep auf", "function mobileNavPrev" in html and "prevStep()" in html.split("function mobileNavPrev")[1][:30])
    check("Fokus: Mobile zeigt Fokus-Schrittzahl", "relevant.length" in html)
    check("Fokus: Sidebar Early-Return in goalMode", "if (goalMode && goalRelevant) {" in html and "sb.innerHTML = html;\n    return;" in html)
    check("Fokus: Focus-Badge in Topbar", "focus-badge" in html)
    check("Fokus: updateFocusBadge()", "function updateFocusBadge" in html)

    # ═══════════════════════════════════════
    print("\n=== ZUSAMMENFASSUNG ===")
    # ═══════════════════════════════════════
    
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
