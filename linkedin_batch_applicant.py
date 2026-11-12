import subprocess
import base64
import time
import json
import sys

def get_linkedin_tab_id():
    ascript = '''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "linkedin.com/jobs" then
                    return (id of t as string)
                end if
            end repeat
        end repeat
        return "NOT_FOUND"
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, _ = p.communicate(ascript)
    tab_id = out.strip()
    return int(tab_id) if tab_id.isdigit() else 33684268

TAB_ID = get_linkedin_tab_id()
print(f"Targeting LinkedIn Tab ID: {TAB_ID}")

def run_js(js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is {TAB_ID})
            return (execute javascript "eval(atob('{b64}'))")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

def solve_current_modal_step():
    js = '''
    (() => {
        const dialog = document.querySelector('dialog, [role="dialog"], .jobs-easy-apply-modal');
        if (!dialog) return JSON.stringify({status: 'no_dialog'});

        // Check if application is already done
        const doneBtn = Array.from(dialog.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Done');
        if (doneBtn) {
            doneBtn.click();
            return JSON.stringify({status: 'submitted_done'});
        }

        // Check if Submit application button is visible
        const submitBtn = Array.from(dialog.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Submit application');
        if (submitBtn) {
            submitBtn.click();
            return JSON.stringify({status: 'clicked_submit'});
        }

        const setInputVal = (el, val) => {
            const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
            const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
            if (setter) setter.call(el, val);
            else el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        };

        // 1. Radio / Fieldset questions
        const radios = Array.from(dialog.querySelectorAll('input[type="radio"]'));
        radios.forEach(r => {
            const aria = (r.getAttribute('aria-label') || '').toLowerCase();
            const fieldset = (r.closest('fieldset, div[role="radiogroup"], div')?.innerText || '').toLowerCase();
            const textToInspect = (aria + ' ' + fieldset).replace(/\\s+/g, ' ');
            const pText = (r.closest('div')?.innerText || '').trim().toLowerCase();

            const isSponsorship = textToInspect.includes('sponsorship') || textToInspect.includes('require visa') || textToInspect.includes('require a visa');
            const targetChoice = isSponsorship ? 'no' : 'yes';

            if (pText === targetChoice) {
                if (!r.checked) {
                    const labelOrP = r.parentElement?.querySelector('label') || r.closest('div')?.querySelector('p, label') || r;
                    labelOrP.click();
                    r.checked = true;
                    r.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        });

        // 2. Select dropdowns
        const selects = Array.from(dialog.querySelectorAll('select'));
        selects.forEach(sel => {
            const label = ((sel.closest('div')?.innerText || '') + ' ' + (sel.getAttribute('aria-label') || '')).toLowerCase();
            if (label.includes('notice period') || label.includes('joining') || label.includes('start date') || label.includes('availability')) {
                for (const opt of sel.options) {
                    const ot = opt.text.toLowerCase();
                    if (ot.includes('immediate') || ot.includes('15') || ot.includes('1 month') || ot.includes('30')) {
                        sel.value = opt.value;
                        sel.dispatchEvent(new Event('change', { bubbles: true }));
                        break;
                    }
                }
            } else if (label.includes('degree') || label.includes('education')) {
                for (const opt of sel.options) {
                    const ot = opt.text.toLowerCase();
                    if (ot.includes('bachelor') || ot.includes('engineering') || ot.includes('computer')) {
                        sel.value = opt.value;
                        sel.dispatchEvent(new Event('change', { bubbles: true }));
                        break;
                    }
                }
            }
        });

        // 3. Text & Number inputs
        const inputs = Array.from(dialog.querySelectorAll('input[type="text"], input[type="number"], input:not([type]), textarea'));
        inputs.forEach(el => {
            const aria = (el.getAttribute('aria-label') || '').toLowerCase();
            const parent = (el.closest('.fb-dash-form-element, fieldset, div')?.innerText || '').toLowerCase();
            const label = (aria + ' ' + parent).replace(/\\s+/g, ' ');

            if (label.includes('linkedin')) {
                setInputVal(el, 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
            } else if (label.includes('website') || label.includes('portfolio') || label.includes('github')) {
                setInputVal(el, 'https://github.com/nileshtiwari');
            } else if (label.includes('base') || label.includes('fixed') || label.includes('basic')) {
                setInputVal(el, label.includes('lpa') || label.includes('lakh') ? '28.75' : '2875000');
            } else if (label.includes('bonus') || label.includes('variable')) {
                setInputVal(el, label.includes('lpa') || label.includes('lakh') ? '2.5' : '250000');
            } else if (label.includes('esop') || label.includes('stock') || label.includes('equity')) {
                setInputVal(el, label.includes('lpa') || label.includes('lakh') ? '4' : '400000');
            } else if (label.includes('current ctc') || label.includes('current compensation') || label.includes('current salary') || label.includes('last drawn')) {
                setInputVal(el, label.includes('lpa') || label.includes('lakh') ? '35' : '3500000');
            } else if (label.includes('expected ctc') || label.includes('expected compensation') || label.includes('expected salary')) {
                setInputVal(el, label.includes('lpa') || label.includes('lakh') ? '42' : '4200000');
            } else if (label.includes('notice period') || label.includes('notice') || label.includes('days to join')) {
                setInputVal(el, '15');
            } else if (label.includes('experience') || label.includes('years')) {
                if (label.includes('python')) setInputVal(el, '2');
                else if (label.includes('node') || label.includes('aws') || label.includes('kafka') || label.includes('docker') || label.includes('kubernetes')) setInputVal(el, '3');
                else setInputVal(el, '4');
            } else if (label.includes('city') || label.includes('location')) {
                setInputVal(el, 'Bengaluru');
            } else if (label.includes('pincode') || label.includes('postal')) {
                setInputVal(el, '560103');
            }
        });

        // 4. Click Review or Next
        const revBtn = Array.from(dialog.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Review');
        if (revBtn) {
            revBtn.click();
            return JSON.stringify({status: 'clicked_review'});
        }

        const nextBtn = Array.from(dialog.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Next');
        if (nextBtn) {
            nextBtn.click();
            return JSON.stringify({status: 'clicked_next'});
        }

        return JSON.stringify({status: 'in_progress'});
    })()
    '''
    raw = run_js(js)
    try:
        return json.loads(raw)
    except:
        return {'status': 'raw', 'val': raw}

def discard_dialog():
    js = '''
    (() => {
        const dialog = document.querySelector('dialog, [role="dialog"], .jobs-easy-apply-modal');
        if (!dialog) return 'no_dialog';
        const closeBtn = dialog.querySelector('button[aria-label="Dismiss"], button[aria-label="Close"], button.artdeco-modal__dismiss');
        if (closeBtn) closeBtn.click();
        
        setTimeout(() => {
            const discardBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Discard');
            if (discardBtn) discardBtn.click();
        }, 500);
        return 'DISCARDED';
    })()
    '''
    run_js(js)
    time.sleep(1.0)

def apply_to_card(title, company):
    # Click Easy Apply button
    click_apply_js = '''
    (() => {
        const btn = document.querySelector('button[aria-label^="Easy Apply"]') || 
                    Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Easy Apply');
        if (btn) {
            btn.click();
            return 'CLICKED';
        }
        return 'NO_BTN';
    })()
    '''
    status = run_js(click_apply_js)
    if status != 'CLICKED':
        print(f"  Easy Apply button not found for '{title}'. Skipping.")
        return False

    time.sleep(2.0)

    # Solve modal steps (up to 8 steps)
    for step in range(1, 9):
        res = solve_current_modal_step()
        st = res.get('status')
        if st == 'no_dialog':
            print(f"  SUCCESS: Applied to '{title}' at '{company}'! (Modal completed)")
            return True
        elif st == 'submitted_done':
            print(f"  SUCCESS: Applied to '{title}' at '{company}'! (Submitted & Done)")
            time.sleep(1.0)
            return True
        elif st == 'clicked_submit':
            time.sleep(2.5)
            # Handle post-submit dialog
            solve_current_modal_step()
            print(f"  SUCCESS: Applied to '{title}' at '{company}'! (Clicked submit)")
            time.sleep(1.0)
            return True
        elif st in ['clicked_next', 'clicked_review']:
            time.sleep(1.5)
        else:
            time.sleep(1.2)

    print(f"  STUCK: Discarding '{title}'...")
    discard_dialog()
    return False

def get_unapplied_cards():
    js = '''
    (() => {
        const cards = Array.from(document.querySelectorAll('div[componentkey^="job-card-component-ref"]'));
        const seen = new Set();
        const results = [];
        cards.forEach((c, idx) => {
            const isApplied = c.innerText.includes('Applied') || c.innerText.includes('Application submitted');
            const lines = c.innerText.split('\\n').map(l => l.trim()).filter(Boolean);
            const title = lines[0] || '';
            const company = lines[1] || '';
            const key = title + '|' + company;
            if (!seen.has(key)) {
                seen.add(key);
                results.push({
                    idx: idx,
                    title: title,
                    company: company,
                    isApplied: isApplied
                });
            }
        });
        return JSON.stringify(results);
    })()
    '''
    raw = run_js(js)
    try:
        return json.loads(raw)
    except:
        return []

def main():
    print("==========================================================")
    print("LINKEDIN EASY APPLY AUTOMATED ROLES APPLICANT")
    print("==========================================================")

    cards = get_unapplied_cards()
    print(f"Found {len(cards)} unique job cards on current page.")

    applied_count = 0
    for card in cards:
        title = card['title']
        company = card['company']
        is_applied = card['isApplied']

        if is_applied:
            print(f"[SKIP Applied] '{title}' at '{company}'")
            continue

        print(f"\nEvaluating: '{title}' at '{company}'...")
        # Click the card
        click_js = f'''
        (() => {{
            const cards = Array.from(document.querySelectorAll('div[componentkey^="job-card-component-ref"]'));
            const c = cards[{card['idx']}];
            if (!c) return 'NOT_FOUND';
            c.scrollIntoView({{behavior: 'instant', block: 'center'}});
            c.click();
            return 'CLICKED';
        }})()
        '''
        run_js(click_js)
        time.sleep(2.0)

        # Check if Easy Apply is available
        check_js = '''
        (() => {
            const hasEasyApply = !!(document.querySelector('button[aria-label^="Easy Apply"]') || 
                                   Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').trim() === 'Easy Apply'));
            const isAlreadyApplied = (document.body.innerText.includes('Application submitted') || document.body.innerText.includes('Applied'));
            return JSON.stringify({hasEasyApply, isAlreadyApplied});
        })()
        '''
        raw_chk = run_js(check_js)
        try:
            chk = json.loads(raw_chk)
        except:
            chk = {'hasEasyApply': False, 'isAlreadyApplied': False}

        if chk.get('isAlreadyApplied'):
            print(f"  [Already Applied] '{title}' at '{company}'")
            continue

        if not chk.get('hasEasyApply'):
            print(f"  [No Easy Apply] '{title}' at '{company}' (External application)")
            continue

        print(f"  --> Launching Easy Apply for '{title}'...")
        if apply_to_card(title, company):
            applied_count += 1
            print(f"  --> [SUCCESS COUNT: {applied_count}]")
            time.sleep(2.0)
        else:
            time.sleep(1.0)

    print("\n==========================================================")
    print(f"LINKEDIN BATCH RUN COMPLETE! Total Submitted: {applied_count}")
    print("==========================================================")

if __name__ == '__main__':
    main()
