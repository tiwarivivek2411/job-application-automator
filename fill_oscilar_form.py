import subprocess, json, base64, time

pitch = (
    "I bring 4.5+ years of core distributed backend engineering experience with Java, Spring Boot, Dropwizard, "
    "Kafka, and AWS across Flipkart and Findem. At Flipkart, I led Kubernetes microservices migrations and Kafka connectors "
    "with callback and sideline flows to ensure zero data loss and lower latency. At Findem, I architected high-throughput "
    "asynchronous pipelines handling millions of records daily. I am deeply passionate about real-time distributed data "
    "systems, high availability, and low-latency architectures, which directly aligns with Oscilar's AI risk-decisioning platform."
)

js_code = f"""
(function() {{
    var res = {{}};

    function setInput(selector, val) {{
        var el = document.querySelector(selector);
        if (el) {{
            el.focus();
            el.value = val;
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            return true;
        }}
        return false;
    }}

    // 1. Text Inputs
    res['name'] = setInput('#_systemfield_name', 'Nilesh Tiwari');
    res['email'] = setInput('#_systemfield_email', 'tiwarivivek2411@gmail.com');
    res['phone'] = setInput('#5b091137-a7f0-4268-9f41-35050b5718d3', '+91 8920952855');
    res['linkedin'] = setInput('#121b09cc-e0e0-4414-aa2a-fdc6637204b3', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    res['why_fit'] = setInput('#3b044024-be58-4b09-b220-ef25093a221c', `{pitch}`);

    // Location
    var locInput = Array.from(document.querySelectorAll('input[type="text"]')).find(i => {{
        var p = i.closest('fieldset, div, .field');
        return p && p.innerText.includes('current location');
    }});
    if (locInput) {{
        locInput.focus();
        locInput.value = 'Bengaluru, India';
        locInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        locInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        res['location'] = true;
    }}

    // 2. Radio/Button selections
    // Find each question container and click matching button
    function clickOptionForQuestion(questionSnippet, buttonText) {{
        var containers = Array.from(document.querySelectorAll('fieldset, [class*="field"], [class*="Container"]'));
        var q = containers.find(c => c.innerText && c.innerText.includes(questionSnippet));
        if (q) {{
            var btn = Array.from(q.querySelectorAll('button, div[role="radio"], label')).find(b => b.innerText.trim() === buttonText);
            if (btn) {{
                btn.click();
                return 'CLICKED_' + buttonText;
            }}
        }}
        return 'NOT_FOUND';
    }}

    res['authorized'] = clickOptionForQuestion('legally authorized', 'Yes');
    res['sponsorship'] = clickOptionForQuestion('require sponsorship', 'No');
    res['8plus_java'] = clickOptionForQuestion('8+ years', 'No');
    res['aws'] = clickOptionForQuestion('experience with AWS', 'Yes');
    res['distributed'] = clickOptionForQuestion('distributed systems', 'Yes');
    res['12am'] = clickOptionForQuestion('12 am IST', 'Yes');

    return JSON.stringify(res);
}})()
"""

ascript_payload = base64.b64encode(js_code.encode('utf-8')).decode('utf-8')
ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "eval(atob('{ascript_payload}'))")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("FILL OSCILAR FORM OUT:\n", out.strip())
