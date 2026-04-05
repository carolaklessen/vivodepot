#!/usr/bin/env python3
"""
Notfallmappe-Assistent — Regressions-Testscript
================================================
Prüft eine HTML-Datei auf bekannte Bugs und Feature-Vollständigkeit.

Verwendung:
  python3 test_notfallmappe.py Notfallmappe_Assistent.html

Dieses Script nach JEDER Änderung laufen lassen.
Ergebnis muss 0 FAIL sein, bevor die Datei als Baseline akzeptiert wird.
"""

import re, sys, subprocess, tempfile, os

def main():
    if len(sys.argv) < 2:
        print("Verwendung: python3 test_notfallmappe.py <datei.html>")
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
        r = subprocess.run(['node', '--check', fname], capture_output=True, text=True)
        ok = r.returncode == 0
        if not ok:
            all_syntax_ok = False
        check(f"Script {i} Syntax", ok, r.stderr[:100] if not ok else "")
        os.unlink(fname)
    
    # ═══════════════════════════════════════
    print("\n=== 2. KRITISCHE BUGS (historisch) ===")
    # ═══════════════════════════════════════
    
    # BUG-01: Welcome-Overlay muss sichtbar per default sein
    wo_match = re.search(r'id="welcome-overlay"[^>]*style="([^"]*)"', html)
    if wo_match:
        check("BUG-01: Welcome-Overlay default sichtbar", 
              'flex' in wo_match.group(1),
              f"Aktuell: style='{wo_match.group(1)}'")
    else:
        check("BUG-01: Welcome-Overlay hat inline-style", False, "Kein style-Attribut gefunden")
    
    # BUG-02: hideAllOverlays muss alle Overlays abdecken
    if 'hideAllOverlays' in html:
        hide_fn_start = html.find('function hideAllOverlays')
        hide_fn_end = html.find('\n}', hide_fn_start) + 2
        hide_fn = html[hide_fn_start:hide_fn_end]
        overlay_ids = re.findall(r'id="([^"]*overlay[^"]*)"', html)
        for oid in overlay_ids:
            if 'crypto' in oid:
                continue  # crypto-overlay hat eigenes Management
            check(f"BUG-02: hideAllOverlays enthält '{oid}'", oid in hide_fn)
    else:
        check("BUG-02: hideAllOverlays existiert", False)
    
    # BUG-03: enterApp muss existieren
    check("BUG-03: enterApp() existiert", 'function enterApp' in html)
    
    # BUG-05: Keine password-type Felder AUSSER Crypto-Modal (set-pw-input, set-pw-confirm, crypto-pw)
    pw_fields = len(re.findall(r"type=['\"]password['\"]", html))
    check("BUG-05: Max 4 password-Felder (Crypto + Angehörige)", pw_fields <= 4, f"Gefunden: {pw_fields}")
    
    # BUG-06: Keine Provider-spezifischen Referenzen
    proton_refs = html.count('Proton')
    check("BUG-06: Keine Proton-Referenzen", proton_refs == 0, f"Gefunden: {proton_refs}")
    
    # BUG-07: Keine Emojis in STEPS-Labels
    steps_match = re.search(r'const\s+STEPS\s*=\s*\[', html)
    if steps_match:
        steps_end = html.find('];', steps_match.start())
        steps_text = html[steps_match.start():steps_end]
        emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]')
        emojis = emoji_pattern.findall(steps_text)
        check("BUG-07: Keine Emojis in STEPS", len(emojis) == 0, f"Gefunden: {len(emojis)}")
    
    # BUG-08: saveAsHTML Init-Template enthält hideAllOverlays
    if 'saveAsHTML' in html:
        save_start = html.find('function saveAsHTML')
        save_end = html.find('\nfunction ', save_start + 20)
        if save_end == -1:
            save_end = save_start + 5000
        save_fn = html[save_start:save_end]
        check("BUG-08: saveAsHTML enthält hideAllOverlays", 'hideAllOverlays' in save_fn)
    
    # BUG-09: Init-Block ruft hideAllOverlays auf
    init_match = re.search(r'// ═+\s*\n\s*// INIT', html)
    if init_match:
        init_block = html[init_match.start():init_match.start()+3000]
        check("BUG-09: Init ruft hideAllOverlays auf", 'hideAllOverlays' in init_block)
    
    # iOS Safari: kein bare 'export:' als Object-Key
    # Suche nach export: das NICHT Teil von exportStep: ist
    bare_export = re.findall(r"['\"]?export['\"]?\s*:", html)
    export_step = re.findall(r"exportStep\s*:", html)
    check("iOS: Kein bare 'export:' Key", 
          len(bare_export) <= len(export_step),
          f"export: {len(bare_export)}, exportStep: {len(export_step)}")
    
    # ═══════════════════════════════════════
    print("\n=== 3. STEPS & RENDERER ===")
    # ═══════════════════════════════════════
    
    steps = re.findall(r"\{[^}]*id:\s*'(\w+)'", html)
    renderers = re.findall(r"(\w+)\s*:\s*\(\)\s*=>", html)
    
    # Die 17 Kern-Steps die einen Renderer haben müssen
    required_steps = [
        'start', 'kontakte', 'infokontakte', 'finanzen', 'versich',
        'immobilien', 'testament', 'vertraege', 'gesundheit', 'haustiere',
        'pflege', 'digital', 'persoenliches', 'bestattung', 'dokumente',
        'erinnerung', 'exportStep'
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
        'importData': 'function importData',  # async oder nicht
        'renderStep': 'function renderStep',
        'renderSidebar': 'function renderSidebar',
        'generatePDF': 'function generatePDF',
        'toast': 'function toast',
        'get (Datenzugriff)': 'function get(',
        'set (Datenzugriff)': 'function set(',
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
    check("Checklist Export", 'generateChecklist' in html or 'Checkliste' in html)
    check("jsPDF geladen", 'jspdf' in html.lower())
    check("docx geladen", 'docx@' in html)
    
    # ═══════════════════════════════════════
    print("\n=== 7. ROBUSTHEIT ===")
    # ═══════════════════════════════════════
    
    check("window.onerror Handler", 'window.onerror' in html)
    check("localStorage Wrapper (_ls)", '_ls' in html and 'function()' in html)
    
    # ═══════════════════════════════════════
    print("\n=== 8. PROFIL-SYSTEM ===")
    # ═══════════════════════════════════════
    
    check("Profil: switchToProfile()", 'function switchToProfile' in html or 'async function switchToProfile' in html)
    check("Profil: addNewProfile()", 'function addNewProfile' in html)
    check("Profil: getProfileManifest()", 'function getProfileManifest' in html)
    check("Profil: updateProfileButton()", 'function updateProfileButton' in html)
    check("Profil: Dropdown UI", 'profile-dropdown' in html)
    check("Profil: STORE_KEY ist let (nicht const)", 'let STORE_KEY' in html)
    check("Profil: setActiveProfile()", 'function setActiveProfile' in html)
    
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
