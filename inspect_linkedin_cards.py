import subprocess
import json

def run_tab_js(tab_idx, js_code):
    cleaned = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    script = f'''
tell application "Google Chrome"
    set t to tab {tab_idx} of window 1
    return (execute t javascript "{cleaned}")
end tell
'''
    p = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate()
    return out.strip(), err.strip()

js = """
(() => {
    const dismissBtns = Array.from(document.querySelectorAll('button[aria-label^="Dismiss "]')).filter(b => b.getAttribute('aria-label').endsWith('job'));
    const jobs = dismissBtns.map(b => {
        const label = b.getAttribute('aria-label');
        const title = label.replace(/^Dismiss /, '').replace(/ job$/, '');
        let card = b.closest('li') || b.parentElement.parentElement.parentElement;
        const link = card ? card.querySelector('a') : null;
        return {
            title: title,
            link: link ? link.href : null,
            cardText: card ? card.innerText.replace(/\\n/g, ' -- ') : null
        };
    });
    return JSON.stringify(jobs);
})()
"""

out, err = run_tab_js(7, js)
print(out)
if err: print('Err:', err)
