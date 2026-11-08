"""Export the accepted edition as a source-free ZIP and combined PDF."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit
from uuid import uuid4
import zipfile

import fitz

from build_course import ROOT, read


PRIVATE_PDF_TEXT = re.compile(
    r'(?i)(?:[a-z]:[/\\]+Users[/\\]+[^/\\\s<>()]+'
    r'|/(?:Users|home)/[^/\s<>()]+'
    r'|\bfile\s*:'
    r'|(?:[a-z0-9-]+\.)+ts\.net\b'
    r'|\btskey-[a-z0-9-]+'
    r'|\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d+\.\d+\b)'
)


def private_pdf_text_matches(text):
    """Do not confuse a public URL's /users/name/ route with a home directory."""
    public_path_spans = []
    for match in re.finditer(r'https?://[^\s<>()]+', text, re.I):
        parsed = urlsplit(match.group())
        if parsed.netloc and parsed.path:
            start = match.start()+len(parsed.scheme)+3+len(parsed.netloc)
            public_path_spans.append((start, start+len(parsed.path)))
    findings = []
    for match in PRIVATE_PDF_TEXT.finditer(text):
        unix_home = match.group().lower().startswith(('/users/', '/home/'))
        if unix_home and any(a <= match.start() < b for a, b in public_path_spans):
            continue
        findings.append(match)
    return findings


def remove_local_file_links(document):
    """Unlink local annotations; let save-time GC remove orphaned objects.

    Freeing an imported annotation with delete_link before saving a newly merged
    document makes MuPDF's collector encounter the freed xref. Rebuilding only
    its page's Annots reference array avoids that dangling-object traversal.
    """
    removed = 0
    for page in document:
        local_xrefs = {link['xref'] for link in page.get_links()
                       if link.get('kind') in (fitz.LINK_LAUNCH, fitz.LINK_GOTOR)
                       or str(link.get('uri', '')).lower().startswith('file:')}
        if not local_xrefs:
            continue
        kind, array = document.xref_get_key(page.xref, 'Annots')
        if kind == 'xref':
            array = document.xref_object(int(array.split()[0]))
        elif kind != 'array':
            raise ValueError('Local links have no supported annotation array')
        references = re.findall(r'(\d+)\s+(\d+)\s+R', array)
        remainder = re.sub(r'\d+\s+\d+\s+R|[\s\[\]]', '', array)
        if remainder or not local_xrefs.issubset({int(x) for x, _ in references}):
            raise ValueError('Unsupported annotation structure; refusing partial cleanup')
        kept = [f'{xref} {generation} R' for xref, generation in references
                if int(xref) not in local_xrefs]
        document.xref_set_key(page.xref, 'Annots', '['+' '.join(kept)+']')
        removed += len(local_xrefs)
    return removed


def link_inventory(document):
    """Record semantic link destinations independently of changing PDF xrefs."""
    external = Counter()
    internal = Counter()
    local = 0
    for page_number, page in enumerate(document):
        for link in page.get_links():
            uri = str(link.get('uri', ''))
            if (link.get('kind') in (fitz.LINK_LAUNCH, fitz.LINK_GOTOR)
                    or uri.lower().startswith('file:')):
                local += 1
            elif uri.lower().startswith(('http://', 'https://')):
                external[uri] += 1
            elif link.get('kind') == fitz.LINK_GOTO:
                point = link.get('to', fitz.Point(0, 0))
                signature = (page_number, link.get('page'),
                             round(point.x, 4), round(point.y, 4))
                internal[signature] += 1
    return {'external': external, 'internal': internal, 'local': local}


def verify_pdf_privacy(path, expected_links, expected_toc):
    """Inspect the saved PDF, including retained xref objects and decoded text."""
    with fitz.open(path) as document:
        after = link_inventory(document)
        findings = []
        # garbage=4 removes orphaned annotations; inspect every saved object too.
        for xref in range(1, document.xref_length()):
            if private_pdf_text_matches(document.xref_object(xref)):
                findings.append({'location': f'xref {xref}'})
        metadata = json.dumps(document.metadata, ensure_ascii=False)
        if private_pdf_text_matches(metadata + document.get_xml_metadata()):
            findings.append({'location': 'decoded metadata'})
        for number, page in enumerate(document, start=1):
            if private_pdf_text_matches(page.get_text()):
                findings.append({'location': f'page {number} text'})
        if after['local'] or findings:
            raise ValueError(f'Private PDF content remained: {findings}; '
                             f'local file links={after["local"]}')
        if after['external'] != expected_links['external']:
            raise ValueError('PDF sanitization changed HTTP(S) source links')
        if after['internal'] != expected_links['internal']:
            raise ValueError('PDF sanitization changed internal GoTo links')
        if document.get_toc() != expected_toc:
            raise ValueError('Saved PDF chapter bookmarks do not match the plan')
        return {'passed': True, 'xref_objects_scanned': document.xref_length()-1,
                'decoded_metadata_and_page_text_scanned': True,
                'private_path_file_uri_tailnet_findings': findings,
                'remaining_local_file_links': after['local'],
                'http_source_links_preserved': sum(after['external'].values()),
                'internal_goto_links_preserved': sum(after['internal'].values()),
                'bookmarks_verified': len(expected_toc)}


def save_sanitized_pdf(document, path, title, toc):
    """Remove local-file actions while retaining external and in-document links."""
    before = link_inventory(document)
    removed = remove_local_file_links(document)
    document.set_toc(toc)
    document.set_metadata({
        'title': title,
        'subject': 'Independent graduate study edition based on NPTEL 115106089',
        'author': 'Independent study notes',
    })
    document.del_xml_metadata()
    # Verify a private staging file before replacing any phone-visible alias.
    pending = path.with_name(f'.{path.stem}-pending-{uuid4().hex}.pdf')
    try:
        document.save(pending, garbage=4, deflate=True)
        verification = verify_pdf_privacy(pending, before, toc)
        pending.replace(path)
    finally:
        pending.unlink(missing_ok=True)
    return {'local_file_links_removed': removed,
            'privacy_verification': verification}


def export_pilot(destination):
    """Make a public pilot copy without changing its private print proof."""
    source = ROOT/'work/validation/ch01-proof.pdf'
    if not source.is_file():
        raise ValueError('Private pilot proof is missing; run check_reader.py 1 --pdf')
    source_hash = sha256(source.read_bytes()).hexdigest()
    chapter = read('plan/course-plan.json')['chapters'][0]
    public = destination/'pilot.pdf'
    toc = [[1, f'Chapter 1: {chapter["title"]}', 1]]
    with fitz.open(source) as document:
        report = save_sanitized_pdf(document, public, 'Stochastic Processes — Pilot', toc)
        report['pdf_pages'] = len(document)
    if sha256(source.read_bytes()).hexdigest() != source_hash:
        raise ValueError('Private pilot proof changed during export')
    report.update({'passed': True, 'source_pdf_sha256': source_hash,
                   'public_pdf_sha256': sha256(public.read_bytes()).hexdigest(),
                   'private_proof_unchanged': True,
                   'scope': 'sanitized copy of the existing private pilot proof; '
                            'print currentness is checked by the owning browser workflow'})
    (destination/'pilot-checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    return report


def main(pilot_only=False):
    destination=ROOT/'work/release';destination.mkdir(parents=True,exist_ok=True)
    if pilot_only:
        print(json.dumps(export_pilot(destination), indent=2))
        return
    if not read('completion.json').get('complete'):
        raise ValueError('Package export requires full-course final integrity acceptance')
    combined=fitz.open()
    toc=[]
    for c in read('plan/course-plan.json')['chapters']:
        pdf=ROOT/f'work/validation/ch{c["number"]:02d}-proof.pdf'
        if not pdf.exists():raise ValueError(f'Missing current print proof {pdf.name}; run check_reader.py --pdf')
        browser=read(f'work/validation/ch{c["number"]:02d}-browser-checks.json')
        html=ROOT/f"chapter-{c['number']:02d}-{c['slug']}.html"
        if browser['html_sha256']!=sha256(html.read_bytes()).hexdigest():
            raise ValueError('Print proof is stale relative to the chapter')
        if not browser.get('pdf_generated') or browser.get('pdf_sha256')!=sha256(pdf.read_bytes()).hexdigest():
            raise ValueError('Print proof is not bound to its current browser evidence')
        toc.append([1, f'Chapter {c["number"]}: {c["title"]}', len(combined)+1])
        source=fitz.open(pdf);combined.insert_pdf(source);source.close()
    pdf_checks=save_sanitized_pdf(combined, destination/'course-notes.pdf',
                                 'Physical Applications of Stochastic Processes', toc)
    shutil.copy2(destination/'course-notes.pdf',ROOT/'course-notes.pdf')
    pages=len(combined);combined.close()
    pilot_checks=export_pilot(destination)
    manifest=read('artifact-manifest.json')['artifacts']
    paths=sorted({entry['path'] for entry in manifest})
    paths.append('artifact-manifest.json')
    for name in paths:
        path=(ROOT/name).resolve()
        if not path.is_relative_to(ROOT) or name.startswith('work/'):
            raise ValueError('Private working evidence cannot enter the source-free archive')
    archive=destination/'stochastic-processes-notes.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as output:
        for name in paths:output.write(ROOT/name,name)
        output.write(destination/'course-notes.pdf','course-notes.pdf')
    report={'passed':True,'scope':'curated source-free export','pdf_pages':pages,
            'pdf_sha256':sha256((destination/'course-notes.pdf').read_bytes()).hexdigest(),
            'zip_sha256':sha256(archive.read_bytes()).hexdigest(),'archive_entries':len(paths)+1,
            'raw_sources_included':False,'private_review_reports_included':False,
            'chapter_bookmarks':len(toc), 'pdf_sanitization':pdf_checks,
            'public_pilot':pilot_checks,
            'reproduction_scope':'chapter labs and figure generation; private audit reports remain with the working edition'}
    (destination/'package-checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot-only',action='store_true',
                        help='Sanitize the existing private pilot proof without a full release')
    main(pilot_only=parser.parse_args().pilot_only)
