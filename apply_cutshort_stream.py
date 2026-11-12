import subprocess
import time
import json
import sys

def exec_js_in_tab(tab_idx, js_code):
    clean_js = js_code.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    apple_script = f"""tell application "Google Chrome"
    tell tab {tab_idx} of window 1
        execute javascript "{clean_js}"
    end tell
end tell"""
    res = subprocess.run(["osascript"], input=apple_script, text=True, capture_output=True)
    if res.returncode != 0:
        return None, res.stderr.strip()
    return res.stdout.strip(), None

def get_cutshort_tab():
    script = """tell application "Google Chrome"
    set i to 1
    repeat with t in tabs of window 1
        if URL of t contains "cutshort.io/profile/all-jobs" then
            return i
        end if
        set i to i + 1
    end repeat
    return 0
end tell"""
    res = subprocess.run(["osascript"], input=script, text=True, capture_output=True)
    out = res.stdout.strip()
    if out and out.isdigit():
        return int(out)
    return 0

def apply_one_job(tab_idx):
    # Step 1: Check available jobs and get first 'Apply now' button info
    get_job_js = """(() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText && b.innerText.trim() === 'Apply now');
        if (btns.length === 0) return JSON.stringify({status: 'NO_JOBS'});
        const b = btns[0];
        let el = b;
        for (let i = 0; i < 6; i++) {
            if (el.parentElement) el = el.parentElement;
        }
        const titleEl = el.querySelector('h2, h3, [class*=title], [class*=role]');
        const title = titleEl ? titleEl.innerText : 'Unknown Title';
        const snippet = el.innerText.substring(0, 150).replace(/\\n/g, ' | ');
        return JSON.stringify({status: 'FOUND', title: title, snippet: snippet});
    })()"""
    
    out, err = exec_js_in_tab(tab_idx, get_job_js)
    if not out or 'NO_JOBS' in out:
        # Try reloading to fetch more
        print("  [Cutshort] No Apply now buttons in current view. Reloading page...")
        exec_js_in_tab(tab_idx, "window.location.reload();")
        time.sleep(4.0)
        out, err = exec_js_in_tab(tab_idx, get_job_js)
        if not out or 'NO_JOBS' in out:
            return False, "No jobs available with 'Apply now'"
    
    try:
        job_info = json.loads(out)
    except Exception as ex:
        return False, f"Failed to parse job info ({ex}): {out}"
        
    title = job_info.get("title", "Unknown Role")
    print(f"\n[Cutshort] Preparing to apply for: '{title}'")
    print(f"  Summary: {job_info.get('snippet', '')[:100]}")
    
    # Step 2: Click 'Apply now' on first button
    click_apply_js = """(() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText && b.innerText.trim() === 'Apply now');
        if (btns.length === 0) return 'NO_BTN';
        btns[0].click();
        return 'CLICKED';
    })()"""
    
    out, err = exec_js_in_tab(tab_idx, click_apply_js)
    if out != "CLICKED":
        return False, f"Failed to click Apply now: {out}"
        
    time.sleep(1.5)
    
    # Step 3: Handle potential 'verify data' modal or check for Send modal
    check_modal_js = """(() => {
        const skipDiv = Array.from(document.querySelectorAll('div, button, a, span')).find(d => d.innerText && d.innerText.trim() === 'Apply without completing profile');
        if (skipDiv) {
            skipDiv.click();
            return 'CLICKED_SKIP';
        }
        const modal = document.querySelector('.modal__wrapper');
        if (modal) return 'MODAL_READY';
        return 'NO_MODAL';
    })()"""
    
    out, _ = exec_js_in_tab(tab_idx, check_modal_js)
    if out == "CLICKED_SKIP":
        time.sleep(1.0)
        
    # Step 4: Focus Send button and press Space
    send_script = f"""tell application "Google Chrome"
    activate
    set active tab index of window 1 to {tab_idx}
    tell tab {tab_idx} of window 1
        execute javascript "(() => {{ document.querySelectorAll('.sc-cd69e1df-1').forEach(el => el.style.pointerEvents = 'none'); const btn = document.querySelector('.modal__wrapper button'); if (btn) {{ btn.focus(); return 'FOCUSED'; }} return 'NO_SEND_BTN'; }})()"
    end tell
end tell
delay 0.3
tell application "System Events"
    keystroke space
end tell"""
    
    subprocess.run(["osascript"], input=send_script, text=True, capture_output=True)
    time.sleep(2.0)
    
    # Step 5: Verify submission
    verify_js = """(() => {
        const modal = document.querySelector('.modal__wrapper');
        const conv = Array.from(document.querySelectorAll('*')).some(el => el.innerText && el.innerText.includes('View conversation'));
        return JSON.stringify({hasModal: !!modal, hasConv: conv});
    })()"""
    
    out, _ = exec_js_in_tab(tab_idx, verify_js)
    try:
        ver_info = json.loads(out)
        if not ver_info.get("hasModal") or ver_info.get("hasConv"):
            return True, f"Successfully applied for '{title}'!"
        else:
            return False, f"Modal still open after Send for '{title}'"
    except Exception as e:
        return False, f"Verification parse error: {e}"

def main():
    tab_idx = get_cutshort_tab()
    if not tab_idx:
        print("Error: Cutshort tab not found!")
        sys.exit(1)
        
    print(f"Found Cutshort on Tab {tab_idx}.")
    max_apps = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    applied_count = 0
    
    for i in range(max_apps):
        success, msg = apply_one_job(tab_idx)
        print(f"[{i+1}/{max_apps}] {msg}")
        if success:
            applied_count += 1
            time.sleep(2.0)
        else:
            if "No jobs available" in msg:
                print("All available Cutshort jobs applied!")
                break
            time.sleep(3.0)
            
    print(f"\nDone! Successfully applied to {applied_count} jobs on Cutshort.")

if __name__ == "__main__":
    main()
