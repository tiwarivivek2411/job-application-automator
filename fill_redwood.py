import subprocess
import urllib.parse
import json

text_answers = {
    "city": "Bengaluru, Karnataka, India (Eager to relocate to Utrecht, Netherlands immediately)",
    "start_date": "Immediate / 15 days notice",
    "salary": "€85,000 EUR",
    "notes": "Experienced Senior Java/Spring Boot & AWS Software Engineer with BITS Pilani CS degree, 4.5+ years experience at Flipkart and Findem. Ready for Netherlands relocation.",
    "java_story": "At Flipkart/Findem, we operated high-throughput Java/Spring Boot microservices deployed on AWS EKS processing millions of ingestion events via Kafka. During a flash event, our ingestion consumers experienced severe thread starvation and memory pressure leading to pod restarts and latency spikes up to 4s. I led the investigation using distributed tracing (Jaeger/Datadog) and heap dump analysis, discovering connection pool exhaustion on the downstream PostgreSQL/Redis caching tier coupled with unbounded blocking I/O calls. Working closely with our platform team, we implemented asynchronous non-blocking event batching using reactive Kafka consumers, tuned HikariCP connection pools with explicit timeouts, and introduced circuit breakers with fallback caching. To prevent recurrence, we added automated load tests in our CI pipeline and established proactive P99 latency and consumer lag alerting, achieving 99.99% uptime during subsequent peak loads."
}

encoded = urllib.parse.quote(json.dumps(text_answers))

js = f"""(() => {{
    const d = JSON.parse(decodeURIComponent("{encoded}"));
    function setVal(id, val) {{
        const el = document.getElementById(id);
        if (!el) return;
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set ||
                             Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value")?.set;
        if (nativeSetter) {{
            nativeSetter.call(el, val);
        }} else {{
            el.value = val;
        }}
        el.dispatchEvent(new Event("input", {{ bubbles: true }}));
        el.dispatchEvent(new Event("change", {{ bubbles: true }}));
    }}

    setVal("question_8269732009", d.city);
    setVal("question_8269734009", d.start_date);
    setVal("question_8269735009", d.salary);
    setVal("question_8269736009", d.notes);
    setVal("question_8269738009", d.java_story);

    const c1 = document.getElementById("gdpr_processing_consent_given_1");
    if (c1 && !c1.checked) c1.click();
    const c2 = document.getElementById("gdpr_retention_consent_given_1");
    if (c2 && !c2.checked) c2.click();

    return "Populated text fields and checked GDPR!";
}})()"""

clean_js = js.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
apple_script = f"""tell application "Google Chrome"
    tell tab 9 of window 1
        execute javascript "{clean_js}"
    end tell
end tell"""

res = subprocess.run(["osascript"], input=apple_script, text=True, capture_output=True)
print("Output:", res.stdout.strip())
print("Error:", res.stderr.strip())
