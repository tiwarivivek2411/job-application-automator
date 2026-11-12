import subprocess
import time
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code):
    escaped = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "jobs.ascendion.com" then
                    return (execute t javascript "{escaped}")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    out, _ = exec_ascript(ascript)
    return out

def set_url(new_url):
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "jobs.ascendion.com" then
                    tell t to set URL to "{new_url}"
                    return "NAVIGATED"
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    out, _ = exec_ascript(ascript)
    return out

print("==========================================================")
print("Starting Comprehensive Application Run across all jobs")
print("Guardrails Active:")
print("  - Automatically SKIP all already applied positions")
print("  - HALT IMMEDIATELY upon encountering any submission error")
print("==========================================================")

total_processed = 0
total_submitted = 0
total_skipped = 0
halt_reason = None

# Scan all pages up to offset 230 (covering 221+ positions)
offsets = list(range(0, 240, 10))

for offset in offsets:
    if halt_reason:
        break

    page_url = f"https://jobs.ascendion.com/careers?domain=ascendion.com&hl=&start={offset}&location=India&sort_by=match&filter_include_remote=1&filter_include_relocation=0"
    print(f"\n==========================================")
    print(f"Scanning Page at start={offset}...")
    print(f"==========================================")
    set_url(page_url)
    time.sleep(3.5)

    # Scrape job cards on this page
    scrape_js = """
    (() => {
        return Array.from(document.querySelectorAll('a[href*="/careers/job/"]'))
            .map(a => a.href.split('/careers/job/')[1].split('?')[0] + ':::' + a.innerText.trim().split('\\n')[0])
            .join('|||');
    })()
    """
    raw_str = run_js(scrape_js)
    if not raw_str or raw_str == "NO_TAB":
        print("  Retrying page load...")
        time.sleep(2)
        raw_str = run_js(scrape_js)

    jobs = []
    if raw_str and raw_str != "NO_TAB":
        seen_pids = set()
        for p in raw_str.split('|||'):
            if ':::' in p:
                pid, title = p.split(':::', 1)
                pid = pid.strip()
                title = title.strip()
                if pid and title and pid not in seen_pids:
                    seen_pids.add(pid)
                    jobs.append((pid, title))

    print(f"  Found {len(jobs)} jobs on this page.")
    if not jobs:
        print("  No more jobs listed. Ending search pagination.")
        break

    for pid, title in jobs:
        total_processed += 1
        print(f"\n[{total_processed}] Checking: {title} (PID: {pid})...")

        # 1. Open Job View
        job_url = f"https://jobs.ascendion.com/careers/job/{pid}?domain=ascendion.com&hl="
        set_url(job_url)
        time.sleep(3.0)

        # 2. Check if already applied or if Apply button exists
        check_applied_js = """
        (() => {
            const text = document.body.innerText || '';
            const isApplied = text.includes('already applied') || text.includes('Application submitted');
            const applyBtn = Array.from(document.querySelectorAll('a, button')).find(x => x.innerText.trim().toLowerCase().includes('apply now'));
            const alerts = Array.from(document.querySelectorAll('.invalid-feedback, [class*="error"], [role="alert"]')).map(e => e.innerText.trim()).filter(Boolean);
            return JSON.stringify({
                isApplied: isApplied,
                hasApplyBtn: !!applyBtn,
                alerts: alerts
            });
        })()
        """
        check_res = run_js(check_applied_js)
        try:
            status_data = json.loads(check_res)
        except:
            status_data = {"isApplied": False, "hasApplyBtn": False, "alerts": []}

        # Check if text or any alert indicates already applied
        alerts = status_data.get("alerts", [])
        has_applied_alert = any("already applied" in a.lower() or "application submitted" in a.lower() for a in alerts)

        if status_data.get("isApplied") or has_applied_alert:
            print(f"    --> [SKIP] Already applied previously.")
            total_skipped += 1
            continue

        if not status_data.get("hasApplyBtn"):
            # Check for genuine errors (excluding already applied)
            real_errs = [a for a in alerts if not ("already applied" in a.lower() or "application submitted" in a.lower())]
            if real_errs:
                halt_reason = f"Error detected on job details page for {title}: {real_errs}"
                print(f"    --> [ERROR DETECTED]: {halt_reason}")
                break
            else:
                print(f"    --> [SKIP] No Apply button available for this position.")
                total_skipped += 1
                continue

        # 3. Click Apply Now
        click_apply_js = """
        (() => {
            const btn = Array.from(document.querySelectorAll('a, button')).find(x => x.innerText.trim().toLowerCase().includes('apply now'));
            if (btn) {
                btn.click();
                return 'CLICKED_APPLY';
            }
            return 'NO_APPLY_BTN';
        })()
        """
        run_js(click_apply_js)
        time.sleep(3.5)

        # 4. Check form & wait for Submit button to enable
        submit_ready = False
        for wait_i in range(5):
            form_status_js = """
            (() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase().includes('submit application'));
                const errs = Array.from(document.querySelectorAll('.invalid-feedback, [class*="error"], [role="alert"]')).map(e => e.innerText.trim()).filter(Boolean);
                return JSON.stringify({
                    hasBtn: !!btn,
                    disabled: btn ? btn.disabled : null,
                    errs: errs
                });
            })()
            """
            f_res = run_js(form_status_js)
            try:
                f_data = json.loads(f_res)
            except:
                f_data = {}

            if f_data.get("errs"):
                halt_reason = f"Form validation error on {title}: {f_data['errs']}"
                print(f"    --> [ERROR DETECTED]: {halt_reason}")
                break

            if f_data.get("hasBtn") and not f_data.get("disabled"):
                submit_ready = True
                break
            time.sleep(1.0)

        if halt_reason:
            break

        if not submit_ready:
            halt_reason = f"Submit button was disabled/unresponsive on {title} (custom questions or missing field required)."
            print(f"    --> [STOP TRIGGERED]: {halt_reason}")
            break

        # 5. Click Submit Application
        submit_action_js = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase().includes('submit application'));
            if (btn && !btn.disabled) {
                btn.click();
                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                return 'SUBMITTED';
            }
            return 'FAILED_TO_SUBMIT';
        })()
        """
        sub_res = run_js(submit_action_js)
        time.sleep(4.0)

        # 6. Verify Confirmation or Error
        verify_js = """
        (() => {
            const text = document.body.innerText;
            const isSuccess = window.location.href.includes('/apply/success') || text.includes('Thank you for your application');
            const errs = Array.from(document.querySelectorAll('.invalid-feedback, [class*="error"], [role="alert"], .toast')).map(e => e.innerText.trim()).filter(Boolean);
            return JSON.stringify({
                isSuccess: isSuccess,
                errs: errs,
                url: window.location.href
            });
        })()
        """
        ver_res = run_js(verify_js)
        try:
            v_data = json.loads(ver_res)
        except:
            v_data = {"isSuccess": False, "errs": [ver_res]}

        if v_data.get("isSuccess"):
            total_submitted += 1
            print(f"    --> [SUCCESS] Successfully applied! (Total new in this run: {total_submitted})")
        else:
            err_msg = v_data.get("errs") or ["Application did not redirect to confirmation page."]
            halt_reason = f"Submission error on {title}: {err_msg} (URL: {v_data.get('url')})"
            print(f"    --> [STOP TRIGGERED]: {halt_reason}")
            break

        # Pacing cooldown to avoid anti-spam blocks
        print("    Cooldown 4.5s...")
        time.sleep(4.5)

print("\n==========================================================")
if halt_reason:
    print(f"PROCESS HALTED DUE TO ERROR/GUARDRAIL: {halt_reason}")
else:
    print("PROCESS COMPLETED SUCCESSFULLY FOR ALL PAGES!")
print(f"Total Positions Evaluated: {total_processed}")
print(f"Skipped (Already Applied / Unavailable): {total_skipped}")
print(f"Newly Submitted: {total_submitted}")
print("==========================================================")
