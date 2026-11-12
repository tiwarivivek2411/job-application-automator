import subprocess, time, json, sys

def run_applescript(script):
    p = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.decode('utf-8').strip(), err.decode('utf-8').strip()

# Already applied PIDs
applied_pids = {
    "1970324837573743", "1970324837568245", "1970324837524060",
    "1970324837570935", "1970324837576448", "1970324837544085",
    "1970324837568242", "1970324837561930", "1970324837568246",
    "1970324837571103", "1970324837577448", "1970324837571096",
    "1970324837571101", "1970324837538045"
}

target_new_applications = 15
newly_applied = []

print(f"Starting page-by-page auto-apply. Target: {target_new_applications} new positions.")

# Find our primary search tab ID / index
# We'll use a dedicated tab for applying
start_offset = 0

while len(newly_applied) < target_new_applications and start_offset < 100:
    page_url = f"https://jobs.ascendion.com/careers?domain=ascendion.com&hl=&start={start_offset}&location=India&sort_by=match&filter_include_remote=1&filter_include_relocation=0"
    print(f"\n--- Loading Page at start={start_offset} ---")
    
    # Navigate the main search tab
    nav_script = f'''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "jobs.ascendion.com/careers" and not (u contains "/apply/success") then
                    tell t to set URL to "{page_url}"
                    return "NAVIGATED"
                end if
            end repeat
        end repeat
        return "NOT_FOUND"
    end tell
    '''
    run_applescript(nav_script)
    time.sleep(4)
    
    # Extract jobs from current page
    get_jobs_script = '''
    tell application "Google Chrome"
        repeat with w in windows
            repeat with t in tabs of w
                set u to (URL of t as string)
                if u contains "jobs.ascendion.com/careers" and not (u contains "/apply") then
                    tell t
                        return execute javascript "
                            (function() {
                                const anchors = Array.from(document.querySelectorAll('a[href*=\"/careers/job/\"], a[href*=\"pid=\"]'));
                                const jobs = [];
                                const seen = new Set();
                                for (const a of anchors) {
                                    let pidMatch = a.href.match(/job\\/(\\d+)/) || a.href.match(/pid=(\\d+)/);
                                    if (pidMatch) {
                                        const pid = pidMatch[1];
                                        if (!seen.has(pid)) {
                                            seen.add(pid);
                                            const title = a.innerText.trim().split('\\n')[0];
                                            if (title) jobs.push({ pid: pid, title: title, href: a.href });
                                        }
                                    }
                                }
                                return JSON.stringify(jobs);
                            })()
                        "
                    end tell
                end if
            end repeat
        end repeat
    end tell
    '''
    jobs_json, _ = run_applescript(get_jobs_script)
    try:
        jobs_on_page = json.loads(jobs_json) if jobs_json else []
    except:
        jobs_on_page = []
        
    print(f"Found {len(jobs_on_page)} jobs on page start={start_offset}:")
    for j in jobs_on_page:
        print(f"  * {j['title']} (PID: {j['pid']})")
        
    if not jobs_on_page:
        print("No more jobs found. Moving to next offset...")
        start_offset += 10
        continue

    # Process unapplied jobs on this page
    for job in jobs_on_page:
        if len(newly_applied) >= target_new_applications:
            break
            
        pid = job['pid']
        title = job['title']
        
        if pid in applied_pids:
            print(f"Skipping already applied: {title} ({pid})")
            continue
            
        print(f"\n[{len(newly_applied)+1}/{target_new_applications}] Applying to: {title} (PID: {pid})...")
        
        # Navigate to apply page for this PID
        apply_url = f"https://jobs.ascendion.com/careers/apply?pid={pid}&domain=ascendion.com&hl="
        nav_apply_script = f'''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    set u to (URL of t as string)
                    if u contains "jobs.ascendion.com/careers" and not (u contains "/apply/success") then
                        tell t to set URL to "{apply_url}"
                        return "NAVIGATED_APPLY"
                    end if
                end repeat
            end repeat
        end tell
        '''
        run_applescript(nav_apply_script)
        time.sleep(3.5)
        
        # Dispatch Submit Application
        submit_script = f'''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    set u to (URL of t as string)
                    if u contains "{pid}" then
                        tell t
                            return execute javascript "
                                (function() {
                                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim().toLowerCase().includes('submit application'));
                                    if (btn) {
                                        if (btn.disabled) return 'DISABLED';
                                        btn.click();
                                        btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                                        btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                                        btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                                        return 'SUBMITTED';
                                    }
                                    return 'NO_BTN';
                                })()
                            "
                        end tell
                    end if
                end repeat
            end repeat
        end tell
        '''
        res, _ = run_applescript(submit_script)
        print(f"  -> Submit click: {res}")
        time.sleep(3.5)
        
        # Verify success
        verify_script = f'''
        tell application "Google Chrome"
            repeat with w in windows
                repeat with t in tabs of w
                    set u to (URL of t as string)
                    if u contains "{pid}" then
                        tell t
                            return execute javascript "
                                (function() {
                                    const isSuccess = window.location.href.includes('/apply/success') || document.body.innerText.includes('Thank you for your application');
                                    return isSuccess ? 'SUCCESS' : ('FAILED_OR_PENDING:' + window.location.href);
                                })()
                            "
                        end tell
                    end if
                end repeat
            end repeat
        end tell
        '''
        v_res, _ = run_applescript(verify_script)
        print(f"  -> Verification: {v_res}")
        
        applied_pids.add(pid)
        newly_applied.append({"title": title, "pid": pid, "status": v_res})
        
        # 5 second human pause between applications
        print("  -> Cooldown 5s...")
        time.sleep(5)
        
    start_offset += 10

print("\n===============================")
print(f"Batch completed! Applied to {len(newly_applied)} new jobs.")
print("===============================")
for item in newly_applied:
    print(f"- {item['title']} ({item['pid']}): {item['status']}")
