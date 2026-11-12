import subprocess, base64, time, json

def run_js(url_sub, js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        repeat with t in tabs of window 1
            if (URL of t as string) contains "{url_sub}" then
                return (execute t javascript "try {{ eval(atob('{b64}')); }} catch(e) {{ 'ERR: ' + e.message; }}")
            end if
        end repeat
        return "NO_TAB"
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

# 1. Fill Text Fields
fill_text_js = r'''
(() => {
    function setVal(id, val) {
        const el = document.getElementById(id);
        if (el) {
            el.focus();
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }
        return false;
    }

    const r = {};
    r.reside = setVal('question_20624689004', 'Bengaluru, Karnataka, India');
    r.salary = setVal('question_20624690004', '₹42,00,000 (42 LPA)');
    r.source = setVal('question_20624692004', 'Greenhouse / LinkedIn');

    return JSON.stringify(r);
})()
'''
print("Text fields:", run_js('zetaglobal', fill_text_js))
time.sleep(0.5)

# 2. Inspect all React Select input containers on the form
inspect_react_selects = r'''
(() => {
    const labels = Array.from(document.querySelectorAll('label')).map(l => {
        const parent = l.closest('div');
        const select = parent ? parent.querySelector('.select__control, [class*="select"]') : null;
        const input = parent ? parent.querySelector('input') : null;
        return {
            text: l.innerText.trim(),
            htmlFor: l.htmlFor,
            inputId: input ? input.id : null,
            hasSelect: !!select
        };
    });
    return JSON.stringify(labels.filter(l => l.hasSelect));
})()
'''
print("Dropdowns:", run_js('zetaglobal', inspect_react_selects))
