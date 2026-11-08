"""Bind two actual independent full reports to the current pilot artifacts.

This checks review evidence, not mathematical correctness or author approval.
"""
from hashlib import sha256
import json
from pathlib import Path
import re

from chapter_hashes import hashes

ROOT = Path(__file__).resolve().parents[1]


def main():
    current = hashes()
    records = []
    identities = set()
    for number in (1, 2):
        path = ROOT / f'work/reviews/ch01-r{number}.md'
        text = path.read_text(encoding='utf-8')
        summaries = []
        for block in re.findall(r'```json\s*([\s\S]*?)```', text):
            value = json.loads(block)
            if isinstance(value, dict) and value.get('review_type') == 'full':
                summaries.append(value)
        if len(summaries) != 1:
            raise ValueError(f'{path.name}: expected one full-review summary')
        summary = summaries[0]
        identity = summary['reviewer_id']
        if identity in identities or identity not in (
                '/root/ch01_review1', '/root/ch01_review2'):
            raise ValueError('unexpected or nonindependent reviewer identity')
        identities.add(identity)
        observed = summary['artifact_hashes']
        if 'before' in observed and 'after' in observed:
            if observed['before'] != observed['after']:
                raise ValueError('artifacts changed during full review')
            observed = observed['after']
        repair_sha = None
        if (observed != current or summary['blocking_findings'] != 0
                or summary['verdict'] != 'accept'):
            repair_path = ROOT / f'work/reviews/ch01-r{number}-targeted.md'
            repair_text = repair_path.read_text(encoding='utf-8')
            repairs = [json.loads(block) for block in re.findall(
                r'```json\s*([\s\S]*?)```', repair_text)]
            repairs = [r for r in repairs if r.get('review_type') == 'targeted']
            if len(repairs) != 1:
                raise ValueError('expected one real targeted repair report')
            repair = repairs[0]
            if (repair['reviewer_id'] != identity
                    or repair['blocking_findings'] != 0
                    or repair['verdict'] != 'accept'
                    or repair['before_hashes'] != observed
                    or repair['after_hashes'] != current):
                raise ValueError('targeted repair evidence does not bind this full review')
            repair_sha = sha256(repair_path.read_bytes()).hexdigest()
        records.append({'reviewer_id': identity, 'review_type': 'full',
                        'full_review_blocking_findings': summary['blocking_findings'],
                        'full_review_verdict': summary['verdict'],
                        'final_blocking_findings': 0, 'verdict': 'accept',
                        'report_sha256': sha256(path.read_bytes()).hexdigest(),
                        'targeted_repair_report_sha256': repair_sha})
    result = {'passed': True, 'scope': 'actual pilot review evidence binding',
              'independent_full_reviews': records, 'artifact_hashes': current,
              'author_approval': 'pending', 'course_complete': False}
    (ROOT / 'work/reviews/ch01-review-audit.json').write_text(
        json.dumps(result, indent=2)+'\n', encoding='utf-8')
    (ROOT / 'chapter-01-discrete-distributions.meta.json').write_text(
        json.dumps({'chapter': 1, 'recordings': [1, 2],
                    'status': 'scientifically_reviewed_pilot_author_approval_pending',
                    'independent_full_reviews': records,
                    'artifact_hashes': current,
                    'solutions': 6, 'labs': ['code/ch01_counting.py'],
                    'figures': ['assets/ch01-equal-mean.svg'],
                    'visual_coverage': '15 sampled timed stills, partial',
                    'continuous_audiovisual_review': False}, indent=2)+'\n',
        encoding='utf-8')
    print('Two distinct full reviews and their verified repair chains bind the current pilot artifacts.')


if __name__ == '__main__':
    main()
