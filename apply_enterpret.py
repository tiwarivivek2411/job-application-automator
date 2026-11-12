import base64
import time
import sys
sys.path.append('/Users/nileshtiwari/.gemini/antigravity/scratch')
from chrome_js import run_js_on_tab

pdf_path = "/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf"
with open(pdf_path, "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode("ascii")

js_fill = f'''(() => {{
    const setVal = (sel, val) => {{
        const el = document.querySelector(sel);
        if (!el) return false;
        el.focus();
        const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value')?.set;
        if (setter) setter.call(el, val);
        else el.value = val;
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return true;
    }};

    setVal('#first_name', 'Nilesh');
    setVal('#last_name', 'Tiwari');
    setVal('#email', 'tiwarivivek2411@gmail.com');
    setVal('#phone', '+91 8920952855');

    // Attach resume
    const fileInput = document.querySelector('#resume, input[type="file"]');
    if (fileInput) {{
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
    }}

    return JSON.stringify({{
        fn: document.querySelector('#first_name')?.value,
        ln: document.querySelector('#last_name')?.value,
        em: document.querySelector('#email')?.value,
        ph: document.querySelector('#phone')?.value,
        file: fileInput?.files?.length
    }});
}})()'''

res = run_js_on_tab(js_fill, tab_id='33684297')
print("Filled:", res)
time.sleep(2.0)

# Submit button click
js_submit = '''(() => {
    const subBtn = document.querySelector('#submit_app, button[type="submit"]') ||
                   Array.from(document.querySelectorAll('button')).find(b => b.innerText.toLowerCase().includes('submit application'));
    if (subBtn) {
        subBtn.scrollIntoView({block: 'center'});
        subBtn.click();
        return 'CLICKED_SUBMIT';
    }
    return 'NO_SUBMIT_BTN';
})()'''
print("Submit:", run_js_on_tab(js_submit, tab_id='33684297'))
time.sleep(5.0)

js_chk = '''(() => {
    return JSON.stringify({
        url: window.location.href,
        bodySnippet: document.body.innerText.substring(0, 400),
        isSubmitted: document.body.innerText.toLowerCase().includes('thank you') || document.body.innerText.toLowerCase().includes('received')
    });
})()'''
print("Confirmation:", run_js_on_tab(js_chk, tab_id='33684297'))
