# Run through browser-harness stdin in an owned window; loopback only.
import json, os, time
from pathlib import Path
from urllib.parse import urlparse
BASE = os.environ['ATLAS_QA_URL']
OUT = Path(os.environ['ATLAS_QA_OUTPUT']); OUT.mkdir(parents=True, exist_ok=True)
CONTRACT = json.loads(Path(os.environ['ATLAS_QA_LINKS']).read_text())
parsed = urlparse(BASE)
assert parsed.hostname in ('127.0.0.1', 'localhost')
BASE = parsed._replace(query='review=draft-links&review=2', fragment='').geturl()
ORIGIN = parsed.scheme + '://' + parsed.netloc
TARGETS = [ident for candidate in CONTRACT for ident in [candidate['id']] + [p['id'] for p in candidate['panels']]]

def val(expr): return js('(() => ' + expr + ')()')
def wait(predicate, label):
    for attempt in range(80):
        try:
            if val('document.visibilityState') != 'visible': cdp('Page.bringToFront')
            if predicate(): return
        except RuntimeError as error:
            # Read-only retry during a dispatched page reload; never repeat input.
            if 'navigated or closed' not in str(error) and 'Cannot find context' not in str(error): raise
        time.sleep(.075)
    raise AssertionError(label)
def loaded(): wait(lambda: val('document.readyState')=='complete','document loaded')
def state(ident):
    return val('''{const el=document.getElementById(''' + json.dumps(ident) + ''');
      if (!el) return null;
      const r=el.getBoundingClientRect();
      const gap=el.querySelector('[data-draft-gap-details]');
      return {id:el.id,hash:location.hash,tab:document.querySelector('main button[aria-current=true]')?.textContent,
        hidden:!!el.closest('[hidden]'), top:r.top,bottom:r.bottom,width:r.width,
        gap:gap?gap.open:null,scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,
        inner:innerWidth, height:innerHeight,modal:!!document.querySelector('dialog[open]')};}''')
def ready(ident):
    s=state(ident)
    return s and s['tab']=='Draft charts' and not s['hidden'] and s['hash']=='#'+ident and s['top']>=64 and s['top']<s['height']-40

def screenshot(name): capture_screenshot(path=str(OUT/(name+'.png')))
def native_click(selector):
    # A fresh fragment can still have its post-layout scroll queued. Recheck the
    # hit target AFTER the screenshot; never dispatch input outside the viewport.
    for attempt in range(5):
        js('(() => document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center",behavior:"instant"}))()')
        capture_screenshot()
        rect=val('document.querySelector('+json.dumps(selector)+').getBoundingClientRect().toJSON()')
        x=rect['x']+rect['width']/2; y=rect['y']+rect['height']/2
        if not (0<x<val('innerWidth') and 64<y<val('innerHeight')): continue
        if not val('document.querySelector('+json.dumps(selector)+').contains(document.elementFromPoint('+str(x)+','+str(y)+'))'): continue
        click_at_xy(x,y)
        return
    raise AssertionError('No settled native hit target: '+selector)

report=[]
goto_url(BASE); loaded(); cdp('Page.bringToFront')
permission=js('(async () => (await navigator.permissions.query({name:"clipboard-read"})).state)()')
cdp('Browser.setPermission',permission={'name':'clipboard-read'},setting='granted',origin=ORIGIN)
try:
    for width in [1440,390,320]:
        cdp('Emulation.setDeviceMetricsOverride',width=width,height=1000,deviceScaleFactor=1,mobile=False)
        for ident in TARGETS:
            goto_url(BASE+'#'+ident);loaded();cdp('Page.reload',ignoreCache=True);loaded();cdp('Page.bringToFront')
            wait(lambda: ready(ident), 'fresh target '+ident+' at '+str(width))
            time.sleep(.12)
            s=state(ident)
            assert ready(ident), s
            assert not s['modal'] and s['gap'] is not False, s
            assert s['inner']==width and s['scroll']<=s['client'],s
            assert val('document.querySelector('+json.dumps('a[href="#'+ident+'"]')+').href')==BASE+'#'+ident
            report.append(dict(viewportWidth=width,**s))
        # Representative native links: candidate, independent panel and explicit gap.
        for ident in ['draft-largest-connectome','draft-panel-largest-connectome-synapses','draft-mapping-cost']:
            goto_url(BASE+'#draft-charts');loaded()
            wait(lambda: val('document.querySelector("main button[aria-current=true]")?.textContent')=='Draft charts','section tab')
            native_click('a[href="#'+ident+'"]')
            wait(lambda: ready(ident), 'native direct link '+ident)
            screenshot('direct-'+ident+'-'+str(width))
            history_length=val('history.length')
            native_click('a[href="#'+ident+'"]')
            wait(lambda: ready(ident), 'repeat direct link '+ident)
            assert val('history.length')==history_length
            native_click('[data-copy-draft-link="'+ident+'"]')
            screenshot('copy-'+ident+'-'+str(width))
            wait(lambda: val('document.querySelector('+json.dumps('[data-copy-draft-link="'+ident+'"]')+').parentElement.querySelector("[role=status]").textContent')=='Copied','copy result')
            assert js('(async () => await navigator.clipboard.readText())()')==BASE+'#'+ident
            assert val('location.hash')=='#'+ident
        # Back/Forward restores target visibility after a tab switch and a modal.
        ident='draft-brain-tissue-mapped'
        goto_url(BASE+'#'+ident);loaded();wait(lambda: ready(ident),'candidate')
        native_click('.draft-charts a[href="#tissue-mapped"]')
        wait(lambda: val('!!document.querySelector("dialog[open]")'),'existing metric modal')
        screenshot('existing-metric-'+str(width));press_key('Escape')
        wait(lambda: ready(ident),'modal return to candidate')
        js('(() => history.forward())()')
        wait(lambda: val('!!document.querySelector("dialog[open]")'),'Forward existing metric')
        press_key('Escape');wait(lambda: ready(ident),'Forward Close')
        native_click('main button:not([aria-current])')
        wait(lambda: val('document.querySelector("main button[aria-current=true]")?.textContent')!='Draft charts','tab changed')
        js('(() => history.back())()');wait(lambda: ready(ident),'Back to candidate')
        js('(() => history.forward())()')
        wait(lambda: val('document.querySelector("main button[aria-current=true]")?.textContent')!='Draft charts','Forward to other tab')
        goto_url(BASE+'#draft-panel-largest-connectome-synapses');loaded();wait(lambda: ready('draft-panel-largest-connectome-synapses'),'final panel')
        screenshot('panel-'+str(width))
    (OUT/'draft-links-browser-report.json').write_text(json.dumps({'targets':len(TARGETS),'freshCases':report,'nativeDirectRepeatCopy':True,'historyAndMetricReturn':True},indent=2)+'\n')
    print(json.dumps({'targets':len(TARGETS),'freshCases':len(report),'nativeDirectRepeatCopy':True,'historyAndMetricReturn':True}))
finally:
    cdp('Browser.setPermission',permission={'name':'clipboard-read'},setting=permission,origin=ORIGIN)
