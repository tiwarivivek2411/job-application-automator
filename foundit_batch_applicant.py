import subprocess, base64, time, json, sys

TAB_ID = 33684127

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

def is_software_role(title):
    t = title.lower()
    # Reject non-software or intern
    if any(neg in t for neg in ['intern', 'marketing', 'sales', 'hr', 'recruiter', 'designer', 'content', 'telecaller']):
        return False
    # Accept software engineering roles
    if any(pos in t for pos in ['developer', 'engineer', 'backend', 'full stack', 'fullstack', 'software', 'java', 'python', 'sde', 'architect']):
        return True
    return False

def apply_current_page():
    # Get all cards on page
    cards_js = '''
    (() => {
        var cards = Array.from(document.querySelectorAll('.cardContainer'));
        return JSON.stringify(cards.map((c, i) => {
            var title = c.querySelector('.jobTitle');
            var comp = c.querySelector('.companyName');
            return {
                index: i,
                id: c.id,
                title: title ? title.innerText.trim() : '',
                company: comp ? comp.innerText.trim() : ''
            };
        }));
    })()
    '''
    raw = run_js(cards_js)
    try:
        cards = json.loads(raw)
    except Exception as e:
        print(f"Error parsing cards: {e}")
        return []

    applied_jobs = []
    print(f"Found {len(cards)} cards on this page.")

    for c in cards:
        idx = c['index']
        title = c['title']
        comp = c['company']

        if not is_software_role(title):
            print(f"  [{idx}] SKIP non-software: {title}")
            continue

        # Click card to open detail pane
        click_card_js = f'''
        (() => {{
            var cards = Array.from(document.querySelectorAll('.cardContainer'));
            if (cards[{idx}]) {{
                cards[{idx}].scrollIntoView({{behavior: 'smooth', block: 'center'}});
                cards[{idx}].click();
                return 'CLICKED';
            }}
            return 'NOT_FOUND';
        }})()
        '''
        res = run_js(click_card_js)
        if res != 'CLICKED':
            print(f"  [{idx}] Failed to click card")
            continue

        time.sleep(1.0)

        # Check apply button status
        check_btn_js = '''
        (() => {
            var btn = Array.from(document.querySelectorAll('#applyNowBtn')).find(b => b.offsetWidth > 0);
            return btn ? btn.innerText.trim() : 'NO_BTN';
        })()
        '''
        btn_text = run_js(check_btn_js)

        if btn_text == 'Applied':
            print(f"  [{idx}] ALREADY APPLIED: {title} @ {comp}")
            continue
        elif btn_text == 'Apply Now':
            # Click apply now
            click_apply_js = '''
            (() => {
                var btn = Array.from(document.querySelectorAll('#applyNowBtn')).find(b => b.offsetWidth > 0);
                if (btn) {
                    btn.click();
                    return 'CLICKED_APPLY';
                }
                return 'NO_BTN';
            })()
            '''
            res_apply = run_js(click_apply_js)
            time.sleep(1.5)

            # Re-check status
            after_text = run_js(check_btn_js)
            if after_text == 'Applied':
                print(f"  [{idx}] SUCCESS: Applied to {title} @ {comp}")
                applied_jobs.append({'title': title, 'company': comp, 'id': c['id']})
            else:
                # Check if an external link / modal opened
                print(f"  [{idx}] NOT APPLIED (Status: {after_text}): {title} @ {comp}")
        else:
            print(f"  [{idx}] Button status '{btn_text}': {title} @ {comp}")

    return applied_jobs

def go_next_page():
    next_js = '''
    (() => {
        var rightArrow = document.querySelector('.pagination .arrow-right');
        if (rightArrow && !rightArrow.classList.contains('disabled')) {
            rightArrow.click();
            return 'CLICKED_NEXT';
        }
        return 'NO_NEXT';
    })()
    '''
    res = run_js(next_js)
    return res == 'CLICKED_NEXT'

def main():
    total_applied = []
    max_pages = 5
    for page in range(1, max_pages + 1):
        print(f"\n=== PROCESSING PAGE {page} ===")
        applied = apply_current_page()
        total_applied.extend(applied)
        print(f"Page {page} finished. Total new applications so far: {len(total_applied)}")

        if page < max_pages:
            print("Navigating to next page...")
            if go_next_page():
                time.sleep(3.0)
            else:
                print("No more pages available.")
                break

    print(f"\n==========================================")
    print(f"FOUNDIT BATCH COMPLETE! Total Applied: {len(total_applied)}")
    for j in total_applied:
        print(f" - {j['title']} @ {j['company']} (ID: {j['id']})")
    print(f"==========================================")

if __name__ == '__main__':
    main()
