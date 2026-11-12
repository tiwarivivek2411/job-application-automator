import subprocess
import urllib.parse
import json
import time
import requests
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_chrome_js(js_code, filter_url="talent500.com"):
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

def get_auth_token():
    cookie_raw = run_chrome_js("(() => encodeURIComponent(document.cookie))()")
    if not cookie_raw or cookie_raw == "NO_TAB":
        raise Exception("Talent500 tab not found in Chrome")
    cookie_str = urllib.parse.unquote(cookie_raw)
    cookies = dict(item.strip().split("=", 1) for item in cookie_str.split(";") if "=" in item)
    auth_token = cookies.get("authToken")
    if not auth_token:
        raise Exception("authToken cookie not found on Talent500")
    return urllib.parse.unquote(auth_token)

TECH_KEYWORDS = [
    'software', 'engineer', 'developer', 'backend', 'frontend', 'full-stack', 'fullstack',
    'platform', 'systems', 'distributed', 'sde', 'architect', 'devops', 'sre', 'cloud',
    'java', 'python', 'golang', 'node', 'react', 'data engineer', 'ai', 'ml', 'machine learning',
    'infrastructure', 'microservices', 'lead', 'staff', 'principal'
]

EXCLUDE_KEYWORDS = [
    'sales', 'account manager', 'marketing', 'recruiter', 'hr', 'talent acquisition',
    'business development', 'b2b sales', 'executive assistant', 'telecaller', 'customer service'
]

def is_matching_role(title):
    t = title.lower()
    if any(ex in t for ex in EXCLUDE_KEYWORDS):
        return False
    return any(kw in t for kw in TECH_KEYWORDS)

def get_applied_job_ids(headers):
    applied_ids = set()
    offset = 0
    limit = 50
    while True:
        url = f"https://prod-warmachine.talent500.co/api/candidate_jobs/?offset={offset}&limit={limit}"
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            break
        data = r.json()
        items = data.get("data", [])
        if not items:
            break
        for item in items:
            job_obj = item.get("job")
            if isinstance(job_obj, dict) and "id" in job_obj:
                applied_ids.add(job_obj["id"])
            elif isinstance(job_obj, str):
                applied_ids.add(job_obj)
            if "job_id" in item:
                applied_ids.add(item["job_id"])
        if len(items) < limit:
            break
        offset += limit
    return applied_ids

def apply_talent500(target_count=35):
    print(f"=== Starting Talent500 Cursor-Paginated Stream (Target: {target_count}) ===")
    token = get_auth_token()
    print("Found active Talent500 Bearer Token.")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://talent500.com",
        "Referer": "https://talent500.com/",
        "Authorization": token
    }

    applied_ids = get_applied_job_ids(headers)
    print(f"Initial applied jobs count in candidate profile: {len(applied_ids)}")

    search_terms = ["Software Engineer", "Backend", "Full Stack", "Platform", "Python", "Java", "Cloud"]
    submitted_count = 0
    successful_jobs = []

    for term in search_terms:
        if submitted_count >= target_count:
            break
        print(f"\n--- Searching term: '{term}' ---")
        search_after = None
        empty_pages = 0

        while submitted_count < target_count and empty_pages < 3:
            if search_after:
                sa_str = urllib.parse.quote(json.dumps(search_after))
                search_url = f"https://prod-warmachine.talent500.co/api/v3/jobs/search/?search_term={urllib.parse.quote(term)}&search_after={sa_str}&limit=20&is_leadership_job=false"
            else:
                search_url = f"https://prod-warmachine.talent500.co/api/v3/jobs/search/?search_term={urllib.parse.quote(term)}&offset=0&limit=20&is_leadership_job=false"

            try:
                res = requests.get(search_url, headers=headers, timeout=10)
                if res.status_code != 200:
                    print(f"Search request failed with status {res.status_code}")
                    break
                data = res.json()
                jobs = data.get("data", [])
                search_after = data.get("search_after")

                if not jobs:
                    empty_pages += 1
                    continue

                for job in jobs:
                    if submitted_count >= target_count:
                        break
                    job_id = job.get("id")
                    title = job.get("title_alias_1") or job.get("title") or "Unknown Title"
                    company_name = job.get("company", {}).get("name") if isinstance(job.get("company"), dict) else "Unknown Company"
                    location = job.get("location") or "Remote / India"

                    if not job_id or job_id in applied_ids:
                        continue

                    if not is_matching_role(title):
                        continue

                    # Apply via candidate_jobs endpoint
                    apply_url = "https://prod-warmachine.talent500.co/api/candidate_jobs/"
                    payload = {
                        "job": job_id,
                        "status": "AP",
                        "privacy_policy_status": True,
                        "source": "T500-Direct",
                        "sourcer": "T500-Direct",
                        "is_int_candidate": False
                    }

                    try:
                        app_res = requests.post(apply_url, headers=headers, json=payload, timeout=10)
                        if app_res.status_code in [200, 201]:
                            app_data = app_res.json()
                            app_id = app_data.get("id")
                            applied_ids.add(job_id)
                            submitted_count += 1
                            log_entry = {
                                "count": submitted_count,
                                "company": company_name,
                                "title": title,
                                "location": location,
                                "application_id": app_id,
                                "job_id": job_id
                            }
                            successful_jobs.append(log_entry)
                            print(f"[{submitted_count}/{target_count}] [CONFIRMED] Applied to '{company_name}' - '{title}' ({location}) -> App ID: {app_id}")
                            time.sleep(1.5)
                        elif app_res.status_code == 400 and "already applied" in app_res.text.lower():
                            applied_ids.add(job_id)
                        else:
                            print(f"[FAILED] Could not apply to '{title}' at '{company_name}': {app_res.status_code} - {app_res.text[:100]}")
                    except Exception as e:
                        print(f"Error applying to job {job_id}: {e}")

                if not search_after:
                    break
            except Exception as e:
                print(f"Error fetching search page: {e}")
                break

    print(f"\n=== Talent500 Stream Complete! Successfully Submitted: {submitted_count} jobs ===")
    return successful_jobs

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 35
    apply_talent500(count)
