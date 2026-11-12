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

def get_job_urls_from_search(job_function="10", offset=0):
    # job_function 10 = Backend Development
    # job_function 11 = Full-Stack Development
    search_url = f"https://www.instahyre.com/search-jobs?company_size=0&isLandingPage=true&job_functions=%2Fapi%2Fv1%2Fjob_function%2F{job_function}&job_type=0&offset={offset}&search=true"
    print(f"Loading search page: offset={offset}...")
    run_chrome_js(f'window.location.href = "{search_url}";')
    time.sleep(3.5)

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
        data = json.loads(raw)
        return data
    except Exception as e:
        print("Error extracting search results:", e, raw[:200])
        return []

def apply_to_job(job_url):
    print(f"\nOpening job: {job_url}")
    run_chrome_js(f'window.location.href = "{job_url}";')
    time.sleep(2.5)

    # Check status
    check_js = """
    (() => {
        const text = document.body.innerText;
        const alreadyApplied = text.includes('Application sent!') || text.includes('You have applied') || text.includes('Applied on');
        const btn = document.querySelector("button[ng-click*='submitChoiceNonMatching']");
        const title = document.title;
        const h1 = document.querySelector('h1, h2, .job-title')?.innerText?.trim() || title;
        return JSON.stringify({
            title: h1,
            alreadyApplied,
            hasBtn: !!btn,
            btnDisabled: btn ? btn.disabled : true,
            btnText: btn ? btn.innerText.trim() : null
        });
    })()
    """
    raw_status = run_chrome_js(check_js)
    try:
        status = json.loads(raw_status)
    except Exception as e:
        print("  Error parsing status:", e, raw_status[:200])
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
    c_res = run_chrome_js(click_js)
    print("  Click Action:", c_res)
    time.sleep(2.0)

    # Verify
    verify_js = """
    (() => {
        const text = document.body.innerText;
        return JSON.stringify({
            confirmed: text.includes('Application sent!') || text.includes('Applied on')
        });
    })()
    """
    raw_ver = run_chrome_js(verify_js)
    try:
        ver = json.loads(raw_ver)
        if ver.get('confirmed'):
            print(f"  --> [SUCCESS] Confirmed application for '{role_title}'!")
            return True, role_title
    except Exception:
        pass

    print("  --> [WARN] Confirmation pending/unconfirmed.")
    return False, "UNCONFIRMED"

def run_instahyre_batch(max_applications=20):
    total_applied = 0
    confirmed_roles = []
    print("==========================================================")
    print("INSTAHYRE PARALLEL 1-CLICK STREAM APPLICANT")
    print(f"Target: Up to {max_applications} confirmed applications")
    print("==========================================================")

    # Functions to cycle: 10 = Backend Development, 11 = Full-Stack Development
    for fn in ["10", "11"]:
        if total_applied >= max_applications:
            break
        for offset in [0, 20, 40, 60]:
            if total_applied >= max_applications:
                break
            jobs = get_job_urls_from_search(job_function=fn, offset=offset)
            print(f"Found {len(jobs)} jobs at offset {offset} for function {fn}.")

            for job in jobs:
                if total_applied >= max_applications:
                    break
                url = job.get('url')
                if not url:
                    continue
                success, title = apply_to_job(url)
                if success:
                    total_applied += 1
                    confirmed_roles.append(title)
                    print(f"  --> Total Confirmed This Session: {total_applied}")
                time.sleep(2.0)

    print("\n==========================================================")
    print(f"INSTAHYRE SESSION COMPLETE. Total Submissions: {total_applied}")
    for idx, r in enumerate(confirmed_roles, 1):
        print(f"  {idx}. {r}")
    print("==========================================================")

if __name__ == '__main__':
    run_instahyre_batch(20)
