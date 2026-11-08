# Notation contract — approved plan, with pilot definitions

Every symbol also receives a local definition before first use. Generic dummy
indices are local. Rates are nonnegative, times are nonnegative unless a
stationary process is defined on the full real axis, and logarithms are natural.
Symbols in the prose-form result statements have the meanings below; “squared”
and “raised to” are converted to typeset notation during section drafting.

## Chapter 1 local definitions

The pilot explicitly uses X for a random count and n for a realized value; N is
the fixed number of Bernoulli opportunities. The generic X row below remains a
book convention rather than a globally identical physical coordinate. Chapter
1's G_X(z) is the probability-generating function; q=1-p is failure probability;
rho_gas is number density (not probability density rho); epsilon=hbar*omega is
photon energy; beta=1/(k_B*T) has inverse-energy units; q_T=exp(-beta*epsilon).
The local alpha is a coherent-state amplitude and is unrelated to later stable
and waiting-tail indices. D_c is a signed count, distinct from diffusion D.
The positive shape r is a literal component count only for integer equal-mode
constructions. Lambda is a random Poisson mean in the gamma mixture, whereas
lambda_plus/minus are deterministic mean counts. Mathcal M_X and Mathcal K_X
are moment/cumulant-generating functions; kappa_k is a cumulant. These scalar
functions are distinct from the book's transition matrix K. eta is constant
detection efficiency. Coefficients a_c,b_c are arbitrary real scaling constants,
not the later SDE coefficients a,b. All counts and generating arguments are
dimensionless in this chapter. Each of these objects is defined locally before
the equation using it; this table does not replace the local definition.

| Symbol | Meaning | Domain and units | First chapter | Scope |
|---|---|---|---|---|
| X, X(t), X_t | scalar random variable or position coordinate, as locally declared | real; model units, position m | 1 | book convention |
| n, j, k | count or summation index; k is Fourier variable only in a transform context | integer or real as locally declared | 1 | local |
| p | Bernoulli success probability; p_n population probability | [0,1]; dimensionless | 1 | book, subscripts distinguish |
| z | probability-generating-function argument | complex, convergence region stated | 1 | book |
| lambda | Poisson rate or count mean; distinction and units stated locally | positive; s^-1 for a rate | 1 | chapter; lambda*t is a mean |
| lambda_plus, lambda_minus | means of independent Poisson count variables | nonnegative; dimensionless | 1 | chapter 1 |
| mu | distribution mean | real; same units as random variable | 1 | book |
| r | negative-binomial number of independent geometric summands | positive integer in the construction | 1 | chapter 1 |
| sigma, sigma_X, sigma_V | standard deviation of named variable | positive; variable units | 2 | book |
| rho | continuous probability density | inverse state-space volume | 2 | book |
| phi(k) | characteristic function | complex; k inverse variable units | 2 | book |
| m | particle mass | positive; kg | 2 | book |
| T | absolute temperature; T(x) explicitly means mean exit time in chapter 20 | positive; K or s | 2, 20 | explicit chapter-local overload |
| k_B | Boltzmann constant | J/K; no numerical value assumed | 2 | book |
| d | number of spatial coordinates | positive integer | 2 | book |
| t, s, tau | observation time, earlier time/integration variable, lag | s; Laplace s explicitly has s^-1 | 3 | transform context declared |
| ell | lattice spacing | positive; m | 3 | book |
| delta_t, h | time step; h(t) is pulse shape only in chapter 18 | positive; s or pulse units | 3, 18 | chapter-local |
| D | scalar spatial diffusion coefficient | nonnegative; m^2/s | 3 | book |
| alpha | stable index or waiting-law tail index, with its range restated | (0,2] or (0,1) | 4, 23 | chapter-local |
| c | scale coefficient in symmetric stable characteristic exponent | positive; units fix c*abs(k)^alpha dimensionless | 4 | chapter 4 |
| s_C | Cauchy scale; written s only in chapter 4 prose-form plan | positive; variable units | 4 | chapter 4 |
| K_ij | one-step probability from state j to state i | dimensionless; columns sum to one | 5 | book |
| pi | stationary probability column; pi in 2*pi denotes the circle constant | nonnegative, unit sum | 5 | typography distinguishes |
| Q_ij | continuous-time transition rate from j to i, off diagonal | s^-1; columns sum to zero | 6 | book |
| a | two-state magnitude in chapter 6; a(x,t) is drift in chapter 9; target distance in chapter 20 | locally defined | 6, 9, 20 | explicit chapter-local overload |
| nu | symmetric switching rate | positive; s^-1 | 6 | book |
| r_plus, r_minus | independent forward/backward jump rates | nonnegative; s^-1 | 6 | book |
| lambda_n, delta_n | population-state birth/death rates | nonnegative; s^-1, delta_0=0 | 7 | book |
| E_n | energy of population/height state n | J | 8 | book |
| a(x,t), b(x,t) | Itô drift and noise amplitude | state/s, state/sqrt(s) | 9 | book |
| W, B | standard Wiener processes; B need not be the same realization as W | sqrt(s) | 9 | book |
| U(x) | confining potential energy | J | 9 | book |
| M | overdamped force mobility | m/(N*s) | 9 | book |
| theta | energy scale k_B*T in chapter 2; thermal velocity variance k_B*T/m in chapters 10–11, explicitly redeclared | J or m^2/s^2 | 2, 10 | chapter-local scale; units stated at use |
| C_cond(t), Sigma(t) | conditional covariance matrix of a specified state vector | product of coordinate units entry by entry | 10 | chapter-local covariance; Q remains the rate generator |
| V, v, v0 | velocity random variable, value, initial value | m/s | 10 | book |
| gamma | velocity relaxation rate; dimensional drag is m*gamma | positive; s^-1 | 10 | book |
| C_v(tau), C(tau) | centered stationary autocovariance | squared variable units | 10 | book |
| omega0 | undamped harmonic angular frequency | positive; rad/s | 11 | book |
| g(x,t) | smooth coordinate transformation | output units locally declared | 13 | local |
| R, Z | radial distance and its square | m, m^2 | 13 | chapter 13 |
| S, a_S, b_S | positive multiplicative process, its drift rate and noise scale | S units, s^-1, s^-1/2 | 13 | chapter 13 |
| u | threshold level | same units as signal | 14 | chapter 14 |
| omega_c | cyclotron frequency magnitude | nonnegative; rad/s | 15 | book |
| omega | angular frequency | rad/s | 16 | book |
| S_x(omega), S_in | centered spectral density or matrix | squared variable units times s | 16 | book |
| H(omega) | transfer function or matrix; pulse transform in chapter 18 | input/output units stated | 16, 18 | chapter-local |
| R_e | electrical resistance; plan writes R in resistor formula | positive; ohm | 16 | chapter 16 |
| chi_x(omega) | displacement response to conjugate force | m/N | 17 | book |
| A_j | independent pulse amplitude | signal units for dimensionless pulse shape | 18 | chapter 18 |
| v_c | telegraph speed; plan writes v in chapter 19 | positive; m/s | 19 | chapter 19 |
| L | absorbing interval length | positive; m | 20 | chapter 20 |
| T(x) | conditional mean first exit time, never temperature within this chapter | nonnegative, possibly infinite; s | 20 | chapter 20 |
| u_n, f_n, U(z), F(z) | return probabilities, first-return probabilities, their generating functions | dimensionless | 21 | chapters 21–22 |
| K_TT | transient-state transition submatrix | dimensionless; column convention | 21 | local |
| N(t) | renewal count | nonnegative integer | 22 | book |
| psi, Psi | waiting density and survival function | s^-1, dimensionless | 22 | book |
| psi_tilde(s) | waiting-density Laplace transform | dimensionless; s has s^-1 | 23 | book |
| mu_J, sigma_J | spatial-jump mean and standard deviation | m | 23 | book |
| tau0 | waiting-law scale | positive; s | 23 | book |
| Gamma | Euler gamma function, not relaxation rate gamma | dimensionless argument | 2 | book |
| T_map | measurable deterministic map; written T only in chapters 24–25 | space to itself | 24 | chapter-local |
| mu_inv | invariant measure; written mu only in chapters 24–25 | normalized probability or stated finite measure | 24 | chapter-local |
| A | measurable target set; unrelated to pulse amplitudes | measurable subset | 24 | chapters 24–25 |
| q | occupied probability in a binary symbolic process | (0,1) | 25 | chapter 25 |

Scoping decisions: density is always rho, the rate matrix is Q, the stochastic
transition matrix is K, and covariance uses C. The prose-form planning records
use ordinary text for formulas; the author must replace the chapter-local
shorthands above with consistent typesetting when drafting. Do not silently
reuse S for a multiplicative process and its spectrum within one chapter.
