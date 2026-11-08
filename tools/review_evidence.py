"""Verify actual review reports and their digest-bound repair chains.

This is an evidence consistency check, not an automated scientific review.
Reports must be written by the independent reviewers themselves.
"""
from hashlib import sha256
import json
from pathlib import Path
import re

from chapter_hashes import ROOT, hashes


def summaries(path, kind):
    values = []
    for block in re.findall(r'```json\s*([\s\S]*?)```', path.read_text(encoding='utf-8')):
        value = json.loads(block)
        if isinstance(value, dict) and value.get('review_type') == kind:
            values.append(value)
    if len(values) != 1:
        raise ValueError(f'{path.name}: expected one {kind} review summary')
    return values[0]


def flat_hashes(value):
    if 'before' in value and 'after' in value:
        if value['before'] != value['after']:
            raise ValueError('scientific artifacts changed during review')
        return value['after']
    return value


def audit(number, metadata):
    current = hashes(number)
    records, identities = [], set()
    for slot in (1, 2):
        report = ROOT / f'work/reviews/ch{number:02d}-r{slot}.md'
        summary = summaries(report, 'full')
        identity = summary['reviewer_id']
        if not identity or identity == metadata.get('author_id') or identity in identities:
            raise ValueError('reviewer must be distinct from author and other reviewer')
        identities.add(identity)
        observed = flat_hashes(summary['artifact_hashes'])
        if set(observed) != set(current):
            raise ValueError('full review omitted or added scientific artifacts')
        previous = observed
        blockers, verdict = summary['blocking_findings'], summary['verdict']
        repairs = []
        paths = sorted((ROOT / 'work/reviews').glob(f'ch{number:02d}-r{slot}-targeted*.md'),
                       key=lambda p: (p.name != f'ch{number:02d}-r{slot}-targeted.md',p.name))
        for repair_path in paths:
            repair = summaries(repair_path, 'targeted')
            if repair['reviewer_id'] != identity or repair['before_hashes'] != previous:
                raise ValueError('repair chain does not continue the same independent review')
            previous = repair['after_hashes']
            blockers, verdict = repair['blocking_findings'], repair['verdict']
            repairs.append({'path': repair_path.relative_to(ROOT).as_posix(),
                            'sha256': sha256(repair_path.read_bytes()).hexdigest()})
        if previous != current or blockers != 0 or verdict != 'accept':
            raise ValueError(f'{report.name}: current scientific artifacts not cleared')
        records.append({'reviewer_id': identity, 'review_type': 'full',
                        'full_review_blocking_findings': summary['blocking_findings'],
                        'full_review_verdict': summary['verdict'],
                        'final_blocking_findings': 0, 'verdict': 'accept',
                        'report': report.relative_to(ROOT).as_posix(),
                        'report_sha256': sha256(report.read_bytes()).hexdigest(),
                        'targeted_repairs': repairs})
    return {'passed': True, 'chapter': number,
            'scope': 'independent review and repair evidence binding',
            'independent_full_reviews': records, 'artifact_hashes': current}


def audit_exported(number,metadata):
    """Check preserved acceptance records when private reports are absent.

    This does not reopen or authenticate the original private review reports.
    It preserves an exported edition only if its current artifacts still match.
    """
    current=hashes(number)
    if metadata.get('status')!='accepted' or metadata.get('artifact_hashes')!=current:
        raise ValueError('exported acceptance does not bind current scientific artifacts')
    records=metadata.get('independent_full_reviews',[])
    identities={r.get('reviewer_id') for r in records}
    if len(records)!=2 or len(identities)!=2 or None in identities or metadata.get('author_id') in identities:
        raise ValueError('export needs two distinct nonauthor acceptance records')
    for record in records:
        if (record.get('review_type')!='full' or record.get('verdict')!='accept'
                or record.get('final_blocking_findings')!=0
                or not re.fullmatch(r'[0-9a-f]{64}',record.get('report_sha256',''))):
            raise ValueError('invalid exported review acceptance record')
    return {'passed':True,'chapter':number,'artifact_hashes':current,
            'independent_full_reviews':records,
            'scope':'exported acceptance-record consistency; private reports not reopened'}


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('chapters', nargs='+', type=int)
    args = parser.parse_args()
    plan = json.loads((ROOT / 'plan/course-plan.json').read_text(encoding='utf-8'))
    for number in args.chapters:
        chapter = next(c for c in plan['chapters'] if c['number'] == number)
        path = ROOT / f"chapter-{number:02d}-{chapter['slug']}.meta.json"
        metadata = json.loads(path.read_text(encoding='utf-8'))
        evidence = audit(number, metadata)
        evidence_path = ROOT / f'work/reviews/ch{number:02d}-review-audit.json'
        evidence_path.write_text(json.dumps(evidence, indent=2)+'\n', encoding='utf-8')
        metadata.update(status='accepted', artifact_hashes=evidence['artifact_hashes'],
                        independent_full_reviews=evidence['independent_full_reviews'],
                        review_audit=evidence_path.relative_to(ROOT).as_posix())
        path.write_text(json.dumps(metadata, indent=2)+'\n', encoding='utf-8')
        print(f'Chapter {number}: two distinct independent full reviews bind current scientific artifacts.')


if __name__ == '__main__':
    main()
