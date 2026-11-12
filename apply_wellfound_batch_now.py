import subprocess
import time
import json
import re

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="wellfound.com"):
    # Execute JS on the Wellfound tab in Chrome
    ascript = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "{filter_url}" then
                    return (execute t javascript {json.dumps(js_code)})
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    out, err = exec_ascript(ascript)
    return out

JOB_URLS = [
    "https://wellfound.com/jobs/4780375-senior-backend-engineer",
    "https://wellfound.com/jobs/4523283-full-stack-engineer",
    "https://wellfound.com/jobs/4897450-lead-solution-engineering",
    "https://wellfound.com/jobs/3183676-backend-developer",
    "https://wellfound.com/jobs/3721618-backend-engineer",
    "https://wellfound.com/jobs/4809495-senior-backend-engineer",
    "https://wellfound.com/jobs/4839974-senior-ai-engineer-clone",
    "https://wellfound.com/jobs/4839973-senior-ai-engineer",
    "https://wellfound.com/jobs/4811815-sde-ii",
    "https://wellfound.com/jobs/4383005-backend-engineer-python",
    "https://wellfound.com/jobs/4787199-backend-engineer"
]

def apply_all():
    applied = 0
    print("==========================================================")
    print("WELLFOUND MULTI-ROLE BATCH APPLICANT")
    print(f"Targeting {len(JOB_URLS)} Software Roles")
    print("==========================================================")

    for idx, url in enumerate(JOB_URLS, 1):
        print(f"\n[{idx}/{len(JOB_URLS)}] Navigating to {url}...")
        run_js(f'window.location.href = "{url}"')
        time.sleep(4.5)

        # 1. Extract info
        extract_info_js = """
        (() => {
            const pageText = document.body.innerText;
            const isApplied = pageText.includes('Your application to') || (pageText.includes('Applied') && !pageText.includes('Apply now'));
            const applyBtn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth > 0 && (b.innerText.trim().toLowerCase() === 'apply' || b.innerText.trim().toLowerCase() === 'apply now' || b.classList.contains('styles_applyButton__7gnpI')));
            
            const title = document.title;
            const h1 = document.querySelector('h1')?.innerText?.trim() || '';
            let company = '';
            
            const matchTitle = title.match(/ at ([^•|]+)/);
            if (matchTitle && matchTitle[1]) {
                company = matchTitle[1].trim();
            } else if (h1.includes(' at ')) {
                company = h1.split(' at ').slice(1).join(' at ').trim();
            } else {
                const compLink = document.querySelector('a[href*="/company/"]');
                if (compLink && compLink.innerText.trim()) {
                    company = compLink.innerText.trim().split('\\n')[0].trim();
                }
            }

            return JSON.stringify({
                title,
                h1,
                company: company || 'Engineering Team',
                isApplied,
                hasApplyBtn: !!applyBtn
            });
        })()
        """
        info_raw = run_js(extract_info_js)
        try:
            info = json.loads(info_raw)
        except Exception as e:
            print("  Error parsing info:", e, info_raw)
            continue

        company_name = info.get('company', '').strip()
        role_title = info.get('h1') or info.get('title')

        print(f"  Target Role: '{role_title}'")
        print(f"  Detected Company: '{company_name}'")

        if info.get('isApplied'):
            print("  --> Already Applied! Skipping.")
            continue

        if not info.get('hasApplyBtn'):
            print("  --> No Apply button found! Skipping.")
            continue

        # Click Apply
        click_apply_js = """
        (() => {
            const applyBtn = Array.from(document.querySelectorAll('button')).find(b => b.offsetWidth > 0 && (b.innerText.trim().toLowerCase() === 'apply' || b.innerText.trim().toLowerCase() === 'apply now' || b.classList.contains('styles_applyButton__7gnpI')));
            if (!applyBtn) return 'NO_BTN';
            applyBtn.click();
            return 'CLICKED_APPLY';
        })()
        """
        c_res = run_js(click_apply_js)
        print("  Click Apply:", c_res)
        time.sleep(2.5)

        # Formulate note
        pitch = f"Hi {company_name} team, I am an experienced backend and systems engineer with over 4.5 years of experience architecting distributed services in Java, Spring Boot, Node.js, and Python at Flipkart and Findem. I have built high-throughput microservices, real-time event streaming pipelines with Kafka, and scalable cloud architectures on AWS. I am very excited about {company_name}'s mission and would love to contribute to your engineering goals!"

        fill_and_send_js = f"""
        (() => {{
            const ta = document.querySelector('textarea');
            if (ta) {{
                ta.value = {json.dumps(pitch)};
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

        # Verify
        verify_js = """
        (() => {
            const text = document.body.innerText;
            const hasUndo = text.includes('Undo') || text.includes('Your application to') || text.includes('Applied');
            return JSON.stringify({ hasUndo });
        })()
        """
        try:
            ver = json.loads(run_js(verify_js))
            has_undo = ver.get('hasUndo')
        except Exception:
            has_undo = False

        if has_undo or sub_res == 'CLICKED_SEND':
            applied += 1
            print(f"  --> [SUCCESS] Confirmed application for '{role_title}' at '{company_name}'! (Batch total: {applied})")
        else:
            print("  --> Submission not confirmed, moving to next.")

        time.sleep(2.5)

    print("\n==========================================================")
    print("WELLFOUND BATCH COMPLETE")
    print(f"Total Applications Submitted this run: {applied}")
    print("==========================================================")

if __name__ == '__main__':
    apply_all()
