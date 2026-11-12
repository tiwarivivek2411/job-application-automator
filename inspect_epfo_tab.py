import subprocess
import json

# Read the JS file
with open("/Users/nileshtiwari/.gemini/antigravity/scratch/inspect.js", "r") as f:
    js_code = f.read()

# Escape double quotes and backslashes for AppleScript
escaped_js = js_code.replace('\\', '\\\\').replace('"', '\\"')

applescript = f"""
tell application "Google Chrome"
    set foundTab to missing value
    set windowList to every window
    repeat with w in windowList
        set tabList to every tab of w
        repeat with t in tabList
            if URL of t contains "mis.epfindia.gov.in" or title of t contains "EPFO-MIS" then
                set foundTab to t
                exit repeat
            end if
        end repeat
        if foundTab is not missing value then exit repeat
    end repeat
    
    if foundTab is not missing value then
        set resultHTML to execute foundTab javascript "{escaped_js}"
        return resultHTML
    else
        return "Tab not found"
    end if
end tell
"""

proc = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
if proc.returncode != 0:
    print("Error:", proc.stderr)
else:
    output = proc.stdout.strip()
    if output == "Tab not found":
        print(output)
    else:
        try:
            data = json.loads(output)
            print("INPUTS:")
            for inp in data["inputs"]:
                print(f"  - ID: {inp['id']}, Name: {inp['name']}, Class: {inp['className']}, Type: {inp['type']}, Placeholder: {inp['placeholder']}, Value: {inp['value']}")
            print("\nBUTTONS/LINKS (sample of 15):")
            for btn in data["buttons"][:15]:
                print(f"  - Tag: {btn['tag']}, ID: {btn['id']}, Text: {btn['text']}, Class: {btn['className']}, Href: {btn['href'][:60]}")
        except Exception as e:
            print("Failed to parse JSON:", e)
            print("Raw output:", output[:1000])
