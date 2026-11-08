"""Build reader navigation and evidence manifests from authored chapters.

No manuscript prose is generated here. Scientific acceptance requires actual
independent review reports bound to the current scientific artifacts.
"""
from collections import Counter
from hashlib import sha256
from html import escape as e
import json
from pathlib import Path
import re

from chapter_hashes import ROOT, hashes
from review_evidence import audit, audit_exported


def read(name, default=None):
    path = ROOT / name
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def write(name, value):
    atomic_text(name,json.dumps(value, indent=2)+'\n')


def atomic_text(name,text):
    target=ROOT/name
    temporary=target.with_name(target.name+'.tmp')
    temporary.write_text(text,encoding='utf-8')
    temporary.replace(target)


def content_digest():
    paths = list(ROOT.glob('chapter-??-*.html'))
    for folder in ('assets', 'code', 'figures'):
        paths.extend(p for p in (ROOT / folder).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts)
    values = {p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest()
              for p in sorted(paths)}
    return sha256(json.dumps(values, sort_keys=True).encode()).hexdigest()


def page(title, body):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark light">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'">
<title>{e(title)} · Physical Applications of Stochastic Processes</title>
<link rel="stylesheet" href="assets/plan.css"><script defer src="assets/plan.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header><a class="brand" href="index.html">Physical Applications of Stochastic Processes</a>
<nav aria-label="Course"><a href="index.html#chapters">Chapters</a><a href="laboratories.html">Laboratories</a><a href="source-map.html">Recordings and evidence</a><a href="VALIDATION.md">Validation</a></nav></header>
<main id="main">{body}</main><footer>Independent study edition. Source course: NPTEL 115106089,
V. Balakrishnan, IIT Madras. No institutional endorsement is implied.
Original exposition and teaching examples; source recordings retain their owners' rights.</footer></body></html>'''


def controls(expand=False):
    return ('<div class="tools" aria-label="Reading controls">'
            '<button id="theme" aria-pressed="false">Light theme</button>'
            '<button id="size" aria-pressed="false">Larger text</button>'
            + ('<button id="expand" aria-pressed="false">Expand chapters</button>' if expand else '') + '</div>')


def build(exported_evidence=False):
    plan, sources = read('plan/course-plan.json'), read('source-manifest.json')
    chapters = plan['chapters']
    prior_completion=read('completion.json',{})
    recordings = {r['lecture']: r for r in sources['recordings']}
    if Counter(x for c in chapters for x in c['lectures']) != Counter(recordings.keys()):
        raise ValueError('recordings must be assigned once')
    entries, cards, labcards, pending, allhashes = [], [], [], [], {}
    for c in chapters:
        n = c['number']
        filename = f"chapter-{n:02d}-{c['slug']}.html"
        meta = read(filename.replace('.html', '.meta.json'), {})
        drafted = bool(meta and (ROOT / filename).exists())
        accepted, reason, reviews = False, None, []
        if drafted:
            allhashes[str(n)] = hashes(n)
            if meta.get('status') == 'accepted':
                try:
                    evidence = audit_exported(n,meta) if exported_evidence else audit(n, meta)
                    accepted, reviews = True, evidence['independent_full_reviews']
                except (ValueError, KeyError, FileNotFoundError) as exc:
                    reason = str(exc)
            coverage = meta.get('source_coverage', [])
            for item in coverage:
                if not isinstance(item, dict) or item.get('lecture') not in recordings:
                    continue
                record = recordings[item['lecture']]
                if item.get('sequentially_read'):
                    record.update(sequentially_read=True, caption_status='acquired and sequentially read',
                                  textual_coverage='full acquired caption text read; section map retained')
                visual = item.get('visual_coverage', record['visual_coverage'])
                if isinstance(visual, dict):
                    visual = visual.get('coverage', 'partial still sampling') + '; times (s): ' + ', '.join(map(str,visual.get('times_seconds',[])))
                record['visual_coverage'] = visual
                record['audio_reviewed_independently'] = item.get('audio_reviewed_independently', False)
        label = 'Reviewed' if accepted else ('Draft · review pending' if drafted else 'In preparation')
        if not accepted:
            pending.append(n)
        entry = {'number': n, 'title': c['title'], 'file': filename,
                 'recordings': c['lectures'], 'status': 'accepted' if accepted else ('draft' if drafted else 'planned'),
                 'page_budget': c['pages'], 'results': [f'R{n:02d}-{i}' for i in range(1,4)],
                 'accepted_reviews': reviews, 'labs': meta.get('labs', []),
                 'figures': meta.get('figures', []), 'solutions': meta.get('solutions', 0),
                 'review_evidence_issue': reason}
        entries.append(entry)
        body = ([f'<p><a href="{filename}"><strong>Read chapter {n}</strong></a> · {label}</p>'] if drafted else [])
        body.extend([f'<p class="meta">Lectures {", ".join(map(str,c["lectures"]))} · Prerequisites: {", ".join(map(str,c["prerequisites"])) or "entry prerequisites"}</p>',
                     f'<p>{e(c["case"])}</p><p>{e(c["coverage"])}</p>'])
        for i, result in enumerate(c['sections'],1):
            body.append(f'<section class="section-plan"><h4>Core result {i}: {e(result["title"])}</h4><p>{e(result["statement"])}</p><p><strong>Boundary.</strong> {e(result["boundary"])}</p></section>')
        body.append(f'<p><strong>Laboratory.</strong> {e(c["lab"])}</p>')
        cards.append(f'<details class="chapter" id="ch{n:02d}"><summary>{n:02d} · {e(c["title"])}<span class="tag">{label}</span></summary><div class="chapter-body">{"".join(body)}</div></details>')
        if drafted:
            links = ' · '.join(f'<a href="{e(p)}">{e(Path(p).name)}</a>' for p in meta.get('labs', []))
            outputs = ' · '.join(f'<a href="{e(p)}">{e(Path(p).name)}</a>' for p in allhashes[str(n)]
                                 if p.startswith('code/') and not p.endswith('.py'))
            labcards.append(f'<h2>{n:02d} · {e(c["title"])}</h2><p>{e(c["lab"])}</p><p>{links}</p><p>{outputs}</p><p><a href="{filename}#laboratory">Read the mathematical model and lab instructions</a></p>')
    accepted = sum(c['status']=='accepted' for c in entries)
    drafted = sum(c['status']!='planned' for c in entries)
    fullreviews = sum(len(c['accepted_reviews']) for c in entries)
    acquired = sum(bool(r.get('caption_sha256')) for r in recordings.values())
    readcount = sum(bool(r.get('sequentially_read')) for r in recordings.values())
    bookcheck = read('work/validation/book-checks.json', {})
    current_digest=content_digest()
    integrity=(bookcheck.get('passed') is True and bookcheck.get('content_digest')==current_digest)
    if exported_evidence:
        integrity=prior_completion.get('complete') is True and prior_completion.get('content_digest')==current_digest
    complete = accepted == len(chapters) and integrity
    phase = 'complete' if complete else ('final_integrity' if accepted==len(chapters) else 'scientific_review' if drafted==len(chapters) else 'autonomous_course_completion')
    state = {'phase': phase, 'complete': complete, 'content_digest':current_digest,
             'review_evidence_mode':'exported acceptance records; private reports not reopened' if exported_evidence else 'actual private reports and repair chains checked',
             'plan_approved': True,
             'pilot_author_approval': 'approved_2026-11-08', 'first_figure_approval': 'approved_2026-11-08',
             'autonomous_completion_authorized': True, 'planned_chapters': len(chapters),
             'drafted_chapters': drafted, 'accepted_chapters': accepted,
             'scientifically_reviewed_chapters': accepted, 'independent_full_reviews': fullreviews,
             'labs': sum(len(c['labs']) for c in entries), 'solved_exercises': sum(c['solutions'] for c in entries),
             'caption_tracks_acquired': acquired, 'caption_tracks_read_sequentially': readcount,
             'continuous_audiovisual_review': False, 'pending_chapters': pending,
             'book_checks': 'passed for current artifacts' if complete else 'pending',
             'publication': read('publication.json', {}).get('scope', 'private local reader; public publication not requested')}
    write('completion.json', state)
    write('chapter-manifest.json', {'status': phase, 'chapters': entries})
    result_graph=read('plan/results.yaml',{})
    for result in result_graph.get('results',[]):
        entry=next(c for c in entries if c['number']==result['planned_chapter'])
        result['manuscript_file']=entry['file']
        result['verification']=('included in independently reviewed chapter; exact proof or citation stated locally'
                                if entry['status']=='accepted' else
                                'drafted; independent review pending' if entry['status']=='draft' else
                                'planning only; no manuscript proof yet')
    write('plan/results.yaml',result_graph)
    state_path=ROOT/'BOOK-STATE.yaml'
    if state_path.exists():
        text=state_path.read_text(encoding='utf-8')
        updates={'phase':phase,'drafted_chapters':[c['number'] for c in entries if c['status']!='planned'],
                 'accepted_chapters':[c['number'] for c in entries if c['status']=='accepted'],
                 'independent_full_reviews':fullreviews,
                 'scientifically_reviewed_chapters':[c['number'] for c in entries if c['status']=='accepted'],
                 'captions_read_sequentially':readcount,
                 'current_chapter':min(pending) if pending else len(chapters),
                 'current_section':'whole_course_complete' if complete else ('independent_scientific_reviews_and_repairs' if drafted==len(chapters) else 'parallel_chapter_authoring_and_independent_review'),
                 'visuals_reviewed':'sampled_stills_with_per_lecture_limits_in_source_map'}
        section_ids=[]
        for entry in entries:
            if entry['status']!='planned':
                section_ids.extend(re.findall(r'<h2\b[^>]*>\s*(\d+\.\d+)',(ROOT/entry['file']).read_text(encoding='utf-8')))
        updates['completed_sections']=section_ids
        for key,value in updates.items():
            text=re.sub(r'(?m)^  '+key+r':.*$', '  '+key+': '+(json.dumps(value) if isinstance(value,list) else str(value)),text)
        unresolved=[]
        if readcount<len(recordings):unresolved.append('Sequential caption reading remains for some assigned lectures; see source manifest.')
        if pending:unresolved.append('Independent review acceptance remains for chapters '+', '.join(map(str,pending))+'.')
        if not complete:unresolved.append('Whole-book final integrity checks and source-free export remain.')
        replacement='  unresolved_evidence: []\n' if not unresolved else '  unresolved_evidence:\n'+''.join('    - '+json.dumps(item)+'\n' for item in unresolved)
        text=re.sub(r'(?m)^  unresolved_evidence:.*\n(?:    - .*\n)*',replacement,text)
        atomic_text('BOOK-STATE.yaml',text)
    for item in sources.get('sources', []):
        if item.get('id','').startswith('L') and item['id'][1:].isdigit():
            record=recordings[int(item['id'][1:])]
            item['status']=record['caption_status']
            item['coverage']={'identity':'verified','textual':record['textual_coverage'],
                              'visual':record['visual_coverage'],'audio':'not independently reviewed'}
    write('source-manifest.json', sources)
    lead = ('Completed course edition' if complete else ('Reviewed manuscript · final checks in progress' if accepted==len(chapters) else 'Complete draft · independent reviews in progress' if drafted==len(chapters) else 'Approved course edition · authoring and review in progress'))
    availability=(f'{len(chapters)} chapters, {state["labs"]} executable laboratories, and {state["solved_exercises"]} worked exercise solutions. Every chapter has two independent AI scientific reviews bound to its current artifacts.'
                  if complete else
                  f'All {len(chapters)} chapters have two independent AI scientific reviews bound to their current artifacts. Whole-book printing and reproduction checks are underway.' if accepted==len(chapters) else
                  f'{accepted} of {len(chapters)} chapters have two independent scientific reviews bound to their current artifacts. {drafted} chapters are available. The pilot and figure style are approved; completion of the full course is authorized.')
    intro = f'''<p class="eyebrow">NPTEL 115106089 · IIT Madras · V. Balakrishnan</p>
<h1>Physical Applications of Stochastic Processes</h1>
<p class="lead">From counting fluctuations to Markov evolution, Brownian paths, noise, first passage, anomalous transport, and recurrence.</p>
<div class="callout"><strong>{lead}.</strong> {availability}</div>
<div class="stats"><div class="stat"><strong>{len(recordings)}</strong><span>source lectures</span></div><div class="stat"><strong>{accepted}/{len(chapters)}</strong><span>chapters reviewed</span></div><div class="stat"><strong>{fullreviews}</strong><span>independent full reviews cleared</span></div><div class="stat"><strong>{sum(c['solutions'] for c in entries)}</strong><span>worked exercise solutions available</span></div></div>
<h2>Study the course</h2><p>The edition develops models through explicit hypotheses, derivations, recurring physical cases, original figures, executable Python laboratories, and fully worked solutions. Use <a href="laboratories.html">the laboratory index</a>, <a href="plan/notation.md">notation conventions</a>, and <a href="source-map.html">recording map</a>. Each chapter can be printed or saved as PDF with solutions.</p>
<h2>Evidence and scope</h2><p>{readcount} of {len(recordings)} acquired caption tracks have been read sequentially. Visual coverage is sampled and recorded by lecture; audio has not been reviewed independently. The instructor's official written exposition covers lectures 1–11; its syllabus and quiz extend across the course. Added derivations, computational experiments, and exercises are identified as teaching constructions.</p>
<p><a href="WORKFLOW.md">Workflow</a> · <a href="VALIDATION.md">Actual validation and limits</a> · <a href="spec/book-spec.md">Specification</a> · <a href="plan/architecture.md">Course architecture</a></p>
<h2 id="chapters">Chapters</h2>'''
    if complete and (ROOT/'course-notes.pdf').exists():
        intro+='<p><a href="course-notes.pdf">Download the complete PDF with solutions</a></p>'
    search = f'<div class="search"><label for="search">Search chapter topics, results, and labs</label><input id="search" type="search" placeholder="Try first passage, Brownian, or spectrum"><p class="meta" id="search-count" aria-live="polite">{len(chapters)} chapters shown</p></div>'
    atomic_text('index.html',page('Course reader',intro+controls(True)+search+''.join(cards)))
    atomic_text('laboratories.html',page('Computational laboratories','<h1>Computational laboratories</h1>'+controls()+'<p>Run each laboratory from the edition root using Python. Install the numerical dependencies listed in <a href="requirements.txt">requirements.txt</a>. Chapter instructions define inputs, outputs, seeds, mathematical checks, and model limits. Retained result files record the executed calculations.</p>'+''.join(labcards)))
    rows=[]
    for n,r in recordings.items():
        c=next(c for c in chapters if n in c['lectures'])
        rows.append(f'<tr><td>{n:02d}</td><td><a href="{e(r["url"])}">{e(r["title"])}</a></td><td><a href="index.html#ch{c["number"]:02d}">{c["number"]}</a></td><td>{r["duration_seconds"]} s</td><td>{e(r.get("textual_coverage","not read"))}</td><td>{e(r.get("visual_coverage","not reviewed"))}</td></tr>')
    body='<h1>Recordings and evidence</h1>'+controls()+'<p>All 29 requested recordings have one primary chapter assignment. Captions are publisher tracks; their human authorship is not established. Reading captions and inspecting selected still frames do not constitute continuous audiovisual review.</p><p><a href="https://archive.nptel.ac.in/content/storage2/courses/115106089/STOCHASTIC_PROCESSES_NPTEL.pdf">Official instructor notes</a>: 118 PDF pages, exposition for lectures 1–11, broader syllabus and quiz. Raw captions, downloaded documents, images, and detailed review reports remain in private working evidence.</p><div class="table-wrap"><table><thead><tr><th>Lecture</th><th>Recording</th><th>Chapter</th><th>Duration</th><th>Caption coverage</th><th>Visual coverage</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
    atomic_text('source-map.html',page('Recordings and evidence',body))
    write('analysis-ir.json', {'phase':phase,'source_evidence':['source-manifest.json','spec/sources.yaml'],
          'canonical_authored_plan':'plan/course-plan.json','result_graph':'plan/results.yaml',
          'reviewed_chapters':[c['number'] for c in entries if c['status']=='accepted'],
          'pending_chapters':pending,'coverage_boundaries':['caption fidelity has the limits recorded per lecture','sampled stills only','no independent audio review'],
          'artifact_dependencies':'artifact-manifest.json'})
    artifacts=[]
    for pattern in ('*.html','*.json','README.md','WORKFLOW.md','VALIDATION.md','ATTRIBUTION.md','reader-preview.png','requirements*.txt','.gitignore','.gitattributes','.nojekyll'):
        artifacts.extend(ROOT.glob(pattern))
    for folder in ('assets','code','figures','tools','spec','plan','validation'):
        artifacts.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    unique=sorted(set(artifacts)-{ROOT/'artifact-manifest.json'})
    write('artifact-manifest.json', {'phase':phase,'artifacts':[{'path':p.relative_to(ROOT).as_posix(),
          'purpose':'Course reader and reproducible scientific artifact','primary':p.name=='index.html',
          'source_dependencies':['S001'],'sha256':sha256(p.read_bytes()).hexdigest()} for p in unique]})
    print(f'Built reader: {drafted}/{len(chapters)} drafts, {accepted} reviewed chapters, {fullreviews} cleared full reviews; complete={complete}.')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exported-evidence',action='store_true',
                        help='Check preserved acceptance records without reopening private reports')
    build(exported_evidence=parser.parse_args().exported_evidence)
