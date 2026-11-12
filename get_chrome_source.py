import subprocess

applescript = """
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
        return source of foundTab
    else
        return "Tab not found"
    end if
end tell
"""

proc = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
if proc.returncode != 0:
    print("Error:", proc.stderr)
else:
    src = proc.stdout
    print("Length of source:", len(src))
    # Save source to a file so we can view it
    with open("/Users/nileshtiwari/.gemini/antigravity/scratch/epfo_source.html", "w") as f:
        f.write(src)
    print("Saved source to /Users/nileshtiwari/.gemini/antigravity/scratch/epfo_source.html")
