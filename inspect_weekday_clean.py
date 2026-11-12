import subprocess

def run_js(js_code, filter_url="weekday.works"):
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
    const btns = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
    const fastBtns = btns.filter(b => b.toLowerCase() === 'fast apply');
    return JSON.stringify({
        title: document.title,
        fastApplyCount: fastBtns.length,
        buttonsSnippet: btns.slice(0, 20)
    });
})()
"""

out, err = run_js(js)
print(out)
