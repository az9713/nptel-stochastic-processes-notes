"""Exact count laws, independent checks, and reproducible sampling for chapter 1.

Run from any directory. Writes JSON and text beside this file. No network calls.
"""
from __future__ import annotations

import json
from math import comb, exp, factorial, sqrt
from pathlib import Path

import numpy as np
from scipy import special, stats

SEED = 20261108
SAMPLES = 200000
MEAN = 4.0


def thin_moments(mean, variance, efficiency):
    """Moments of independent binomial thinning at fixed efficiency."""
    if not 0 <= efficiency <= 1:
        raise ValueError('efficiency must lie in [0, 1]')
    if mean < 0 or variance < 0:
        raise ValueError('moments must be nonnegative')
    return (efficiency*mean,
            efficiency**2*variance + efficiency*(1-efficiency)*mean)


def total_variation(a, b):
    """Finite-grid contribution to total variation; caller controls tail mass."""
    return float(np.abs(np.asarray(a)-np.asarray(b)).sum()/2)


def main():
    rng = np.random.default_rng(SEED)
    n = np.arange(401)
    laws = [
        ('Binomial(20, 0.2)', stats.binom(20, .2), 3.2,
         lambda: rng.binomial(20, .2, SAMPLES)),
        ('Poisson(4)', stats.poisson(MEAN), 4.0,
         lambda: rng.poisson(MEAN, SAMPLES)),
        ('Geometric(mean 4)', stats.geom(1/5, loc=-1), 20.0,
         lambda: rng.geometric(1/5, SAMPLES)-1),
        ('Negative binomial(r=4, mean 4)', stats.nbinom(4, .5), 8.0,
         lambda: rng.negative_binomial(4, .5, SAMPLES)),
    ]
    output = {'seed': SEED, 'samples_per_law': SAMPLES, 'laws': []}
    lines = ['Equal mean = 4 counts; exact probabilities, not fitted data.']
    for name, law, variance, sampler in laws:
        mass = law.pmf(n)
        assert law.sf(n[-1]) < 1e-30
        assert np.isclose(mass.sum(), 1, atol=1e-12)
        assert np.isclose(n @ mass, MEAN, atol=1e-11)
        assert np.isclose((n-MEAN)**2 @ mass, variance, atol=1e-10)
        sample = sampler()
        sample_mean = float(sample.mean())
        sample_variance = float(sample.var(ddof=1))
        # A coarse six-standard-error check uses each law's exact fourth moment.
        excess_kurtosis = float(law.stats(moments='k'))
        fourth_central = (excess_kurtosis+3)*variance**2
        se_variance = sqrt((fourth_central-variance**2)/SAMPLES)
        assert abs(sample_mean-MEAN) < 6*sqrt(variance/SAMPLES)
        assert abs(sample_variance-variance) < 6*se_variance
        row = {'name': name, 'mean': MEAN, 'variance': variance,
               'fano': variance/MEAN, 'p_zero': float(law.pmf(0)),
               'p_at_least_10': float(law.sf(9)),
               'sample_mean': sample_mean, 'sample_variance': sample_variance,
               'sample_fano': sample_variance/sample_mean,
               'pmf_0_to_40': mass[:41].tolist(),
               'tail_above_40': float(law.sf(40))}
        output['laws'].append(row)
        lines.append(f"{name}: variance={variance:.6f}, F={row['fano']:.6f}, "
                     f"P0={row['p_zero']:.8f}, P(X>=10)={row['p_at_least_10']:.8f}")
        lines.append(f'  sampled mean={sample_mean:.6f}, '
                     f'variance={sample_variance:.6f}, '
                     f'F={row["sample_fano"]:.6f}')
    distances = []
    for trials in (20, 100, 1000, 10000):
        tv = total_variation(stats.binom.pmf(n, trials, MEAN/trials),
                             stats.poisson.pmf(n, MEAN))
        distances.append({'trials': trials, 'tv': tv})
        lines.append(f'Binomial -> Poisson: trials={trials}, TV={tv:.9f}')
    output['binomial_to_poisson'] = distances
    # An independent finite factorial sum checks the PMF used in the library.
    manual_binomial = [comb(20, k)*.2**k*.8**(20-k) for k in range(21)]
    assert np.allclose(manual_binomial, stats.binom.pmf(np.arange(21), 20, .2))
    assert np.isclose(exp(-MEAN)*MEAN**4/factorial(4), stats.poisson.pmf(4, MEAN))
    diff_grid = np.arange(-100, 101)
    plus, minus = 7.0, 3.0
    convolution_indices = np.arange(150)
    direct = np.array([
        np.sum(stats.poisson.pmf(convolution_indices+max(k, 0), plus)
               * stats.poisson.pmf(convolution_indices+max(-k, 0), minus))
        for k in diff_grid])
    library = stats.skellam.pmf(diff_grid, plus, minus)
    assert np.allclose(direct, library, atol=1e-14)
    assert np.isclose(direct.sum(), 1)
    assert np.isclose(diff_grid @ direct, 4)
    assert np.isclose((diff_grid-4)**2 @ direct, 10)
    assert np.isclose(exp(-10)*special.iv(0, 2*sqrt(21)), stats.skellam.pmf(0, 7, 3))
    output['skellam'] = {'mean': 4, 'variance': 10,
                          'p_zero': float(stats.skellam.pmf(0, 7, 3))}
    lines.append(f"Skellam(7, 3): mean=4, variance=10, P0={output['skellam']['p_zero']:.8f}")
    modes = []
    for count in (1, 2, 4, 20, 100):
        distribution = stats.nbinom(count, count/(count+MEAN))
        row = {'r': count, 'variance': MEAN+MEAN**2/count,
               'p_zero': float(distribution.pmf(0)),
               'tv_from_poisson': total_variation(distribution.pmf(n),
                                                  stats.poisson.pmf(n, MEAN))}
        modes.append(row)
        lines.append(f"Thermal modes r={count}: variance={row['variance']:.6f}, "
                     f"P0={row['p_zero']:.8f}, TV={row['tv_from_poisson']:.8f}")
    output['modes_fixed_total_mean'] = modes
    loss_rows = []
    for variance in (3.2, 4.0, 20.0, 8.0):
        mean_out, var_out = thin_moments(4, variance, .25)
        loss_rows.append({'input_variance': variance, 'mean': mean_out,
                          'variance': var_out, 'fano': var_out/mean_out})
    output['thinning_efficiency_0_25'] = loss_rows
    lines.append('At efficiency 0.25: ' + '; '.join(
        f"input variance {r['input_variance']:g} -> mean {r['mean']:g}, "
        f"variance {r['variance']:g}, F {r['fano']:g}" for r in loss_rows))
    # Exercise counterexample: independent Poisson(2) plus geometric(mean 2).
    mixture_zero = exp(-2)/3
    matched_nb_zero = stats.nbinom.pmf(0, 4, .5)
    output['same_mean_variance_counterexample'] = {
        'mean': 4, 'variance': 8, 'poisson_plus_geometric_p0': mixture_zero,
        'matched_negative_binomial_p0': float(matched_nb_zero)}
    lines.append(f'Equal mean/variance counterexample: P0={mixture_zero:.8f} '
                 f'versus {matched_nb_zero:.8f}')
    output['shared_poisson_counterexample'] = {
        'marginal_mean': 4, 'sum_mean': 8, 'sum_variance': 16,
        'difference_mean': 0, 'difference_variance': 0}
    lines.append('Shared Poisson X=Y: sum mean=8 variance=16; difference variance=0')
    two_point = np.array([0, 2])
    assert two_point.mean() == two_point.var() == 1
    nb_mass = stats.nbinom.pmf(n, 4, .5)
    third_cumulant = float((n-4)**3 @ nb_mass)
    assert np.isclose(third_cumulant, 24)
    for trials in (20, 100, 1000, 10000):
        assert stats.binom.sf(400, trials, 4/trials) < 1e-30
        expanded = np.arange(801)
        larger_tv = total_variation(
            stats.binom.pmf(expanded, trials, 4/trials),
            stats.poisson.pmf(expanded, 4))
        smaller_tv = next(r['tv'] for r in distances if r['trials'] == trials)
        assert np.isclose(larger_tv, smaller_tv, rtol=0, atol=1e-14)
    unequal = rng.geometric(.25, SAMPLES)+rng.geometric(.5, SAMPLES)-2
    unequal_row = {'mean': 4, 'variance': 14, 'p_zero': .125,
                   'effective_shape': 1.6, 'detected_fano': 1.625,
                   'sample_mean': float(unequal.mean()),
                   'sample_variance': float(unequal.var(ddof=1)),
                   'sample_p_zero': float(np.mean(unequal == 0))}
    assert abs(unequal_row['sample_mean']-4) < 6*sqrt(14/SAMPLES)
    kappa4_sum = sum(m*(1+m)*(1+6*m+6*m*m) for m in (3, 1))
    assert abs(unequal_row['sample_variance']-14) < 6*sqrt((kappa4_sum+2*14**2)/SAMPLES)
    assert abs(unequal_row['sample_p_zero']-.125) < 6*sqrt(.125*.875/SAMPLES)
    output['exercise_checks'] = {'negative_binomial_third_cumulant': third_cumulant,
                                  'unequal_modes': unequal_row,
                                  'expanded_grid_tv_unchanged': True,
                                  'two_point_nonpoisson_mean_and_variance': 1}
    lines.append(f'NB(4, mean 4) third cumulant={third_cumulant:.6f}')
    lines.append('Unequal thermal modes (3,1): exact mean=4 variance=14 '
                 'P0=0.125 effective shape=1.6 detected F=1.625')
    lines.append(f"  sampled mean={unequal_row['sample_mean']:.6f}, "
                 f"variance={unequal_row['sample_variance']:.6f}, "
                 f"P0={unequal_row['sample_p_zero']:.6f}")
    output['die_score'] = {'mean': 7, 'variance': 35/6,
                           'p_score_7': 1/6, 'p_score_3': 1/18}
    dice = np.array([a+b for a in range(1, 7) for b in range(1, 7)])
    assert dice.mean() == 7 and np.isclose(dice.var(), 35/6)
    assert np.mean(dice == 7) == 1/6 and np.mean(dice == 3) == 1/18
    lines.append(f'Dice: mean=7, variance={35/6:.8f}, P7={1/6:.8f}, P3={1/18:.8f}')
    lines.append('All exact-law and sampling checks passed.')
    target = Path(__file__).resolve().parent
    (target / 'ch01-results.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    (target / 'ch01-output.txt').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
