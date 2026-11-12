import subprocess
import time
import json
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js_in_tab(js_code, url_filter):
    escaped = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "{url_filter}" then
                    return (execute t javascript "{escaped}")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    out, _ = exec_ascript(ascript)
    return out

def close_tab_with_url(url_filter):
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "{url_filter}" then
                    close t
                    return "CLOSED"
                end if
            end repeat
        end repeat
        return "NOT_FOUND"
    end tell
    '''
    out, _ = exec_ascript(ascript)
    return out

print("==========================================================")
print("Resuming Multi-Tab Application Run from Page 2 (start=10)")
print("Rules Active:")
print("  - Skip already applied positions")
print("  - On any error: log error, skip that job, and CONTINUE")
print("==========================================================")

total_checked = 0
total_submitted = 0
total_skipped_applied = 0
total_skipped_error = 0

# Start from offset 10 through 230
offsets = list(range(10, 240, 10))

for offset in offsets:
    search_url = f"https://jobs.ascendion.com/careers?domain=ascendion.com&hl=&start={offset}&location=India&sort_by=match&filter_include_remote=1&filter_include_relocation=0"
    print(f"\n==========================================")
    print(f"Loading Page at offset start={offset}...")
    print(f"==========================================")

    # 1. Navigate search tab via JS
    nav_js = f"window.location.href = '{search_url}';"
    run_js_in_tab(nav_js, "jobs.ascendion.com")
    time.sleep(4.0)

    # 2. Extract job cards on this page
    scrape_js = """
    (() => {
        return Array.from(document.querySelectorAll('a[href*="/careers/job/"]'))
            .map(a => a.href.split('/careers/job/')[1].split('?')[0] + ':::' + a.innerText.trim().split('\\n')[0])
            .join('|||');
    })()
    """
    raw_str = run_js_in_tab(scrape_js, "jobs.ascendion.com/careers")
    if not raw_str or raw_str == "NO_TAB":
        time.sleep(2.0)
        raw_str = run_js_in_tab(scrape_js, "jobs.ascendion.com/careers")

    jobs = []
    seen = set()
    if raw_str and raw_str != "NO_TAB":
        for item in raw_str.split('|||'):
            if ':::' in item:
                pid, title = item.split(':::', 1)
                pid = pid.strip()
                title = title.strip()
                if pid and title and pid not in seen:
                    seen.add(pid)
                    jobs.append((pid, title))

    print(f"Found {len(jobs)} jobs on page start={offset}.")
    if not jobs:
        print("No more jobs listed. Completed all pages.")
        break

    # 3. Process each job in a separate tab
    for idx, (pid, title) in enumerate(jobs, 1):
        total_checked += 1
        job_url = f"https://jobs.ascendion.com/careers/job/{pid}?domain=ascendion.com&hl="
        print(f"\n  [{total_checked}] Opening Job: {title} (PID: {pid})...")

        # Open in new tab
        open_ascript = f'''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    if (URL of t as string) contains "jobs.ascendion.com" then
                        tell w
                            set newTab to make new tab with properties {{URL:"{job_url}"}}
                            return "OPENED"
                        end tell
                    end if
                end repeat
            end repeat
            return "NO_TAB"
        end tell
        '''
        exec_ascript(open_ascript)
        time.sleep(3.5)

        # Check in the newly opened tab
        check_js = """
        (() => {
            const text = document.body.innerText || '';
            const isApplied = text.includes('already applied') || text.includes('Application submitted');
            const applyBtn = Array.from(document.querySelectorAll('a, button')).find(x => x.innerText.trim().toLowerCase().includes('apply now'));
            if (isApplied) return 'ALREADY_APPLIED';
            if (applyBtn) {
                applyBtn.click();
                return 'CLICKED_APPLY';
            }
            return 'NO_APPLY_BTN';
        })()
        """
        check_res = run_js_in_tab(check_js, pid)

        if check_res == "ALREADY_APPLIED":
            print(f"      --> [SKIP] Already applied. Closing tab.")
            close_tab_with_url(pid)
            total_skipped_applied += 1
            continue

        if check_res != "CLICKED_APPLY":
            print(f"      --> [SKIP] No Apply button ({check_res}). Closing tab.")
            close_tab_with_url(pid)
            total_skipped_applied += 1
            continue

        print(f"      Clicked 'Apply Now'. Waiting for form...")
        time.sleep(3.5)

        # Submit Application in that tab
        submit_js = """
        (() => {
            const errs = Array.from(document.querySelectorAll('.invalid-feedback, [class*="error"], [role="alert"]')).map(e => e.innerText.trim()).filter(Boolean);
            if (errs.length > 0) return 'ERROR:' + errs.join('; ');
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase().includes('submit application'));
            if (btn) {
                if (btn.disabled) return 'DISABLED';
                btn.click();
                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                return 'SUBMITTED';
            }
            return 'NO_SUBMIT_BTN';
        })()
        """
        sub_res = run_js_in_tab(submit_js, pid)
        print(f"      Submit trigger: {sub_res}")

        if "ERROR:" in sub_res or sub_res == "DISABLED":
            close_tab_with_url(pid)
            print(f"      --> [ERROR ON FORM - SKIPPING]: {sub_res}")
            total_skipped_error += 1
            continue

        time.sleep(4.0)

        # Verify Success or Error
        verify_js = """
        (() => {
            const text = document.body.innerText || '';
            if (window.location.href.includes('/apply/success') || text.includes('Thank you for your application')) return 'SUCCESS';
            const errs = Array.from(document.querySelectorAll('.invalid-feedback, [class*="error"], [role="alert"], .toast')).map(e => e.innerText.trim()).filter(Boolean);
            if (errs.length > 0) return 'ERROR:' + errs.join('; ');
            return 'PENDING:' + window.location.href;
        })()
        """
        ver_res = run_js_in_tab(verify_js, pid)
        print(f"      Verification: {ver_res}")

        close_tab_with_url(pid)

        if "ERROR:" in ver_res:
            print(f"      --> [ERROR ON SUBMISSION - SKIPPING]: {ver_res}")
            total_skipped_error += 1
        elif "SUCCESS" in ver_res:
            total_submitted += 1
            print(f"      --> [SUCCESS] Application complete! (Total new in this run: {total_submitted})")
        else:
            print(f"      --> [STATUS: {ver_res}] Closed tab.")

        print("      Cooldown 4s...")
        time.sleep(4.0)

print("\n==========================================================")
print("ALL REMAINING PAGES PROCESSED!")
print(f"Total Jobs Checked: {total_checked}")
print(f"Skipped (Already Applied): {total_skipped_applied}")
print(f"Skipped (Errors Encountered): {total_skipped_error}")
print(f"Newly Submitted: {total_submitted}")
print("==========================================================")
