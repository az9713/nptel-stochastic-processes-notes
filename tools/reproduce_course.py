"""Reproduce numerical results and figures in a copy without raw sources."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from build_course import ROOT, content_digest, read
from chapter_hashes import scientific_files


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('chapters',nargs='*',type=int)
    args=parser.parse_args()
    plan=read('plan/course-plan.json')['chapters']
    selected=args.chapters or [c['number'] for c in plan
                               if (ROOT/f"chapter-{c['number']:02d}-{c['slug']}.meta.json").exists()]
    out=ROOT/'work/validation';out.mkdir(parents=True,exist_ok=True)
    target=Path(tempfile.mkdtemp(prefix='source-free-',dir=out))
    for folder in ('assets','code','figures','tools','spec','plan','validation'):
        shutil.copytree(ROOT/folder,target/folder,ignore=shutil.ignore_patterns('__pycache__'))
    for pattern in ('*.html','*.json','README.md','WORKFLOW.md','VALIDATION.md','ATTRIBUTION.md','reader-preview.png','requirements*.txt','.gitignore','.gitattributes','.nojekyll','course-notes.pdf'):
        for path in ROOT.glob(pattern):shutil.copy2(path,target/path.name)
    assert not (target/'work').exists()
    chapters=[]
    for number in selected:
        assert not (target/'work').exists(), 'A chapter must not inherit private work from earlier runs'
        files=scientific_files(number)
        outputs=[name for name in files if not name.endswith(('.html','.py'))]
        for name in outputs:(target/name).unlink(missing_ok=True)
        scripts=[name for name in files if name.endswith('.py')]
        logs=[]
        for script in sorted(scripts,key=lambda name:(not name.startswith('code/'),name)):
            result=subprocess.run([sys.executable,'-X','utf8',str(target/script)],
                                  cwd=target,capture_output=True,text=True,timeout=180)
            logs.append({'script':script,'exit_code':result.returncode,
                         'stdout':result.stdout,'stderr':result.stderr})
            if result.returncode:break
        comparisons=[]
        for name in outputs:
            generated=target/name
            comparisons.append({'path':name,'exists':generated.exists(),
                                'byte_identical':generated.is_file() and generated.read_bytes()==(ROOT/name).read_bytes(),
                                'expected_sha256':sha256((ROOT/name).read_bytes()).hexdigest(),
                                'actual_sha256':sha256(generated.read_bytes()).hexdigest() if generated.exists() else None})
        passed=all(log['exit_code']==0 for log in logs) and all(r['byte_identical'] for r in comparisons)
        chapters.append({'chapter':number,'passed':passed,'scripts':logs,'outputs':comparisons})
        private_work=(target/'work').resolve()
        if private_work.exists():
            saved=(target/'generated-previews'/f'ch{number:02d}').resolve()
            if not private_work.is_relative_to(target.resolve()) or not saved.is_relative_to(target.resolve()):
                raise ValueError('Preview archive must remain inside the source-free validation copy')
            saved.parent.mkdir(parents=True,exist_ok=True)
            private_work.rename(saved)
        print(f'Chapter {number}: source-free reproduction passed={passed}',flush=True)
    navigation=None
    if not args.chapters and len(selected)==len(plan):
        result=subprocess.run([sys.executable,'-X','utf8',str(target/'tools/build_course.py'),'--exported-evidence'],
                              cwd=target,capture_output=True,text=True,timeout=60)
        pages=['index.html','source-map.html','laboratories.html']
        comparison={name:(target/name).read_bytes()==(ROOT/name).read_bytes() for name in pages}
        navigation={'passed':result.returncode==0 and all(comparison.values()),
                    'byte_identical_pages':comparison,'stdout':result.stdout,'stderr':result.stderr,
                    'evidence_mode':'preserved exported acceptance records; private reports not reopened'}
        print(f'Source-free navigation rebuild passed={navigation["passed"]}',flush=True)
    report={'passed':bool(chapters) and all(r['passed'] for r in chapters) and (navigation is None or navigation['passed']),
            'scope':'numerical labs and figure generators without private source inputs',
            'copy':target.relative_to(ROOT).as_posix(),'chapters':chapters,'navigation':navigation,
            'content_digest':content_digest()}
    (out/'course-reproduction-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not report['passed'])


if __name__=='__main__':main()
