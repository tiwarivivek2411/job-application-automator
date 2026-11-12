import subprocess

def run_js(js_code, filter_url="wellfound.com"):
    # Strip any comment lines to avoid commenting out minified JS
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
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=ascript.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

js = """
(() => {
    const res = {};
    res.url = window.location.href;
    res.title = document.title;
    
    // Find all job listings or apply buttons
    const applyBtns = Array.from(document.querySelectorAll('button, a'))
        .filter(b => b.innerText && (b.innerText.toLowerCase().includes('apply') || b.innerText.toLowerCase().includes('quick apply') || b.innerText.toLowerCase().includes('easy apply')))
        .map(b => ({tag: b.tagName, text: b.innerText.trim(), cls: b.className}));
    res.applyBtns = applyBtns;

    // Find job cards
    const cards = Array.from(document.querySelectorAll('[data-test="JobListing"], .styles_jobListing__2m4y_, [class*="JobListing"], [class*="styles_component__"]'))
        .slice(0, 10)
        .map(c => c.innerText.replace(/\\n/g, ' | ').slice(0, 150));
    res.cards = cards;

    return JSON.stringify(res);
})()
"""

out, err = run_js(js)
print(out)
