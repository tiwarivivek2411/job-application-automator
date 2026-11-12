import subprocess, time

# 1. Click the file upload button to trigger the macOS file picker sheet
click_js = """
(function() {
    var btn = Array.from(document.querySelectorAll("button")).find(b => b.innerText && b.innerText.includes("Upload File"));
    if (btn) {
        btn.click();
        return "CLICKED_UPLOAD";
    }
    var fileInput = document.getElementById("_systemfield_resume");
    if (fileInput) {
        fileInput.click();
        return "CLICKED_FILE_INPUT";
    }
    return "NO_UPLOAD_BTN";
})()
"""

cleaned = ' '.join([l.strip() for l in click_js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{cleaned}")
    end tell
end tell
'''
p = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(ascript)
print("TRIGGER UPLOAD:", out.strip())

# Wait 0.8s for the native file dialog sheet to open
time.sleep(0.8)

# 2. Use System Events to navigate to the exact path
dialog_ascript = '''
tell application "System Events"
    tell process "Google Chrome"
        keystroke "g" using {command down, shift down}
        delay 0.6
        keystroke "/Users/nileshtiwari/Downloads/Resume-Nilesh-Tiwari-1302.pdf"
        delay 0.6
        key code 36 -- Return to enter path
        delay 0.8
        key code 36 -- Return to choose file
    end tell
end tell
'''
p2 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out2, err2 = p2.communicate(dialog_ascript)
print("FILE DIALOG SCRIPT OUT:", out2.strip())
if err2: print("ERR:", err2)

time.sleep(2.0)

# 3. Check if file is attached on Ashby form
check_js = """
(function() {
    var fileInput = document.getElementById("_systemfield_resume");
    var hasFile = fileInput && fileInput.files && fileInput.files.length > 0;
    var fileName = hasFile ? fileInput.files[0].name : "none";
    var textSnippet = document.body.innerText.slice(0, 500);
    var hasResumeText = textSnippet.includes("Resume-Nilesh-Tiwari-1302.pdf") || textSnippet.includes("1302.pdf");
    return JSON.stringify({
        hasFile: hasFile,
        fileName: fileName,
        hasResumeText: hasResumeText
    });
})()
"""
cleaned_check = ' '.join([l.strip() for l in check_js.split('\n') if l.strip() and not l.strip().startswith('//')]).replace('\\', '\\\\').replace('"', '\\"')
ascript_check = f'''
tell application "Google Chrome"
    tell (first tab of window 1 whose id is 33684133)
        return (execute javascript "{cleaned_check}")
    end tell
end tell
'''
p3 = subprocess.Popen(['osascript'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out3, err3 = p3.communicate(ascript_check)
print("FILE ATTACH STATUS:", out3.strip())
