import subprocess
import time
import json
import urllib.parse
import pypdf

# Extract resume text
reader = pypdf.PdfReader("/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf")
resume_text = ""
for page in reader.pages:
    resume_text += page.extract_text() + "\n"

# Prepare field values
answers = {
    "first_name": "Nilesh",
    "last_name": "Tiwari",
    "email": "tiwarivivek2411@gmail.com",
    "phone": "+91 8920952855",
    "address": "Bellandur",
    "city": "Bengaluru",
    "state": "Karnataka",
    "postal": "560103",
    "linkedin": "https://www.linkedin.com/in/nilesh-tiwari-b31330128/",
    "salary": "$110,000 USD",
    "citizen_val": "40", # Non-citizen seeking work authorization
    "q1": "Bitovi's deep engineering focus on cloud platform consulting, resilient microservices, and distributed workflow orchestrations using Temporal and Kubernetes aligns strongly with my experience. I've designed and operated event-driven workflow systems and microservices deployed on Kubernetes, and I want to consult and solve mission-critical workflow reliability challenges.",
    "q2": "Recently architected an event-driven data pipeline and distributed workflow system handling high-throughput asynchronous workloads using Spring Boot, Kafka, and Kubernetes. Reduced p99 latency by 35% through connection pooling, query tuning, and resilient retry/dead-letter queues.",
    "q3": "Spring Boot (Java) and Express/Fastify (Node.js). My favorite aspects of Spring Boot are its mature ecosystem, battle-tested dependency injection, comprehensive observability tooling (Actuator/Micrometer), and first-class Kafka/Kubernetes integration. Least favorite is the startup time overhead and verbose configuration when dealing with legacy annotations.",
    "q4": "Outside of architecting backend systems, I'm an avid chess enthusiast and enjoy studying classic grandmaster endgames and tactical patterns. I'm deeply passionate about systems literature, tech podcasts, and exploring new developments in distributed systems and autonomous developer tooling.",
    "id_val": "Yes",
    "resume_text": resume_text
}

encoded_data = urllib.parse.quote(json.dumps(answers))

fill_js = f"""(() => {{
    const d = JSON.parse(decodeURIComponent("{encoded_data}"));
    
    function setVal(id, val) {{
        const el = document.getElementById(id);
        if (!el) return;
        el.value = val;
        el.dispatchEvent(new Event("input", {{ bubbles: true }}));
        el.dispatchEvent(new Event("change", {{ bubbles: true }}));
    }}

    setVal("resumator-firstname-value", d.first_name);
    setVal("resumator-lastname-value", d.last_name);
    setVal("resumator-email-value", d.email);
    setVal("resumator-phone-value", d.phone);
    setVal("resumator-address-value", d.address);
    setVal("resumator-city-value", d.city);
    setVal("resumator-state-value", d.state);
    setVal("resumator-postal-value", d.postal);
    setVal("resumator-linkedin-value", d.linkedin);
    setVal("resumator-salary-value", d.salary);

    const citizen = document.getElementById("resumator-citizen-value");
    if (citizen) {{
        citizen.value = d.citizen_val;
        citizen.dispatchEvent(new Event("change", {{ bubbles: true }}));
    }}

    const idVer = document.getElementById("resumator-questionnaire-q3077355");
    if (idVer) {{
        idVer.value = d.id_val;
        idVer.dispatchEvent(new Event("change", {{ bubbles: true }}));
    }}

    setVal("resumator-questionnaire-q1230332", d.q1);
    setVal("resumator-questionnaire-q1230333", d.q2);
    setVal("resumator-questionnaire-q1230334", d.q3);
    setVal("resumator-questionnaire-q1230335", d.q4);

    const rText = document.getElementById("resumator-resumetext-value");
    if (rText) {{
        rText.value = d.resume_text;
        rText.dispatchEvent(new Event("input", {{ bubbles: true }}));
        rText.dispatchEvent(new Event("change", {{ bubbles: true }}));
    }}

    return "SUCCESS: All Bitovi fields populated!";
}})()"""

clean_js = fill_js.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
apple_script = f"""tell application "Google Chrome"
    tell tab 11 of window 1
        execute javascript "{clean_js}"
    end tell
end tell"""

res = subprocess.run(["osascript"], input=apple_script, text=True, capture_output=True)
print("Fill Output:", res.stdout.strip())
print("Fill Error:", res.stderr.strip())
