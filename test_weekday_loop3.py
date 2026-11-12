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

print("--- TESTING 3 CONSECUTIVE APPLICATIONS ON WEEKDAY ---")

for i in range(1, 4):
    print(f"\n[Job {i}/3]")
    # 1. Find and click Fast Apply
    click_js = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button'))
            .filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'fast apply');
        if (btns.length === 0) return 'NO_BUTTONS';
        btns[0].click();
        return 'CLICKED_FAST_APPLY';
    })()
    """
    res = run_js(click_js)[0]
    print(f"  1. Open: {res}")
    time.sleep(2.0)

    # 2. In modal, get title and click Submit
    sub_js = """
    (() => {
        const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
        if (!modal) return 'NO_MODAL';
        
        const title = modal.querySelector('h1, h2, h3, [class*="title"], [class*="Role"]')?.innerText || 'Role';
        const subBtn = Array.from(modal.querySelectorAll('button'))
            .find(b => b.innerText.trim().toLowerCase().includes('submit application'));
        if (!subBtn) {
            const already = Array.from(modal.querySelectorAll('button, div, span'))
                .some(e => e.innerText && e.innerText.toLowerCase().includes('already applied'));
            if (already) return 'ALREADY_APPLIED: ' + title;
            return 'NO_SUBMIT: ' + title;
        }
        subBtn.click();
        return 'SUBMITTED: ' + title;
    })()
    """
    res = run_js(sub_js)[0]
    print(f"  2. Submit: {res}")
    time.sleep(2.0)

    # 3. Reload page to load fresh card
    run_js('window.location.reload()')
    print("  3. Page reloaded, waiting 3.5s...")
    time.sleep(3.5)

print("\n--- TEST FINISHED ---")
