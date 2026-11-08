# Detailed result-group outline — approved

This is a planning artifact, not chapter prose. See the specification and notation contract.
Each result group expands into modelling, derivation, interpretation, and checks during drafting.

## Chapter 1: Counting fluctuations: discrete distributions and cumulants

Lectures: [1, 2]. Prerequisites: entry prerequisites.
Estimated pages: 24.

Purpose and running case: Distinguish independent particle counts from thermal bunching using equal mean counts.

Coverage: Bernoulli, binomial, geometric, Poisson, Skellam, negative binomial; generating functions, moments, and cumulants.

### 1.1 Independent trials and the rare-event limit

Purpose: establish R01-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For n independent Bernoulli trials with success probability p, the count has probability-generating function (1-p+p*z)^n; its mean is n*p and variance n*p*(1-p). With n*p fixed at lambda as n tends to infinity, its law converges to Poisson(lambda).
Uses: entry prerequisites.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Check normalization and moments by exact finite sums; test convergence of masses as trial count grows.
Limit and proof hinge to expose: Independence and rare-event scaling are hypotheses; an arbitrary event count is not Poisson.
Transition: Bunching, summation, and signed counts.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 1.2 Bunching, summation, and signed counts

Purpose: establish R01-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A geometric count on nonnegative integers with mean mu has variance mu*(1+mu). A sum of r independent such counts is negative binomial for positive integer r. The difference of independent Poisson counts of means lambda_plus and lambda_minus has mean lambda_plus-lambda_minus and variance lambda_plus+lambda_minus.
Uses: R01-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover the geometric law at r=1 and the one-sided Poisson law when the negative-count mean vanishes.
Limit and proof hinge to expose: State support and parameter conventions; the integer-sum construction alone does not establish every real-shape parameterization.
Transition: Cumulants expose independence.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 1.3 Cumulants expose independence

Purpose: establish R01-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a random variable whose moment-generating function exists near zero, cumulants are derivatives at zero of its logarithm. Independent sums add cumulants. Translation changes only the first cumulant; cumulants of order k scale by the kth power under scalar multiplication.
Uses: R01-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the first four cumulants from the generating functions and verify the Poisson special case.
Limit and proof hinge to expose: A moment-generating function need not exist; later chapters use characteristic functions for heavy tails.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 1 computational and assessment sections

Laboratory: Compare exact probability masses and cumulants with seeded sampling; diagnose when equal means conceal different variances.
Figure teaching job: Equal-mean count distributions and their variance-to-mean ratios.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 2: Densities, transformations, and characteristic functions

Lectures: [3]. Prerequisites: 1.
Estimated pages: 16.

Purpose and running case: Convert a Gaussian velocity model into the kinetic-energy distribution of an ideal gas.

Coverage: Continuous densities, characteristic functions, Gaussian moments and cumulants, ideal-gas energy.

### 2.1 Probability transforms with every preimage

Purpose: establish R02-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a differentiable transformation y=g(x), a continuous input density transforms to the sum of input density divided by absolute derivative over regular inverse branches. The branch formula applies away from critical values, with singular behavior treated by integration.
Uses: R01-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Use y=x squared for a centered Gaussian and integrate the resulting positive density to one.
Limit and proof hinge to expose: A noninvertible transformation requires all preimages; atoms and flat branches need separate treatment.
Transition: Characteristic functions and the Gaussian law.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 2.2 Characteristic functions and the Gaussian law

Purpose: establish R02-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: The characteristic function of a real random variable is the expectation of exp(i*k*X) for real k and always exists. A Gaussian with mean mu and variance sigma squared has characteristic function exp(i*k*mu-sigma squared*k squared/2). Its cumulants beyond order two vanish.
Uses: R02-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover the variance by differentiating the characteristic function and verify Gaussian fourth moment equals three times the squared variance.
Limit and proof hinge to expose: Differentiation under expectation needs moment conditions; existence of the characteristic function does not imply existence of moments.
Transition: Energy as a sum of squared Gaussian coordinates.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 2.3 Energy as a sum of squared Gaussian coordinates

Purpose: establish R02-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: If d independent velocity components are centered Gaussians of variance k_B*T/m, the kinetic energy m times squared speed divided by two has a gamma density of shape d/2 and scale k_B*T. Its mean is d*k_B*T/2.
Uses: R02-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Check the one-coordinate density against the transformation formula and the d=3 mean against equipartition.
Limit and proof hinge to expose: This is classical, nonrelativistic equilibrium with independent quadratic degrees of freedom.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 2 computational and assessment sections

Laboratory: Compare change-of-variable formulas with sampled velocities and energy histograms, including Jacobian normalization.
Figure teaching job: Velocity-to-energy mapping with the positive and negative preimages shown explicitly.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 3: The central limit theorem and the diffusion scale

Lectures: [4]. Prerequisites: 1, 2.
Estimated pages: 16.

Purpose and running case: Decide when a many-step random flight can be replaced by a Gaussian propagator.

Coverage: Gaussian sums, finite-variance central limit theorem, uniform sums, random flights, diffusion scaling.

### 3.1 Convolution becomes multiplication

Purpose: establish R03-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For independent real variables, the characteristic function of their sum is the product of their characteristic functions. Independent Gaussian sums are Gaussian with summed means and variances.
Uses: R01-3, R02-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Compare an exact convolution of uniform densities with a numerical Fourier inversion.
Limit and proof hinge to expose: Dependence invalidates factorization even when the marginals are Gaussian.
Transition: A finite-variance central limit theorem.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 3.2 A finite-variance central limit theorem

Purpose: establish R03-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For independent identically distributed variables with finite mean mu and positive finite variance sigma squared, the centered sum divided by sigma times the square root of the number of terms converges in distribution to a standard Gaussian.
Uses: R03-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the characteristic-function limit and compare exact binomial cumulative probabilities with the Gaussian approximation.
Limit and proof hinge to expose: Convergence in distribution gives neither a universal finite-sample rate nor uniformly correct rare-event tails.
Transition: The Brownian scaling of a lattice walk.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 3.3 The Brownian scaling of a lattice walk

Purpose: establish R03-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For independent unbiased steps of length ell taken every delta_t, the variance after elapsed time t is ell squared*t/delta_t on grid times. Holding ell squared/(2*delta_t)=D fixed yields the one-dimensional diffusion kernel in the continuum scaling limit.
Uses: R03-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover variance 2*D*t and test the continuum kernel against the discrete law after accounting for lattice parity.
Limit and proof hinge to expose: A continuum approximation loses finite-speed support and needs a stated mode of convergence.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 3 computational and assessment sections

Laboratory: Measure distributional convergence and lattice-to-diffusion error across step sizes; compare the central region with tails.
Figure teaching job: Rescaled walk densities approaching a Gaussian and ballistic lattice support at finite time.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 4: Stable laws, heavy tails, and infinite divisibility

Lectures: [5]. Prerequisites: 1, 2, 3.
Estimated pages: 16.

Purpose and running case: Determine whether averaging repeated measurements actually reduces their scatter.

Coverage: Stable-law definitions, Gaussian/Cauchy/Levy examples, divisibility and infinite divisibility.

### 4.1 Stable scaling

Purpose: establish R04-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A symmetric strictly stable law with index alpha in (0,2] and characteristic function exp(-c*absolute(k)^alpha), c positive, is closed under independent sums: n equal copies rescale by n raised to 1/alpha without centering.
Uses: R01-3, R02-3, R03-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Multiply characteristic functions and recover Gaussian square-root scaling at alpha=2 and Cauchy linear scaling at alpha=1.
Limit and proof hinge to expose: Use this symmetric subclass for the proof; general skewed stable laws need explicit centering and parameter conventions.
Transition: Why the sample mean may not concentrate.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 4.2 Why the sample mean may not concentrate

Purpose: establish R04-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: The mean of n independent centered Cauchy variables with scale s has the same Cauchy law and scale s for every positive integer n. For a centered Gaussian of variance sigma squared, the sample mean has variance sigma squared/n.
Uses: R04-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Compare empirical interquartile ranges of repeated means with the exact Cauchy and Gaussian quantiles.
Limit and proof hinge to expose: The Cauchy mean and variance do not exist; a sample average is still a defined random variable.
Transition: Divisibility is a property of the whole law.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 4.3 Divisibility is a property of the whole law

Purpose: establish R04-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A law is infinitely divisible when, for each positive integer n, it is the law of a sum of n independent identically distributed variables. Poisson laws have this property by dividing their intensity; a nondegenerate fixed-trial binomial law is not infinitely divisible on the real line.
Uses: R04-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the Poisson factorization; give a separate support-and-variance argument for the binomial obstruction and examine geometric and Skellam cases.
Limit and proof hinge to expose: Being decomposable into a particular number of summands is weaker than infinite divisibility; the one-sided Levy example is separate from the symmetric subclass.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 4 computational and assessment sections

Laboratory: Compare Gaussian and Cauchy sample means using quantiles rather than nonexistent Cauchy moments.
Figure teaching job: Width of sample-mean quantiles versus sample size for Gaussian and Cauchy inputs.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 5: From random variables to Markov state descriptions

Lectures: [6]. Prerequisites: 1, 2.
Estimated pages: 16.

Purpose and running case: Explain why matching single-time histograms does not determine the evolution of a system.

Coverage: Joint and conditional laws, stationarity, Markov property, chains, Chapman-Kolmogorov, equilibrium relaxation.

### 5.1 A process is a family of joint laws

Purpose: establish R05-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: Strict stationarity means invariance of every finite-dimensional joint distribution under a common time shift. Constancy of the one-time marginal alone does not imply strict stationarity.
Uses: R01-3, R02-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Construct a counterexample with constant marginals and a time-dependent two-time law.
Limit and proof hinge to expose: Wide-sense stationarity is a different, second-moment condition; Gaussianity is needed to recover the full law from first and second moments.
Transition: State sufficiency and composition.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 5.2 State sufficiency and composition

Purpose: establish R05-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a time-homogeneous Markov chain with K_ij equal to the probability of the next state being i given current state j, distribution columns evolve by multiplication by K. Multi-step transitions satisfy K raised to (n+m)=K raised to n times K raised to m.
Uses: R05-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Compare path enumeration with matrix multiplication in a three-state chain.
Limit and proof hinge to expose: An observed coordinate of a Markov process need not itself be Markov.
Transition: Equilibrium is not automatic convergence.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 5.3 Equilibrium is not automatic convergence

Purpose: establish R05-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A stationary probability column pi satisfies K*pi=pi. A finite irreducible aperiodic chain converges to its unique stationary distribution from every initial distribution; irreducibility without aperiodicity is insufficient.
Uses: R05-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Contrast a mixing two-state chain with a deterministic two-cycle.
Limit and proof hinge to expose: Infinite state spaces require additional recurrence conditions; a stationary vector alone does not prove mixing.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 5 computational and assessment sections

Laboratory: Construct processes with equal marginals and different correlations; evolve a finite transition matrix.
Figure teaching job: Two processes with identical marginals but contrasting temporal persistence.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 6: Generators, detailed balance, and exactly soluble jump processes

Lectures: [7, 8]. Prerequisites: 1, 5.
Estimated pages: 24.

Purpose and running case: Predict relaxation, event counts, and displacement from transition rates rather than time-step probabilities.

Coverage: Master-equation semigroups, stationary laws, detailed balance, dichotomous correlations, Poisson process, biased lattice walks.

### 6.1 A conservative generator

Purpose: establish R06-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a finite-state continuous-time chain with nonnegative off-diagonal rates Q_ij from j to i and zero column sums, the probability column satisfies dp/dt=Q*p and evolves by exp(t*Q). A stationary law satisfies Q*pi=0; detailed balance requires Q_ij*pi_j=Q_ji*pi_i.
Uses: R01-3, R05-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Verify probability conservation and compare reversible and circulating three-state chains.
Limit and proof hinge to expose: Detailed balance is sufficient for stationarity and stronger than it; infinite generators need nonexplosion and domain control.
Transition: Two states retain a correlation time.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 6.2 Two states retain a correlation time

Purpose: establish R06-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a symmetric process taking values plus or minus a and switching at rate nu from either state, the stationary mean is zero and autocovariance is a squared times exp(-2*nu*absolute(tau)).
Uses: R06-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the conditional transition probabilities and check the covariance at zero and long lag.
Limit and proof hinge to expose: Asymmetric switching changes the mean and variance; starting out of equilibrium changes two-time statistics.
Transition: Counting and displacement generating functions.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 6.3 Counting and displacement generating functions

Purpose: establish R06-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A homogeneous Poisson process of rate lambda has count generating function exp(lambda*t*(z-1)). The difference of two independent Poisson processes with rates r_plus and r_minus has mean displacement ell*(r_plus-r_minus)*t and variance ell squared*(r_plus+r_minus)*t.
Uses: R06-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover the one-way counting process and the unbiased lattice diffusion coefficient.
Limit and proof hinge to expose: Independent stationary increments and exponential waiting times distinguish these models from general renewal processes.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 6 computational and assessment sections

Laboratory: Compare exact matrix exponentials and generating functions with event-driven jump simulations.
Figure teaching job: State diagram and correlation decay of a two-state fluctuator beside a Poisson counting path.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 7: Lattice transport and state-dependent birth and death

Lectures: [9]. Prerequisites: 1, 6.
Estimated pages: 16.

Purpose and running case: Identify which observables remain tractable when event rates depend on the present population.

Coverage: Walk cumulants, higher-dimensional walks, one-step birth/death generators, nonstationary Poisson counts, linear rates.

### 7.1 Transport cumulants

Purpose: establish R07-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For lattice displacement ell times the difference of independent Poisson counts with rates r_plus and r_minus, the kth displacement cumulant is ell raised to k times (r_plus+(-1) raised to k*r_minus)*t. Independent coordinate walks factorize their joint characteristic function.
Uses: R01-3, R06-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Separate odd drift cumulants from even fluctuation cumulants and verify a two-dimensional example.
Limit and proof hinge to expose: Coordinate independence is an assumption, not a consequence of living on a lattice.
Transition: One-step population generators.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 7.2 One-step population generators

Purpose: establish R07-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For births at rate lambda_n and deaths at rate delta_n in population state n, with delta_0=0, the probability equation is dp_n/dt=lambda_(n-1)*p_(n-1)+delta_(n+1)*p_(n+1)-(lambda_n+delta_n)*p_n, with nonexistent negative-state terms omitted.
Uses: R07-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Sum the equations to establish conservation, explicitly handling the n=0 boundary.
Limit and proof hinge to expose: Unbounded state spaces can permit explosion; a formal conservative expression is insufficient without existence conditions.
Transition: Time-dependent intensity.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 7.3 Time-dependent intensity

Purpose: establish R07-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A nonhomogeneous Poisson process with deterministic locally integrable rate lambda(t) has count mean and variance equal to the integrated rate from zero to t, and Poisson increments on disjoint intervals are independent.
Uses: R07-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Solve its generating-function equation and test a piecewise constant intensity by time rescaling.
Limit and proof hinge to expose: A random intensity defines a different model; replacing it by its expectation generally loses overdispersion.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 7 computational and assessment sections

Laboratory: Compare exact walk cumulants and moment equations with event-driven population simulations.
Figure teaching job: Ballistic mean displacement and diffusive spread; population-dependent transition arrows.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 8: Stationary populations, fluctuations, and physical balance

Lectures: [10]. Prerequisites: 6, 7.
Estimated pages: 16.

Purpose and running case: Decide whether a rate model admits an equilibrium population or only a formal stationary sequence.

Coverage: Birth/death stationary products; sedimentation, chemistry, radiation, population models; linear-rate moments.

### 8.1 The stationary product formula

Purpose: establish R08-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For an irreducible birth-death chain on nonnegative integers with positive neighbor rates and zero boundary current, a stationary probability is proportional to the product from j=0 to n-1 of lambda_j/delta_(j+1), provided the sum of these weights is finite and the process is nonexplosive.
Uses: R06-3, R07-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover Poisson immigration-death equilibrium from constant birth rate and linear death rate.
Limit and proof hinge to expose: A positive recurrence criterion cannot be replaced by writing down unnormalized weights.
Transition: Balance laws in physical examples.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 8.2 Balance laws in physical examples

Purpose: establish R08-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: If nearest-neighbor rate ratios equal exp(-(E_(n+1)-E_n)/(k_B*T)), the zero-current stationary weights are proportional to exp(-E_n/(k_B*T)) whenever normalizable.
Uses: R08-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Apply the ratio condition to sedimentation on a height lattice and distinguish state degeneracy from transition multiplicity.
Limit and proof hinge to expose: Thermal balance requires the stated bath assumptions; population models need not be thermal or reversible.
Transition: Closed moment equations.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 8.3 Closed moment equations

Purpose: establish R08-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a nonexplosive birth-death process with finite required moments, the derivative of the mean equals the expectation of lambda_n-delta_n; the derivative of the second moment equals the expectation of (2*n+1)*lambda_n+(-2*n+1)*delta_n. Affine rates close these equations.
Uses: R08-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Solve immigration-death mean and variance transients and compare exact equilibrium limits.
Limit and proof hinge to expose: Nonlinear rates generally introduce higher moments; closure is then an approximation requiring justification.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 8 computational and assessment sections

Laboratory: Reproduce immigration-death equilibrium and diagnose a nonnormalizable stationary candidate.
Figure teaching job: Stationary population tails as birth/death ratios cross the normalization boundary.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 9: From jump generators to diffusion equations

Lectures: [11]. Prerequisites: 3, 6, 7, 8.
Estimated pages: 16.

Purpose and running case: Choose a continuum approximation that preserves drift, fluctuations, and probability current.

Coverage: Continuous-state master equations, Kramers-Moyal, Pawula scope, Fokker-Planck, Smoluchowski, Wiener and SDE correspondence.

### 9.1 Conditional increment moments

Purpose: establish R09-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For an Itô diffusion dX=a(X,t)*dt+b(X,t)*dW with scalar Wiener process W, sufficient coefficient regularity, and an existing smooth density rho, the forward equation is partial_t rho=-partial_x(a*rho)+(1/2)*partial_xx(b squared*rho).
Uses: R03-3, R06-3, R07-3, R08-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover constant-drift Gaussian transport and check mass conservation by integrating the probability current.
Limit and proof hinge to expose: Noise amplitude b and diffusion coefficient b squared/2 differ; singular boundaries require boundary classification.
Transition: The controlled lattice limit.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 9.2 The controlled lattice limit

Purpose: establish R09-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a nearest-neighbor walk with spacing ell and rates r_plus and r_minus, drift is ell*(r_plus-r_minus) and diffusion coefficient is ell squared*(r_plus+r_minus)/2. A diffusive limit holds when these combinations approach finite values and higher jump effects vanish in the limit.
Uses: R09-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover the unbiased heat equation and demonstrate loss of accuracy before the many-jump regime.
Limit and proof hinge to expose: Truncating the Kramers-Moyal series is not automatically a positive probability evolution; cite Pawula's precise theorem after verifying its source.
Transition: Current, confinement, and stationary density.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 9.3 Current, confinement, and stationary density

Purpose: establish R09-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For constant D positive and drift -M*U'(x) with mobility M positive, zero stationary current yields density proportional to exp(-M*U(x)/D), if normalizable. At thermal equilibrium D=M*k_B*T gives the Gibbs density.
Uses: R09-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Use a quadratic potential to recover a Gaussian stationary law and show failure for a nonconfining flat potential on the line.
Limit and proof hinge to expose: Zero-current equilibrium depends on the domain and boundary conditions; it is distinct from a driven steady state.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 9 computational and assessment sections

Laboratory: Match lattice drift and diffusion coefficients and measure continuum approximation error under grid refinement.
Figure teaching job: Jump kernel, continuum density, and boundary probability flux in the same transport model.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 10: Velocity relaxation and the emergence of spatial diffusion

Lectures: [12, 13]. Prerequisites: 2, 6, 9.
Estimated pages: 24.

Purpose and running case: Find when a Brownian particle's displacement changes from ballistic to diffusive.

Coverage: Langevin/FPE correspondence, thermal noise strength, OU transition law, velocity correlation, MSD, Green-Kubo, joint density and Gaussian-Markov qualification.

### 10.1 The velocity transition law

Purpose: establish R10-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For dV=-gamma*V*dt+sqrt(2*gamma*k_B*T/m)*dW, gamma positive, deterministic initial velocity v0, and independent Wiener increments, V(t) is Gaussian with mean v0*exp(-gamma*t) and variance (k_B*T/m)*(1-exp(-2*gamma*t)).
Uses: R02-3, R06-3, R09-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover deterministic initial data as t tends to zero and the Maxwell velocity variance at long time.
Limit and proof hinge to expose: gamma is a velocity relaxation rate, not the dimensional drag coefficient m*gamma.
Transition: Correlation and integrated displacement.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 10.2 Correlation and integrated displacement

Purpose: establish R10-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: With a thermal stationary initial velocity, the velocity autocovariance is (k_B*T/m)*exp(-gamma*absolute(tau)). The displacement variance is 2*D*(t-(1-exp(-gamma*t))/gamma), where D=k_B*T/(m*gamma).
Uses: R10-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover ballistic variance (k_B*T/m)*t squared at short times and 2*D*t at long times.
Limit and proof hinge to expose: The quoted displacement law uses stationary initial velocity; a fixed initial velocity gives a different transient variance.
Transition: Green-Kubo and joint phase-space dynamics.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 10.3 Green-Kubo and joint phase-space dynamics

Purpose: establish R10-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a stationary zero-mean velocity with integrable autocovariance C_v, displacement variance equals twice the integral from zero to t of (t-s)*C_v(s) ds, and its long-time diffusion coefficient equals the integral of C_v from zero to infinity. Position and velocity together form a Markov state in the inertial Langevin model.
Uses: R10-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Integrate the OU covariance and compare the joint Gaussian covariance with sampled trajectories.
Limit and proof hinge to expose: The position coordinate alone generally has memory at finite inertia; Doob classification requires a separate precise cited statement.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 10 computational and assessment sections

Laboratory: Compare exact OU updates with Euler discretization and recover the ballistic-to-diffusive displacement crossover.
Figure teaching job: Mean-square displacement and its local logarithmic slope across the momentum-relaxation time.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 11: Confinement, phase space, and the overdamped limit

Lectures: [14]. Prerequisites: 9, 10.
Estimated pages: 16.

Purpose and running case: Determine whether eliminating velocity preserves the relaxation times of a trapped particle.

Coverage: Coupled position/velocity Langevin equations, harmonic stationary density and rates, high friction, arbitrary-potential Kramers equation.

### 11.1 A linear stochastic oscillator

Purpose: establish R11-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For dX=V*dt and dV=(-gamma*V-omega0 squared*X)*dt+sqrt(2*gamma*k_B*T/m)*dW, positive gamma and omega0 give stable mean dynamics whose eigenvalues solve r squared+gamma*r+omega0 squared=0.
Uses: R09-3, R10-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Distinguish oscillatory, critical, and overdamped mean relaxation and verify the critical limit without dividing by a vanishing root difference.
Limit and proof hinge to expose: Stability of mean dynamics alone is not a proof of the full stationary distribution.
Transition: Kramers equilibrium.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 11.2 Kramers equilibrium

Purpose: establish R11-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a confining differentiable potential U, the inertial Langevin forward operator with force -U' and thermal noise admits a stationary phase-space density proportional to exp(-(m*v squared/2+U(x))/(k_B*T)), when the normalization is finite and boundary flux conditions hold.
Uses: R11-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Substitute the density into the Kramers equation and recover independent harmonic position and velocity variances.
Limit and proof hinge to expose: Stationary phase-space streaming need not vanish term by term; do not impose overdamped detailed-balance language on each current component.
Transition: Eliminating the fast velocity.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 11.3 Eliminating the fast velocity

Purpose: establish R11-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For the harmonic model with gamma much larger than omega0, one relaxation rate approaches -gamma and the slow rate approaches -omega0 squared/gamma. On slow time scales, constant-friction thermal reduction gives dX=-U'(X)/(m*gamma)*dt+sqrt(2*k_B*T/(m*gamma))*dW.
Uses: R11-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Compare exact eigenvalues and simulated position covariances across the time-scale separation.
Limit and proof hinge to expose: The reduction fails at momentum time scales; position-dependent friction needs additional care.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 11 computational and assessment sections

Laboratory: Compare inertial and overdamped harmonic correlations as damping changes; check equilibrium covariances.
Figure teaching job: Two phase-space relaxation rates and the parameter range where one-coordinate reduction is accurate.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 12: Wiener paths, roughness, and exceptional time statistics

Lectures: [15]. Prerequisites: 3, 9, 10, 11.
Estimated pages: 16.

Purpose and running case: Understand why refining a Brownian trajectory makes its apparent velocity more erratic.

Coverage: Vector Langevin dynamics, free and magnetic velocity correlations as a bridge; Wiener covariance, rough paths, Holder regularity, arcsine law, iterated logarithm, OU-Wiener relation.

### 12.1 Covariance without stationarity

Purpose: establish R12-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A standard Wiener process starts at zero, has continuous paths and independent Gaussian increments of variance equal to elapsed time. Its covariance at nonnegative times s and t is min(s,t); the process is nonstationary although its increments are stationary.
Uses: R03-3, R09-3, R10-3, R11-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Compute the covariance from independent increments and compare a covariance heat map with ensemble samples.
Limit and proof hinge to expose: Continuous paths do not imply differentiable paths; Brownian motion is not finite-correlation colored noise.
Transition: Quadratic variation and path regularity.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 12.2 Quadratic variation and path regularity

Purpose: establish R12-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: On uniform partitions of a fixed time interval, the sum of squared Wiener increments converges in mean square to the interval length. Finite-difference velocity over a step h has variance 1/h. Almost-sure differentiability and Holder claims require their own theorem statements and verified citations.
Uses: R12-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the mean and variance of quadratic-variation sums and perform mesh refinement.
Limit and proof hinge to expose: A numerical path cannot prove almost-sure nondifferentiability, the arcsine law, or the iterated-logarithm theorem.
Transition: Gaussian time changes and exceptional observables.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 12.3 Gaussian time changes and exceptional observables

Purpose: establish R12-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: The zero-initial OU process solving dX=-gamma*X*dt+b*dW has the same finite-dimensional law as b*exp(-gamma*t)*B((exp(2*gamma*t)-1)/(2*gamma)), where B is a standard Wiener process. The equality is in law unless a coupling is constructed.
Uses: R12-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Match both Gaussian covariance functions; separately plan cited statements and numerical illustrations of occupation-time and iterated-logarithm results.
Limit and proof hinge to expose: Finite-dimensional law equivalence should not be confused with equality of arbitrary sampled paths.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 12 computational and assessment sections

Laboratory: Measure mesh-dependent finite-difference velocities and quadratic variation; illustrate occupation-time distributions without claiming proof.
Figure teaching job: Nested Brownian increments and converging quadratic variation despite diverging apparent velocity variance.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 13: Itô transformations, radial diffusion, and multiplicative noise

Lectures: [16]. Prerequisites: 2, 9, 12.
Estimated pages: 16.

Purpose and running case: Transform a noisy coordinate without silently losing its noise-induced drift.

Coverage: Itô/FPE transformation, radial diffusion, Bessel and squared-Bessel conventions, powers/exponentials of Wiener motion, geometric Brownian motion, Black-Scholes boundary.

### 13.1 The second derivative survives

Purpose: establish R13-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For scalar dX=a*dt+b*dW and a sufficiently smooth function g(x,t), Itô's rule gives dg=(partial_t g+a*partial_x g+(b squared/2)*partial_xx g)*dt+b*partial_x g*dW, under standard local integrability and existence hypotheses.
Uses: R02-3, R09-3, R12-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Apply the rule to X squared and recover the missing b squared drift.
Limit and proof hinge to expose: This is the Itô convention; Stratonovich notation carries a different chain rule and drift conversion.
Transition: Radius and squared radius.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 13.2 Radius and squared radius

Purpose: establish R13-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For d-dimensional Brownian diffusion with coordinate noise amplitude sqrt(2*D), the radius away from zero has drift D*(d-1)/R and noise amplitude sqrt(2*D). Its square Z obeys dZ=2*d*D*dt+sqrt(8*D*Z)*dB.
Uses: R13-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover mean squared radius 2*d*D*t and the chi radial law from independent coordinates.
Limit and proof hinge to expose: The radius formula is singular at zero; d=1 requires treatment of the reflecting local-time term. State which scaled process is called Bessel or squared Bessel.
Transition: Exponential transformations.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 13.3 Exponential transformations

Purpose: establish R13-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For dS=a_S*S*dt+b_S*S*dW with positive initial S, the solution is S0*exp((a_S-b_S squared/2)*t+b_S*W(t)). Its expectation is S0*exp(a_S*t) when the coefficients are constant.
Uses: R13-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Compare exact logarithmic updates with discretizations that can generate negative values.
Limit and proof hinge to expose: The Black-Scholes equation additionally requires a market and pricing argument; it does not follow from the change of variables alone.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 13 computational and assessment sections

Laboratory: Contrast correct Itô transformed moments with an ordinary-chain-rule implementation; check positive geometric paths.
Figure teaching job: Radial entropic drift and the discrepancy caused by omitting the Itô correction.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 14: Threshold crossings and extremes of smooth random signals

Lectures: [17]. Prerequisites: 2, 5, 10, 11, 12.
Estimated pages: 16.

Purpose and running case: Estimate false alarm crossings from a fluctuating signal without counting every sampled sign change as a physical event.

Coverage: Crossing counts and rates, up/down crossings, Brownian oscillator, extrema, introductory spectral examples.

### 14.1 Crossings require a derivative law

Purpose: establish R14-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a stationary differentiable real process with a regular joint density of value and derivative and finite crossing intensity, the mean upcrossing rate at level u is the integral over positive v of v times that joint density at (u,v).
Uses: R02-3, R05-3, R10-3, R11-3, R12-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the swept-interval argument and recover equal up/down mean rates for a stationary symmetric model.
Limit and proof hinge to expose: These regularity hypotheses exclude direct application to nondifferentiable Wiener and OU coordinates.
Transition: The Gaussian Rice rate.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 14.2 The Gaussian Rice rate

Purpose: establish R14-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a stationary zero-mean differentiable Gaussian process with positive value and derivative standard deviations sigma_X and sigma_V, the upcrossing rate is sigma_V/(2*pi*sigma_X) times exp(-u squared/(2*sigma_X squared)); stationarity makes value and derivative uncorrelated and hence independent.
Uses: R14-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover the harmonic Brownian position's zero-level crossing rate from equilibrium variances.
Limit and proof hinge to expose: Finite derivative variance is essential; high-frequency smoothing changes crossing statistics.
Transition: Extrema and finite-window events.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 14.3 Extrema and finite-window events

Purpose: establish R14-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a twice differentiable regular process, counting maxima can be expressed as zero crossings of the derivative weighted by negative second derivative. The expected number of level crossings does not by itself specify the probability of at least one crossing in a time window.
Uses: R14-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Construct repeated clustered crossings with the same expected count as a more dispersed process and compare event probabilities.
Limit and proof hinge to expose: Poisson approximations for rare crossings need additional dependence assumptions. The Brownian oscillator's velocity is not differentiable; do not apply this twice-differentiable extrema formula to it without smoothing.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 14 computational and assessment sections

Laboratory: Compare sampled crossing rates of an integrated velocity oscillator with the Gaussian Rice prediction and test sampling bias.
Figure teaching job: Resolved versus missed crossings as the same differentiable signal is sampled at different intervals.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 15: Charged Brownian motion and anisotropic diffusion

Lectures: [18]. Prerequisites: 10, 11, 12.
Estimated pages: 16.

Purpose and running case: Explain how a magnetic field suppresses transverse diffusion without changing thermal speed variance.

Coverage: Vector Langevin and FPE, rotating frame, velocity density and correlation matrix, Green-Kubo tensor, longitudinal and transverse diffusion.

### 15.1 Rotation and damping

Purpose: establish R15-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a uniform magnetic field, isotropic drag rate gamma positive, and thermal additive noise, the velocity drift matrix is -gamma times identity plus the antisymmetric Lorentz-rotation matrix. The matrix exponential is exponential damping times the corresponding rotation.
Uses: R10-3, R11-3, R12-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Verify kinetic energy is unchanged by the Lorentz term and recover the zero-field OU law.
Limit and proof hinge to expose: Specify signed charge, field orientation, and rotation convention before component formulas.
Transition: Velocity covariance and thermal invariance.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 15.2 Velocity covariance and thermal invariance

Purpose: establish R15-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For stationary thermal velocity, the equal-time covariance matrix is (k_B*T/m) times identity. At positive lag the covariance is the drift matrix exponential times this equal-time covariance, so transverse correlations oscillate while decaying.
Uses: R15-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Solve the covariance balance equation and test both signed cross-correlations.
Limit and proof hinge to expose: Antisymmetric cross-correlations do not imply an antisymmetric covariance at equal times.
Transition: The symmetric diffusion tensor.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 15.3 The symmetric diffusion tensor

Purpose: establish R15-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: With cyclotron frequency magnitude omega_c, longitudinal diffusion is k_B*T/(m*gamma) and transverse diffusion is (k_B*T/m)*gamma/(gamma squared+omega_c squared). The displacement-covariance diffusion tensor is the symmetric part of the integrated velocity-correlation matrix.
Uses: R15-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover isotropy at zero field and transverse suppression at large omega_c/gamma.
Limit and proof hinge to expose: An antisymmetric integrated response can encode Hall transport; it is not a contribution to mean-square displacement.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 15 computational and assessment sections

Laboratory: Use exact linear-Gaussian velocity updates to compare field-parallel and perpendicular displacement variances.
Figure teaching job: Rotating velocity correlations and field-dependent longitudinal/transverse diffusion.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 16: Noise spectra, filters, and thermal fluctuations

Lectures: [19]. Prerequisites: 6, 10, 12, 14.
Estimated pages: 16.

Purpose and running case: Infer a relaxation time from a noisy record without confusing spectral convention or finite-record artifacts with physics.

Coverage: Wiener-Khinchin, white/colored noise, linear transfer functions, matrix spectra, resistor thermal noise.

### 16.1 Convention and Wiener-Khinchin

Purpose: establish R16-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a real stationary zero-mean process with integrable autocovariance C, define the two-sided angular-frequency spectral density S(omega) as the integral over all lag of C(tau)*exp(i*omega*tau). Then C(0) equals the integral of S divided by 2*pi under the corresponding inversion conditions.
Uses: R06-3, R10-3, R12-3, R14-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Transform an exponential covariance and integrate the resulting Lorentzian to recover the variance.
Limit and proof hinge to expose: White noise is a generalized process; a nonzero mean adds a zero-frequency delta to the uncentered spectrum.
Transition: Linear filtering and matrix spectra.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 16.2 Linear filtering and matrix spectra

Purpose: establish R16-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a stable linear time-invariant filter with transfer matrix H and stationary input spectral matrix S_in, the output spectral matrix is H*S_in*H conjugate-transpose. A valid spectral matrix is Hermitian and positive semidefinite at each frequency where defined.
Uses: R16-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover the scalar modulus-squared transfer rule and test positivity for correlated two-channel noise.
Limit and proof hinge to expose: Transfer formulas require a stationary output and appropriate stability/integrability assumptions.
Transition: Thermal-noise normalization.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 16.3 Thermal-noise normalization

Purpose: establish R16-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: In the classical low-frequency equilibrium limit, the resistor voltage-noise density is 2*k_B*T*R in the two-sided angular-frequency convention used here; the corresponding one-sided density per hertz is 4*k_B*T*R. Integrating a physically filtered spectrum gives finite measured variance.
Uses: R16-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the conversion of conventions and recover capacitor equipartition through a resistor-capacitor filter.
Limit and proof hinge to expose: The ideal white spectrum is bandwidth-limited physically; quantum and frequency-dependent corrections lie outside this approximation.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 16 computational and assessment sections

Laboratory: Compare covariance integration, a periodogram averaged over ensembles, and an analytic OU Lorentzian.
Figure teaching job: The same OU process in covariance and spectral representations, with spectral-area normalization.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 17: Causality, susceptibility, and fluctuation-dissipation

Lectures: [20]. Prerequisites: 10, 11, 16.
Estimated pages: 16.

Purpose and running case: Predict the weak driven motion of a Brownian particle from its spontaneous fluctuations.

Coverage: Dynamic mobility, causal response, generalized susceptibility, first/second fluctuation-dissipation relations, analyticity, classical response, LCR example.

### 17.1 A retarded response kernel

Purpose: establish R17-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A causal linear response has change in mean observable at time t equal to the integral over nonnegative lag of response kernel times applied field at t minus lag. With the positive-exponential Fourier convention, susceptibility is the one-sided transform of this kernel.
Uses: R10-3, R11-3, R16-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Solve the driven damped velocity equation and derive mobility 1/(m*(gamma-i*omega)).
Limit and proof hinge to expose: Linear response is a small-perturbation statement around a specified reference state.
Transition: Fluctuations and dissipation.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 17.2 Fluctuations and dissipation

Purpose: establish R17-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a classical equilibrium coordinate coupled to a force through energy -force times coordinate, its centered two-sided spectrum satisfies S_x(omega)=2*k_B*T*Im(chi_x(omega))/omega for nonzero real omega in the stated convention, with the zero-frequency limit taken when it exists.
Uses: R17-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover both the harmonic oscillator spectrum and the free-particle velocity mobility relation using the correctly conjugate variables.
Limit and proof hinge to expose: The observable, conjugate field, equilibrium hypothesis, and transform sign determine the formula; do not transplant it to arbitrary driven noise.
Transition: Causality constrains frequency response.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 17.3 Causality constrains frequency response

Purpose: establish R17-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a sufficiently decaying real causal response kernel, the positive-exponential susceptibility is analytic in the upper complex-frequency half-plane and obeys conjugate symmetry on the real axis. Dispersion relations require the corresponding decay or subtraction hypotheses.
Uses: R17-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Locate the damped oscillator poles in the lower half-plane and verify the real/imaginary response relation numerically with a finite-band error study.
Limit and proof hinge to expose: A truncated numerical Hilbert transform is a check with bandwidth error, not a proof of a dispersion relation.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 17 computational and assessment sections

Laboratory: Compare equilibrium spectral estimates with a weak periodic-force response and identify nonlinear-drive failure.
Figure teaching job: Response amplitude and phase alongside the equilibrium fluctuation spectrum of the same oscillator.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 18: Random pulses, counting cumulants, and shot noise

Lectures: [21]. Prerequisites: 1, 6, 16.
Estimated pages: 16.

Purpose and running case: Separate information about pulse shape from information about event timing in a detector's noise spectrum.

Coverage: Poisson pulse sequences, Campbell cumulants, Carson spectrum, rectangular pulses, Barkhausen example, integrated dichotomous process bridge.

### 18.1 Poisson pulses and mean level

Purpose: establish R18-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For stationary Poisson arrivals on the real time axis of intensity lambda, independent identically distributed amplitudes A, and an integrable pulse shape h, the signal sum A_j*h(t-T_j) has mean lambda*E[A] times the integral of h when the required integrability conditions hold.
Uses: R01-3, R06-3, R16-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Calculate the mean for finite-width rectangular pulses and compare with a padded stationary simulation.
Limit and proof hinge to expose: Starting arrivals at time zero produces a transient; it is not the stationary construction.
Transition: Covariance and cumulants.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 18.2 Covariance and cumulants

Purpose: establish R18-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: Under square-integrable h and finite amplitude second moment, the centered covariance is lambda*E[A squared] times the integral of h(s)*h(s+tau) ds. At one time, the kth cumulant is lambda*E[A raised to k] times the integral of h raised to k when finite.
Uses: R18-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover triangular covariance for rectangular pulses and verify the second cumulant equals the variance.
Limit and proof hinge to expose: Use amplitude raw moments in these formulas, not amplitude cumulants; correlated arrivals change the result.
Transition: Pulse spectra and persistent motion.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 18.3 Pulse spectra and persistent motion

Purpose: establish R18-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: The centered shot-noise spectrum is lambda*E[A squared]*absolute(H(omega)) squared for pulse transform H. A nonzero mean contributes a separate delta at zero frequency to the uncentered spectrum. Integrating a two-state velocity process creates a continuous position process with memory in its velocity.
Uses: R18-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the rectangular-pulse spectral zeros and connect two-state velocity correlation to the next chapter's displacement variance.
Limit and proof hinge to expose: A finite-record zero-frequency bin is not a literal Dirac delta; distinguish centered and uncentered estimates.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 18 computational and assessment sections

Laboratory: Simulate stationary shot noise with burn-in and boundary padding; compare mean, covariance, and spectral envelope.
Figure teaching job: A pulse train and the pulse-shape envelope of its centered power spectrum.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 19: Persistent walks and finite-speed diffusion

Lectures: [22]. Prerequisites: 6, 10, 18.
Estimated pages: 16.

Purpose and running case: Construct transport with finite propagation speed and determine when ordinary diffusion becomes accurate.

Coverage: Poisson covariance, persistent lattice walk, dichotomous diffusion equations, initial data, exact law, MSD, diffusion limit.

### 19.1 Velocity as the missing state variable

Purpose: establish R19-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For velocity plus or minus v with symmetric switching rate nu, the two position densities satisfy coupled advection-switching equations. Their sum rho satisfies partial_tt rho+2*nu*partial_t rho=v squared*partial_xx rho, with two initial conditions inherited from the initial position and velocity law.
Uses: R06-3, R10-3, R18-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover the no-switching wave limit and verify conservation of total probability.
Limit and proof hinge to expose: The second-order equation alone does not specify initial velocity bias; position is not a Markov state by itself.
Transition: Atoms at the propagation fronts.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 19.2 Atoms at the propagation fronts

Purpose: establish R19-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: Starting at the origin with equally likely initial velocities, the position law has atoms of mass exp(-nu*t)/2 at each of plus and minus v*t, in addition to a continuous interior component for positive time.
Uses: R19-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Identify the zero-switch event probability and check that interior probability plus both atoms sums to one.
Limit and proof hinge to expose: A histogram or smooth density formula that omits the atoms is incomplete at finite time.
Transition: The ballistic-to-diffusive crossover.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 19.3 The ballistic-to-diffusive crossover

Purpose: establish R19-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: The displacement mean square for symmetric stationary initial velocity is (v squared/nu)*(t-(1-exp(-2*nu*t))/(2*nu)). At long time the effective diffusion coefficient is v squared/(2*nu); at short time the mean square is v squared*t squared.
Uses: R19-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Integrate the velocity covariance and compare with the inertial Brownian crossover.
Limit and proof hinge to expose: A Gaussian diffusion limit describes the central scaling region and does not preserve finite-speed fronts.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 19 computational and assessment sections

Laboratory: Compare event-driven telegraph trajectories with the density's continuous part and ballistic front masses.
Figure teaching job: Finite-speed support, decaying ballistic atoms, and the long-time Gaussian core.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 20: First passage, absorbing boundaries, and renewal

Lectures: [23, 24]. Prerequisites: 6, 9, 12, 19.
Estimated pages: 24.

Purpose and running case: Choose between eventual arrival probability, typical arrival time, and mean arrival time for the same target.

Coverage: Telegraph crossings, first-passage density and moments, lattice backward equations, renewal transforms, random walk dimension and fractal introduction.

### 20.1 Arrival is a stopping event

Purpose: establish R20-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For one-dimensional Brownian diffusion of coefficient D starting distance a positive from an absorbing target on an otherwise unbounded line, the first-arrival density is a*exp(-a squared/(4*D*t))/sqrt(4*pi*D*t cubed) for t positive. Its total probability is one while its mean time diverges.
Uses: R06-3, R09-3, R12-3, R19-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive by reflection or image construction, integrate the density, and inspect its long-time first-moment integral.
Limit and proof hinge to expose: A finite simulation cutoff can produce a finite sample mean even when the mathematical mean is infinite.
Transition: The backward generator answers a different question.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 20.2 The backward generator answers a different question

Purpose: establish R20-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For Brownian diffusion in an interval (0,L) absorbed at both endpoints, the mean first-exit time solves D*T''=-1 with T(0)=T(L)=0 and equals x*(L-x)/(2*D). The probability of first exiting at L is x/L.
Uses: R20-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Solve both boundary-value problems and compare with a finite-state absorbing-chain calculation.
Limit and proof hinge to expose: Changing either boundary to reflecting changes the problem; forward and backward operators act on different arguments.
Transition: Renewal and Laplace transforms.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 20.3 Renewal and Laplace transforms

Purpose: establish R20-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a time-homogeneous Markov process with a regenerative first-arrival decomposition at the target and appropriate transition density or mass, the target propagator is the time convolution of first-arrival law with the target-to-target propagator. Laplace transforms turn this convolution into a product.
Uses: R20-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the Brownian first-arrival transform exp(-a*sqrt(s/D)) and a discrete lattice generating-function counterpart.
Limit and proof hinge to expose: Point targets in higher-dimensional continuous space and non-Markov observations need separate hitting and renewal assumptions; fractal scaling is not Euclidean by default.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 20 computational and assessment sections

Laboratory: Compare exact absorbing-interval results with numerical backward equations; demonstrate bias from discrete-time missed crossings.
Figure teaching job: A heavy first-passage tail beside finite-interval survival and the effect of absorbing versus reflecting boundaries.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 21: Return laws, recurrence, and fractal transport

Lectures: [25]. Prerequisites: 3, 6, 20.
Estimated pages: 16.

Purpose and running case: Determine whether a walk returns almost surely even when its mean return time is infinite.

Coverage: Sierpinski walk dimension, first-passage/return generating functions, recurrence criterion, biased/unbiased line walks and divergent means.

### 21.1 A first return excludes time zero

Purpose: establish R21-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a discrete-time Markov chain started at state i, let u_n be the probability of being at i at step n with u_0=1 and f_n its first-return probability for n at least one. The renewal identity is u_n equal to the sum over k=1 through n of f_k*u_(n-k); hence U(z)=1/(1-F(z)) for absolute z less than one.
Uses: R03-3, R06-3, R20-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Verify the identity by exact path enumeration for a small finite chain.
Limit and proof hinge to expose: A return time starts after the initial visit; including time zero destroys the first-return definition.
Transition: Almost-sure return and infinite mean.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 21.2 Almost-sure return and infinite mean

Purpose: establish R21-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: The state is recurrent exactly when the sum of its return probabilities u_n diverges. For the unbiased nearest-neighbor walk on the integer line, return is almost sure but the mean positive return time is infinite. A biased walk with positive step probabilities p and 1-p has return probability 2*min(p,1-p).
Uses: R21-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Obtain the return generating function and check its limit as bias tends to zero.
Limit and proof hinge to expose: Recurrence does not imply a finite mean return time or a normalizable invariant law on an infinite lattice.
Transition: Geometry changes the walk scale.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 21.3 Geometry changes the walk scale

Purpose: establish R21-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: On a finite absorbing graph with transient transition submatrix K_TT in the book's column convention, expected exit times satisfy (identity-K_TT transpose)*T=ones. Scaling these solutions across graph sizes defines a numerical walk-dimension estimate rather than a theorem by itself.
Uses: R21-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover quadratic exit-time scaling on a line; derive or obtain a page-verified renormalization argument before stating an exact gasket walk exponent.
Limit and proof hinge to expose: Separate graph distance, embedding distance, finite-size fit, and exact asymptotic walk dimension.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 21 computational and assessment sections

Laboratory: Compute first-return probabilities by absorbing-chain methods and explore transport scaling on finite gasket approximations.
Figure teaching job: First-return tails for biased and unbiased line walks; a separately labelled finite gasket scaling example.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 22: Recurrence by dimension and random walk clocks

Lectures: [26]. Prerequisites: 3, 6, 20, 21.
Estimated pages: 16.

Purpose and running case: Separate the geometry of a lattice walk from the clock that determines its physical-time progress.

Coverage: Return on d-dimensional lattices, recurrence/transience threshold, continuous-time walks, exponential and nonexponential waiting times.

### 22.1 The return-probability criterion in dimension d

Purpose: establish R22-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: The symmetric nearest-neighbor walk on the integer d-dimensional lattice is recurrent for d=1 or d=2 and transient for d at least 3. The local return probability on its allowed even times decays proportionally to n raised to -d/2 at large n.
Uses: R03-3, R06-3, R20-3, R21-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive the small-wave-number Green-function divergence and check parity against exact low-step counts.
Limit and proof hinge to expose: A continuum Gaussian density at a point is not itself a lattice return probability; the allowed-time lattice normalization matters.
Transition: A random number of jumps.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 22.2 A random number of jumps

Purpose: establish R22-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For independent identically distributed jumps and independent identically distributed positive waiting times, the position at time t is the sum of the first N(t) jumps, where N(t) is the renewal count. Exponential waiting times give a memoryless clock and a continuous-time Markov walk.
Uses: R22-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover Poisson jump counts for exponential waiting and compare equal-rate discrete and continuous time laws.
Limit and proof hinge to expose: Spatial jump recurrence and elapsed-time return moments are different questions.
Transition: Age restores information about the clock.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 22.3 Age restores information about the clock

Purpose: establish R22-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a waiting density psi with survival function Psi positive at age a, the conditional instantaneous event rate is psi(a)/Psi(a). This hazard is constant for an exponential law; for a general waiting law the position alone omits the elapsed waiting age needed to determine future jump timing.
Uses: R22-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Derive residual waiting survival as Psi(a+t)/Psi(a) and compare several ages.
Limit and proof hinge to expose: A non-Markov position process can often be embedded in a larger Markov state containing age, but existence and boundary details must be specified.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### Chapter 22 computational and assessment sections

Laboratory: Estimate lattice return Green functions with parity handled correctly; attach exponential and heavy-tailed clocks to identical spatial jumps.
Figure teaching job: One spatial jump path with different renewal clocks, alongside dimension-dependent return probabilities.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 23: Renewal memory and anomalous diffusion

Lectures: [27]. Prerequisites: 1, 3, 20, 22.
Estimated pages: 16.

Purpose and running case: Diagnose subdiffusion without interpreting a biased walk's mean-square displacement as its centered variance.

Coverage: Biased continuous-time random walks, Fourier-Laplace solution, mean/variance asymptotics, non-Markovian and subdiffusive criteria.

### 23.1 The Fourier-Laplace renewal solution

Purpose: establish R23-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a decoupled continuous-time walk started at a renewal at the origin, jump characteristic function phi(k), and waiting-time Laplace transform psi_tilde(s), its position transform is (1-psi_tilde(s))/(s*(1-psi_tilde(s)*phi(k))) for positive s, under the usual nonexplosive renewal construction.
Uses: R01-3, R03-3, R20-3, R22-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Recover the Markov compound-Poisson transform for exponential waits.
Limit and proof hinge to expose: Aged initial conditions and coupled jump/wait laws change this formula.
Transition: Mean and variance from a random sum.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 23.2 Mean and variance from a random sum

Purpose: establish R23-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For independent jumps with finite mean mu_J and variance sigma_J squared, independent of the renewal clock, mean position is mu_J*E[N(t)] and centered position variance is sigma_J squared*E[N(t)]+mu_J squared*Var(N(t)).
Uses: R23-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Use total expectation and total variance; verify the Poisson-clock limit.
Limit and proof hinge to expose: Uncentered mean-square displacement also contains the squared mean; bias changes scaling conclusions.
Transition: An infinite-mean waiting scale.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 23.3 An infinite-mean waiting scale

Purpose: establish R23-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: If the waiting transform obeys 1-psi_tilde(s) asymptotic to (tau0*s)^alpha for alpha in (0,1), standard renewal Tauberian hypotheses yield E[N(t)] asymptotic to (t/tau0)^alpha/Gamma(1+alpha). For zero-mean finite-variance independent jumps this gives centered displacement variance asymptotic to sigma_J squared times that expression.
Uses: R23-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: State the Tauberian conditions and compare ensemble scaling with finite-horizon simulations using uncertainty estimates.
Limit and proof hinge to expose: A power-law fit over a short window does not establish an asymptotic exponent or ergodicity; biased clocks add a separate renewal-count variance term.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: cite_pending_page_verification.

### Chapter 23 computational and assessment sections

Laboratory: Compare ensemble displacement, centered variance, and time averages under exponential and infinite-mean clocks.
Figure teaching job: Distinct mean, centered variance, and uncentered mean-square displacement for heavy-tailed clocks with and without drift.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 24: Deterministic maps, invariant measures, and coarse observations

Lectures: [28]. Prerequisites: 2, 5, 21.
Estimated pages: 16.

Purpose and running case: Explain how deterministic evolution can produce probabilistic observations without replacing the dynamics by an arbitrary random model.

Coverage: Flows and maps, coarse graining, invariant measure, Frobenius-Perron evolution, ergodicity, escape/return definitions, Poincare statement.

### 24.1 Pushforward probability

Purpose: establish R24-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: A measurable map T transports a probability measure mu to a measure assigning each measurable set A the value mu(T inverse of A). An invariant measure satisfies mu(T inverse of A)=mu(A) for every measurable A.
Uses: R02-3, R05-3, R21-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Use the doubling map modulo one to verify invariance of uniform measure on intervals.
Limit and proof hinge to expose: An invariant density depends on the reference measure and need not exist for every invariant measure.
Transition: The transfer operator counts preimages.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 24.2 The transfer operator counts preimages

Purpose: establish R24-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a piecewise smooth map with regular inverse branches and nonzero branch derivatives, density transfer at y is the sum of input density at each inverse point divided by the absolute map derivative. For the doubling map it is one half of rho(y/2)+rho((y+1)/2).
Uses: R24-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Verify mass conservation and transfer a nonuniform density through repeated iterations.
Limit and proof hinge to expose: Coarse-grained cells need not form an exact Markov chain; finite-precision periodicity is a numerical artifact to examine explicitly.
Transition: Ergodicity and recurrence are separate.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 24.3 Ergodicity and recurrence are separate

Purpose: establish R24-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a measure-preserving map on a probability space, ergodicity means every invariant measurable set has measure zero or one. Under the ergodic theorem, time averages of integrable observables equal their invariant-measure mean almost everywhere when the map is ergodic.
Uses: R24-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Compare a map with disconnected invariant components with the doubling map; distinguish the theorem from finite-time convergence evidence.
Limit and proof hinge to expose: Measure preservation alone yields recurrence in finite measure but does not imply ergodicity or mixing.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: cite_pending_page_verification.

### Chapter 24 computational and assessment sections

Laboratory: Evolve densities under the doubling map and compare exact symbolic cylinders with finite-precision orbit experiments.
Figure teaching job: Map preimages, density transfer, and the distinction between an orbit and an ensemble.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.

## Chapter 25: Sojourn, escape, and recurrence in deterministic dynamics

Lectures: [29]. Prerequisites: 20, 21, 24.
Estimated pages: 16.

Purpose and running case: Choose the correct entrance-conditioned statistic when measuring residence and return times from a coarse-grained orbit.

Coverage: Sojourn and escape distributions, recurrence differences, Poincare proof, Smoluchowski modification, Bernoulli shift example.

### 25.1 Sampling residence intervals

Purpose: establish R25-1 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For an independent binary occupancy sequence with occupied probability q in (0,1), the occupied-run length observed at an entrance has probability (1-q)*q raised to (n-1) for positive n. An interval sampled at an arbitrary occupied time is length-biased relative to the entrance-sampled interval.
Uses: R20-3, R21-3, R24-3.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Enumerate short binary words and compare entrance-sampled lengths with occupancy-sampled total run lengths.
Limit and proof hinge to expose: Define discrete endpoints before differencing sojourn probabilities; memoryless residual lengths do not eliminate length bias of total intervals.
Transition: Finite-measure recurrence.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 25.2 Finite-measure recurrence

Purpose: establish R25-2 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For a measure-preserving transformation on a finite-measure space and a measurable set A, almost every point of A returns to A infinitely often. This requires neither independent visits nor ergodicity.
Uses: R25-1.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Prove recurrence using disjoint escaping sets and finite measure, handling the null set of exceptional points.
Limit and proof hinge to expose: The theorem does not bound return time and fails without its finite invariant measure hypothesis.
Transition: Mean returns and correlated observations.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: derive_or_prove_here_under_stated_hypotheses.

### 25.3 Mean returns and correlated observations

Purpose: establish R25-3 for the running case.
Question: under which hypotheses does this result hold, and what changes when they fail?
Exact result: For an ergodic measure-preserving transformation on a probability space and A of positive measure, the conditional mean positive return time to A is 1/mu(A), under the standard Kac return-time theorem. Independent Bernoulli visits provide a geometric example; overlapping symbolic cylinders generally produce correlated visits.
Uses: R25-2.
Defines: all new objects named in the exact result, with the domains and units in `notation.md`; definitions appear locally before use.
Check: Verify the geometric mean by summation, then enumerate an overlapping cylinder to expose failure of an independence-based recurrence formula.
Limit and proof hinge to expose: Kac's formula needs its precise measure-theoretic conditions; any Smoluchowski or finite-difference sojourn formula must be verified against the lecture's endpoint and conditioning conventions before drafting.
Transition: compute the running case, diagnose its limits, and solve the exercises.
Recording interval: verify during sequential caption reading; not assigned from metadata.
Status plan: cite_pending_page_verification.

### Chapter 25 computational and assessment sections

Laboratory: Enumerate symbolic cylinders and compare residence, first-return, and arbitrary-time residual residence laws.
Figure teaching job: A binary occupancy record with entrance, exit, return, and residual intervals separately marked.
Exercises: two conceptual/counterexample, two derivational, two computational/design; fully worked solutions.
Source note: verified recording intervals, primary-source pages, lecture/extension/example distinctions, and visual coverage limits.
