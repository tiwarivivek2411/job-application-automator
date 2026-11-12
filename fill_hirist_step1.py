import base64
import time
from chrome_js import run_js_on_tab

pdf_path = "/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf"
with open(pdf_path, "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode("ascii")

js = f'''(() => {{
    const setInputVal = (el, val) => {{
        const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
        if (setter) setter.call(el, val);
        else el.value = val;
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }};

    // 1. Phone number
    const phoneInput = document.querySelector('input[name="phoneNumber"]');
    if (phoneInput) {{
        setInputVal(phoneInput, '8920952855');
    }}

    // 2. Gender
    const maleBtn = Array.from(document.querySelectorAll('button, div, span, label')).find(el => el.innerText && el.innerText.trim() === 'Male');
    if (maleBtn) {{
        maleBtn.click();
    }}

    // 3. Location buttons (Suggested Locations: Bengaluru / Bangalore)
    const bglrBtn = Array.from(document.querySelectorAll('button, div, span, p')).find(el => el.innerText && (el.innerText.trim() === 'Bengaluru / Bangalore' || el.innerText.trim() === 'Bengaluru'));
    if (bglrBtn) {{
        bglrBtn.click();
    }}

    // 4. LinkedIn & GitHub
    const liInput = document.querySelector('input[name="linkedin"]');
    if (liInput) setInputVal(liInput, 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');

    const ghInput = document.querySelector('input[name="github"]');
    if (ghInput) setInputVal(ghInput, 'https://github.com/nileshtiwari');

    // 5. Resume upload
    const fileInput = document.querySelector('input[type="file"]');
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
        phone: phoneInput ? phoneInput.value : 'missing',
        fileAttached: fileInput ? fileInput.files.length : 0
    }});
}})()'''

res = run_js_on_tab(js, tab_id="33684280")
print("RESULT:", res)
