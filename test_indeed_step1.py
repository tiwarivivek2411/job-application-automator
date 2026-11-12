import subprocess
import json

def run_js(js_code, filter_url="indeed.com"):
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
    const inputs = Array.from(document.querySelectorAll('input')).filter(i => i.placeholder && i.placeholder.includes('select an option'));
    const info = [];
    inputs.forEach((inp, idx) => {
        let parent = inp.closest('div');
        info.push({
            idx: idx,
            id: inp.id,
            val: inp.value,
            parentHTML: inp.parentElement ? inp.parentElement.outerHTML : ''
        });
    });
    return JSON.stringify(info);
})()
"""

out, err = run_js(js)
print("OUT:", out)
print("ERR:", err)
