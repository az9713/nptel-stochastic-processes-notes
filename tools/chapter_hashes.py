"""Hash a chapter's scientific body and executable/figure artifacts.

Navigation and shared presentation stay outside the manuscript-body digest.
"""
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = ['chapter-01-discrete-distributions.html', 'code/ch01_counting.py',
         'code/ch01-results.json', 'code/ch01-output.txt',
         'figures/ch01_equal_mean.py', 'assets/ch01-equal-mean.svg']


def scientific_files(number=1):
    if number == 1:
        return FILES
    plan = json.loads((ROOT / 'plan/course-plan.json').read_text(encoding='utf-8'))
    chapter = next(c for c in plan['chapters'] if c['number'] == number)
    name = f"chapter-{number:02d}-{chapter['slug']}.html"
    metadata = ROOT / name.replace('.html', '.meta.json')
    if metadata.exists():
        data = json.loads(metadata.read_text(encoding='utf-8'))
        if data.get('scientific_files'):
            names = data['scientific_files']
            if name not in names:
                raise ValueError('scientific files omit chapter manuscript')
            return names
    names = [name]
    for folder, pattern in [('code', f'ch{number:02d}*'),
                            ('figures', f'ch{number:02d}*.py'),
                            ('assets', f'ch{number:02d}*.svg')]:
        names.extend(p.relative_to(ROOT).as_posix() for p in sorted(
            (ROOT / folder).glob(pattern)) if p.is_file())
    return names


def hashes(number=1):
    output = {}
    for name in scientific_files(number):
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or path.is_symlink():
            raise ValueError('scientific artifact outside book')
        data = path.read_bytes()
        if name.endswith('.html'):
            if data.count(b'<!-- BEGIN CHAPTER -->') != 1 or data.count(b'<!-- END CHAPTER -->') != 1:
                raise ValueError('manuscript requires exactly one hash region')
            data = data.split(b'<!-- BEGIN CHAPTER -->', 1)[1].split(
                b'<!-- END CHAPTER -->', 1)[0]
        output[name] = sha256(data).hexdigest()
    return output


if __name__ == '__main__':
    print(json.dumps(hashes(int(sys.argv[1]) if len(sys.argv) > 1 else 1), indent=2))
