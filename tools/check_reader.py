"""Render actual chapter files offline in installed Edge and test the reader."""
import argparse
from hashlib import sha256
import json

from playwright.sync_api import sync_playwright

from build_course import ROOT, content_digest, read


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('chapters',nargs='*',type=int)
    parser.add_argument('--pdf',action='store_true')
    args=parser.parse_args()
    selected=args.chapters or [c['number'] for c in read('plan/course-plan.json')['chapters']
                               if (ROOT/f"chapter-{c['number']:02d}-{c['slug']}.meta.json").exists()]
    out=ROOT/'work/validation';out.mkdir(parents=True,exist_ok=True)
    results=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge')
        context=browser.new_context(viewport={'width':1440,'height':1050})
        context.set_offline(True)
        for c in read('plan/course-plan.json')['chapters']:
            n=c['number']
            if n not in selected: continue
            path=ROOT/f"chapter-{n:02d}-{c['slug']}.html"
            page=context.new_page();js_errors=[];network=[]
            page.on('pageerror',lambda error:js_errors.append(str(error)))
            page.on('requestfailed',lambda request:network.append(request.url))
            errors=[]
            page.goto(path.as_uri())
            page.wait_for_function("document.documentElement.dataset.mathReady === 'true'",timeout=60000)
            math=page.locator('mjx-container').count()
            if not math: errors.append('no rendered mathematics')
            if n==1 and 'Pilot for author review' in page.locator('article .eyebrow').inner_text():
                errors.append('obsolete pilot status displayed')
            if page.locator('mjx-merror,[data-mjx-error]').count():
                errors.append('MathJax rendering error')
            if page.locator('details.solution').count()!=6:errors.append('not six solutions')
            page.locator('#solutions').click()
            if page.locator('details.solution[open]').count()!=6:errors.append('show-solutions control')
            page.locator('#solutions').click()
            if page.locator('details.solution[open]').count():errors.append('hide-solutions control')
            for control,classname in [('#theme','light'),('#size','large')]:
                page.locator(control).click()
                if not page.locator('body').evaluate('(n,c)=>n.classList.contains(c)',classname):
                    errors.append(f'{control} control failed')
                page.locator(control).click()
            if page.locator('.copybtn').count():
                button=page.locator('.copybtn').first
                button.click()
                page.wait_for_timeout(100)
                if button.inner_text()!='Copied!': errors.append('code copying failed')
            else:errors.append('no code-copy control')
            for width in (1440,390):
                page.set_viewport_size({'width':width,'height':1050})
                page.reload()
                page.wait_for_function("document.documentElement.dataset.mathReady === 'true'")
                if not page.evaluate('document.documentElement.scrollWidth<=innerWidth'):
                    errors.append(f'page overflow at {width}px')
                if width==390 and page.locator('#toc-disclosure').count() and page.locator('#toc-disclosure').evaluate('n=>n.open'):
                    errors.append('mobile contents not collapsed')
                page.screenshot(path=str(out/f'ch{n:02d}-{width}-top.png'))
                figures=page.locator('figure')
                for i in range(figures.count()):
                    fig=figures.nth(i);fig.scroll_into_view_if_needed()
                    if width==390:fig.screenshot(path=str(out/f'ch{n:02d}-figure-{i+1}-phone.png'))
                broken=page.locator('img').evaluate_all('nodes=>nodes.filter(n=>!n.complete||n.naturalWidth===0).map(n=>n.src)')
                if broken:errors.append(f'broken images: {broken}')
                if page.locator('figure img').count()!=page.locator('figure a.figure-link img').count():
                    errors.append('figure lacks full-size link')
            page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
            if page.locator('details.solution[open]').count()!=6:errors.append('print did not expand solutions')
            if args.pdf:
                page.emulate_media(media='print')
                page.pdf(path=str(out/f'ch{n:02d}-proof.pdf'),format='A4',print_background=True)
            page.evaluate("window.dispatchEvent(new Event('afterprint'))")
            page.emulate_media(media='screen')
            if page.locator('details.solution[open]').count():errors.append('print state not restored')
            errors.extend(js_errors)
            errors.extend('offline request failed: '+url for url in network)
            result={'chapter':n,'passed':not errors,'math_containers':math,'errors':errors,
                    'html_sha256':sha256(path.read_bytes()).hexdigest(),
                    'widths':[1440,390],'offline':True,'solutions':6,
                    'pdf_generated':args.pdf,
                    'pdf_sha256':sha256((out/f'ch{n:02d}-proof.pdf').read_bytes()).hexdigest() if args.pdf else None}
            results.append(result)
            (out/f'ch{n:02d}-browser-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
            print(f'Chapter {n}: math={math}, passed={not errors}, errors={errors}',flush=True)
            page.close()
        browser.close()
    report={'passed':bool(results) and all(r['passed'] for r in results),
            'scope':'actual offline Edge rendering and reading controls',
            'chapters':results,'content_digest':content_digest()}
    (out/'course-browser-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not report['passed'])


if __name__=='__main__':main()
