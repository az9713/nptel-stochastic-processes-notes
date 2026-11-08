"""Export bounded public attestations from validated private producer evidence."""
from hashlib import sha256
import json

from build_course import ROOT, content_digest, read
from review_evidence import audit


def write(name, value):
    path = ROOT/'validation'/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')


def main():
    digest = content_digest()
    completion = read('completion.json')
    if not completion.get('complete') or completion['content_digest'] != digest:
        raise ValueError('Export requires the current completed edition')
    for chapter in read('plan/course-plan.json')['chapters']:
        number = chapter['number']
        meta = read(f"chapter-{number:02d}-{chapter['slug']}.meta.json")
        evidence = audit(number, meta)
        reviews = []
        for review in evidence['independent_full_reviews']:
            record = {key: value for key, value in review.items()
                      if key not in ('report', 'targeted_repairs')}
            record['targeted_repairs'] = [
                {'sha256': repair['sha256']}
                for repair in review['targeted_repairs']]
            reviews.append(record)
        write(f'chapters/ch{number:02d}.json', {
            'passed': True, 'chapter': number,
            'scope': 'producer attestation after actual private review audit',
            'author_id': meta['author_id'],
            'artifact_hashes': evidence['artifact_hashes'],
            'independent_full_reviews': reviews,
            'continuous_audiovisual_review': False})
    inputs = {}
    for source, target in [('course-static-checks', 'structure-checks'),
                           ('course-browser-checks', 'reader-checks'),
                           ('course-reproduction-checks', 'reproduction-checks'),
                           ('book-checks', 'release-checks')]:
        name = f'work/validation/{source}.json'
        data = read(name)
        if data.get('passed') is not True or data.get('content_digest') != digest:
            raise ValueError(f'Missing or stale producer check: {source}')
        inputs[source] = sha256((ROOT/name).read_bytes()).hexdigest()
        if source == 'course-reproduction-checks':
            data = {key: value for key, value in data.items() if key != 'copy'}
            data['chapters'] = [{
                'chapter': c['chapter'], 'passed': c['passed'],
                'scripts': [{'script': s['script'], 'exit_code': s['exit_code']}
                            for s in c['scripts']],
                'outputs': c['outputs']} for c in data['chapters']]
            data['navigation'] = {key: value for key, value in data['navigation'].items()
                                  if key not in ('stdout', 'stderr')}
        data.update(producer_report_sha256=inputs[source],
                    evidence_origin='exported producer checks; private raw evidence excluded')
        write(target+'.json', data)
    write('export-checks.json', {
        'passed': True, 'content_digest': digest, 'chapters': 25,
        'independent_full_reviews': 50, 'producer_report_sha256': inputs,
        'scope': 'public attestation export after actual private evidence audit',
        'private_raw_reports_included': False})
    print('Exported 25 chapter attestations and current producer check summaries.')


if __name__ == '__main__':
    main()
