import subprocess
import time

ascript = '''
tell application "Google Chrome"
    repeat with w in windows
        repeat with t in tabs of w
            if (id of t as string) is "33684123" then
                return (execute t javascript "(() => {
                    const btn = document.querySelector('button[data-testid=\\"30e6dd3d81aa4705705e2ef002ff579b59e06fe7bbe5e8efa2e5839926f47369\\"]') || Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase() === 'continue');
                    if (!btn) return 'no btn';
                    btn.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true, view: window}));
                    btn.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true, view: window}));
                    btn.click();
                    return 'CLICKED_CONTINUE';
                })()")
            end if
        end repeat
    end repeat
    return "NO_TAB"
end tell
'''
p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate(input=ascript.encode('utf-8'))
print("OUT:", out.decode('utf-8').strip())
if err: print("ERR:", err.decode('utf-8').strip())
