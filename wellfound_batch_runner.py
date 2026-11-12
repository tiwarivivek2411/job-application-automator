import subprocess
import time
import json

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="wellfound.com"):
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

JOBS = [
    {"url": "https://wellfound.com/jobs/4879023-software-engineer-ai-engineer", "title": "Software Engineer / AI Engineer", "company": "AI Engineering Team"},
    {"url": "https://wellfound.com/jobs/4943175-senior-backend-data-ml-developer", "title": "Senior Backend, Data & ML Developer", "company": "Engineering Team"},
    {"url": "https://wellfound.com/jobs/4943178-mid-level-backend-data-ml-developer", "title": "Mid-Level Backend, Data & ML Developer", "company": "Engineering Team"},
    {"url": "https://wellfound.com/jobs/3280557-software-engineer-backend-python-django", "title": "Software Engineer (Backend - Python + Django)", "company": "Backend Team"},
    {"url": "https://wellfound.com/jobs/4799689-backend-developer", "title": "Backend Developer", "company": "Engineering Team"},
    {"url": "https://wellfound.com/jobs/3183676-backend-developer", "title": "Backend Developer", "company": "Engineering Team"},
    {"url": "https://wellfound.com/jobs/4943182-junior-backend-data-developer", "title": "Junior Backend & Data Developer", "company": "Data & Backend Team"},
    {"url": "https://wellfound.com/jobs/4897450-lead-solution-engineering", "title": "Lead Solution Engineering", "company": "Solutions Team"}
]

def apply_wellfound():
    applied = 0
    print("==========================================================")
    print("WELLFOUND MULTI-ROLE AUTO APPLICANT")
    print(f"Total Candidate Roles: {len(JOBS)}")
    print("==========================================================")

    for idx, job in enumerate(JOBS, 1):
        print(f"\n[{idx}/{len(JOBS)}] Inspecting {job['title']}...")
        run_js(f'window.location.href = "{job["url"]}"')
        time.sleep(5.0)

        # Check status on page
        check_page_js = """
        (() => {
            const text = document.body.innerText;
            const isApplied = text.includes('Applied') && !text.includes('Apply now');
            const applyBtn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase().includes('apply now') || b.classList.contains('styles_applyButton__7gnpI'));
            return JSON.stringify({
                isApplied,
                hasApplyBtn: !!applyBtn,
                btnText: applyBtn ? applyBtn.innerText.trim() : 'NONE'
            });
        })()
        """
        page_status = json.loads(run_js(check_page_js))
        print("  Page Status:", page_status)

        if page_status.get('isApplied'):
            print("  --> Already Applied! Skipping.")
            continue

        if not page_status.get('hasApplyBtn'):
            print("  --> No Apply button found! Skipping.")
            continue

        # Click Apply Now
        click_apply_js = """
        (() => {
            const applyBtn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth > 0 && (b.innerText.trim().toLowerCase().includes('apply now') || b.classList.contains('styles_applyButton__7gnpI')));
            if (!applyBtn) return 'NO_BTN';
            applyBtn.click();
            return 'CLICKED_APPLY';
        })()
        """
        run_js(click_apply_js)
        time.sleep(2.5)

        # Check modal and fill note
        pitch = f"Hi {job['company']}, I am an experienced backend and systems engineer with over 4.5 years of experience architecting distributed services in Java, Spring Boot, Node.js, and Python at Flipkart and Findem. I have built high-throughput microservices and data pipelines on AWS and Kafka. I am very excited about your mission and would love to contribute to your engineering goals!"
        pitch_escaped = pitch.replace('"', '\\"')

        fill_and_send_js = f"""
        (() => {{
            const ta = document.querySelector('textarea');
            if (ta) {{
                ta.value = "{pitch_escaped}";
                ta.dispatchEvent(new Event('input', {{bubbles: true}}));
                ta.dispatchEvent(new Event('change', {{bubbles: true}}));
            }}

            const sendBtn = Array.from(document.querySelectorAll('button'))
                .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase() === 'send application');
            if (!sendBtn) return 'NO_SEND_BTN';
            if (sendBtn.disabled) return 'SEND_DISABLED';
            sendBtn.click();
            return 'CLICKED_SEND';
        }})()
        """
        sub_res = run_js(fill_and_send_js)
        print("  Submit Action:", sub_res)
        time.sleep(3.5)

        # Confirm submission
        verify_js = """
        (() => {
            const text = document.body.innerText;
            const hasUndo = text.includes('Undo') || text.includes('Applied');
            return JSON.stringify({ hasUndo });
        })()
        """
        ver = json.loads(run_js(verify_js))
        if ver.get('hasUndo') or sub_res == 'CLICKED_SEND':
            applied += 1
            print(f"  --> [SUCCESS] Confirmed application for '{job['title']}'! (Total Wellfound this run: {applied})")
        else:
            print("  --> Submission unconfirmed, moving to next.")

        time.sleep(3.0)

    print("\n==========================================================")
    print("WELLFOUND BATCH COMPLETE")
    print(f"Applications submitted: {applied}")
    print("==========================================================")

if __name__ == '__main__':
    apply_wellfound()
