import base64
import time
import sys
sys.path.append('/Users/nileshtiwari/.gemini/antigravity/scratch')
from chrome_js import run_js_on_tab

pdf_path = "/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf"
with open(pdf_path, "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode("ascii")

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
    res['legal_first'] = setVal('a1529799-27e4-4654-9c1f-e8962001c434', 'Nilesh');
    res['legal_last'] = setVal('9b5a508c-09ca-4390-a2c8-d6481a246e43', 'Tiwari');
    res['email'] = setVal('_systemfield_email', 'tiwarivivek2411@gmail.com');
    res['phone'] = setVal('55ccbb5e-0a4a-44e7-9308-a7ca87e4aa8e', '+91 8920952855');
    res['linkedin'] = setVal('c5048108-508d-4acf-83c6-042fbffdcb99', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    res['github'] = setVal('1070b429-be7b-4a98-a2c7-c7a473f19416', 'https://github.com/nileshtiwari');

    // Why Temporal
    const whyText = "Having architected distributed systems and asynchronous workflows at Flipkart and Findem using Java, Kafka, and microservices, I have seen firsthand how Temporal solves stateful workflow orchestration and fault-tolerant execution. I am passionate about helping enterprise banking teams build resilient, mission-critical architectures on Temporal.";
    res['why'] = setVal('658e009c-ac2f-4839-879e-3a4d0af59db7', whyText);

    // Radio: Authorized / No sponsorship
    const authRadio = document.getElementById('a90ce211-b60c-4510-9455-52fdd476b09f_94787f3a-090e-4d84-85ba-6e89c138c79e-labeled-radio-0');
    if (authRadio) {
        authRadio.closest('label')?.click();
        authRadio.checked = true;
        authRadio.dispatchEvent(new Event('change', { bubbles: true }));
        res['authRadio'] = true;
    }

    // Radio: Recording consent
    const recRadio = document.getElementById('a90ce211-b60c-4510-9455-52fdd476b09f__systemfield_recording_consent-labeled-radio-0');
    if (recRadio) {
        recRadio.closest('label')?.click();
        recRadio.checked = true;
        recRadio.dispatchEvent(new Event('change', { bubbles: true }));
        res['recRadio'] = true;
    }

    return JSON.stringify(res);
})()
"""

print("Fill:", run_js_on_tab(js_fill, tab_id='33684276'))
time.sleep(1.5)

# Attach resume PDF
js_attach = f"""
(() => {{
    const fileInput = document.getElementById('_systemfield_resume') || document.querySelector('input[type="file"]');
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

print("Attach:", run_js_on_tab(js_attach, tab_id='33684276'))
time.sleep(2.5)

# Submit
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

# Check confirmation
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
