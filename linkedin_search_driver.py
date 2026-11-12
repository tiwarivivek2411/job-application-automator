import subprocess
import json
import time
import Quartz
import sys

def run_tab_js(tab_idx, js_code):
    lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
    cleaned = ' '.join(lines).replace('\\', '\\\\').replace('"', '\\"')
    script = f'''
tell application "Google Chrome"
    set t to tab {tab_idx} of window 1
    return (execute t javascript "{cleaned}")
end tell
'''
    p = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    return out.strip(), err.strip()

def activate_chrome_tab(tab_idx):
    ascript = f'''
tell application "Google Chrome"
    activate
    set index of window 1 to 1
    set active tab index of window 1 to {tab_idx}
end tell
'''
    subprocess.run(['osascript', '-e', ascript])
    time.sleep(0.5)

def click_screen(x, y):
    move_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, move_event)
    time.sleep(0.1)
    down_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, down_event)
    time.sleep(0.1)
    up_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseUp, (x, y), Quartz.kCGMouseButtonLeft)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, up_event)
    time.sleep(0.5)

def solve_dialog(tab_idx=7):
    # Runs the multi-step form filler
    js_solve = '''
    (() => {
        const dialog = document.querySelector('dialog');
        if (!dialog) return JSON.stringify({status: 'no_dialog'});
        
        const text = dialog.innerText;
        
        // Check if application is already submitted / Done
        const submitDoneBtn = Array.from(dialog.querySelectorAll('button')).find(b => b.innerText.trim() === 'Done');
        if (submitDoneBtn) {
            submitDoneBtn.click();
            return JSON.stringify({status: 'submitted_done'});
        }
        
        // Find Submit application button
        const submitBtn = Array.from(dialog.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit application');
        if (submitBtn) {
            submitBtn.click();
            return JSON.stringify({status: 'clicked_submit'});
        }
        
        // Answer any visible inputs
        const inputs = Array.from(dialog.querySelectorAll('input, select, textarea'));
        for (const el of inputs) {
            const tag = el.tagName.toLowerCase();
            const type = (el.type || '').toLowerCase();
            const aria = (el.getAttribute('aria-label') || '').toLowerCase();
            const parent = (el.closest('div')?.innerText || '').toLowerCase();
            const label = (aria + ' ' + parent).replace(/\\s+/g, ' ');
            const isDatePicker = el.getAttribute('data-testid') === 'date-picker-input' || label.includes('date');
            
            if (type === 'radio') {
                const radioGroup = el.closest('fieldset, div');
                const groupText = (radioGroup ? radioGroup.innerText : '').toLowerCase();
                const optionLabel = (el.parentElement?.innerText || '').toLowerCase();
                
                if (groupText.includes('authorized') || groupText.includes('commute') || groupText.includes('relocate') || groupText.includes('on-site') || groupText.includes('hybrid') || groupText.includes('comfortable')) {
                    if (optionLabel.includes('yes') && !el.checked) {
                        el.click();
                    }
                } else if (groupText.includes('sponsorship') || groupText.includes('require visa') || groupText.includes('require sponsorship')) {
                    if (optionLabel.includes('no') && !el.checked) {
                        el.click();
                    }
                }
                continue;
            }
            
            if (tag === 'select') {
                if (label.includes('notice period') || label.includes('joining')) {
                    for (const opt of el.options) {
                        const ot = opt.text.toLowerCase();
                        if (ot.includes('immediate') || ot.includes('15') || ot.includes('1 month') || ot.includes('30')) {
                            el.value = opt.value;
                            el.dispatchEvent(new Event('change', { bubbles: true }));
                            break;
                        }
                    }
                } else if (label.includes('category') || label.includes('professional category')) {
                    for (const opt of el.options) {
                        if (opt.text.toLowerCase().includes('experienced')) {
                            el.value = opt.value;
                            el.dispatchEvent(new Event('change', { bubbles: true }));
                            break;
                        }
                    }
                } else if (label.includes('degree')) {
                    for (const opt of el.options) {
                        if (opt.text.toLowerCase().includes('bachelor') || opt.text.toLowerCase().includes('engineering')) {
                            el.value = opt.value;
                            el.dispatchEvent(new Event('change', { bubbles: true }));
                            break;
                        }
                    }
                }
                continue;
            }
            
            // Text inputs
            if (tag === 'input' && (type === 'text' || type === 'number' || !type)) {
                if (el.value && el.value.trim().length > 0) continue; // Already filled
                
                if (label.includes('linkedin')) {
                    el.value = 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/';
                } else if (label.includes('website') || label.includes('portfolio') || label.includes('github')) {
                    el.value = 'https://github.com/nileshtiwari';
                } else if (isDatePicker) {
                    el.value = '11/26/2026';
                } else if (label.includes('current ctc') || label.includes('current compensation') || label.includes('current salary') || label.includes('fixed comp')) {
                    el.value = '3500000';
                } else if (label.includes('expected ctc') || label.includes('expected compensation') || label.includes('expected salary')) {
                    el.value = '4200000';
                } else if (label.includes('variable') || label.includes('rsu') || label.includes('stocks')) {
                    el.value = '0';
                } else if (label.includes('notice period') || label.includes('notice') || label.includes('days to join')) {
                    el.value = '15';
                } else if (label.includes('experience') || label.includes('years')) {
                    if (label.includes('python')) el.value = '2';
                    else if (label.includes('node') || label.includes('aws') || label.includes('kafka') || label.includes('docker') || label.includes('kubernetes')) el.value = '3';
                    else el.value = '4';
                }
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
        
        // Click Next or Review
        const nextBtn = Array.from(dialog.querySelectorAll('button')).find(b => {
            const t = b.innerText.trim();
            return t === 'Next' || t === 'Review';
        });
        if (nextBtn) {
            nextBtn.click();
            return JSON.stringify({status: 'clicked_next', button: nextBtn.innerText.trim(), preview: text.substring(0, 100)});
        }
        
        return JSON.stringify({status: 'in_progress', preview: text.substring(0, 100)});
    })()
    '''
    out, err = run_tab_js(tab_idx, js_solve)
    try:
        return json.loads(out)
    except:
        return {'status': 'raw', 'out': out, 'err': err}

def complete_application(tab_idx=7, max_steps=8):
    for step in range(max_steps):
        time.sleep(1.0)
        res = solve_dialog(tab_idx)
        print(f"Step {step+1}: {res}")
        if res.get('status') == 'no_dialog':
            print("Dialog closed - finished!")
            return True
        if res.get('status') == 'submitted_done':
            print("Submitted and done clicked!")
            time.sleep(1.0)
            return True
        if res.get('status') == 'clicked_submit':
            print("Submit application clicked! Waiting for confirmation...")
            time.sleep(2.0)
            # Check for final done button
            res_done = solve_dialog(tab_idx)
            print("Post-submit check:", res_done)
            return True
    return False

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'
    if cmd == 'select':
        idx = int(sys.argv[2])
        js = f'''
        (() => {{
            const dismissBtns = Array.from(document.querySelectorAll('button[aria-label^="Dismiss "]')).filter(b => b.getAttribute('aria-label').endsWith('job'));
            const targetBtn = dismissBtns[{idx}];
            if (!targetBtn) return "card not found";
            const card = targetBtn.closest('li') || targetBtn.parentElement.parentElement.parentElement;
            const clickable = card.querySelector('a') || card;
            clickable.scrollIntoView({{behavior: "instant", block: "center"}});
            clickable.click();
            return "selected card " + {idx};
        }})()
        '''
        out, err = run_tab_js(7, js)
        print("Select result:", out, "Err:", err)
    elif cmd == 'detail':
        js = '''
        (() => {
            const h2 = document.querySelector('.job-details-jobs-unified-top-card__job-title, h1, h2');
            const title = h2 ? h2.innerText.trim() : 'no title';
            const easyApplyBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().includes('Easy Apply'));
            let r = null;
            if (easyApplyBtn) {
                const rect = easyApplyBtn.getBoundingClientRect();
                r = {left: rect.left, top: rect.top, width: rect.width, height: rect.height, text: easyApplyBtn.innerText.trim()};
            }
            return JSON.stringify({title, easyApplyBtn: r, winTop: window.screenTop, winLeft: window.screenLeft});
        })()
        '''
        out, err = run_tab_js(7, js)
        print("Detail result:", out)
    elif cmd == 'solve':
        res = complete_application(7)
        print("Solve result:", res)
