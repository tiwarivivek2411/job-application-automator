import subprocess
import json

def inspect_viewjob():
    ascript = '''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (URL of t as string) contains "indeed.com/viewjob" then
                    return (execute t javascript "(() => {
                        const btns = Array.from(document.querySelectorAll('button, a')).filter(b => b.innerText && b.innerText.toLowerCase().includes('apply'));
                        const h1 = document.querySelector('h1')?.innerText?.trim();
                        return JSON.stringify({
                            url: window.location.href,
                            title: document.title,
                            h1: h1,
                            applyBtns: btns.map(b => ({text: b.innerText.trim(), tag: b.tagName, id: b.id, className: b.className}))
                        });
                    })()")
                end if
            end repeat
        end repeat
        return "NO_TAB"
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(input=ascript.encode('utf-8'))
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

out, err = inspect_viewjob()
print("OUT:", out)
if err: print("ERR:", err)
