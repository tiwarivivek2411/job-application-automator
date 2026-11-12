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

click_js = """
(() => {
    const btns = Array.from(document.querySelectorAll('button'))
        .filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'fast apply');
    if (btns.length === 0) return 'NO_BUTTONS';
    btns[0].click();
    return 'CLICKED_FAST_APPLY';
})()
"""
out, _ = run_js(click_js)
print("CLICK:", out)
time.sleep(2.5)

inspect_js = """
(() => {
    const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
    if (!modal) return 'NO_MODAL';
    const text = modal.innerText.slice(0, 300);
    const buttons = Array.from(modal.querySelectorAll('button')).map(b => b.innerText.trim());
    return JSON.stringify({text, buttons});
})()
"""
out, _ = run_js(inspect_js)
print("MODAL:", out)

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
out, _ = run_js(close_js)
print("CLOSE:", out)
