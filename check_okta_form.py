import subprocess
import json

def check_form():
    ascript = '''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                if (id of t as string) is "33684123" then
                    return (execute t javascript "(() => {
                        const errors = Array.from(document.querySelectorAll('[aria-invalid=\\"true\\"], [class*=\\"error\\"], [role=\\"alert\\"]')).map(e => e.innerText.trim()).filter(Boolean);
                        const radios = Array.from(document.querySelectorAll('input[type=\\"radio\\"]')).map(r => ({id: r.id, checked: r.checked, val: r.value}));
                        const cb = document.querySelector('input[type=\\"checkbox\\"]');
                        if (cb && !cb.checked) {
                            const lbl = cb.closest('label') || document.querySelector('label[for=\\"' + cb.id + '\\"]');
                            if (lbl) lbl.click();
                            else cb.click();
                        }
                        const contBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase() === 'continue');
                        if (contBtn) contBtn.click();
                        return JSON.stringify({
                            errors,
                            radiosChecked: radios.filter(r => r.checked),
                            cbChecked: cb ? cb.checked : 'no cb',
                            hasContinue: !!contBtn
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

out, err = check_form()
print("OUT:", out)
if err: print("ERR:", err)
