import base64
import time
import sys
sys.path.append('/Users/nileshtiwari/.gemini/antigravity/scratch')
from chrome_js import run_js_on_tab

pdf_path = "/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf"
with open(pdf_path, "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode("ascii")

js_fill = f'''(() => {{
    const setVal = (el, val) => {{
        if (!el) return false;
        el.focus();
        const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
        if (setter) setter.call(el, val);
        else el.value = val;
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return true;
    }};

    const results = {{}};

    // 1. Name & Email
    results['name'] = setVal(document.getElementById('_systemfield_name'), 'Nilesh Tiwari');
    results['email'] = setVal(document.getElementById('_systemfield_email'), 'tiwarivivek2411@gmail.com');

    // 2. LinkedIn Profile
    results['linkedin'] = setVal(document.getElementById('2c9da40b-cc37-46db-9ac4-06c05ba0031a'), 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');

    // 3. Achievement Textarea
    const achText = "At Flipkart and Findem, I architected high-throughput distributed microservices handling millions of events daily. At Flipkart, I led the migration of high-volume transaction processing pipelines to event-driven Kafka and distributed caching architectures, cutting p99 latency by over 35% and drastically reducing infrastructure footprint. At Findem, I designed scalable data aggregation and search workflows across massive candidate datasets using Java and Python, ensuring zero-downtime deployments and resilient system design.";
    results['achievement'] = setVal(document.getElementById('af943e85-dc08-4302-91ea-d275cc569592'), achText);

    // 4. File upload
    const fileInput = document.getElementById('_systemfield_resume');
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
        results['fileAttached'] = true;
    }}

    return JSON.stringify(results);
}})()'''

print("Fill result:", run_js_on_tab(js_fill, tab_id='33684276'))
time.sleep(3.0)

# Submit
js_submit = '''(() => {
    const subBtn = document.querySelector('button.ashby-application-form-submit-button, button[type="submit"]._submitButton_5yu8i_411');
    if (subBtn) {
        subBtn.scrollIntoView({block: 'center'});
        subBtn.click();
        return 'CLICKED_SUBMIT';
    }
    return 'NO_SUBMIT_BTN';
})()'''
print("Submit:", run_js_on_tab(js_submit, tab_id='33684276'))
time.sleep(5.0)

js_chk = '''(() => {
    return JSON.stringify({
        url: window.location.href,
        bodySnippet: document.body.innerText.substring(0, 400),
        isSubmitted: document.body.innerText.toLowerCase().includes('success') || 
                     document.body.innerText.toLowerCase().includes('thank you') ||
                     document.body.innerText.toLowerCase().includes('submitted')
    });
})()'''
print("Confirmation:", run_js_on_tab(js_chk, tab_id='33684276'))
