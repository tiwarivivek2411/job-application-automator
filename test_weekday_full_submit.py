import base64, subprocess, time

def run_js(js_code):
    b64 = base64.b64encode(js_code.encode('utf-8')).decode('ascii')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "weekday.works" then
                    return (execute t javascript "eval(atob('{b64}'))")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=ascript.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

# 1. Click Fast Apply
open_js = """
(() => {
    const btns = Array.from(document.querySelectorAll('button'))
        .filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'fast apply');
    if (btns.length === 0) return 'NO_BUTTONS';
    btns[0].click();
    return 'CLICKED_OPEN';
})()
"""
print("1. OPEN:", run_js(open_js)[0])
time.sleep(2.5)

# 2. Click Submit Application
click_sub_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
    if (!modal) return 'NO_MODAL';
    const subBtn = Array.from(modal.querySelectorAll('button'))
        .find(b => b.innerText.trim().toLowerCase() === 'submit application');
    if (!subBtn) return 'NO_SUBMIT';
    subBtn.click();
    return 'SUBMIT_CLICKED';
})()
"""
print("2. SUBMIT:", run_js(click_sub_js)[0])

# 3. Wait and inspect every second for 6 seconds
for s in range(1, 6):
    time.sleep(1.0)
    inspect_js = f"""
    (() => {{
        const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
        if (!modal) return 'MODAL_GONE';
        const btns = Array.from(modal.querySelectorAll('button')).map(b => b.innerText.trim());
        const text = modal.innerText.replace(/\\n/g, ' ').slice(0, 120);
        return 'T+{s}: text=' + text + ' | btns=' + JSON.stringify(btns);
    }})()
    """
    print(run_js(inspect_js)[0])

# 4. Close if open
close_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
    if (!modal) return 'NO_MODAL';
    const closeBtn = Array.from(modal.querySelectorAll('button'))
        .find(b => b.innerText.trim().toLowerCase() === 'close' || b.getAttribute('aria-label') === 'close');
    if (closeBtn) {
        closeBtn.click();
        return 'CLOSED';
    }
    return 'NO_CLOSE';
})()
"""
print("4. CLOSE:", run_js(close_js)[0])
