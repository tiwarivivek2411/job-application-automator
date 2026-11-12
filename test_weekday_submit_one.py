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
click_js = """
(() => {
    const btns = Array.from(document.querySelectorAll('button'))
        .filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'fast apply');
    if (btns.length === 0) return 'NO_BUTTONS';
    btns[0].click();
    return 'CLICKED_FAST_APPLY';
})()
"""
print("CLICK:", run_js(click_js)[0])
time.sleep(2.5)

# 2. Click Submit Application
submit_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
    if (!modal) return 'NO_MODAL';

    const submitBtn = Array.from(modal.querySelectorAll('button'))
        .find(b => b.innerText.trim().toLowerCase().includes('submit application'));
    if (!submitBtn) return 'NO_SUBMIT_BTN';
    if (submitBtn.disabled) return 'DISABLED';

    submitBtn.click();
    return 'SUBMIT_CLICKED';
})()
"""
print("SUBMIT:", run_js(submit_js)[0])
time.sleep(3.0)

# 3. Check status after submit
check_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
    if (!modal) return 'MODAL_CLOSED';
    return 'MODAL_STILL_OPEN: ' + modal.innerText.slice(0, 150).replace(/\n/g, ' ');
})()
"""
print("AFTER SUBMIT:", run_js(check_js)[0])

# 4. Close if still open
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
    document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
    return 'ESCAPED';
})()
"""
print("CLOSE:", run_js(close_js)[0])
