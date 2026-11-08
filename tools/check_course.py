"""Check structure, local navigation, timestamps, and review evidence.

Run with --release only after every chapter has two independent reviews.
Numerical reproduction and real-browser checks have separate evidence reports.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
import re
from urllib.parse import parse_qs, unquote, urlsplit

from bs4 import BeautifulSoup

from build_course import ROOT, content_digest, read
from review_evidence import audit, audit_exported
from chapter_hashes import scientific_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', action='store_true')
    parser.add_argument('--exported-evidence', action='store_true',
                        help='Check preserved public acceptance records without private reports')
    args = parser.parse_args()
    errors, diagnostics = [], []
    plan = read('plan/course-plan.json')['chapters']
    source = read('source-manifest.json')
    if [c['number'] for c in plan]!=list(range(1,26)):
        errors.append('approved chapter sequence must contain chapters1–25 exactly once')
    if Counter(n for c in plan for n in c['lectures'])!=Counter(r['lecture'] for r in source['recordings']):
        errors.append('every requested lecture must have exactly one primary chapter')
    for c in plan:
        if any(dep<1 or dep>=c['number'] for dep in c['prerequisites']):
            errors.append(f'Chapter {c["number"]}: invalid or forward prerequisite')
    seen=set()
    for result in read('plan/results.yaml')['results']:
        if result['id'] in seen or any(dep not in seen for dep in result['depends_on']):
            errors.append(f'Result graph has duplicate, missing or forward edge: {result["id"]}')
        seen.add(result['id'])
    recording = {r['video_id']:r for r in source['recordings']}
    docs = {p.resolve():BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
            for p in ROOT.glob('*.html')
            if args.release or not p.name.startswith('chapter-')
            or p.with_suffix('.meta.json').exists()}
    links, timestamps = 0, 0
    for path, soup in docs.items():
        ids = [tag['id'] for tag in soup.select('[id]')]
        if len(ids)!=len(set(ids)):
            errors.append(f'{path.name}: duplicate HTML ids')
        if len(soup.select('h1'))!=1 or not soup.select_one('meta[name=viewport]'):
            errors.append(f'{path.name}: missing document contract')
        text = path.read_text(encoding='utf-8')
        if re.search(r'C:[/\\]Users[/\\]|\[(?:PROOF NEEDED|CITATION NEEDED|NUMBER NOT YET COMPUTED|AUTHOR DECISION NEEDED)',text):
            errors.append(f'{path.name}: private path or unresolved placeholder')
        for tag in soup.select('[href], [src]'):
            for attr in ('href','src'):
                if not tag.has_attr(attr):
                    continue
                link = tag[attr]
                parts = urlsplit(link)
                if parts.scheme in ('http','https'):
                    if 'youtube.com' in parts.netloc and parts.path=='/watch':
                        query=parse_qs(parts.query)
                        vid=query.get('v',[''])[0]
                        if vid not in recording:
                            errors.append(f'{path.name}: unassigned recording {vid}')
                        if 't' in query and vid in recording:
                            value=query['t'][0].rstrip('s')
                            if not value.isdigit() or not 0<=int(value)<=recording[vid]['duration_seconds']:
                                errors.append(f'{path.name}: invalid timestamp {link}')
                            timestamps+=1
                    continue
                if parts.scheme=='data':
                    continue
                if parts.scheme or parts.netloc:
                    errors.append(f'{path.name}: unsupported link {link}')
                    continue
                target=(path.parent/unquote(parts.path)).resolve() if parts.path else path
                if not target.is_relative_to(ROOT) or not target.is_file():
                    # During production a declared future chapter may not exist yet.
                    future=any(target.name==f"chapter-{c['number']:02d}-{c['slug']}.html" for c in plan)
                    if args.release or not future:
                        errors.append(f'{path.name}: missing local target {link}')
                elif parts.fragment and target in docs and not docs[target].find(id=unquote(parts.fragment)):
                    errors.append(f'{path.name}: missing fragment {link}')
                links+=1
    for c in plan:
        n=c['number']
        filename=f"chapter-{n:02d}-{c['slug']}.html"
        path=(ROOT/filename).resolve()
        if path not in docs:
            if args.release: errors.append(f'Chapter {n}: not authored')
            continue
        soup=docs[path]
        article=soup.select_one('article')
        if article is None:
            errors.append(f'{filename}: missing article')
            continue
        plain=article.get_text(' ',strip=True)
        plain=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$', '', plain)
        if re.search(r'\\(?:mathrm|mathbb|frac|theta|gamma|sum|begin)\b',plain):
            errors.append(f'{filename}: TeX command outside math delimiters')
        tags=re.findall(r'\\tag\{([^}]+)\}',str(article))
        if len(tags)!=len(set(tags)) or any(not tag.startswith(f'{n}.') for tag in tags):
            errors.append(f'{filename}: duplicate or wrong chapter equation numbering')
        solutions=soup.select('details.solution')
        if len(solutions)!=6:
            errors.append(f'{filename}: needs six solutions, found {len(solutions)}')
        for number,solution in enumerate(solutions,1):
            if len(solution.get_text(' ',strip=True).split())<25:
                errors.append(f'{filename}: solution {number} lacks developed reasoning')
        for fig in soup.select('figure'):
            if not fig.select_one('figcaption') or any(not img.get('alt') for img in fig.select('img')):
                errors.append(f'{filename}: figure caption/alt missing')
        for selector in ('#theme','#size','#solutions','#print','#laboratory'):
            if not soup.select_one(selector): errors.append(f'{filename}: missing {selector}')
        meta=read(filename.replace('.html','.meta.json'),{})
        science=set(scientific_files(n))
        if not meta.get('labs') or not meta.get('figures'):
            errors.append(f'{filename}: missing retained laboratory or original figure')
        for tag in article.select('[href],img[src]'):
            target=tag.get('href',tag.get('src',''))
            if target.startswith(('code/','figures/')) or (target.startswith('assets/') and target.endswith('.svg')):
                if target not in science:
                    errors.append(f'{filename}: linked scientific file omitted from review digest: {target}')
        coverage=meta.get('source_coverage',[])
        if n!=1 and Counter(item.get('lecture') for item in coverage)!=Counter(c['lectures']):
            errors.append(f'{filename}: source coverage does not match assigned lectures')
        for item in coverage:
            rec=next((r for r in source['recordings'] if r['lecture']==item.get('lecture')),None)
            if rec is None:continue
            for span in item.get('transcript_spans',[]):
                start,end=(span.get('start'),span.get('end')) if isinstance(span,dict) else span[:2]
                if not isinstance(start,(int,float)) or not isinstance(end,(int,float)) or not 0<=start<=end<=rec['duration_seconds']+2:
                    errors.append(f'{filename}: source span outside recording bounds')
        review='not yet accepted'
        if meta.get('status')=='accepted':
            try:
                (audit_exported if args.exported_evidence else audit)(n,meta)
                review=('two preserved acceptance records bind current artifacts' if args.exported_evidence
                        else 'two full reviews bind current artifacts')
            except (KeyError,ValueError,FileNotFoundError) as exc:
                errors.append(f'{filename}: {exc}')
        elif args.release:
            errors.append(f'{filename}: not accepted')
        diagnostics.append({'chapter':n,'article_text_words':len(article.get_text(' ',strip=True).split()),
                            'main_sections':len(article.select('h2')),'solutions':len(solutions),
                            'figures':len(article.select('figure')),'review':review,
                            'html_sha256':sha256(path.read_bytes()).hexdigest()})
    for r in source['recordings']:
        path=ROOT/'work/sources/captions'/f"{r['lecture']:02d}-{r['video_id']}.json"
        if path.exists() and sha256(path.read_bytes()).hexdigest()!=r['caption_sha256']:
            errors.append(f'Caption source digest changed: L{r["lecture"]}')
        if args.release and not r.get('sequentially_read'):
            errors.append(f'Caption not sequentially read: L{r["lecture"]}')
    report={'passed':not errors,'scope':'structure, link, timestamp and review-evidence consistency',
            'release_mode':args.release,
            'review_evidence_mode':'preserved exported records' if args.exported_evidence else 'actual private reports',
            'errors':errors,'local_links_checked':links,
            'timestamp_links_checked':timestamps,'chapters':diagnostics,'content_digest':content_digest(),
            'limits':['does not replace scientific review','does not certify caption fidelity or continuous audiovisual coverage']}
    out=ROOT/'work/validation';out.mkdir(parents=True,exist_ok=True)
    (out/'course-static-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    raise SystemExit(bool(errors))


if __name__=='__main__':
    main()
