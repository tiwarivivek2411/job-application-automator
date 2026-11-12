import subprocess
import time
import base64
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="jobs.weekday.works"):
    b64 = base64.b64encode(js_code.encode('utf-8')).decode('ascii')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "{filter_url}" then
                    return (execute t javascript "eval(atob('{b64}'))")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    out, _ = exec_ascript(ascript)
    return out

def apply_weekday(target_count=30):
    print("==========================================================")
    print(f"WEEKDAY FAST APPLY RUNNER (Target: {target_count} jobs)")
    print("==========================================================")

    applied_count = 0
    skipped_count = 0

    for step in range(1, target_count + 1):
        print(f"\n[{step}/{target_count}] Looking for next Fast Apply role...")

        # Find first visible Fast Apply button
        click_fast_apply_js = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'))
                .filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'fast apply');
            if (btns.length === 0) {
                window.scrollBy(0, 600);
                return 'SCROLLED';
            }
            btns[0].click();
            return 'CLICKED';
        })()
        """
        c_res = run_js(click_fast_apply_js)
        print(f"  Fast Apply button: {c_res}")

        if c_res == "SCROLLED":
            time.sleep(2.0)
            c_res = run_js(click_fast_apply_js)
            if c_res == "SCROLLED":
                print("  No more Fast Apply buttons available.")
                break

        time.sleep(2.5)

        # In modal, check & submit
        submit_modal_js = """
        (() => {
            const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
            if (!modal) return 'NO_MODAL';

            const title = modal.querySelector('h1, h2, h3, [class*="title"], [class*="Role"]')?.innerText || 'Unknown Position';
            const company = modal.querySelector('[class*="Company"], [class*="employer"]')?.innerText || '';

            const alreadyApplied = Array.from(modal.querySelectorAll('button, div, span'))
                .some(e => e.innerText && e.innerText.toLowerCase().includes('already applied'));
            if (alreadyApplied) return 'ALREADY_APPLIED:' + title;

            const submitBtn = Array.from(modal.querySelectorAll('button'))
                .find(b => b.innerText.trim().toLowerCase().includes('submit application'));
            if (!submitBtn) return 'NO_SUBMIT_BTN:' + title;
            if (submitBtn.disabled) return 'DISABLED:' + title;

            submitBtn.click();
            return 'SUBMITTED:' + title + ' (' + company.trim() + ')';
        })()
        """
        sub_res = run_js(submit_modal_js)
        print(f"  Submit result: {sub_res}")

        time.sleep(3.0)

        # Close modal
        close_modal_js = """
        (() => {
            const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
            if (!modal) return 'NO_MODAL';
            const closeBtn = Array.from(modal.querySelectorAll('button'))
                .find(b => b.innerText.trim().toLowerCase() === 'close' || b.getAttribute('aria-label') === 'close');
            if (closeBtn) {
                closeBtn.click();
                return 'CLOSED';
            }
            // Press Escape
            document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
            return 'ESCAPE';
        })()
        """
        run_js(close_modal_js)
        time.sleep(1.5)

        if "SUBMITTED:" in sub_res:
            applied_count += 1
            print(f"  --> [SUCCESS] Applied on Weekday! (Total: {applied_count})")
        else:
            skipped_count += 1
            print(f"  --> [SKIPPED]: {sub_res}")

        time.sleep(2.0)

    print("\n==========================================================")
    print("WEEKDAY RUN COMPLETED!")
    print(f"Newly Applied: {applied_count}")
    print(f"Skipped / Already Applied: {skipped_count}")
    print("==========================================================")

if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    apply_weekday(count)
