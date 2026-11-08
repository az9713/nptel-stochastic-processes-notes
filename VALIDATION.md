# Review and validation evidence

The completed edition contains 25 chapters, 25 executable laboratories, 25 original
reproducible figures and 150 worked solutions, covering all 29 course recordings.
The user approved the plan, pilot and first figure, then authorized completion of
the entire course, then requested GitHub publication using the prior course workflow.
The public snapshot excludes raw source material and private reports.

Each chapter has two independent full AI scientific reviews by reviewers distinct
from its author and from each other. Reports bind the scientific manuscript body,
lab, outputs, figure generator and SVG by SHA-256. Required bounded repairs have
same-reviewer verification chains; changed arguments receive fresh full review.
The final 50 full-review records clear all current scientific artifacts. Original
and superseded reports remain private. These are AI editorial reviews, not human
expert certification; mechanical consistency checks do not prove mathematics.

The full-course release checks passed against one final content digest:

- Structure, backward prerequisite graph, numbering, all six solutions per
  chapter, 919 local links and 143 bounded recording-timestamp links.
- Installed Microsoft Edge with networking disabled, at 1440px and 390px widths:
  all chapters render mathematics with zero MathJax or JavaScript errors, load
  figures, and avoid page-wide overflow. Theme, text size, code copying, mobile
  contents and show/hide-solution controls pass.
- Every print proof includes expanded solutions and restores the reader state
  afterward. Proof hashes bind the current chapter HTML and browser evidence.
- All 25 labs and figure generators run in an isolated copy without captions,
  source PDFs or private working inputs; regenerated JSON, text and SVG outputs
  are byte-identical. Each chapter starts without private work inherited from
  earlier chapters. Source-free navigation rebuilding also passes.
- Actual Edge geometry checks place all 876 SVG text labels inside their canvases.
  Figure interpretation, units and model fidelity are covered by scientific
  reviewers; this bounds test alone does not check their meaning.

Applicable static skill checks cover TeX, internal links, Python code style, SVG,
prose and proof structure. One TeX-checker false positive is documented: chapter8
uses the valid command `\rightleftarrows`, which a substring-based left/right
counter misclassifies. Actual offline MathJax renders it correctly. The whole-book
link script must run on the curated source-free edition: recursively checking the
working tree also includes preserved, unfinished historical validation copies.
The owning release checker checks current files. Inline-SVG overlap/frame scripts
do not inspect these external Matplotlib SVGs; retained generators, reviewer figure
inspections and direct SVG canvas measurements provide the applicable evidence.

The combined PDF has one bookmark per chapter. Export removes local-file launch
annotations created by file-based printing, preserves HTTP(S) source and internal
PDF links, and checks saved PDF objects, decoded metadata and page text for local
paths and private network identifiers. The curated offline archive contains reader
files, numerical programs, figure generators and rebuild tools. Raw sources and
private reviews are excluded. Packaging checks are separate from science review.

All 29 acquired caption tracks were read sequentially; timed still sampling is
recorded per lecture in the recording map and sidecars. Lecture24 has no visual
review. No independent continuous audio/video review is claimed. The official
118-page instructor document supplies main exposition only through lectures1–11;
later chapters use separate primary/authoritative sources. Corrections, added
derivations, code and exercises are independently authored.

Install `requirements.txt` for laboratories. Retained numerical-library versions
are pinned in `requirements-numerical-lock.txt`, with actual runtime versions in
`runtime-versions.json`. Finite seeded checks are not general theorems. The reader
bundles MathJax and its license and works offline after extraction.

The archive preserves original acceptance records without private reports. Run
`python tools/build_course.py --exported-evidence` there to check unchanged
scientific hashes and rebuild navigation. This preserves original acceptance;
it does not reopen or authenticate private review reports.

The public GitHub Pages deployment is checked separately in
`validation/publication-checks.json`: 256 served files match the recorded content
commit, and eight live browser checks cover the index and chapters1,9,25 at
desktop and phone widths. This bounded live sample complements the full-course
offline checks; it does not replace scientific review or source validation.
