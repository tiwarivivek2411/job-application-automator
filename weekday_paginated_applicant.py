import base64
import subprocess
import time
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="weekday.works"):
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
    out, err = exec_ascript(ascript)
    return out

def apply_weekday_paginated(target_jobs=40):
    print("==========================================================")
    print(f"WEEKDAY PAGINATED FAST APPLY (Target: {target_jobs} jobs)")
    print("==========================================================")

    applied_count = 0
    skipped_count = 0
    page_num = 2  # Current page

    while applied_count < target_jobs:
        print(f"\n--- Checking Page {page_num} for Fast Apply buttons ---")

        # Check how many Fast Apply buttons are currently on this page
        count_js = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'))
                .filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'fast apply');
            return '' + btns.length;
        })()
        """
        c_str = run_js(count_js)
        avail = int(c_str) if c_str.isdigit() else 0
        print(f"Fast Apply buttons available on Page {page_num}: {avail}")

        if avail == 0:
            # Click Next Page
            click_next_js = """
            (() => {
                const nextBtn = Array.from(document.querySelectorAll('button'))
                    .find(b => b.innerText && b.innerText.trim().toLowerCase() === 'next');
                if (nextBtn && !nextBtn.disabled) {
                    nextBtn.click();
                    return 'CLICKED_NEXT';
                }
                return 'NO_NEXT';
            })()
            """
            next_res = run_js(click_next_js)
            print(f"Navigation: {next_res}")
            if next_res == "CLICKED_NEXT":
                page_num += 1
                print(f"Advancing to Page {page_num}, waiting 4s for render...")
                time.sleep(4.0)
                continue
            else:
                print("No more pages available on Weekday.")
                break

        # Process first unapplied Fast Apply button on page
        # Scroll button into view to ensure it is rendered and clickable
        click_fast_js = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'))
                .filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'fast apply');
            if (btns.length === 0) return 'NO_BUTTONS';
            
            const btn = btns[0];
            btn.scrollIntoView({block: 'center'});
            btn.click();
            return 'OPENED_MODAL';
        })()
        """
        click_res = run_js(click_fast_js)
        print(f"[{applied_count + 1}/{target_jobs}] Click Fast Apply: {click_res}")

        if click_res != "OPENED_MODAL":
            time.sleep(2.0)
            continue

        time.sleep(2.5)

        # In modal: read title, company, match, and click Submit application
        submit_js = """
        (() => {
            const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
            if (!modal) return 'NO_MODAL';

            const title = modal.querySelector('h1, h2, h3, [class*="title"], [class*="Role"]')?.innerText || 'Position';
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
        sub_res = run_js(submit_js)
        print(f"  Submit: {sub_res}")

        time.sleep(2.0)

        # Close modal
        close_js = """
        (() => {
            const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
            if (!modal) return 'MODAL_CLOSED';
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
        run_js(close_js)
        time.sleep(1.0)

        if "SUBMITTED:" in sub_res:
            applied_count += 1
            print(f"  --> [SUCCESS] Submitted application on Weekday! (Batch total: {applied_count})")
        else:
            skipped_count += 1
            print(f"  --> [SKIPPED]: {sub_res}")

        time.sleep(1.5)

    print("\n==========================================================")
    print("WEEKDAY RUN COMPLETE")
    print(f"Total Applied: {applied_count}")
    print(f"Total Skipped: {skipped_count}")
    print("==========================================================")

if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    apply_weekday_paginated(count)
