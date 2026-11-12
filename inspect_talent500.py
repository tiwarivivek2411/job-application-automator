import subprocess
import urllib.parse
import json

js_code = """
(function() {
    try {
        let card = document.querySelector('div[class*="CardContainer"]');
        if (!card) return encodeURIComponent("NO CARD");
        
        // Find all clickable children or inspect React props
        let reactKey = Object.keys(card).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance') || k.startsWith('__reactProps'));
        let props = reactKey ? card[reactKey] : null;
        
        // Let's see if card has an onclick or if its children have onclick
        let cardChild = card.firstElementChild;
        let cardChildReactKey = cardChild ? Object.keys(cardChild).find(k => k.startsWith('__reactProps')) : null;
        let cardChildProps = (cardChild && cardChildReactKey) ? cardChild[cardChildReactKey] : null;

        // Let's also check if clicking cardChild triggers anything
        let res = {
            hasReactKey: !!reactKey,
            cardTag: card.tagName,
            childTag: cardChild ? cardChild.tagName : null,
            childClass: cardChild ? cardChild.className : null,
            onClickOnChild: cardChildProps ? typeof cardChildProps.onClick : 'none'
        };
        return encodeURIComponent(JSON.stringify(res));
    } catch(e) {
        return "ERR: " + encodeURIComponent(e.message);
    }
})()
"""

def run_js(tab_idx, code):
    cleaned = ' '.join([line.strip() for line in code.splitlines() if line.strip()]).replace('\\', '\\\\').replace('"', '\\"')
    apple_script = f'''
    tell application "Google Chrome"
        set t to tab {tab_idx} of front window
        return execute t javascript "{cleaned}"
    end tell
    '''
    res = subprocess.run(['osascript', '-e', apple_script], capture_output=True, text=True)
    raw = res.stdout.strip()
    return urllib.parse.unquote(raw)

print(run_js(6, js_code))
