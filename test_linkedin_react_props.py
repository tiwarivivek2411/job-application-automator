from inspect_linkedin_view import run_js
import time

js = """
(() => {
    const btn = Array.from(document.querySelectorAll('button'))
        .find(b => b.offsetWidth > 0 && b.innerText && b.innerText.toLowerCase().includes('easy apply'));
    if (!btn) return 'NO_BTN';

    const reactKey = Object.keys(btn).find(k => k.startsWith('__reactProps') || k.startsWith('__reactEventHandlers'));
    if (!reactKey) {
        // Check parent
        const pKey = Object.keys(btn.parentElement || {}).find(k => k.startsWith('__reactProps'));
        return 'NO_KEY_ON_BTN, parent: ' + pKey;
    }

    const props = btn[reactKey];
    const handlerNames = Object.keys(props).filter(k => typeof props[k] === 'function');
    
    if (props.onClick) {
        props.onClick({
            preventDefault: () => {},
            stopPropagation: () => {},
            target: btn,
            currentTarget: btn,
            nativeEvent: new MouseEvent('click')
        });
        return 'TRIGGERED_REACT_ONCLICK: ' + handlerNames.join(', ');
    }
    
    return 'NO_ONCLICK_IN_PROPS: ' + handlerNames.join(', ');
})()
"""
out, _ = run_js(js)
print(out)
time.sleep(2.0)

check_js = """
(() => {
    const dialogs = Array.from(document.querySelectorAll('*')).filter(el => {
        return (el.getAttribute('role') === 'dialog' || el.getAttribute('aria-modal') === 'true');
    });
    return 'DIALOGS: ' + dialogs.length;
})()
"""
print(run_js(check_js)[0])
