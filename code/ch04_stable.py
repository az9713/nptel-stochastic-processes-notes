"""Quantile-based checks of stable averaging and Gaussian transformations."""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad
from scipy.special import erfc
from scipy.stats import cauchy, kstest, levy, norm


def main():
    rng = np.random.default_rng(202611084)
    repetitions = 20_000
    rows = []
    for n in (1, 4, 16, 64, 256):
        gaussian = rng.normal(size=(repetitions, n)).mean(axis=1)
        heavy = rng.standard_cauchy(size=(repetitions, n)).mean(axis=1)
        gaussian_iqr = float(np.diff(np.quantile(gaussian, [.25, .75]))[0])
        cauchy_iqr = float(np.diff(np.quantile(heavy, [.25, .75]))[0])
        expected = float(2*norm.ppf(.75)/np.sqrt(n))
        rows.append({"n": n, "gaussian_iqr": gaussian_iqr,
                     "gaussian_exact_iqr": expected, "cauchy_iqr": cauchy_iqr,
                     "cauchy_exact_iqr": 2.0})
        assert abs(gaussian_iqr/expected-1) < .08
        assert abs(cauchy_iqr-2) < .2
    first = 2*rng.normal(size=200_000)
    second = rng.normal(size=200_000)
    ratio = first/second
    ratio_ks = float(kstest(ratio, cauchy(scale=2).cdf).statistic)
    assert ratio_ks < .01
    reciprocal = 1/rng.normal(size=200_000)**2
    levy_ks = float(kstest(reciprocal, levy.cdf).statistic)
    assert levy_ks < .01
    laplace = []
    for s in (.1, 1, 5):
        numerical = quad(lambda z: np.sqrt(2/np.pi)*np.exp(-z*z/2-s/(z*z)),
                         0, np.inf)[0]
        exact = float(np.exp(-np.sqrt(2*s)))
        assert abs(numerical-exact) < 1e-9
        laplace.append({"s": s, "numerical": numerical, "exact": exact})
    result = {"seed": 202611084, "repetitions": repetitions, "mean_iqr_rows": rows,
              "ratio_scale2_ks": ratio_ks, "reciprocal_square_levy_ks": levy_ks,
              "levy_laplace": laplace,
              "levy_cdf_at_1": float(erfc(1/np.sqrt(2))),
              "cauchy_absolute_tail_over10": float(2*cauchy.sf(10)),
              "cauchy_mean_absolute_tail_over10_for_any_n": float(2*cauchy.sf(10))}
    directory = Path(__file__).resolve().parent
    (directory / "ch04-results.json").write_text(json.dumps(result, indent=2)+"\n")
    lines = ["Repeated sample-mean IQRs (Gaussian exact shrinks; Cauchy exact = 2):"]
    for row in rows:
        lines.append("n={n}: Gaussian={gaussian_iqr:.6f} "
                     "(exact {gaussian_exact_iqr:.6f}), Cauchy={cauchy_iqr:.6f}".format(**row))
    lines.append(f"Gaussian ratio, scale2 KS: {ratio_ks:.6f}")
    lines.append(f"Reciprocal Gaussian square, Levy KS: {levy_ks:.6f}")
    report = "\n".join(lines)+"\n"
    (directory / "ch04-output.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
