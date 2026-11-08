"""Bind full-course mechanical checks and genuine review acceptance.

Run after check_course.py --release, check_reader.py and reproduce_course.py.
"""
import json

from build_course import ROOT, build, content_digest, read
from review_evidence import audit


def main():
    chapters=read('plan/course-plan.json')['chapters']
    required={c['number'] for c in chapters}
    digest=content_digest()
    evidence={}
    for name in ('course-static-checks','course-browser-checks','course-reproduction-checks'):
        data=read(f'work/validation/{name}.json',{})
        if data.get('passed') is not True or data.get('content_digest')!=digest:
            raise ValueError(f'{name}: missing, failed, or stale evidence')
        if {c['chapter'] for c in data['chapters']}!=required:
            raise ValueError(f'{name}: not every chapter was checked')
        if name=='course-static-checks' and not data.get('release_mode'):
            raise ValueError('static check did not use release mode')
        if name=='course-reproduction-checks' and not data.get('navigation',{}).get('passed'):
            raise ValueError('source-free navigation rebuild is missing or failed')
        evidence[name]={'passed':True,'chapters':len(required)}
    for c in chapters:
        meta=read(f"chapter-{c['number']:02d}-{c['slug']}.meta.json",{})
        if meta.get('status')!='accepted':raise ValueError(f'Chapter {c["number"]} not accepted')
        audit(c['number'],meta)
    report={'passed':True,'scope':'whole-course integrity and evidence binding',
            'content_digest':digest,'chapters':len(required),
            'independent_full_reviews':2*len(required),'checks':evidence,
            'limits':['mathematical acceptance comes from recorded independent scientific reviews',
                      'caption reading and sampled stills do not constitute continuous audiovisual review',
                      'finite seeded numerical tests are not mathematical proofs']}
    (ROOT/'work/validation/book-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    build()
    print('All chapter reviews and full-course checks bind the current edition.')


if __name__=='__main__':main()
