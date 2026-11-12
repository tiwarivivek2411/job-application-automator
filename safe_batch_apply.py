import subprocess
import time
import json
import re

def run_applescript(script_str):
    p = subprocess.Popen(['osascript', '-e', script_str], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

APPLIED_PIDS = {
    "1970324837573743", "1970324837568245", "1970324837524060",
    "1970324837570935", "1970324837576448", "1970324837544085",
    "1970324837568242", "1970324837561930", "1970324837568246",
    "1970324837571103", "1970324837577448", "1970324837571096",
    "1970324837571101", "1970324837538045"
}

KEYWORDS = [
    "engineer", "developer", "development", "devops", "cloud",
    "backend", "frontend", "fullstack", "software", "architect",
    "data", "qa", "test", "tech", "java", "python", "golang",
    "node", "ui", "sre", "reliability"
]

EXCLUDE = ["sales", "talent", "recruiter", "marketing", "hr", "account executive"]

def is_matching_role(title):
    lower = title.lower()
    if any(ex in lower for ex in EXCLUDE):
        return False
    return any(kw in lower for kw in KEYWORDS)

TARGET_NEW = 20
newly_applied = []

print("==================================================")
print(f"Starting Safe Batch Auto-Apply (Target: {TARGET_NEW} Engineering Jobs)")
print(f"Already Confirmed Submissions: {len(APPLIED_PIDS)}")
print("==================================================")

start_offset = 0

while len(newly_applied) < TARGET_NEW and start_offset < 150:
    page_url = f"https://jobs.ascendion.com/careers?domain=ascendion.com&hl=&start={start_offset}&location=India&sort_by=match&filter_include_remote=1&filter_include_relocation=0"
    print(f"\nScanning Page (start={start_offset})...")

    # Navigate the worker tab (the one not showing /apply/success)
    nav_cmd = '''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "jobs.ascendion.com/careers" and not (u contains "/apply/success") then
                    tell t to set URL to "''' + page_url + '''"
                    return "NAVIGATED"
                end if
            end repeat
        end repeat
        return "NONE"
    end tell
    '''
    run_applescript(nav_cmd)
    time.sleep(4)

    # Scrape job cards from this page
    scrape_cmd = '''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "jobs.ascendion.com/careers" and not (u contains "/apply") then
                    tell t
                        return execute javascript "
                            (function() {
                                const anchors = Array.from(document.querySelectorAll('a[href*=\"/careers/job/\"], a[href*=\"pid=\"]'));
                                const res = [];
                                const seen = new Set();
                                for (const a of anchors) {
                                    const m = a.href.match(/job\\\\/(\\\\d+)/) || a.href.match(/pid=(\\\\d+)/);
                                    if (m) {
                                        const pid = m[1];
                                        if (!seen.has(pid)) {
                                            seen.add(pid);
                                            const title = a.innerText.trim().split('\\\\n')[0];
                                            if (title) res.push({ pid: pid, title: title });
                                        }
                                    }
                                }
                                return JSON.stringify(res);
                            })()
                        "
                    end tell
                end if
            end repeat
        end repeat
        return "[]"
    end tell
    '''
    raw_jobs, _ = run_applescript(scrape_cmd)
    try:
        page_jobs = json.loads(raw_jobs) if raw_jobs else []
    except Exception as e:
        page_jobs = []

    print(f"Found {len(page_jobs)} total listings on this page.")

    if not page_jobs:
        print("No job cards rendered or reached end of list. Incrementing offset...")
        start_offset += 10
        continue

    for job in page_jobs:
        if len(newly_applied) >= TARGET_NEW:
            break

        pid = job['pid']
        title = job['title']

        if pid in APPLIED_PIDS:
            print(f"  [Skip - Already Applied] {title} ({pid})")
            continue

        if not is_matching_role(title):
            print(f"  [Skip - Non-Engineering] {title} ({pid})")
            continue

        print(f"\n--> [{len(newly_applied)+1}/{TARGET_NEW}] Applying: {title} (PID: {pid})...")

        # Navigate to apply page
        apply_url = f"https://jobs.ascendion.com/careers/apply?pid={pid}&domain=ascendion.com&hl="
        nav_apply = '''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    set u to (URL of t as string)
                    if u contains "jobs.ascendion.com/careers" and not (u contains "/apply/success") then
                        tell t to set URL to "''' + apply_url + '''"
                        return "OK"
                    end if
                end repeat
            end repeat
        end tell
        '''
        run_applescript(nav_apply)
        time.sleep(3.5)

        # Click Submit Application
        submit_js = '''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    set u to (URL of t as string)
                    if u contains "''' + pid + '''" then
                        tell t
                            return execute javascript "
                                (function() {
                                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase().includes('submit application'));
                                    if (btn) {
                                        if (btn.disabled) return 'DISABLED';
                                        btn.click();
                                        btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                                        btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                                        btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                                        return 'SUBMITTED';
                                    }
                                    return 'NO_BTN';
                                })()
                            "
                        end tell
                    end if
                end repeat
            end repeat
        end tell
        '''
        submit_res, _ = run_applescript(submit_js)
        print(f"      Submit status: {submit_res}")
        time.sleep(3.5)

        # Verify Success
        verify_js = '''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    set u to (URL of t as string)
                    if u contains "''' + pid + '''" then
                        tell t
                            return execute javascript "
                                (function() {
                                    const isSuccess = window.location.href.includes('/apply/success') || document.body.innerText.includes('Thank you for your application');
                                    return isSuccess ? 'SUCCESS' : ('PENDING:' + window.location.href);
                                })()
                            "
                        end tell
                    end if
                end repeat
            end repeat
        end tell
        '''
        ver_res, _ = run_applescript(verify_js)
        print(f"      Verification: {ver_res}")

        APPLIED_PIDS.add(pid)
        newly_applied.append({"title": title, "pid": pid, "status": ver_res})

        print("      Cooldown 5s...")
        time.sleep(5)

    start_offset += 10

print("\n==================================================")
print(f"Batch Complete! Successfully applied to {len(newly_applied)} engineering roles.")
print(f"Total confirmed applications: {len(APPLIED_PIDS)}")
print("==================================================")
for idx, item in enumerate(newly_applied, 1):
    print(f"{idx}. {item['title']} (PID: {item['pid']}) -> {item['status']}")
