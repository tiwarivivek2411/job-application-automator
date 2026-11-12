import subprocess
import time
import sys

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

def run_js(js_code, filter_url="instahyre.com"):
    escaped = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
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
    out, _ = exec_ascript(ascript)
    return out

def main():
    print("==========================================================")
    print("INSTAHYRE FULL SWEEP RUNNER (VISIBLE APPLICANT)")
    print("==========================================================")

    applied_total = 0
    skipped_total = 0

    for page in range(1, 5):
        print(f"\n==========================================")
        print(f"Processing Instahyre Page {page}...")
        print(f"==========================================")

        count_js = """
        (() => {
            const a = Array.from(document.querySelectorAll('a[ng-click*="openApplyModal"]'));
            return '' + a.length;
        })()
        """
        c_str = run_js(count_js)
        total_cards = int(c_str) if c_str.isdigit() else 0
        print(f"Found {total_cards} opportunity cards on Page {page}.")

        if total_cards == 0:
            print("No cards found. Reached end of opportunities.")
            break

        for idx in range(total_cards):
            open_card_js = f"""
            (() => {{
                const links = Array.from(document.querySelectorAll('a[ng-click*="openApplyModal"]'));
                if (links.length > {idx}) {{
                    links[{idx}].click();
                    return 'OPENED:' + links[{idx}].innerText.split('\\n')[0];
                }}
                return 'NOT_FOUND';
            }})()
            """
            card_res = run_js(open_card_js)
            print(f"\n[{idx+1}/{total_cards}] Opening: {card_res}")
            time.sleep(2.5)

            # Check visible buttons
            apply_js = """
            (() => {
                const wrap = document.querySelector('.application-modal-wrap');
                if (!wrap) return 'NO_MODAL';

                const already = Array.from(wrap.querySelectorAll('button, div, span'))
                    .some(e => e.offsetWidth > 0 && e.innerText && e.innerText.includes('Application Sent'));
                if (already) return 'ALREADY_SENT';

                const applyBtn = Array.from(wrap.querySelectorAll('button'))
                    .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase() === 'apply');
                if (applyBtn) {
                    applyBtn.click();
                    return 'CLICKED_APPLY';
                }

                const extBtn = Array.from(wrap.querySelectorAll('button'))
                    .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase().includes('apply on company site'));
                if (extBtn) return 'EXTERNAL_ONLY';

                return 'NO_APPLY_BTN';
            })()
            """
            app_res = run_js(apply_js)
            print(f"  Apply: {app_res}")
            time.sleep(2.0)

            # Close modal
            close_js = """
            (() => {
                const c = document.querySelector('.application-modal-close');
                if (c) { c.click(); return 'CLOSED'; }
                return 'NO_CLOSE';
            })()
            """
            run_js(close_js)
            time.sleep(1.5)

            if app_res == "CLICKED_APPLY":
                applied_total += 1
                print(f"  --> [SUCCESS] Application Sent! (Total on Instahyre: {applied_total})")
            else:
                skipped_total += 1
                print(f"  --> [SKIPPED]: {app_res}")

        # Navigate to next page
        next_page_js = """
        (() => {
            const nextBtn = Array.from(document.querySelectorAll('a, button'))
                .find(e => e.innerText && (e.innerText.trim().toLowerCase().includes('next') || e.innerText.trim() === '»'));
            if (nextBtn) {
                nextBtn.click();
                return 'CLICKED_NEXT';
            }
            return 'NO_NEXT_PAGE';
        })()
        """
        n_res = run_js(next_page_js)
        print(f"\nNext page status: {n_res}")
        if n_res != "CLICKED_NEXT":
            print("Completed all available pages on Instahyre.")
            break
        time.sleep(4.0)

    print("\n==========================================================")
    print("INSTAHYRE RUN COMPLETED!")
    print(f"Total Applied in Run: {applied_total}")
    print(f"Total Skipped: {skipped_total}")
    print("==========================================================")

if __name__ == '__main__':
    main()
