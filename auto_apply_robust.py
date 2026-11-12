import subprocess
import time
import json
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

# Already confirmed applied PIDs
APPLIED_PIDS = {
    "1970324837573743", "1970324837568245", "1970324837524060",
    "1970324837570935", "1970324837576448", "1970324837544085",
    "1970324837568242", "1970324837561930", "1970324837568246",
    "1970324837571103", "1970324837577448", "1970324837571096",
    "1970324837571101", "1970324837538045", "1970324837576420"
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

print("==================================================")
print("Step 1: Collecting matching Engineering jobs across search pages...")
print("==================================================")

candidate_jobs = []
seen_pids = set(APPLIED_PIDS)

offsets = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

for offset in offsets:
    if len(candidate_jobs) >= 25:
        break
    page_url = f"https://jobs.ascendion.com/careers?domain=ascendion.com&hl=&start={offset}&location=India&sort_by=match&filter_include_remote=1&filter_include_relocation=0"
    set_url(page_url)
    time.sleep(3.5)

    scrape_js = """
    (() => {
        return Array.from(document.querySelectorAll('a[href*="/careers/job/"]'))
            .map(a => a.href.split('/careers/job/')[1].split('?')[0] + ':::' + a.innerText.trim().split('\\n')[0])
            .join('|||');
    })()
    """
    raw_str = run_js(scrape_js)
    if raw_str and raw_str != "NO_TAB":
        for item in raw_str.split('|||'):
            if ':::' in item:
                pid, title = item.split(':::', 1)
                pid = pid.strip()
                title = title.strip()
                if pid and title and pid not in seen_pids:
                    if is_matching(title):
                        seen_pids.add(pid)
                        candidate_jobs.append((pid, title))

print(f"Collected {len(candidate_jobs)} unapplied Engineering & Developer positions:")
for idx, (pid, title) in enumerate(candidate_jobs, 1):
    print(f"  {idx}. {title} (PID: {pid})")

TARGET = min(17, len(candidate_jobs))
newly_applied = []

print("\n==================================================")
print(f"Step 2: Submitting applications for top {TARGET} positions...")
print("==================================================")

for i in range(TARGET):
    pid, title = candidate_jobs[i]
    print(f"\n[{i+1}/{TARGET}] Applying: {title} (PID: {pid})...")

    # Navigate to apply page
    apply_url = f"https://jobs.ascendion.com/careers/apply?pid={pid}&domain=ascendion.com&hl="
    set_url(apply_url)
    
    # Wait for page & form to render (typically 3-4s)
    time.sleep(4)

    # Click Submit with retry up to 3 times
    submitted = False
    for attempt in range(3):
        click_js = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase().includes('submit application'));
            if (btn && !btn.disabled) {
                btn.click();
                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                return 'CLICKED_SUBMIT';
            }
            return btn ? (btn.disabled ? 'BTN_DISABLED' : 'BTN_NOT_CLICKABLE') : 'NO_BTN';
        })()
        """
        res = run_js(click_js)
        print(f"      Attempt {attempt+1}: {res}")
        if res == 'CLICKED_SUBMIT':
            submitted = True
            break
        time.sleep(2)

    # Wait for submission network request & redirect to success
    time.sleep(4)

    # Check verification
    check_js = """
    (() => {
        const text = document.body.innerText;
        const isSuccess = window.location.href.includes('/apply/success') || text.includes('Thank you for your application');
        return isSuccess ? 'SUCCESS' : ('PENDING:' + window.location.href);
    })()
    """
    v_res = run_js(check_js)
    print(f"      Status: {v_res}")

    APPLIED_PIDS.add(pid)
    newly_applied.append({"pid": pid, "title": title, "status": v_res})

    print("      Cooling down 5s...")
    time.sleep(5)

print("\n==================================================")
print(f"Execution Complete! Successfully processed {len(newly_applied)} applications.")
print(f"Total Applications on Record: {len(APPLIED_PIDS)}")
print("==================================================")
for idx, item in enumerate(newly_applied, 1):
    print(f"{idx}. {item['title']} -> {item['status']}")
