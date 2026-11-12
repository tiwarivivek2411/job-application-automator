import subprocess
import urllib.parse

def exec_ascript(script_str):
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=script_str.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

code = """
(() => {
    return JSON.stringify({
        url: window.location.href,
        title: document.title,
        bodyText: document.body.innerText.slice(0, 1000)
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
