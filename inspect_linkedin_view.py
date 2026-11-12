import subprocess

def run_js(js_code, filter_url="linkedin.com"):
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
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        easyApplyBtn: Array.from(document.querySelectorAll('button')).filter(b => b.innerText && b.innerText.toLowerCase().includes('easy apply')).map(b => ({
            text: b.innerText.trim().replace(/\\n/g, ' '),
            cls: b.className,
            visible: b.offsetWidth > 0
        })),
        applyBtn: Array.from(document.querySelectorAll('button, a')).filter(b => b.innerText && b.innerText.toLowerCase().includes('apply')).map(b => ({
            tag: b.tagName,
            text: b.innerText.trim().replace(/\\n/g, ' '),
            cls: b.className
        })).slice(0, 5)
    });
})()
"""

out, err = run_js(js)
print(out)
