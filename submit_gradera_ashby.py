import subprocess, base64, time, json

TAB_ID = 33684280

def run_js(js):
    b64 = base64.b64encode(js.encode('utf-8')).decode('utf-8')
    ascript = f'''
    tell application "Google Chrome"
        tell (first tab of window 1 whose id is {TAB_ID})
            return (execute javascript "eval(atob('{b64}'))")
        end tell
    end tell
    '''
    p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(ascript)
    return out.strip()

# Read PDF bytes
with open('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

fill_and_submit_js = f'''
(() => {{
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

    // 1. System fields
    results['name'] = setVal(document.getElementById('_systemfield_name'), 'Nilesh Tiwari');
    results['email'] = setVal(document.getElementById('_systemfield_email'), 'tiwarivivek2411@gmail.com');

    // 2. Phone
    results['phone'] = setVal(document.getElementById('94d2a5f6-2b6e-416c-b484-98b8b201b7ce'), '8920952855');

    // 3. Links
    results['linkedin'] = setVal(document.getElementById('afc17969-a0b4-4d3e-8400-69af6dc1c45d'), 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    results['github'] = setVal(document.getElementById('5559cd4e-aa53-47af-96ae-7a0033742865'), 'https://github.com/nileshtiwari');

    // 4. Source (LinkedIn checkbox)
    const liCb = document.querySelector('input[name="LinkedIn"]');
    if (liCb && !liCb.checked) {{
        const lbl = liCb.closest('label') || liCb;
        lbl.click();
        results['source'] = true;
    }}

    // 5. Experience
    results['total_exp'] = setVal(document.getElementById('2a7cc0df-831a-434f-a30b-8b9d5e20df5a'), '4.5');
    results['rel_exp'] = setVal(document.getElementById('5d9ad9ad-7151-4ade-b028-53fbb513c1d5'), '4.5');

    // 6. Current Employer & Title
    results['employer'] = setVal(document.getElementById('e5ef98eb-d27f-468b-acd4-63aaeca5741a'), 'Alrium Technologies');
    results['title'] = setVal(document.getElementById('00742fbd-8aa5-4356-ac35-ed16b75a938c'), 'Senior Software Engineer');

    // 7. Employment Status (Currently Employed or Serving Notice Period)
    const empStatusRadios = Array.from(document.querySelectorAll('input[type="radio"]')).filter(r => r.name.includes('385d574d'));
    empStatusRadios.forEach(r => {{
        const pText = (r.closest('div')?.innerText || '').toLowerCase();
        if (pText.includes('serving notice') || pText.includes('currently employed')) {{
            const lbl = r.closest('label') || r;
            lbl.click();
            results['status'] = true;
        }}
    }});

    // 8. Notice Period (Immediate or Less than 15 Days)
    const noticeRadios = Array.from(document.querySelectorAll('input[type="radio"]')).filter(r => r.name.includes('309af125'));
    noticeRadios.forEach(r => {{
        const pText = (r.closest('div')?.innerText || '').toLowerCase();
        if (pText.includes('immediate') || pText.includes('less than 15')) {{
            const lbl = r.closest('label') || r;
            lbl.click();
            results['notice'] = true;
        }}
    }});

    // 9. Compensation (CTC) - Current & Expected
    results['current_ctc'] = setVal(document.getElementById('1eac624d-35a9-442a-96ae-2fdaaa117337'), '3500000');
    results['expected_ctc'] = setVal(document.getElementById('24673898-4035-46a8-981f-e2683ea14e2e'), '4200000');

    // 10. Offers (No)
    const offersField = document.querySelector('[data-field-path="3f944e2a-0708-41e4-a152-899935557f80"]');
    if (offersField) {{
        const noBtn = offersField.querySelector('button[data-option="no"]');
        if (noBtn) noBtn.click();
        results['offers'] = true;
    }}

    // 11. Work Preferences (Any)
    const anyPref = document.querySelector('input[name="Any"]') || document.querySelector('input[name="Work from Office"]');
    if (anyPref && !anyPref.checked) {{
        const lbl = anyPref.closest('label') || anyPref;
        lbl.click();
        results['work_pref'] = true;
    }}

    // 12. Willing to Relocate (Yes)
    const relocField = document.querySelector('[data-field-path="75642bb9-9bf8-4c17-91d9-dfeffc2c45ae"]');
    if (relocField) {{
        const yesBtn = relocField.querySelector('button[data-option="yes"]');
        if (yesBtn) yesBtn.click();
        results['reloc'] = true;
    }}

    // 13. Declaration & Consent
    const consentCb = document.querySelector('input[name="I Agree"]');
    if (consentCb && !consentCb.checked) {{
        const lbl = consentCb.closest('label') || consentCb;
        lbl.click();
        results['consent'] = true;
    }}

    // 14. Resume Attachment via DataTransfer
    try {{
        var b64Data = "{pdf_b64}";
        var byteCharacters = atob(b64Data);
        var byteNumbers = new Array(byteCharacters.length);
        for (var i = 0; i < byteCharacters.length; i++) {{
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }}
        var byteArray = new Uint8Array(byteNumbers);
        var blob = new Blob([byteArray], {{ type: "application/pdf" }});
        var file = new File([blob], "Resume-Nilesh-Tiwari-1302.pdf", {{ type: "application/pdf" }});

        var fileInput = document.getElementById("_systemfield_resume");
        if (fileInput) {{
            var dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
            fileInput.dispatchEvent(new Event("change", {{ bubbles: true }}));
            fileInput.dispatchEvent(new Event("input", {{ bubbles: true }}));
            results['resume'] = true;
        }}
    }} catch (e) {{
        results['resume_error'] = e.message;
    }}

    return JSON.stringify(results);
}})()
'''

print("Filling form and attaching resume...")
fill_res = run_js(fill_and_submit_js)
print("Fill status:", fill_res)

time.sleep(2.0)

# Check errors and submit button
check_js = '''
(() => {
    const invalidFields = Array.from(document.querySelectorAll('[aria-invalid="true"]')).map(e => e.innerText.trim()).filter(Boolean);
    const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim().toLowerCase().includes('submit application'));
    return JSON.stringify({
        invalidFields,
        submitBtnText: submitBtn ? submitBtn.innerText.trim() : null,
        submitDisabled: submitBtn ? submitBtn.disabled : null
    });
})()
'''
print("Form verification:", run_js(check_js))

# Submit
print("Clicking Submit Application...")
click_submit_js = '''
(() => {
    const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim().toLowerCase().includes('submit application'));
    if (submitBtn) {
        submitBtn.click();
        return 'CLICKED_SUBMIT';
    }
    return 'NO_SUBMIT_BTN';
})()
'''
print(run_js(click_submit_js))

time.sleep(5.0)

# Verify post submit
post_js = '''
(() => {
    return JSON.stringify({
        url: window.location.href,
        snippet: document.body.innerText.substring(0, 500)
    });
})()
'''
print("Post-submission:", run_js(post_js))
