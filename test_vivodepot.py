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
    check("BUG-05: Max 6 password-Felder", pw_fields <= 6, f"Gefunden: {pw_fields}")
    
    proton_refs = html.lower().count('protonmail') + html.lower().count('proton.me')
    check("BUG-06: Keine Proton-Referenzen", proton_refs == 0, f"Gefunden: {proton_refs}")
    
    steps_match = re.search(r'(?:const|var|let)\s+STEPS\s*=\s*\[([\s\S]*?)\];', html)
    if steps_match:
        steps_block = steps_match.group(1)
        emojis = re.findall(r"label:\s*'[^']*[\U00010000-\U0010ffff]", steps_block)
        check("BUG-07: Keine Emojis in STEPS", len(emojis) == 0, f"Gefunden: {len(emojis)}")
    
    save_fn = re.search(r'function saveAsHTML\(\)\s*\{([\s\S]*?)\n\}', html)
    if save_fn:
        check("BUG-08: saveAsHTML enthält hideAllOverlays", 'hideAllOverlays' in save_fn.group(1))
    
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
    check("localStorage Wrapper (_ls)", '_ls' in html and 'function()' in html)
    
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
