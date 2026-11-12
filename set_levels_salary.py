import subprocess

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

code = """
(() => {
    function setReactVal(el, val) {
        let lastVal = el.value;
        el.value = val;
        let event = new Event('input', { bubbles: true });
        // React 16+ tracker
        let tracker = el._valueTracker;
        if (tracker) {
            tracker.setValue(lastVal);
        }
        el.dispatchEvent(event);
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }
    
    let baseInp = document.getElementById('minBaseSalary');
    let compInp = document.getElementById('minTotalCompensation');
    
    if (baseInp) setReactVal(baseInp, '90000');
    if (compInp) setReactVal(compInp, '110000');
    
    return JSON.stringify({
        baseVal: baseInp ? baseInp.value : 'NO_BASE',
        compVal: compInp ? compInp.value : 'NO_COMP'
    });
})()
"""

cleaned = ' '.join([l.strip() for l in code.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript = f'''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "levels.fyi" then
                return (execute t javascript "{cleaned}")
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''
out, _ = exec_ascript(ascript)
print(out)
