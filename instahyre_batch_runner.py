import subprocess
import time
import sys
import re

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="instahyre.com"):
    # Strip any comment lines to avoid commenting out minified JS
    cleaned_lines = []
    for line in js_code.split('\n'):
        line = line.strip()
        if not line or line.startswith('//'):
            continue
        cleaned_lines.append(line)
    single_line = ' '.join(cleaned_lines)
    escaped = single_line.replace('\\', '\\\\').replace('"', '\\"')

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

def run_instahyre_batch(max_jobs=35):
    print("==========================================================")
    print(f"INSTAHYRE CLEAN STREAMLINED AUTO-APPLY (Target: {max_jobs})")
    print("==========================================================")

    applied_count = 0
    skipped_count = 0

    for step in range(1, max_jobs + 1):
        open_next_js = """
        (() => {
            const blocks = Array.from(document.querySelectorAll('.employer-block:not([data-agent-handled="true"])'));
            if (blocks.length === 0) return 'NO_MORE_BLOCKS';
            
            const b = blocks[0];
            b.setAttribute('data-agent-handled', 'true');
            
            const fullTitle = (b.innerText || '').split('\\n')[0].trim();
            const link = b.querySelector('a[ng-click*="openApplyModal"]') || 
                         Array.from(b.querySelectorAll('a, button')).find(e => e.innerText && e.innerText.includes('View job'));
            if (!link) return 'NO_LINK:' + fullTitle;
            
            link.click();
            return 'OPENED:' + fullTitle;
        })()
        """
        open_res = run_js(open_next_js)
        print(f"\n[{step}/{max_jobs}] {open_res}")

        if open_res == "NO_MORE_BLOCKS":
            print("  No more unhandled blocks on current view. Checking for Next page...")
            next_page_js = """
            (() => {
                const nextBtn = Array.from(document.querySelectorAll('a, button'))
                    .find(e => e.innerText && (e.innerText.trim().toLowerCase().includes('next') || e.innerText.trim() === '»'));
                if (nextBtn && !nextBtn.parentElement.classList.contains('disabled')) {
                    nextBtn.click();
                    return 'CLICKED_NEXT';
                }
                return 'NO_NEXT';
            })()
            """
            next_res = run_js(next_page_js)
            if next_res == "CLICKED_NEXT":
                print("  Clicked Next Page, waiting 4s...")
                time.sleep(4.0)
                continue
            else:
                print("  Finished all available blocks/pages on Instahyre.")
                break

        time.sleep(2.5)

        modal_action_js = """
        (() => {
            const wrap = document.querySelector('.application-modal-wrap');
            if (!wrap) return 'NO_MODAL';

            const wrapText = wrap.innerText || '';
            if (wrapText.includes('Share  on social profile') || wrapText.includes('Want to move your application to the top')) {
                return 'ALREADY_SUBMITTED_SHARE';
            }
            if (wrapText.includes('Application Sent')) {
                return 'ALREADY_SENT';
            }

            const applyBtn = Array.from(wrap.querySelectorAll('button'))
                .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase() === 'apply');
            if (applyBtn) {
                applyBtn.click();
                return 'CLICKED_APPLY';
            }

            const extBtn = Array.from(wrap.querySelectorAll('button, a'))
                .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase().includes('apply on company site'));
            if (extBtn) {
                return 'EXTERNAL_REDIRECT';
            }

            return 'UNKNOWN_STATE';
        })()
        """
        modal_res = run_js(modal_action_js)
        print(f"  Modal Action: {modal_res}")

        time.sleep(2.0)

        close_modal_js = """
        (() => {
            const c = document.querySelector('.application-modal-close') || document.querySelector('.close');
            if (c) { c.click(); return 'CLOSED'; }
            return 'NO_CLOSE';
        })()
        """
        run_js(close_modal_js)
        time.sleep(1.0)

        if "CLICKED_APPLY" in modal_res or "ALREADY_SUBMITTED_SHARE" in modal_res:
            applied_count += 1
            print(f"  --> [SUCCESS] Submitted application! (Batch total: {applied_count})")
        else:
            skipped_count += 1
            print(f"  --> [SKIPPED]: {modal_res}")

        time.sleep(1.5)

    print("\n==========================================================")
    print("INSTAHYRE RUN COMPLETED")
    print(f"Total Applied this batch: {applied_count}")
    print(f"Total Skipped: {skipped_count}")
    print("==========================================================")

if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 35
    run_instahyre_batch(limit)
