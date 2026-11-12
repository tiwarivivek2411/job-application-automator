import subprocess, time

js_code = """
(function() {
    // Find first software card
    var cards = document.querySelectorAll(".srpResultCard, .cardContainer, div[class*='cardContainer'], div[class*='srpResultCard']");
    for (var i = 0; i < cards.length; i++) {
        var t = cards[i].querySelector(".jobTitle, [class*='jobTitle'], h3, a[href*='job-desc']");
        if (t && t.innerText.includes("Java Backend Developer IRC306122")) {
            t.click();
            return "Clicked card: " + t.innerText.trim();
        }
    }
    return "Card not found";
})()
"""

escaped_js = js_code.replace('\n', ' ').replace('"', '\\"')
apple_script = 'tell application "Google Chrome"\n' \
               '    tell (first tab of window 1 whose id is 33684127)\n' \
               f'        return execute javascript "{escaped_js}"\n' \
               '    end tell\n' \
               'end tell'

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(apple_script)
print("CLICK CARD:", out)

time.sleep(2)

# Now check right pane for Apply Now button
js_check = """
(function() {
    var btns = Array.from(document.querySelectorAll("button, .applyBtnCont, a")).filter(function(b) {
        return b.innerText && b.innerText.trim().includes("Apply");
    }).map(function(b) {
        return b.tagName + " | " + b.className + " | " + b.innerText.replace(/\\n/g, ' ');
    });
    return btns.join(';;;');
})()
"""
escaped_check = js_check.replace('\n', ' ').replace('"', '\\"')
apple_script2 = 'tell application "Google Chrome"\n' \
               '    tell (first tab of window 1 whose id is 33684127)\n' \
               f'        return execute javascript "{escaped_check}"\n' \
               '    end tell\n' \
               'end tell'

p2 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out2, err2 = p2.communicate(apple_script2)
print("APPLY BUTTONS ON RIGHT PANE:", out2)
