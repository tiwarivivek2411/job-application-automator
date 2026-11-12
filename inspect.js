(function() {
    var inputs = document.querySelectorAll('input');
    var info = [];
    inputs.forEach(function(inp) {
        info.push({
            id: inp.id || '',
            name: inp.name || '',
            className: inp.className || '',
            type: inp.type || '',
            placeholder: inp.placeholder || '',
            value: inp.value || ''
        });
    });
    
    var buttons = document.querySelectorAll('button, a, [role="button"]');
    var btnInfo = [];
    buttons.forEach(function(btn) {
        var txt = btn.innerText ? btn.innerText.trim() : '';
        if (txt !== '') {
            btnInfo.push({
                tag: btn.tagName,
                id: btn.id || '',
                text: txt,
                className: btn.className || '',
                href: btn.href || ''
            });
        }
    });
    
    return JSON.stringify({inputs: info, buttons: btnInfo});
})()
