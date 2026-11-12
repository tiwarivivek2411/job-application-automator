import subprocess
import time
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="naukri.com"):
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

def apply_naukri_batches(target_batches=4):
    print("==========================================================")
    print(f"NAUKRI MULTI-APPLY BATCH RUNNER (Target: {target_batches * 5} jobs)")
    print("==========================================================")

    # First ensure we are on recommendedjobs
    nav_js = 'window.location.href = "https://www.naukri.com/mnjuser/recommendedjobs"'
    run_js(nav_js)
    time.sleep(4.5)

    total_submitted = 0

    for batch_num in range(1, target_batches + 1):
        print(f"\n--- Batch {batch_num}/{target_batches} ---")
        
        # Select up to 5 software roles
        select_js = """
        (() => {
            function isSoftwareRole(title) {
                if (!title) return false;
                const t = title.toLowerCase();
                const blocked = [
                    'sales', 'marketing', 'product owner', 'product manager', 'hr',
                    'recruiter', 'business analyst', 'operations', 'content', 'designer'
                ];
                if (blocked.some(b => t.includes(b))) return false;
                const allowed = [
                    'software', 'developer', 'backend', 'full stack', 'fullstack',
                    'devops', 'sde', 'engineer', 'architect', 'data engineer',
                    'programmer', 'tech lead', 'qa', 'sdet'
                ];
                return allowed.some(a => t.includes(a));
            }

            const articles = Array.from(document.querySelectorAll('article.jobTuple'));
            let selected = 0;
            const selectedList = [];

            for (const art of articles) {
                if (selected >= 5) break;
                const titleEl = art.querySelector('a.title, .title');
                const title = titleEl ? titleEl.innerText.trim() : '';
                const comp = art.querySelector('.comp-name, [class*="comp-name"]')?.innerText.trim() || '';

                if (isSoftwareRole(title)) {
                    const cb = art.querySelector('input.tuple-check-input');
                    const label = art.querySelector('label.tuple-check-box');
                    if (cb && !cb.checked && label) {
                        label.click();
                        selected++;
                        selectedList.push(title + ' (' + comp + ')');
                    } else if (cb && cb.checked) {
                        selected++;
                        selectedList.push(title + ' (' + comp + ')');
                    }
                }
            }

            return JSON.stringify({
                selected,
                selectedList,
                btnDisabled: document.querySelector('.multi-apply-button')?.disabled
            });
        })()
        """
        sel_res = run_js(select_js)
        print(f"Selection Result: {sel_res}")

        try:
            import json
            data = json.loads(sel_res)
            count = data.get('selected', 0)
        except Exception:
            count = 0

        if count == 0:
            print("No more selectable software roles on current view.")
            break

        time.sleep(2.0)

        # Click Multi-Apply
        click_apply_js = """
        (() => {
            const btn = document.querySelector('.multi-apply-button');
            if (!btn || btn.disabled) return 'CANNOT_CLICK';
            btn.click();
            return 'CLICKED_APPLY';
        })()
        """
        click_res = run_js(click_apply_js)
        print(f"Apply Button: {click_res}")

        time.sleep(4.0)

        total_submitted += count
        print(f"--> [SUCCESS] Batch {batch_num} Submitted {count} jobs! (Total on Naukri: {total_submitted})")

        # Reload for next batch
        run_js('window.location.href = "https://www.naukri.com/mnjuser/recommendedjobs"')
        print("Reloading recommended jobs, waiting 5.0s...")
        time.sleep(5.0)

    print("\n==========================================================")
    print("NAUKRI RUN COMPLETE")
    print(f"Total Applications Submitted this run: {total_submitted}")
    print("==========================================================")

if __name__ == '__main__':
    batches = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    apply_naukri_batches(batches)
