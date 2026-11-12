import subprocess
import json

script = '''
tell application "Google Chrome"
    return (execute tab 5 of window 1 javascript "(() => {
        const toast = document.querySelector('.toast, .snackbar, .success, [class*=\\"toast\\"], [class*=\\"snackbar\\"], [class*=\\"success\\"]') ? document.querySelector('.toast, .snackbar, .success, [class*=\\"toast\\"], [class*=\\"snackbar\\"], [class*=\\"success\\"]').innerText : '';
        const btn = document.querySelector('.multi-apply-button');
        const appliedCount = document.querySelectorAll('.applied-tag, [class*=\\"applied\\"]').length;
        return JSON.stringify({toast, btnText: btn ? btn.innerText.trim() : 'no btn', appliedCount});
    })()")
end tell
'''
p = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate()
print("OUT:", out)
if err: print("ERR:", err)
