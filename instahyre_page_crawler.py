import subprocess
import time
import json
import re

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_chrome_js(js_code, filter_url="instahyre.com"):
    cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
    escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "{filter_url}" then
                    return (execute t javascript "{escaped}")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    out, err = exec_ascript(ascript)
    return out

TECH_KEYWORDS = [
    'software', 'engineer', 'developer', 'backend', 'frontend', 'full-stack', 'full stack',
    'platform', 'systems', 'distributed', 'sde', 'architect', 'devops', 'sre', 'cloud',
    'java', 'python', 'golang', 'node', 'react', 'data engineer', 'ai', 'ml', 'machine learning',
    'infrastructure', 'microservices', 'lead'
]

EXCLUDE_KEYWORDS = [
    'sales', 'account manager', 'marketing', 'recruiter', 'hr', 'talent acquisition',
    'business development', 'b2b sales', 'executive assistant'
]

def is_tech_role(text):
    t = text.lower()
    if any(ex in t for ex in EXCLUDE_KEYWORDS):
        return False
    return any(kw in t for kw in TECH_KEYWORDS)

def get_page_jobs():
    extract_js = """
    (() => {
        const opps = Array.from(document.querySelectorAll("[ng-repeat*='opp in opportunities']"));
        return JSON.stringify(opps.map(el => {
            const link = el.querySelector("a[href*='/job-']");
            const text = el.innerText.slice(0, 150).replace(/\\n/g, ' ');
            return {
                url: link ? link.href : null,
                text: text
            };
        }).filter(item => item.url));
    })()
    """
    raw = run_chrome_js(extract_js)
    try:
        return json.loads(raw)
    except Exception as e:
        print("  Error extracting page jobs:", e)
        return []

def apply_to_job(job_url):
    print(f"\nOpening job: {job_url}")
    run_chrome_js(f'window.location.href = "{job_url}";')
    time.sleep(2.5)

    check_js = """
    (() => {
        const text = document.body.innerText;
        const alreadyApplied = text.includes('Application sent!') || text.includes('You have applied') || text.includes('Applied on');
        const btn = document.querySelector("button[ng-click*='submitChoiceNonMatching']");
        const h1 = document.querySelector('h1, h2, .job-title')?.innerText?.trim() || document.title;
        return JSON.stringify({
            title: h1,
            alreadyApplied,
            hasBtn: !!btn,
            btnDisabled: btn ? btn.disabled : true
        });
    })()
    """
    raw_status = run_chrome_js(check_js)
    try:
        status = json.loads(raw_status)
    except Exception as e:
        print("  Error parsing status:", e)
        return False, "PARSE_ERROR"

    role_title = status.get('title')
    print(f"  Role: '{role_title}'")

    if status.get('alreadyApplied'):
        print("  --> Already Applied! Skipping.")
        return False, "ALREADY_APPLIED"

    if not status.get('hasBtn') or status.get('btnDisabled'):
        print(f"  --> Apply button not available (btn: {status.get('hasBtn')}, disabled: {status.get('btnDisabled')}). Skipping.")
        return False, "NO_BUTTON"

    # Click apply
    click_js = """
    (() => {
        const btn = document.querySelector("button[ng-click*='submitChoiceNonMatching']");
        if (!btn) return 'NO_BTN';
        btn.click();
        return 'CLICKED';
    })()
    """
    run_chrome_js(click_js)
    time.sleep(1.8)

    # Verify
    verify_js = """
    (() => {
        const text = document.body.innerText;
        return JSON.stringify({
            confirmed: text.includes('Application sent!') || text.includes('Applied on')
        });
    })()
    """
    try:
        ver = json.loads(run_chrome_js(verify_js))
        if ver.get('confirmed'):
            print(f"  --> [SUCCESS] Confirmed application for '{role_title}'!")
            return True, role_title
    except Exception:
        pass

    return False, "UNCONFIRMED"

def crawl_pages(start_page=3, end_page=8):
    total_applied = 0
    confirmed = []
    print("==========================================================")
    print("INSTAHYRE DEEP PAGE CRAWLER & APPLICANT")
    print(f"Pages: {start_page} to {end_page}")
    print("==========================================================")

    for p in range(start_page, end_page + 1):
        print(f"\n--- Navigating to Search Page {p} ---")
        run_chrome_js('window.location.href = "https://www.instahyre.com/search-jobs";')
        time.sleep(3.0)

        # Click pagination page number
        click_page_js = f"""
        (() => {{
            const li = Array.from(document.querySelectorAll('.pagination li')).find(el => el.innerText.trim() === '{p}');
            if (li) {{
                li.click();
                return 'CLICKED_PAGE';
            }}
            return 'NOT_FOUND';
        }})()
        """
        run_chrome_js(click_page_js)
        time.sleep(2.5)

        jobs = get_page_jobs()
        print(f"Found {len(jobs)} total jobs on page {p}.")

        tech_jobs = [j for j in jobs if is_tech_role(j.get('text', ''))]
        print(f"Matched {len(tech_jobs)} Software/Tech jobs on page {p}.")

        for job in tech_jobs:
            url = job.get('url')
            if not url:
                continue
            success, title = apply_to_job(url)
            if success:
                total_applied += 1
                confirmed.append(title)
                print(f"  --> Total Confirmed in Crawler: {total_applied}")
            time.sleep(1.5)

    print("\n==========================================================")
    print(f"CRAWLER COMPLETE. Total Submissions: {total_applied}")
    for idx, r in enumerate(confirmed, 1):
        print(f"  {idx}. {r}")
    print("==========================================================")

if __name__ == '__main__':
    crawl_pages(3, 8)
