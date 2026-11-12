import subprocess
import time
import sys
import json
import base64

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="weekday.works"):
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
    out, err = exec_ascript(ascript)
    return out

def handle_rate_limit(curr_target_page):
    check_rl_js = """
    (() => {
        return window.location.href.includes('rate-limit') || document.body.innerText.includes('Too many requests');
    })()
    """
    if run_js(check_rl_js) == "true":
        print("\n[RATE LIMIT DETECTED] Pausing for 5 minutes cooldown...")
        for min_remaining in range(5, 0, -1):
            print(f"  Cooling down... {min_remaining} minutes remaining.")
            time.sleep(60)
        print("  Cooldown complete. Resuming...")
        run_js('window.location.href = "https://jobs.weekday.works/?jobsTab=fastApplysearch&candidateId=U2FsdGVkX1%2FE0bXnhkqN1ESSbY2keUlhdarlloDoTByAJmdIgguWqfZ%2FoujrcAmv"')
        time.sleep(6.0)
        for p in range(1, curr_target_page):
            print(f"  Advancing back to page {curr_target_page} (clicking Next on page {p})...")
            run_js("""
            (() => {
                const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim().toLowerCase() === 'next');
                if (nextBtn && !nextBtn.disabled) nextBtn.click();
            })()
            """)
            time.sleep(3.0)
        print(f"  Resumed on Page {curr_target_page}.")

def run_weekday_perfect_applicant(target_applications=50, start_page=2):
    print("==========================================================")
    print("WEEKDAY PERFECT SOFTWARE ROLES AUTO-APPLICANT")
    print(f"Target Submissions: {target_applications} Roles")
    print(f"Starting at Page: {start_page}")
    print("==========================================================")

    applied_count = 0
    skipped_count = 0
    applied_titles = {'Developer Education Engineer', 'Senior PEGA Developer'}

    # Check rate limit before starting
    handle_rate_limit(start_page)

    curr_p = start_page
    print(f"Ready to evaluate and apply starting on Page {curr_p}.")

    while applied_count < target_applications:
        handle_rate_limit(curr_p)

        find_next_role_js = f"""
        (() => {{
            function isTargetRole(title) {{
                if (!title) return false;
                const t = ' ' + title.toLowerCase().replace(/[-_\\/]/g, ' ') + ' ';

                const strictlyNonTech = [
                    'civil engineer', 'structural engineer', 'chemical engineer', 'petroleum',
                    'mining engineer', 'hvac engineer', 'plumbing', 'construction engineer',
                    'nurse', 'doctor', 'physician', 'dentist', 'pharmacist', 'hospital',
                    'cashier', 'store manager', 'retail sales', 'merchandiser', 'receptionist',
                    'telecaller', 'telesales', 'insurance agent', 'legal counsel', 'paralegal'
                ];
                for (const b of strictlyNonTech) {{
                    if (t.includes(b)) {{
                        const overrides = ['software', 'developer', 'programmer', 'devops', 'sde', 'swe'];
                        if (!overrides.some(o => t.includes(o))) return false;
                    }}
                }}

                const targetTokens = [
                    'software', 'engineer', 'developer', 'programmer', 'coder', 'architect',
                    'sde', 'swe', 'mts', 'smts', 'pmts', 'cmts', 'dmts', 'devops', 'sre', 'sysadmin',
                    'cloud', 'platform', 'infrastructure', 'systems', 'production engineer',
                    'release engineer', 'build engineer', 'network engineer', 'virtualization', 'mainframe',
                    'data', 'analytics', 'scientist', 'machine learning', 'ml', 'ai', 'deep learning',
                    'computer vision', 'nlp', 'mlops', 'dataops', 'dba', 'database',
                    'tech lead', 'technical lead', 'team lead', 'lead', 'staff', 'principal',
                    'distinguished', 'fellow', 'solutions', 'sales engineer', 'pre sales',
                    'forward deployed', 'fdse', 'customer engineer', 'field application', 'fae',
                    'implementation', 'professional services', 'tam', 'customer support engineer',
                    'technical support', 'escalation', 'devrel', 'developer relations', 'developer advocate',
                    'partner engineer', 'product manager', 'technical product', 'pm', 'tpm', 'gpm',
                    'product owner', 'program manager', 'project manager', 'intern', 'trainee', 'apprentice',
                    'associate', 'junior', 'front end', 'frontend', 'back end', 'backend', 'full stack',
                    'fullstack', 'web', 'mobile', 'ios', 'android', 'desktop', 'ui', 'api',
                    'integration', 'qa', 'sdet', 'test', 'verification', 'embedded', 'firmware',
                    'java', 'python', 'golang', 'node', 'react', 'cobol', 'sap', 'abap', 'guidewire',
                    'aem', 'sailpoint', 'oracle', 'wms', 'dot net', '.net', 'pega', 'mulesoft'
                ];

                return targetTokens.some(token => t.includes(token));
            }}

            const appliedTitles = new Set({json.dumps(list(applied_titles))});

            const unhandledBtns = Array.from(document.querySelectorAll('button'))
                .filter(b => b.innerText && b.innerText.trim().toLowerCase() === 'fast apply' && !b.getAttribute('data-agent-checked'));

            if (unhandledBtns.length === 0) return JSON.stringify({{status: 'PAGE_COMPLETE'}});

            for (const btn of unhandledBtns) {{
                btn.setAttribute('data-agent-checked', 'true');
                
                let card = btn.parentElement;
                let title = '';
                for (let i = 0; i < 6 && card; i++) {{
                    const h = card.querySelector('h1, h2, h3, h4, h5, h6, [class*="Role"], [class*="title"]');
                    if (h && h.innerText) {{
                        title = h.innerText.trim();
                        break;
                    }}
                    card = card.parentElement;
                }}

                if (appliedTitles.has(title)) {{
                    continue;
                }}

                const passes = isTargetRole(title);
                if (passes) {{
                    btn.scrollIntoView({{block: 'center'}});
                    btn.click();
                    return JSON.stringify({{status: 'OPENED_TARGET_ROLE', title: title}});
                }} else {{
                    return JSON.stringify({{status: 'SKIPPED_NON_TARGET', title: title}});
                }}
            }}

            return JSON.stringify({{status: 'PAGE_COMPLETE'}});
        }})()
        """
        raw_res = run_js(find_next_role_js)
        try:
            eval_data = json.loads(raw_res)
        except Exception:
            eval_data = {'status': 'ERROR', 'raw': raw_res}

        status = eval_data.get('status')
        title = eval_data.get('title', 'Unknown')

        if status == 'PAGE_COMPLETE':
            print(f"\nAll roles on Page {curr_p} evaluated. Advancing to next page...")
            click_next_js = """
            (() => {
                const nextBtn = Array.from(document.querySelectorAll('button'))
                    .find(b => b.innerText && b.innerText.trim().toLowerCase() === 'next');
                if (nextBtn && !nextBtn.disabled) {
                    nextBtn.click();
                    return 'CLICKED_NEXT';
                }
                return 'NO_NEXT';
            })()
            """
            next_res = run_js(click_next_js)
            if next_res == "CLICKED_NEXT":
                curr_p += 1
                print(f"--> Navigated to Page {curr_p}. Waiting 4.5s for render...")
                time.sleep(4.5)
                continue
            else:
                print("No more pages available on Weekday.")
                break

        elif status == 'SKIPPED_NON_TARGET':
            skipped_count += 1
            print(f"[SKIP Non-Target] '{title}'")
            continue

        elif status == 'OPENED_TARGET_ROLE':
            print(f"\n[{applied_count + 1}/{target_applications}] Matching Software/Tech Role: '{title}'")
            time.sleep(2.5)

            # In modal: fill custom questions and fields
            handle_questions_js = """
            (() => {
                const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
                if (!modal) return 'NO_MODAL';

                const company = modal.querySelector('[class*="Company"], [class*="employer"]')?.innerText?.trim() || 'the team';
                const textareas = Array.from(modal.querySelectorAll('textarea, input[type="text"]')).filter(i => i.offsetWidth > 0 && !i.value);
                
                for (const input of textareas) {
                    const label = (input.closest('div')?.innerText || input.placeholder || '').toLowerCase();
                    if (label.includes('why') || label.includes('interest') || label.includes('note') || label.includes('cover')) {
                        input.value = "I am deeply passionate about engineering robust backend systems and scalable architectures. With over 4.5 years of experience at Flipkart and Findem designing distributed services in Java, Go, and Python on AWS, I am excited by " + company + "'s mission and look forward to contributing to high-impact technical initiatives on your team.";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                        input.dispatchEvent(new Event('change', {bubbles: true}));
                    } else if (label.includes('notice')) {
                        input.value = "15 days";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                    } else if (label.includes('current ctc') || label.includes('current compensation') || label.includes('current salary') || label.includes('last drawn')) {
                        input.value = label.includes('lpa') ? "35" : "3500000";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                    } else if (label.includes('expected ctc') || label.includes('expected compensation') || label.includes('expected salary')) {
                        input.value = label.includes('lpa') ? "42" : "4200000";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                    } else if (label.includes('base') || label.includes('fixed')) {
                        input.value = label.includes('lpa') ? "28.75" : "2875000";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                    } else if (label.includes('bonus') || label.includes('variable')) {
                        input.value = label.includes('lpa') ? "2.5" : "250000";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                    } else if (label.includes('esop') || label.includes('equity') || label.includes('stock')) {
                        input.value = label.includes('lpa') ? "4" : "400000";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                    } else if (label.includes('experience') || label.includes('years')) {
                        input.value = "4.5";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                    } else if (label.includes('relocat')) {
                        input.value = "Yes";
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                    }
                }
                return 'QUESTIONS_HANDLED';
            })()
            """
            run_js(handle_questions_js)
            time.sleep(1.0)

            # Submit
            submit_modal_js = """
            (() => {
                const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
                if (!modal) return 'NO_MODAL';

                const subBtn = Array.from(modal.querySelectorAll('button'))
                    .find(b => b.innerText.trim().toLowerCase().includes('submit application'));
                if (!subBtn) {
                    const already = Array.from(modal.querySelectorAll('button, div, span'))
                        .some(e => e.innerText && e.innerText.toLowerCase().includes('already applied'));
                    if (already) return 'ALREADY_APPLIED';
                    return 'NO_SUBMIT_BUTTON';
                }
                if (subBtn.disabled) return 'SUBMIT_DISABLED';

                subBtn.click();
                return 'SUBMIT_SUCCESS';
            })()
            """
            sub_res = run_js(submit_modal_js)
            print(f"  Submit Result: {sub_res}")
            time.sleep(2.0)

            # Close modal
            close_js = """
            (() => {
                const modal = document.querySelector('[role="dialog"], .MuiModal-root, .MuiDialog-root');
                if (!modal) return 'NO_MODAL';
                const closeBtn = Array.from(modal.querySelectorAll('button'))
                    .find(b => b.innerText.trim().toLowerCase() === 'close' || b.getAttribute('aria-label') === 'close');
                if (closeBtn) {
                    closeBtn.click();
                    return 'CLOSED';
                }
                document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
                return 'ESCAPED';
            })()
            """
            run_js(close_js)
            time.sleep(1.0)

            if sub_res == 'SUBMIT_SUCCESS':
                applied_count += 1
                applied_titles.add(title)
                print(f"  --> [SUCCESS] Submitted application for '{title}'! (Total: {applied_count})")
            else:
                skipped_count += 1
                print(f"  --> [SKIPPED]: {sub_res}")

            # Pacing delay to avoid rate limit
            time.sleep(4.0)

        else:
            time.sleep(2.0)

    print("\n==========================================================")
    print("WEEKDAY PERFECT APPLICANT FINISHED")
    print(f"Target Software Roles Applied: {applied_count}")
    print(f"Non-Target Skipped: {skipped_count}")
    print("==========================================================")

if __name__ == '__main__':
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    start_page = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    run_weekday_perfect_applicant(target, start_page)
