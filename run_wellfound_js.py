import subprocess

def run_js(js_code, filter_url="wellfound.com"):
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
    const matches = [];
    const elements = Array.from(document.querySelectorAll('a, button, span, div'));
    for (const el of elements) {
        if (el.children.length === 0 && el.innerText && el.innerText.trim() === 'Apply on Wellfound') {
            matches.push({
                tag: el.tagName,
                cls: el.className,
                pTag: el.parentElement ? el.parentElement.tagName : '',
                pCls: el.parentElement ? el.parentElement.className : ''
            });
        }
    }
    return JSON.stringify(matches);
})()
"""

out, err = run_js(js)
print("MATCHES:", out)
