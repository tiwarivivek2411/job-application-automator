import subprocess, json, base64, time

pitch = (
    "I have 4.5+ years of experience architecting distributed backend services and data pipelines using Java, "
    "Spring Boot, Dropwizard, Apache Kafka, and AWS Lambda across Flipkart and Findem. At Flipkart, I led Kubernetes "
    "microservices migrations and developed custom Kafka connectors with callback logic to minimize latency and ensure zero data loss. "
    "At Findem, I designed and scaled event-driven pipelines processing millions of candidate records asynchronously. "
    "I have deep hands-on expertise in distributed systems, high throughput, and fault-tolerant architecture, which makes Oscilar's "
    "real-time AI risk intelligence mission an ideal match for my technical background."
)

js_code = f"""
(function() {{
    function setReactValue(el, val) {{
        if (!el) return false;
        var proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        var setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        return true;
    }}

    var results = {{}};

    // 1. Inputs
    results['name'] = setReactValue(document.getElementById('_systemfield_name'), 'Nilesh Tiwari');
    results['email'] = setReactValue(document.getElementById('_systemfield_email'), 'tiwarivivek2411@gmail.com');
    results['phone'] = setReactValue(document.getElementById('5b091137-a7f0-4268-9f41-35050b5718d3'), '+91 8920952855');
    results['linkedin'] = setReactValue(document.getElementById('121b09cc-e0e0-4414-aa2a-fdc6637204b3'), 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    results['pitch'] = setReactValue(document.getElementById('3b044024-be58-4b09-b220-ef25093a221c'), `{pitch}`);

    // Location
    var locInput = document.querySelector('input[placeholder*="Start typing"]');
    if (locInput) {{
        setReactValue(locInput, 'Bengaluru, India');
        results['location'] = true;
    }}

    // 2. Yes/No button clicks
    var yesNoMap = [
        ['bc91a612-b0cf-4ce7-a22a-381574223dd1', 'yes'], // authorized
        ['670688b6-0182-4d30-81f3-e8728d00d36e', 'no'],  // sponsorship
        ['5eadfe3e-64ad-4c43-b98d-ad1f997fd6a6', 'no'],  // 8+ years
        ['29851d7d-fe18-4c10-a653-37397ef6bf68', 'yes'], // AWS
        ['c50c99d7-7baa-4c61-8d0e-e3aaa13a7dc6', 'yes'], // distributed systems
        ['09be66ba-8bb4-4aec-ad75-eb7cfecfa51b', 'yes']  // 12 am IST
    ];

    yesNoMap.forEach(function(item) {{
        var name = item[0];
        var opt = item[1];
        var cb = document.querySelector("input[name='" + name + "']");
        if (cb) {{
            var parent = cb.closest('._yesno_1e3gg_148, [class*="yesno"]') || cb.parentElement;
            var btn = parent.querySelector("button[data-option='" + opt + "']");
            if (btn) {{
                btn.click();
                results[name] = 'CLICKED_' + opt;
            }} else {{
                results[name] = 'BTN_NOT_FOUND';
            }}
        }} else {{
            results[name] = 'CB_NOT_FOUND';
        }}
    }});

    return JSON.stringify(results);
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
print("FILL RESULTS:\n", out.strip())
