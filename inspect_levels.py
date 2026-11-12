import subprocess
import urllib.parse
import json

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

code = """
(() => {
    let select = document.querySelector('.MuiSelect-select');
    if (select) select.click();
    setTimeout(() => {
        let items = Array.from(document.querySelectorAll('li[role="option"]')).map(li => li.innerText);
        window.__currencyOptions = items;
    }, 300);
    return "CLICKED";
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
exec_ascript(ascript)

import time
time.sleep(1)

code2 = """
(() => {
    let options = window.__currencyOptions || [];
    // Also check if menu is open
    let menuItems = Array.from(document.querySelectorAll('li[role="option"]')).map(li => li.innerText);
    return JSON.stringify(menuItems.length ? menuItems : options);
})()
"""
cleaned2 = ' '.join([l.strip() for l in code2.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript2 = f'''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (URL of t as string) contains "levels.fyi" then
                return (execute t javascript "{cleaned2}")
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''
out, _ = exec_ascript(ascript2)
print("Options:", out)
