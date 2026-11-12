import subprocess, json, base64, time

TAB_ID = 33684133

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

print("1. Attaching Resume to Ashby...")
with open('/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf', 'rb') as f:
    pdf_b64 = base64.b64encode(f.read()).decode('utf-8')

attach_js = f"""
(function() {{
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
            return "ATTACHED: " + fileInput.files[0].name;
        }}
        return "NO_RESUME_INPUT";
    }} catch(e) {{
        return "ERROR: " + e.message;
    }}
}})()
"""
res_attach = run_js(attach_js)
print("ATTACH RES:", res_attach)

time.sleep(1.0)

print("2. Filling Text Inputs and Textareas...")
system_owned = "I owned and architected the high-throughput event processing and indexing pipeline at Findem and Alrium, handling tens of millions of records daily using Java, Spring Boot, Apache Kafka, and AWS (ECS, Lambda, DynamoDB). I designed the microservice architecture end-to-end, wrote comprehensive unit/integration test suites, configured CI/CD deployment pipelines on AWS via Terraform/Docker, and managed production operations with Prometheus/Grafana monitoring, ensuring 99.99% uptime and sub-second p99 latency."

payment_timeout = "1) Idempotency Keys: Generate and attach a cryptographically unique idempotency key to every payment request so retries cannot result in double charges.\\n2) Ambiguous State & Re-query: If a timeout occurs, transition the local transaction state to PENDING_CONFIRMATION rather than failing or immediately retrying.\\n3) Outbox Pattern & Background Polling: Enqueue an async status check job via an Outbox worker or SQS delay queue to query the provider's transaction lookup API.\\n4) Webhook Handling: Reconcile asynchronously received provider webhooks using signature verification and idempotent state machine transitions.\\n5) Reconciliation & Settlement: Fallback to daily batch settlement file reconciliation with dead-letter queue (DLQ) alerts for any unresolved discrepancies."

ai_tools = "I use AI coding tools daily for rapid scaffolding of boilerplate, generating edge-case unit test suites, exploring unfamiliar API designs, and optimizing complex database queries. To verify the output, I treat AI-generated code as an untrusted PR: I conduct thorough manual code reviews, verify correctness against strict typing and system invariants, run isolated unit/integration tests covering edge cases (such as network partition and concurrency timeouts), and benchmark performance before merging."

fill_js = f"""
(function() {{
    function setVal(id, val) {{
        var el = document.getElementById(id);
        if (el) {{
            el.focus();
            var nativeSetter = Object.getOwnPropertyDescriptor(
                el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype,
                'value'
            ).set;
            nativeSetter.call(el, val);
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return true;
        }}
        return false;
    }}

    var r = {{}};
    r.name = setVal('_systemfield_name', 'Nilesh Tiwari');
    r.email = setVal('_systemfield_email', 'tiwarivivek2411@gmail.com');
    r.phone = setVal('35c460b3-dd31-4de3-b56a-3d74eb0eb3ae', '+91 8920952855');
    r.linkedin = setVal('30c916b5-0d4e-4348-858f-475cc7b9bc80', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    r.exp = setVal('00ae0781-d6d9-487b-a03e-6a00334616d7', '4.5');
    r.system_owned = setVal('e2a410ee-8554-4dad-8510-1d7451fe57cb', `{system_owned}`);
    r.payment_timeout = setVal('11efb97a-8c55-4325-8868-25d19c888ce8', `{payment_timeout}`);
    r.ai_tools = setVal('36b7aaa0-91d4-4fd5-9312-7998ce6470da', `{ai_tools}`);
    r.notice = setVal('8153f24f-3917-44ee-91f9-31698993ccbe', '15 Days (Immediate / Negotiable)');
    r.salary = setVal('b510458f-becf-4a19-bfb8-10ec91212dba', '₹42,00,000 (42 LPA)');
    r.adjustments = setVal('db61d0bc-db84-481b-a443-9a246755736d', 'None required');

    // Hybrid yes/no button
    var yesBtn = document.querySelector('button[data-option=\"yes\"]');
    if (yesBtn) {{
        yesBtn.click();
        r.hybrid = 'YES_CLICKED';
    }}

    // Consent checkbox
    var consent = document.getElementById('0ec08a07-600c-4159-9265-e54ac7102f53__systemfield_data_consent_ack-labeled-checkbox-0');
    if (consent && !consent.checked) {{
        consent.click();
        r.consent = 'CONSENT_CHECKED';
    }}

    return JSON.stringify(r);
}})()
"""
res_fill = run_js(fill_js)
print("FILL RES:", res_fill)

time.sleep(1.0)

print("3. Checking for Errors / Incomplete Fields...")
check_errs_js = """
(() => {
    var errs = Array.from(document.querySelectorAll('.ashby-application-form-error, [class*="error"]')).filter(e => e.offsetWidth > 0).map(e => e.innerText.trim());
    return JSON.stringify(errs);
})()
"""
print("ERRORS:", run_js(check_errs_js))

print("4. Submitting Application...")
submit_js = """
(() => {
    var btn = document.querySelector('.ashby-application-form-submit-button, button[type="submit"]');
    if (btn) {
        btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        btn.focus();
        btn.click();
        return "CLICKED SUBMIT";
    }
    return "NO SUBMIT BTN";
})()
"""
res_sub = run_js(submit_js)
print("SUBMIT ACTION:", res_sub)

time.sleep(4.0)

check_page_js = """
(() => {
    return window.location.href + ' ||| ' + document.body.innerText.slice(0, 300);
})()
"""
print("FINAL PAGE:", run_js(check_page_js))
