import base64
import time
import sys
sys.path.append('/Users/nileshtiwari/.gemini/antigravity/scratch')
from chrome_js import run_js_on_tab

pdf_path = "/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf"
with open(pdf_path, "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode("ascii")

# 1. Fill all text inputs and radio buttons
js_fill = """
(() => {
    const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (!el) return 'NOT_FOUND';
        el.focus();
        const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
        if (setter) setter.call(el, val);
        else el.value = val;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        return el.value;
    };

    const res = {};
    res['name'] = setVal('_systemfield_name', 'Nilesh Tiwari');
    res['email'] = setVal('_systemfield_email', 'tiwarivivek2411@gmail.com');
    res['location'] = setVal('2953e314-ca27-4d2b-8c40-a8197a325a49', 'Bengaluru, Karnataka, India');
    res['company'] = setVal('5ff4daaf-8e44-44a7-a6db-f7d02a7cdd38', 'Alrium Technologies');
    res['phone'] = setVal('e49092dd-c589-4165-8cb1-4f348dd7b940', '+91 8920952855');
    res['linkedin'] = setVal('74a9bab8-ba3a-42e8-ab40-876aff50a3ed', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    res['github'] = setVal('def8cf92-0f00-44d7-9987-57821eb9676c', 'https://github.com/nileshtiwari');

    // Radio: No visa sponsorship
    const noRadio = document.getElementById('d1ea7c8c-463f-4a59-bff1-49c404d3ff1b_942ecf24-8aad-4a65-8a58-327c21ca6164-labeled-radio-1');
    if (noRadio) {
        const lbl = noRadio.closest('label') || noRadio;
        lbl.click();
        noRadio.checked = true;
        noRadio.dispatchEvent(new Event('change', { bubbles: true }));
        res['noRadio'] = true;
    }

    return JSON.stringify(res);
})()
"""

print("Text Fill:", run_js_on_tab(js_fill, tab_id='33684276'))
time.sleep(1.5)

# 2. Attach resume PDF
js_attach = f"""
(() => {{
    const fileInput = document.getElementById('_systemfield_resume');
    if (!fileInput) return 'NO_FILE_INPUT';

    const b64Data = "{pdf_b64}";
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
    fileInput.files = dt.files;
    fileInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

    return 'ATTACHED_' + fileInput.files.length;
}})()
"""

print("Attach File:", run_js_on_tab(js_attach, tab_id='33684276'))
time.sleep(2.5)

# 3. Submit
js_submit = """
(() => {
    const subBtn = document.querySelector('button.ashby-application-form-submit-button, button[type="submit"]._submitButton_5yu8i_411');
    if (subBtn) {
        subBtn.scrollIntoView({block: 'center'});
        subBtn.click();
        return 'CLICKED_SUBMIT';
    }
    return 'NO_SUBMIT_BTN';
})()
"""
print("Submit:", run_js_on_tab(js_submit, tab_id='33684276'))
time.sleep(5.0)

# 4. Confirmation
js_chk = """
(() => {
    return JSON.stringify({
        url: window.location.href,
        bodySnippet: document.body.innerText.substring(0, 400),
        isSubmitted: document.body.innerText.toLowerCase().includes('success') || 
                     document.body.innerText.toLowerCase().includes('thank you') ||
                     document.body.innerText.toLowerCase().includes('submitted')
    });
})()
"""
print("Confirmation:", run_js_on_tab(js_chk, tab_id='33684276'))
