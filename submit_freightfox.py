from inspect_wellfound_tab import run_js
import time

submit_js = """
(() => {
    const ta = document.querySelector('textarea');
    if (ta) {
        ta.value = "Hi FreightFox team, I am an experienced backend engineer with a strong background in Java, Spring Boot, microservices, and distributed systems from Flipkart and Findem. I am very excited about FreightFox's work and would love to contribute to your engineering goals!";
        ta.dispatchEvent(new Event('input', {bubbles: true}));
        ta.dispatchEvent(new Event('change', {bubbles: true}));
    }

    const sendBtn = Array.from(document.querySelectorAll('button'))
        .find(b => b.offsetWidth > 0 && b.innerText.trim().toLowerCase() === 'send application');
    if (!sendBtn) return 'NO_SEND_BTN';
    sendBtn.click();
    return 'CLICKED_SEND_APPLICATION';
})()
"""

out, _ = run_js(submit_js)
print("SUBMIT STATUS:", out)
time.sleep(3.5)

check_js = """
(() => {
    const btns = Array.from(document.querySelectorAll('button')).filter(b => b.offsetWidth > 0).map(b => b.innerText.trim());
    const textSnippet = document.body.innerText.slice(0, 200).replace(/\\n/g, '  ');
    return JSON.stringify({
        buttons: btns.slice(-6),
        textSnippet
    });
})()
"""
out, _ = run_js(check_js)
print("AFTER SUBMISSION:", out)
