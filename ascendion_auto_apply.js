// ==UserScript==
// @name         Ascendion Auto-Apply Assistant
// @namespace    https://jobs.ascendion.com/
// @version      1.0
// @description  Automate applying to relevant jobs on Ascendion career portal with safety controls
// @match        https://jobs.ascendion.com/careers*
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  // State management
  let isRunning = false;
  let shouldStop = false;
  let appliedCount = 0;
  let targetLimit = 25; // Recommended safe limit to avoid maxApplicationsSpam (50)
  let delayBetweenMs = 5000;
  let filterKeywords = []; // e.g. ["software", "java", "developer"]

  // Helper sleep
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  // Helper: Find button by text regex
  function findButton(regex, parent = document) {
    const elements = Array.from(parent.querySelectorAll('button, a[role="button"], div[role="button"], input[type="submit"]'));
    return elements.find(el => {
      const text = (el.innerText || el.value || el.getAttribute('aria-label') || '').trim();
      return regex.test(text) && el.offsetParent !== null && !el.disabled;
    });
  }

  // Create In-Page Control UI
  function createUI() {
    if (document.getElementById('ascendion-bot-panel')) return;

    const panel = document.createElement('div');
    panel.id = 'ascendion-bot-panel';
    panel.style.cssText = `
      position: fixed;
      top: 70px;
      right: 20px;
      width: 320px;
      background: #ffffff;
      border: 2px solid #6464d7;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.2);
      z-index: 999999;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      padding: 16px;
      color: #333;
    `;

    panel.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <h4 style="margin:0; font-size:15px; font-weight:700; color:#6464d7;">Ascendion Auto-Apply</h4>
        <span id="bot-status-tag" style="background:#e0e0e0; font-size:11px; padding:2px 8px; border-radius:10px; font-weight:600;">IDLE</span>
      </div>

      <div style="margin-bottom:10px;">
        <label style="font-size:12px; font-weight:600; display:block; margin-bottom:4px;">Keyword Filter (Comma separated, empty for all):</label>
        <input id="bot-keywords" type="text" placeholder="e.g. Developer, Java, Engineer" style="width:100%; box-sizing:border-box; padding:6px 8px; border:1px solid #ccc; border-radius:6px; font-size:12px;">
      </div>

      <div style="display:flex; gap:10px; margin-bottom:12px;">
        <div style="flex:1;">
          <label style="font-size:12px; font-weight:600; display:block; margin-bottom:4px;">Max Jobs:</label>
          <input id="bot-max-jobs" type="number" value="25" min="1" max="50" style="width:100%; box-sizing:border-box; padding:6px 8px; border:1px solid #ccc; border-radius:6px; font-size:12px;">
          <small style="color:#d9534f; font-size:10px;">ATS limit: 50</small>
        </div>
        <div style="flex:1;">
          <label style="font-size:12px; font-weight:600; display:block; margin-bottom:4px;">Delay (sec):</label>
          <input id="bot-delay" type="number" value="5" min="3" max="30" style="width:100%; box-sizing:border-box; padding:6px 8px; border:1px solid #ccc; border-radius:6px; font-size:12px;">
        </div>
      </div>

      <div style="display:flex; gap:8px; margin-bottom:12px;">
        <button id="bot-start-btn" style="flex:1; background:#6464d7; color:#fff; border:none; padding:8px 0; border-radius:6px; font-weight:600; cursor:pointer; font-size:13px;">Start</button>
        <button id="bot-stop-btn" style="flex:1; background:#ef4444; color:#fff; border:none; padding:8px 0; border-radius:6px; font-weight:600; cursor:pointer; font-size:13px;" disabled>Stop</button>
      </div>

      <div id="bot-log" style="height:100px; overflow-y:auto; background:#f8f9fa; border:1px solid #eee; border-radius:6px; padding:6px 8px; font-size:11px; color:#555; font-family:monospace; line-height:1.4;">
        Ready. Ensure you are logged in and your profile/resume is saved.
      </div>
    `;

    document.body.appendChild(panel);

    const logEl = document.getElementById('bot-log');
    const statusTag = document.getElementById('bot-status-tag');
    const startBtn = document.getElementById('bot-start-btn');
    const stopBtn = document.getElementById('bot-stop-btn');

    function log(msg, color = '#555') {
      const p = document.createElement('div');
      p.style.color = color;
      p.innerText = `[${new Date().toLocaleTimeString()}] ${msg}`;
      logEl.appendChild(p);
      logEl.scrollTop = logEl.scrollHeight;
      console.log(`[AutoApply] ${msg}`);
    }

    startBtn.onclick = () => {
      const kwVal = document.getElementById('bot-keywords').value.trim();
      filterKeywords = kwVal ? kwVal.split(',').map(s => s.trim().toLowerCase()).filter(Boolean) : [];
      targetLimit = parseInt(document.getElementById('bot-max-jobs').value, 10) || 25;
      delayBetweenMs = Math.max(3000, (parseInt(document.getElementById('bot-delay').value, 10) || 5) * 1000);

      isRunning = true;
      shouldStop = false;
      startBtn.disabled = true;
      stopBtn.disabled = false;
      statusTag.innerText = 'RUNNING';
      statusTag.style.background = '#dcfce7';
      statusTag.style.color = '#15803d';

      log(`Started. Max jobs: ${targetLimit}, Delay: ${delayBetweenMs / 1000}s`);
      if (filterKeywords.length > 0) {
        log(`Filtering for keywords: ${filterKeywords.join(', ')}`);
      } else {
        log(`No filter applied (processing all positions).`);
      }

      runLoop(log);
    };

    stopBtn.onclick = () => {
      shouldStop = true;
      log('Stopping requested...', '#b91c1c');
    };
  }

  // Find job cards on current search page
  function getVisibleJobCards() {
    // Look inside search results
    const container = document.querySelector('[class*="searchResultContainer"]') || document.querySelector('#pcsx');
    if (!container) return [];

    // Find card elements: Look for position titles or clickable cards
    // Often Eightfold cards contain an h2, h3, or h4 with the role title
    const potentialCards = Array.from(container.querySelectorAll('div')).filter(div => {
      const hasHeading = div.querySelector('h1, h2, h3, h4, [class*="jobTitle"], [class*="positionTitle"]');
      const isCardLevel = div.getAttribute('role') === 'button' || div.getAttribute('tabindex') === '0' || div.className.includes('Card') || div.className.includes('card');
      return hasHeading && isCardLevel;
    });

    if (potentialCards.length > 0) return potentialCards;

    // Fallback: collect all h3 / h4 within container and take their closest clickable parent
    const titles = Array.from(container.querySelectorAll('h2, h3, h4'));
    const cards = [];
    titles.forEach(t => {
      const card = t.closest('div[class*="container"], div[class*="Card"], div[role="button"]') || t.parentElement;
      if (card && !cards.includes(card)) cards.push(card);
    });

    return cards;
  }

  // Check if job matches user filter
  function matchesFilter(cardText) {
    if (filterKeywords.length === 0) return true;
    const lower = cardText.toLowerCase();
    return filterKeywords.some(kw => lower.includes(kw));
  }

  // Find Next Page Button
  function findNextPageButton() {
    // 1. Button or link with "Next" or aria-label "Next"
    const nextBtn = findButton(/next|›|»/i);
    if (nextBtn) return nextBtn;

    // 2. Chevron icon next
    const icon = document.querySelector('i[class*="chevron-right"], i[class*="angle-right"], svg[class*="chevron-right"]');
    if (icon) {
      return icon.closest('button, a, div[role="button"]');
    }

    return null;
  }

  // Main processing loop
  async function runLoop(log) {
    const statusTag = document.getElementById('bot-status-tag');
    const startBtn = document.getElementById('bot-start-btn');
    const stopBtn = document.getElementById('bot-stop-btn');

    try {
      while (isRunning && !shouldStop && appliedCount < targetLimit) {
        const cards = getVisibleJobCards();
        log(`Found ${cards.length} job cards on current view.`);

        if (cards.length === 0) {
          log('No job cards found. Ensure search results have loaded.', '#b91c1c');
          break;
        }

        let processedOnPage = 0;

        for (let i = 0; i < cards.length; i++) {
          if (shouldStop || appliedCount >= targetLimit) break;

          const card = cards[i];
          const title = (card.querySelector('h1, h2, h3, h4') || card).innerText.trim().split('\n')[0];

          if (!matchesFilter(card.innerText)) {
            log(`Skipping: "${title}" (Doesn't match keywords)`);
            continue;
          }

          log(`Selecting job [${appliedCount + 1}/${targetLimit}]: "${title}"`);

          // 1. Click card to display details
          card.scrollIntoView({ behavior: 'smooth', block: 'center' });
          card.click();
          await sleep(1500);

          // 2. Check if already applied
          const alreadyApplied = findButton(/applied|application submitted/i);
          if (alreadyApplied) {
            log(`Already applied to "${title}". Skipping.`);
            continue;
          }

          // 3. Find and click "Apply" or "Apply now"
          const applyBtn = findButton(/^apply(\s+now)?$/i);
          if (!applyBtn) {
            log(`"Apply" button not found or already applied for "${title}".`);
            continue;
          }

          log(`Clicking "Apply" for "${title}"...`);
          applyBtn.click();
          await sleep(2500);

          // 4. Look for Submit Application button
          // Either in modal, drawer, or apply-form-container
          const submitBtn = findButton(/^(submit\s+application|submit)$/i);

          if (submitBtn) {
            log(`Found Submit button. Submitting application...`);
            submitBtn.click();
            await sleep(3000);

            // 5. Check for confirmation modal / Close button
            const closeBtn = findButton(/^(done|close|okay|ok|dismiss|×)$/i) || document.querySelector('button[aria-label="Close"], [class*="closeButton"]');
            if (closeBtn) {
              closeBtn.click();
              await sleep(1000);
            }

            appliedCount++;
            processedOnPage++;
            log(`Successfully applied to "${title}"! (Total: ${appliedCount})`, '#15803d');

            // Delay between applications
            log(`Waiting ${delayBetweenMs / 1000}s cooldown before next application...`);
            await sleep(delayBetweenMs);
          } else {
            log(`Notice: Extra questions or resume required for "${title}". Pausing 5s for manual review...`, '#d97706');
            await sleep(5000);
          }
        }

        if (appliedCount >= targetLimit) {
          log(`Target limit reached (${targetLimit} jobs applied). Halting to prevent spam flags.`, '#15803d');
          break;
        }

        // Try navigating to next page
        const nextBtn = findNextPageButton();
        if (nextBtn && !nextBtn.disabled && nextBtn.getAttribute('aria-disabled') !== 'true') {
          log('Moving to next page of jobs...');
          nextBtn.click();
          await sleep(3500);
        } else {
          log('No more pages or next button found.');
          break;
        }
      }
    } catch (err) {
      log(`Error occurred: ${err.message}`, '#b91c1c');
    } finally {
      isRunning = false;
      startBtn.disabled = false;
      stopBtn.disabled = true;
      statusTag.innerText = 'FINISHED';
      statusTag.style.background = '#e0e0e0';
      statusTag.style.color = '#333';
      log(`Execution ended. Total applied: ${appliedCount}`);
    }
  }

  // Initialize UI once page is ready
  window.addEventListener('load', () => setTimeout(createUI, 1500));
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(createUI, 1500);
  }
})();
