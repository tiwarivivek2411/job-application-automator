import subprocess, time

# 1. Fix phone number and country
phone_js = """
(function() {
    var phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.focus();
        phoneInput.value = '8920952855';
        phoneInput.dispatchEvent(new Event('input', { bubbles: true }));
        phoneInput.dispatchEvent(new Event('change', { bubbles: true }));
    }
    
    // Country to India
    var search = document.getElementById('iti-0__search-input') || document.querySelector('.iti__search-input');
    if (search) {
        search.focus();
        search.value = 'India';
        search.dispatchEvent(new Event('input', { bubbles: true }));
    }
    var ind = Array.from(document.querySelectorAll('.iti__country')).find(el => el.innerText.includes('India') && el.innerText.includes('+91'));
    if (ind) {
        ind.click();
    }
    return 'PHONE_FIXED';
})()
"""

cleaned_phone = ' '.join([l.strip() for l in phone_js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript_phone = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{cleaned_phone}")
    end tell
end tell
'''
p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, _ = p.communicate(ascript_phone)
print("PHONE RESULT:", out.strip())

# 2. Fix the 4 remaining questions
# question_64239204 (stack) -> option-1 ("Java / Spring Boot") or option-0 ("Node.js...")
# question_64239206 (ai tools) -> option-0 ("Use daily")
# question_65143957 (mentored) -> option-0 ("Yes, both mentoring and leading cross-team projects")
# question_64239209 (notice period) -> option-1 ("Less than 15 days") or option-0 ("Immediate Joiner")

questions_to_fix = [
    ("question_64239204", 1), # Java / Spring Boot
    ("question_64239206", 0), # Use daily
    ("question_65143957", 0), # Yes, both mentoring
    ("question_64239209", 1)  # Less than 15 days
]

for qid, opt_idx in questions_to_fix:
    fix_js = f"""
    (function() {{
        var inp = document.getElementById('{qid}');
        if (!inp) return 'NO_INP: ' + '{qid}';
        var control = inp.closest('.select__control') || inp.parentElement;
        if (control) {{
            control.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            control.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            control.click();
        }}
        
        var opt = document.getElementById('react-select-{qid}-option-{opt_idx}');
        if (!opt) {{
            var lb = document.getElementById('react-select-{qid}-listbox');
            if (lb) {{
                var allOpts = lb.querySelectorAll('.select__option');
                if (allOpts.length > {opt_idx}) opt = allOpts[{opt_idx}];
            }}
        }}
        if (opt) {{
            opt.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
            opt.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
            opt.click();
            return 'SUCCESS: ' + opt.innerText.trim();
        }}
        return 'OPT_NOT_FOUND for ' + '{qid}';
    }})()
    """
    cleaned_fix = ' '.join([l.strip() for l in fix_js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
    ascript_fix = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is 33684133)
            return (execute javascript "{cleaned_fix}")
        end tell
    end tell
    '''
    p_fix = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_fix, _ = p_fix.communicate(ascript_fix)
    print(f"[{qid}] -> {out_fix.strip()}")
    time.sleep(0.3)

print("All remaining questions fixed!")
