import subprocess
import time
import json
import base64
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url):
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

def open_tab(url):
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "ascendion.com" then
                    tell w
                        make new tab with properties {{URL:"{url}"}}
                        return "OPENED"
                    end tell
                end if
            end repeat
        end repeat
    end tell
    '''
    exec_ascript(ascript)

def close_tab(filter_url):
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            close (every tab of w whose URL contains "{filter_url}")
        end repeat
    end tell
    '''
    exec_ascript(ascript)

def main():
    print("==========================================================")
    print("ASCENDION ALL-JOBS APPLICATION RUNNER (PRODUCTION)")
    print("==========================================================")

    # Step 1: Read dashboard
    print("\n[Step 1] Fetching live submitted applications from profile...")
    open_tab("https://jobs.ascendion.com/careers/applications")
    time.sleep(5.0)

    dash_js = """
    (() => {
        const text = document.body.innerText || '';
        const matches = Array.from(text.matchAll(/Job ID:\\s*([0-9]+)/g)).map(m => m[1]);
        return Array.from(new Set(matches)).join(',');
    })()
    """
    dash_str = run_js(dash_js, "careers/applications")
    applied_ids = set(dash_str.split(',')) if dash_str and dash_str != "NO_TAB" else set()
    close_tab("careers/applications")
    print(f"--> Found {len(applied_ids)} applications already confirmed on dashboard.")

    # Step 2: Scrape all jobs across all pages
    print("\n[Step 2] Scraping all jobs across all pages (start=0 to 220)...")
    all_jobs = []
    seen_pids = set()

    scrape_js = """
    (() => {
        return Array.from(document.querySelectorAll('a[href*="/careers/job/"]'))
            .map(a => a.href.split('/careers/job/')[1].split('?')[0] + ':::' + a.innerText.trim().split('\\n')[0])
            .join('|||');
    })()
    """

    for offset in range(0, 240, 10):
        search_url = f"https://jobs.ascendion.com/careers?domain=ascendion.com&hl=&start={offset}&location=India&sort_by=match&filter_include_remote=1&filter_include_relocation=0"
        nav_js = f"window.location.href = '{search_url}';"
        run_js(nav_js, "jobs.ascendion.com")
        time.sleep(3.5)

        raw = run_js(scrape_js, "jobs.ascendion.com")
        count_page = 0
        if raw and raw != "NO_TAB":
            for item in raw.split('|||'):
                if ':::' in item:
                    pid, title = item.split(':::', 1)
                    pid = pid.strip()
                    title = title.strip()
                    if pid and title and pid not in seen_pids:
                        seen_pids.add(pid)
                        all_jobs.append((pid, title))
                        count_page += 1

        print(f"  Page start={offset:3d}: +{count_page} new jobs (Total unique jobs: {len(all_jobs)})")
        if count_page == 0 and offset >= 200:
            print("  --> End of pagination reached.")
            break

    total_jobs = len(all_jobs)
    print(f"\n==========================================================")
    print(f"Total Unique Positions on Portal: {total_jobs}")
    print(f"Already Confirmed on Dashboard: {len(applied_ids)}")
    print(f"==========================================================")

    # Step 3: Iterate through every position
    new_submissions = 0
    skipped_applied = 0
    skipped_errors = 0

    check_page_js = """
    (() => {
        const text = document.body.innerText || '';
        if (text.includes('already applied') || text.includes('Application submitted')) return 'ALREADY_APPLIED';
        const applyBtn = Array.from(document.querySelectorAll('a, button')).find(x => x.innerText.trim().toLowerCase().includes('apply now'));
        if (applyBtn) {
            applyBtn.click();
            return 'CLICKED_APPLY';
        }
        return 'NO_APPLY_BTN';
    })()
    """

    submit_form_js = """
    (() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase().includes('submit application'));
        if (!btn) return 'NO_SUBMIT_BTN';
        if (btn.disabled) return 'DISABLED';
        btn.click();
        btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
        btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
        btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return 'SUBMITTED';
    })()
    """

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

    for i, (pid, title) in enumerate(all_jobs, 1):
        if pid in applied_ids:
            print(f"[{i:3d}/{total_jobs}] {title} (PID: {pid}) -> [SKIP] Already confirmed on dashboard.")
            skipped_applied += 1
            continue

        print(f"\n[{i:3d}/{total_jobs}] Processing: {title} (PID: {pid})...")
        open_tab(f"https://jobs.ascendion.com/careers/job/{pid}?domain=ascendion.com&hl=")
        time.sleep(3.5)

        c_res = run_js(check_page_js, pid)
        print(f"      Job page status: {c_res}")

        if c_res == "ALREADY_APPLIED":
            print("      --> [SKIP] Marked as already applied.")
            close_tab(pid)
            applied_ids.add(pid)
            skipped_applied += 1
            continue

        if c_res != "CLICKED_APPLY":
            print(f"      --> [SKIP] No apply button ({c_res}).")
            close_tab(pid)
            skipped_errors += 1
            continue

        time.sleep(3.5)
        s_res = run_js(submit_form_js, pid)
        print(f"      Submit trigger: {s_res}")

        if s_res != "SUBMITTED":
            print(f"      --> [SKIP Form Error]: {s_res}")
            close_tab(pid)
            skipped_errors += 1
            continue

        time.sleep(4.0)
        v_res = run_js(verify_js, pid)
        print(f"      Verification: {v_res}")
        close_tab(pid)

        if "ERROR:" in v_res:
            print(f"      --> [SKIP Submission Error]: {v_res}")
            skipped_errors += 1
        else:
            new_submissions += 1
            applied_ids.add(pid)
            print(f"      --> [SUCCESS] Submitted! Total new in this run: {new_submissions}")

        time.sleep(3.0)

    print("\n==========================================================")
    print("ALL POSITIONS PROCESSED!")
    print(f"Total Portal Positions: {total_jobs}")
    print(f"Already Applied / Skipped: {skipped_applied}")
    print(f"Newly Submitted in this Run: {new_submissions}")
    print(f"Skipped Due to Ineligibility / Errors: {skipped_errors}")
    print("==========================================================")

    # Final Dashboard Audit
    print("\n[Step 4] Running final audit on applications dashboard...")
    open_tab("https://jobs.ascendion.com/careers/applications")
    time.sleep(5.0)
    final_str = run_js(dash_js, "careers/applications")
    final_ids = set(final_str.split(',')) if final_str and final_str != "NO_TAB" else set()
    print(f"--> FINAL CONFIRMED SUBMITTED APPLICATIONS ON PROFILE: {len(final_ids)}")
    print("==========================================================")

if __name__ == '__main__':
    main()
