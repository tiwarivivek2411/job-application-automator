import subprocess
import time
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js_in_search_tab(js_code):
    escaped = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "jobs.ascendion.com/careers" and not (u contains "/apply/success") then
                    return (execute t javascript "{escaped}")
                end if
            end repeat
        end repeat
        return "NO_SEARCH_TAB"
    end tell
    '''
    out, _ = exec_ascript(ascript)
    return out

def set_search_tab_url(new_url):
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
            set u to (URL of t as string)
            if u contains "jobs.ascendion.com/careers" and not (u contains "/apply/success") then
                tell t to set URL to "{new_url}"
                return "NAVIGATED"
            end if
        end repeat
    end repeat
    return "NO_SEARCH_TAB"
end tell
    '''
    out, _ = exec_ascript(ascript)
    return out

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

EXCLUDE = ["sales", "talent", "recruiter", "marketing", "hr", "account executive", "manager - business"]

def is_matching(title):
    lower = title.lower()
    if any(ex in lower for ex in EXCLUDE):
        return False
    return any(kw in lower for kw in KEYWORDS)

TARGET = 20
newly_applied = []

print("=========================================================")
print(f"Targeting next {TARGET} Engineering & Developer jobs in India")
print(f"Base already submitted: {len(APPLIED_PIDS)}")
print("=========================================================")

offsets = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]

for offset in offsets:
    if len(newly_applied) >= TARGET:
        break

    page_url = f"https://jobs.ascendion.com/careers?domain=ascendion.com&hl=&start={offset}&location=India&sort_by=match&filter_include_remote=1&filter_include_relocation=0"
    print(f"\n--> Fetching search page: start={offset}")
    set_search_tab_url(page_url)
    time.sleep(4)

    scrape_js = """
    (() => {
        return Array.from(document.querySelectorAll('a[href*="/careers/job/"]'))
            .map(a => a.href.split('/careers/job/')[1].split('?')[0] + ':::' + a.innerText.trim().split('\\n')[0])
            .join('|||');
    })()
    """
    raw_str = run_js_in_search_tab(scrape_js)
    if not raw_str or raw_str == "NO_SEARCH_TAB":
        print("    Could not read search tab. Retrying...")
        time.sleep(2)
        raw_str = run_js_in_search_tab(scrape_js)

    jobs = []
    if raw_str and raw_str != "NO_SEARCH_TAB":
        pairs = raw_str.split('|||')
        seen_pids = set()
        for p in pairs:
            if ':::' in p:
                pid, title = p.split(':::', 1)
                pid = pid.strip()
                title = title.strip()
                if pid and title and pid not in seen_pids:
                    seen_pids.add(pid)
                    jobs.append((pid, title))

    print(f"    Found {len(jobs)} listings on page start={offset}.")

    for pid, title in jobs:
        if len(newly_applied) >= TARGET:
            break

        if pid in APPLIED_PIDS:
            continue

        if not is_matching(title):
            print(f"    [Skip - Non-Dev] {title}")
            continue

        print(f"\n[{len(newly_applied)+1}/{TARGET}] Applying to: {title} (PID: {pid})...")

        # Navigate to apply page
        apply_url = f"https://jobs.ascendion.com/careers/apply?pid={pid}&domain=ascendion.com&hl="
        set_search_tab_url(apply_url)
        time.sleep(3.5)

        # Dispatch click and submit
        submit_js = """
        (() => {
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
        sub_res = run_js_in_search_tab(submit_js)
        print(f"    Submit action: {sub_res}")
        time.sleep(4)

        # Verify
        verify_js = """
        (() => {
            const isSuccess = window.location.href.includes('/apply/success') || document.body.innerText.includes('Thank you for your application');
            return isSuccess ? 'SUCCESS' : ('URL: ' + window.location.href);
        })()
        """
        ver_res = run_js_in_search_tab(verify_js)
        print(f"    Verification: {ver_res}")

        APPLIED_PIDS.add(pid)
        newly_applied.append({"pid": pid, "title": title, "status": ver_res})

        print("    Cooling down 5s...")
        time.sleep(5)

print("\n=========================================================")
print(f"Safe Batch Finished! Applied to {len(newly_applied)} engineering roles.")
print(f"Grand Total Applied for Profile: {len(APPLIED_PIDS)}")
print("=========================================================")
for i, item in enumerate(newly_applied, 1):
    print(f"{i}. {item['title']} (PID: {item['pid']}) -> {item['status']}")
