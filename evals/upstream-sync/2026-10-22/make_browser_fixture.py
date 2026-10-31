"""Build disposable browser examples from the adopted Markdown HTML/CSS."""
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(__file__).resolve().parents[3]
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
for skill, reference, prefix, control, param, count in [
    ('state-machine', 'switcher.md', 'state', 'state-switcher', '__state', 30),
    ('variant', 'picker.md', 'variant', 'variant-picker', '__variant', 3),
]:
    text = (root / 'skills/design' / skill / reference).read_text()
    markup = re.search(r'```html\n(.*?)\n```', text, re.S).group(1)
    css = re.search(r'```css\n(.*?)\n```', text, re.S).group(1)
    groups = [('Data', 0, 10), ('Account', 10, 20), ('Access', 20, 30)] if count == 30 else [('Density', 0, 3)]
    rows, options = [], []
    for name, first, last in groups:
        labels = [(f'choice-{i}', f'{name} {i+1}: 상태와 접근 권한') for i in range(first, last)]
        rows.append(f'<div class="{control}-group" role="group" aria-labelledby="group-{name}"><span class="{control}-heading" id="group-{name}">{name}</span>' + ''.join(f'<button type="button" data-{prefix}="{key}">{label}</button>' for key, label in labels) + '</div>')
        options.append(f'<optgroup label="{name}">' + ''.join(f'<option value="{key}">{label}</option>' for key, label in labels) + '</optgroup>')
    markup = re.sub(r'(<nav[^>]*>).*?(</nav>)', lambda m: m[1] + ''.join(rows) + m[2], markup, flags=re.S)
    markup = re.sub(r'(<select[^>]*>).*?(</select>)', lambda m: m[1] + ''.join(options) + m[2], markup, flags=re.S)
    markup = re.sub(r'<!-- the (?:component|piece),.*?-->', '<section><h1>Demo component</h1><p id="active"></p><label>Working input <input id="draft" value="keep this text"></label><button id="save">Save draft</button><p id="feedback"></p></section>', markup)
    # This adapter demonstrates the prose contract; it is not shipped skill code.
    behavior = '''const config = CONFIG;
const buttons = [...document.querySelectorAll(`[data-${config.prefix}]`)];
const select = document.querySelector('select');
const keys = buttons.map(b => b.dataset[config.prefix]);
function show(key, write=true) {
 if (!keys.includes(key)) key=keys[0];
 if (write) { const url=new URL(location);url.searchParams.set(config.param,key);history.replaceState({},'',url); }
 buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset[config.prefix]===key)));
 select.value=key;document.querySelector('#active').textContent=key;
 const active=buttons.find(b=>b.dataset[config.prefix]===key);
 const nav=document.querySelector('nav');
 if(getComputedStyle(nav).display!=='none')nav.scrollTop=active.offsetTop-nav.offsetTop-nav.clientHeight/2;
}
buttons.forEach(b=>b.addEventListener('click',()=>show(b.dataset[config.prefix])));
select.addEventListener('change',()=>show(select.value));
document.querySelector('#save').addEventListener('click',()=>document.querySelector('#feedback').textContent='Saved: '+document.querySelector('#draft').value);
document.addEventListener('keydown',e=>{
 if(e.defaultPrevented||e.metaKey||e.ctrlKey||e.altKey||e.shiftKey||e.target.closest('input,textarea,select,[contenteditable]'))return;
 if(e.key.toLowerCase()==='h'){e.preventDefault();document.body.classList.toggle('controls-hidden');return;}
 const delta={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[e.key];
 if(delta){e.preventDefault();show(keys[(keys.indexOf(select.value)+delta+keys.length)%keys.length]);}
});
show(new URL(location).searchParams.get(config.param));
'''.replace('CONFIG', json.dumps({'prefix': prefix, 'param': param}))
    page = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Upstream control fixture</title><link rel="icon" href="data:,"><style>body{margin:0;font:16px system-ui;background:#eee}main{max-width:960px;margin:auto}section{background:white;padding:16px}input{max-width:100%;box-sizing:border-box}button:focus-visible,input:focus-visible{outline:2px solid blue}body.controls-hidden nav,body.controls-hidden [class$="-select"]{display:none!important}</style><style>'+css+'</style><main>'+markup+'</main><script>'+behavior+'</script>'
    (out / (skill + '.html')).write_text(page)
print(out)
