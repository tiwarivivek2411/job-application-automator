import subprocess
import time
import base64
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="instahyre.com"):
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

def apply_instahyre(target_count=30):
    print("==========================================================")
    print(f"INSTAHYRE 1-CLICK APPLY RUNNER (Target: {target_count} jobs)")
    print("==========================================================")

    applied_count = 0
    skipped_count = 0

    for step in range(1, target_count + 1):
        print(f"\n[{step}/{target_count}] Checking next opportunity...")

        # Find first unapplied 'View job »' button
        find_and_open_js = """
        (() => {
            const items = Array.from(document.querySelectorAll('.opportunity, [class*="opportunity"]'))
                .filter(el => el.innerText && el.innerText.includes('View job') && !el.innerText.includes('Applied'));
            
            if (items.length === 0) {
                // Try finding any 'View job' button directly
                const btn = Array.from(document.querySelectorAll('button, a'))
                    .find(b => b.innerText && b.innerText.trim().toLowerCase().includes('view job'));
                if (btn) {
                    btn.click();
                    return 'OPENED_FROM_BTN';
                }
                return 'NO_OPPORTUNITIES';
            }

            const first = items[0];
            const btn = Array.from(first.querySelectorAll('button, a'))
                .find(b => b.innerText && b.innerText.trim().toLowerCase().includes('view job'));
            if (btn) {
                btn.click();
                return 'OPENED';
            }
            return 'NO_BTN_IN_ITEM';
        })()
        """
        open_res = run_js(find_and_open_js)
        print(f"  Open modal: {open_res}")

        if "NO_" in open_res:
            print("  No more unapplied opportunities visible on this page.")
            break

        time.sleep(2.5)

        # Extract job info & click Apply
        apply_js = """
        (() => {
            const wrap = document.querySelector('.application-modal-wrap');
            if (!wrap) return 'NO_MODAL';

            const title = wrap.querySelector('h1, h2, h3, [class*="title"], [class*="role"]')?.innerText || 'Unknown Role';
            const company = wrap.querySelector('[class*="company"], [class*="employer"]')?.innerText || '';

            const applyBtn = Array.from(wrap.querySelectorAll('button'))
                .find(b => b.innerText.trim().toLowerCase() === 'apply');
            
            if (!applyBtn) {
                const alreadySent = Array.from(wrap.querySelectorAll('button, div, span'))
                    .some(e => e.innerText && e.innerText.includes('Application Sent'));
                if (alreadySent) return 'ALREADY_SENT:' + title;
                return 'NO_APPLY_BTN:' + title;
            }

            applyBtn.click();
            return 'CLICKED_APPLY:' + title + ' (' + company.trim() + ')';
        })()
        """
        app_res = run_js(apply_js)
        print(f"  Apply action: {app_res}")

        time.sleep(2.5)

        # Close modal
        close_js = """
        (() => {
            const closeBtn = document.querySelector('.application-modal-close');
            if (closeBtn) {
                closeBtn.click();
                return 'CLOSED';
            }
            return 'NO_CLOSE_BTN';
        })()
        """
        run_js(close_js)
        time.sleep(1.5)

        if "CLICKED_APPLY:" in app_res:
            applied_count += 1
            print(f"  --> [SUCCESS] Application Sent! (Total on Instahyre: {applied_count})")
        else:
            skipped_count += 1
            print(f"  --> [SKIPPED]: {app_res}")

        time.sleep(2.0)

    print("\n==========================================================")
    print("INSTAHYRE RUN COMPLETED!")
    print(f"Newly Applied: {applied_count}")
    print(f"Skipped / Already Applied: {skipped_count}")
    print("==========================================================")

if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    apply_instahyre(count)
