import subprocess, base64, time

def run_js(url_sub, js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        repeat with t in tabs of window 1
            if (URL of t as string) contains "{url_sub}" then
                return (execute t javascript "try {{ eval(atob('{b64}')); }} catch(e) {{ 'ERR: ' + e.message; }}")
            end if
        end repeat
        return "NO_TAB"
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

with open('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

attach_js = f'''
(() => {{
    const fileInp = document.querySelector('input[type="file"]');
    if (!fileInp) return 'NO_FILE_INPUT';

    const b64Data = '{pdf_b64}';
    const byteCharacters = atob(b64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {{
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }}
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], {{ type: 'application/pdf' }});
    const file = new File([blob], 'Resume-Nilesh-Tiwari-1302.pdf', {{ type: 'application/pdf' }});

    const dt = new DataTransfer();
    dt.items.add(file);
    fileInp.files = dt.files;
    fileInp.dispatchEvent(new Event('change', {{ bubbles: true }}));
    fileInp.dispatchEvent(new Event('input', {{ bubbles: true }}));

    return 'ATTACHED: ' + fileInp.files[0].name;
}})()
'''

print("Attach Result:", run_js('cutshort.io/profile/all-jobs', attach_js))
time.sleep(2.0)

# Click Save and continue
save_js = r'''
(() => {
    const btn = Array.from(document.querySelectorAll('button')).find(b => (b.innerText || '').toLowerCase().includes('save and continue'));
    if (btn) {
        btn.click();
        return 'CLICKED_SAVE';
    }
    return 'NO_BTN';
})()
'''

print("Save Result:", run_js('cutshort.io/profile/all-jobs', save_js))
time.sleep(3.0)

# Check what dialog or stage is now active
check_post = r'''
(() => {
    const modal = document.querySelector('[role="dialog"], .modal, [class*="modal"], [class*="dialog"], [class*="drawer"]');
    return JSON.stringify({
        hasModal: !!modal,
        modalText: modal ? modal.innerText.slice(0, 400) : null,
        bodySnippet: document.body.innerText.slice(0, 300)
    });
})()
'''

print("Status:", run_js('cutshort.io/profile/all-jobs', check_post))
