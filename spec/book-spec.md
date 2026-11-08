# Physical Applications of Stochastic Processes — book specification

Status: completed study edition; GitHub publication is authorized by the user's subsequent commit-and-push request. The user approved the plan, pilot and first figure, and authorized completion of all 25 chapters. All 25 chapters have two independent scientific reviews and final integrity checks; see VALIDATION.md for evidence and source-coverage limits.

## Conceptual spine

Choose a state description, derive its probability evolution, extract observables,
and determine which conclusions survive a change of scale or loss of memory.
The course moves from probability laws to Markov dynamics, diffusion, fluctuations,
first passage, anomalous transport, and deterministic recurrence.

## Reader and prerequisites

A quantitatively trained graduate returning to the subject. Assume multivariable
calculus, finite-dimensional linear algebra, elementary probability, Fourier and
Laplace transforms, ordinary differential equations, undergraduate mechanics and
thermal physics, and basic Python. Refresh characteristic functions, conditional
probability, matrix exponentials, and transform conventions locally. Do not assume
stochastic calculus, Markov-chain theory, ergodic theory, or anomalous diffusion.

## Reader before and after

Before: can normalize a density, compute a variance, diagonalize a small matrix,
solve a linear differential equation, and run a numerical experiment.

After: can derive and test the central result in every chapter record in
`plan/course-plan.json`. In particular, can distinguish a distribution from a
process; construct a conservative Markov generator; calculate stationary laws and
currents; connect jump processes, stochastic differential equations, and density
evolution under explicit hypotheses; compute correlations, spectra, and response;
solve first-passage and recurrence problems; diagnose anomalous scaling and
ergodicity failures. Each outcome is attached to chapter result IDs and exercises.

## Scope

All 29 recordings of NPTEL 115106089, V. Balakrishnan, IIT Madras. Completed:
25 chapters, preserving lecture order, combining 1–2, 7–8, 12–13, and 23–24.
Chapter boundaries follow the approved plan and sequential caption reading.
Equation-frame checks are sampled and individually bounded. No missing or
inaccessible source content is invented.

The mathematical treatment includes exact finite-state examples, one-dimensional
diffusions, Gaussian processes, noise and response, renewal methods, lattice and
fractal walks, and recurrence in finite-measure dynamics. Six original worked
exercises per chapter: two conceptual/counterexample, two derivational, and two
computational/design. One substantive Python lab per chapter; multiple figures
where they clarify different inferences. The completed counts are 25 labs,
25 original figures and 150 worked solutions.

## Extensions and exclusions

Short, explicitly marked connections may link Ornstein–Uhlenbeck dynamics to
generative diffusion, backward generators to control, heavy-tailed renewal to
aging, and path roughness to numerical sampling. These are optional additions;
the course remains the organizing source. No production generative model,
investment advice, numerical treatment recommendation, comprehensive stochastic
analysis monograph, or copied slide collection is planned.

## Results assumed without proof

Elementary transform inversion, dominated convergence under stated conditions,
finite-dimensional spectral theory, and elementary integration/ODE methods.
Deep path theorems (arcsine law, iterated logarithm, full Gaussian-Markov
classification) need verified theorem statements and primary/authoritative page
citations. They must not be presented as proved by a simulation. The scalar Itô
rule will receive a derivation at the course's level, with its analytic scope
stated. The central-limit theorem gets a characteristic-function proof for the
independent identically distributed finite-variance case, not unrestricted claims.

## Course use and length budget

Playlist metadata: 101,978 seconds = 28 h 19 min 38 s. Proposed reading budget:
432 typeset-equivalent pages, allocated in the chapter records, excluding code
source listings. Page budgets are estimates and never a prose quota. Read in
lecture order or use the dependency map; computation accompanies the theory.

## Format and numbering

Dark-by-default local HTML; one chapter per root file; bundled MathJax; chapter
search; section and recording links; code-copy buttons; expandable worked
solutions; phone layouts; print/PDF styles; original reproducible figures.
Chapter.N numbering for sections, equations, results, and figures. Python labs
use NumPy/SciPy/Matplotlib only where needed and record actual outputs and seeds.
Final reader builds must work without private source files or network access.

## Primary sources and evidence

The requested playlist is S001. Official instructor notes are S002 (118 PDF
pages); page 1 explicitly limits their main exposition to recordings 1–11.
The syllabus and quiz extend beyond that boundary. Captions, downloaded PDFs,
equation frames, and review reports stay in ignored `work/`. Acquisition is
distinct from reading, and sampled stills are distinct from continuous viewing.
Exact source pages and recording intervals are verified before drafting each
section; no timestamp is assigned from a title alone.

## Author decisions reserved

Approve the scope, result graph/notation, architecture, and detailed outline
together or request changes. Then approve one pilot chapter and the first
representative figure of a new visual class as required by the textbook skill.
The prior project's permission to publish does not transfer: this request
authorizes creating local notes; public repository creation/push/Pages is a
separate decision, now authorized by the subsequent GitHub publication request. No paid external model calls are needed for planning.

## Proposed scientific review

Preserve the prior course's author → independent review 1 → scoped repair →
independent review 2 → repair verification sequence. Use actual reviewer
identities and artifact SHA-256 digests. Preserve failed and superseded reports.
No acceptance until two full independent reviews and any required targeted
checks clear the final artifacts. Mechanical checks do not certify the science.
