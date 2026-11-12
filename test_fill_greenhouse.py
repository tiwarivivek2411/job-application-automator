import subprocess, json, time

js_code = """
(function() {
    // Fill text inputs
    function setVal(id, val) {
        var el = document.getElementById(id);
        if (el) {
            el.focus();
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }
        return false;
    }

    var res = {};
    res['first_name'] = setVal('first_name', 'Nilesh');
    res['last_name'] = setVal('last_name', 'Tiwari');
    res['email'] = setVal('email', 'tiwarivivek2411@gmail.com');
    res['phone'] = setVal('phone', '8920952855');
    
    // Country
    setVal('country', 'India');

    // Questions
    res['exp'] = setVal('question_64239203', '4');
    res['stack'] = setVal('question_64239204', 'Java, Spring Boot, Node.js, Python');
    res['schema'] = setVal('question_64239205', 'Yes, extensive experience with PostgreSQL, MySQL, and MongoDB schemas.');
    res['architecture'] = setVal('question_65143956', 'Yes, architected high-throughput microservices and Kafka event streams at Flipkart and Findem.');
    res['ai_tools'] = setVal('question_64239206', 'Yes');
    res['mentored'] = setVal('question_65143957', 'Yes, conducted code reviews, system design sessions, and mentored junior developers.');
    res['relocate'] = setVal('question_64239208', 'Already based in Bangalore');
    res['location'] = setVal('question_64239207', 'Bengaluru, Karnataka');
    res['notice'] = setVal('question_64239209', '15 Days');
    res['salary'] = setVal('question_64239210', '42 LPA');
    res['offers'] = setVal('question_64239211', 'In active interview processes');
    res['linkedin'] = setVal('question_64239212', 'https://www.linkedin.com/in/nilesh-tiwari-b31330128/');
    res['github'] = setVal('question_64239213', 'https://github.com/nileshtiwari');

    return JSON.stringify(res);
})()
"""

cleaned_lines = [l.strip() for l in js_code.split('\n') if l.strip() and not l.strip().startswith('//')]
escaped = ' '.join(cleaned_lines).replace('\\', '\\\\').replace('"', '\\"')

ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{escaped}")
    end tell
end tell
'''

p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("FILL RESULT:", out)
if err: print("ERR:", err)
