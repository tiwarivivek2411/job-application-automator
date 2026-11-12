import subprocess
import time
import json
import re

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
            close (every tab of w whose URL contains "{url_filter}")
        end repeat
        return "CLOSED"
    end tell
    '''
    out, _ = exec_ascript(ascript)
    return out

def open_new_tab(url):
    open_ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "ascendion.com" then
                    tell w
                        set newTab to make new tab with properties {{URL:"{url}"}}
                        return "OPENED"
                    end tell
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    out, _ = exec_ascript(open_ascript)
    return out

def main():
    print("==========================================================")
    print("Step 1: Reading candidate's submitted applications dashboard...")
    print("==========================================================")

    # Open dashboard tab
    open_new_tab("https://jobs.ascendion.com/careers/applications")
    time.sleep(5)

    dash_js = """
    (() => {
        const text = document.body.innerText || '';
        const matches = Array.from(text.matchAll(/Job ID:\\s*([0-9]+)/g)).map(m => m[1]);
        return Array.from(new Set(matches)).join(',');
    })()
    """
    applied_str = run_js_in_tab(dash_js, "careers/applications")
    applied_set = set(applied_str.split(',')) if applied_str and applied_str != "NO_TAB" else set()
    print(f"Found {len(applied_set)} applications already confirmed on dashboard.")

    # Close dashboard tab for now
    close_tab_with_url("careers/applications")

    print("\n==========================================================")
    print("Step 2: Scraping all listings across all pages (start 0 to 230)...")
    print("==========================================================")

    all_jobs = []
    seen_all_pids = set()

    for offset in range(0, 240, 10):
        search_url = f"https://jobs.ascendion.com/careers?domain=ascendion.com&hl=&start={offset}&location=India&sort_by=match&filter_include_remote=1&filter_include_relocation=0"
        
        # Navigate search tab
        nav_js = f"window.location.href = '{search_url}';"
        run_js_in_tab(nav_js, "jobs.ascendion.com")
        time.sleep(3.5)

        scrape_js = """
        (() => {
            return Array.from(document.querySelectorAll('a[href*="/careers/job/"]'))
                .map(a => a.href.split('/careers/job/')[1].split('?')[0] + ':::' + a.innerText.trim().split('\\n')[0])
                .join('|||');
        })()
        """
        raw_str = run_js_in_tab(scrape_js, "jobs.ascendion.com")
        if not raw_str or raw_str == "NO_TAB":
            time.sleep(2.0)
            raw_str = run_js_in_tab(scrape_js, "jobs.ascendion.com")

        count_this_page = 0
        if raw_str and raw_str != "NO_TAB":
            for item in raw_str.split('|||'):
                if ':::' in item:
                    pid, title = item.split(':::', 1)
                    pid = pid.strip()
                    title = title.strip()
                    if pid and title and pid not in seen_all_pids:
                        seen_all_pids.add(pid)
                        all_jobs.append((pid, title))
                        count_this_page += 1

        print(f"  Offset start={offset}: Found {count_this_page} new listings (Total unique portal jobs so far: {len(all_jobs)})")
        if count_this_page == 0 and offset > 200:
            print("  Reached end of search results.")
            break

    # Find unapplied jobs
    unapplied = [j for j in all_jobs if j[0] not in applied_set]
    print(f"\n==========================================================")
    print(f"Total Unique Jobs on Portal: {len(all_jobs)}")
    print(f"Already Submitted on Dashboard: {len(applied_set)}")
    print(f"Pending to Apply: {len(unapplied)}")
    print("==========================================================")

    if not unapplied:
        print("All jobs are already submitted! Nothing more to apply.")
    else:
        # Process pending jobs
        submitted_new = 0
        errors_encountered = 0

        for idx, (pid, title) in enumerate(unapplied, 1):
            print(f"\n[{idx}/{len(unapplied)}] Processing: {title} (PID: {pid})...")
            apply_url = f"https://jobs.ascendion.com/careers/apply?pid={pid}&domain=ascendion.com&hl="

            open_new_tab(apply_url)
            time.sleep(3.5)

            # Check if already applied or if form loaded
            check_js = """
            (() => {
                const text = document.body.innerText || '';
                if (text.includes('already applied') || text.includes('Application submitted')) return 'ALREADY_APPLIED';
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase().includes('submit application'));
                if (!btn) return 'NO_SUBMIT_BTN';
                if (btn.disabled) return 'DISABLED';

                // Filter real form validation errors (ignore aria status messages like 'Application loaded')
                const errs = Array.from(document.querySelectorAll('.invalid-feedback, [class*="error"]'))
                    .map(e => e.innerText.trim())
                    .filter(t => t && !t.includes('Application loaded') && !t.includes('already applied'));
                if (errs.length > 0) return 'ERROR:' + errs.join('; ');

                btn.click();
                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                return 'SUBMITTED';
            })()
            """
            submit_res = run_js_in_tab(check_js, pid)
            if submit_res == "NO_SUBMIT_BTN":
                # Give another 2 seconds
                time.sleep(2.0)
                submit_res = run_js_in_tab(check_js, pid)

            print(f"  Submit result: {submit_res}")

            if submit_res == "ALREADY_APPLIED":
                print("  --> [SKIP] Already applied.")
                close_tab_with_url(pid)
                applied_set.add(pid)
                continue

            if submit_res == "SUBMITTED":
                time.sleep(4.5)
                # Verify outcome
                verify_js = """
                (() => {
                    const text = document.body.innerText || '';
                    if (window.location.href.includes('/apply/success') || text.includes('Thank you for your application')) return 'SUCCESS';
                    const errs = Array.from(document.querySelectorAll('.invalid-feedback, [class*="error"], [role="alert"], .toast'))
                        .map(e => e.innerText.trim())
                        .filter(t => t && !t.includes('Application loaded') && !t.includes('already applied'));
                    if (errs.length > 0) return 'ERROR:' + errs.join('; ');
                    return 'SUBMITTED_OK';
                })()
                """
                ver_res = run_js_in_tab(verify_js, pid)
                print(f"  Verification: {ver_res}")
                close_tab_with_url(pid)

                if "ERROR:" in ver_res:
                    print(f"  --> [ERROR ON SUBMISSION - SKIPPED]: {ver_res}")
                    errors_encountered += 1
                else:
                    submitted_new += 1
                    applied_set.add(pid)
                    print(f"  --> [CONFIRMED SUBMITTED] (Total new in mop-up: {submitted_new})")
            else:
                print(f"  --> [SKIPPED]: {submit_res}")
                close_tab_with_url(pid)
                errors_encountered += 1

            time.sleep(3.0)

    print("\n==========================================================")
    print("Step 4: Final verification on dashboard...")
    print("==========================================================")
    open_new_tab("https://jobs.ascendion.com/careers/applications")
    time.sleep(5)
    final_ids_str = run_js_in_tab(dash_js, "careers/applications")
    final_ids = set(final_ids_str.split(',')) if final_ids_str and final_ids_str != "NO_TAB" else set()
    print(f"FINAL CONFIRMED APPLICATIONS ON DASHBOARD: {len(final_ids)}")
    print("==========================================================")

if __name__ == '__main__':
    main()
