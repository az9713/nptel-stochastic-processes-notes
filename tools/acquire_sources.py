"""Acquire the requested playlist and private captions; never download video.

Run: python -X utf8 tools/acquire_sources.py captions --start 1 --end 29
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import time

import yt_dlp

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'source-manifest.json'
PRIVATE = ROOT / 'work' / 'sources'


def save(data):
    MANIFEST.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def clean_vtt(raw):
    segments = []
    previous = ''
    for block in re.split(r'\n\s*\n', raw.replace('\r\n', '\n')):
        lines = block.strip().splitlines()
        for i, line in enumerate(lines):
            match = re.match(
                r'(\d+):(\d+):(\d+)\.(\d+)\s+-->\s+'
                r'(\d+):(\d+):(\d+)\.(\d+)', line)
            if not match:
                continue
            values = list(map(int, match.groups()))
            start = sum(a*b for a, b in zip(values[:4], [3600, 60, 1, .001]))
            end = sum(a*b for a, b in zip(values[4:], [3600, 60, 1, .001]))
            for caption in lines[i+1:]:
                caption = html.unescape(re.sub(r'<[^>]*>', '', caption))
                caption = re.sub(r'\s+', ' ', caption).strip()
                if caption and caption != previous:
                    segments.append({'start': start, 'end': end, 'text': caption})
                    previous = caption
            break
    return segments


def captions(start, end):
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    target = PRIVATE / 'captions'
    target.mkdir(parents=True, exist_ok=True)
    opts = {'quiet': True, 'no_warnings': True, 'retries': 1,
            'fragment_retries': 1, 'socket_timeout': 25,
            'cachedir': str(ROOT / 'work' / 'cache')}
    for record in data['recordings']:
        number = record['lecture']
        if not start <= number <= end:
            continue
        stem = f"{number:02d}-{record['video_id']}"
        dest = target / f'{stem}.json'
        if dest.exists() and record.get('caption_sha256'):
            print(f'{number:02d} cached', flush=True)
            continue
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(record['url'], download=False)
            publisher = info.get('subtitles') or {}
            automatic = info.get('automatic_captions') or {}
            languages = [x for x in publisher if x.startswith('en')]
            if languages:
                language = 'en' if 'en' in languages else languages[0]
                kind = 'publisher caption track; authorship not established'
                is_auto = False
            elif 'en-orig' in automatic or 'en' in automatic:
                language = 'en-orig' if 'en-orig' in automatic else 'en'
                kind = 'automatic captions'
                is_auto = True
            else:
                record['caption_status'] = 'unavailable'
                save(data)
                print(f'{number:02d} no English track', flush=True)
                continue
            vtt = target / f'{stem}.{language}.vtt'
            if not vtt.exists():
                download = {**opts, 'skip_download': True,
                            'writesubtitles': not is_auto,
                            'writeautomaticsub': is_auto,
                            'subtitleslangs': [language],
                            'subtitlesformat': 'vtt',
                            'outtmpl': str(target / stem)}
                with yt_dlp.YoutubeDL(download) as ydl:
                    ydl.download([record['url']])
            segments = clean_vtt(vtt.read_text(encoding='utf-8'))
            if not segments:
                raise ValueError('English track has no parseable timed segments')
            record.update({
                'caption_status': 'acquired; not yet read sequentially',
                'caption_kind': kind, 'caption_language': language,
                'caption_segments': len(segments),
                'caption_first_seconds': min(s['start'] for s in segments),
                'caption_last_seconds': max(s['end'] for s in segments),
                'caption_vtt_sha256': hashlib.sha256(vtt.read_bytes()).hexdigest(),
                'upload_date': info.get('upload_date'),
                'caption_acquired_at_utc': datetime.now(timezone.utc).isoformat(),
                'textual_coverage': 'acquired; reading audit pending'})
            dest.write_text(json.dumps({'video_id': record['video_id'],
                                       'kind': kind, 'segments': segments},
                                      indent=2) + '\n', encoding='utf-8')
            record['caption_sha256'] = hashlib.sha256(dest.read_bytes()).hexdigest()
            dest.with_suffix('.txt').write_text('\n'.join(
                f"[{s['start']:.1f}] {s['text']}" for s in segments) + '\n',
                encoding='utf-8')
            print(f'{number:02d} acquired {len(segments)} segments: {kind}',
                  flush=True)
        except Exception as error:
            record['caption_status'] = 'acquisition failed; retry explicitly'
            record['caption_error_type'] = type(error).__name__
            print(f'{number:02d} failed: {type(error).__name__}', flush=True)
        save(data)
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['captions'])
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=29)
    args = parser.parse_args()
    captions(args.start, args.end)
