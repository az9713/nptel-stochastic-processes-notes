"""Joint-law counterexamples and finite Markov-chain checks (column convention)."""
from pathlib import Path
import itertools
import json

import numpy as np
from scipy.linalg import expm


def main():
    kernel = np.array([[.6, .2, .1], [.3, .5, .2], [.1, .3, .7]])
    system = kernel-np.eye(3)
    system[-1] = 1
    stationary = np.linalg.solve(system, [0, 0, 1])
    assert np.allclose(kernel.sum(axis=0), 1)
    assert np.allclose(kernel @ stationary, stationary)
    enumeration = np.zeros((3, 3))
    for initial, intermediate, final in itertools.product(range(3), repeat=3):
        enumeration[final, initial] += kernel[final, intermediate]*kernel[intermediate, initial]
    assert np.allclose(enumeration, kernel @ kernel)
    convergence = []
    for steps in (0, 1, 5, 20):
        law = np.linalg.matrix_power(kernel, steps) @ np.array([1, 0, 0])
        convergence.append({"steps": steps, "law": law.tolist(),
                            "total_variation": float(.5*abs(law-stationary).sum())})
    # Deterministic phase cycle with observed values 0,0,1,1.
    observed = np.array([0, 0, 1, 1])
    transitions = np.zeros((2, 2))
    second = np.zeros((2, 2))
    for phase in range(4):
        transitions[observed[(phase+1) % 4], observed[phase]] += .5
        second[observed[(phase+2) % 4], observed[phase]] += .5
    assert np.allclose(transitions, .5)
    assert np.allclose(second, [[0, 1], [1, 0]])
    generator = np.array([[-2, 1], [2, -1]])
    propagator = expm(generator*.7)
    assert np.allclose(propagator.sum(axis=0), 1)
    assert np.all(propagator >= 0)
    assert np.allclose(expm(generator*.3) @ expm(generator*.4), propagator)
    result = {"kernel": kernel.tolist(), "stationary": stationary.tolist(),
              "convergence": convergence, "two_step_enumeration": enumeration.tolist(),
              "hidden_cycle_one_step": transitions.tolist(),
              "hidden_cycle_two_step": second.tolist(),
              "continuous_generator": generator.tolist(),
              "continuous_eigenvalues": np.linalg.eigvals(generator).tolist(),
              "propagator_at_0_7": propagator.tolist()}
    directory = Path(__file__).resolve().parent
    (directory / "ch05-results.json").write_text(json.dumps(result, indent=2)+"\n")
    lines = ["Three-state stationary law: "+", ".join(f"{x:.9f}" for x in stationary)]
    for row in convergence:
        lines.append(f"n={row['steps']}: distance={row['total_variation']:.9f}")
    lines.append("Hidden cycle: one-step probability of staying = 0.5; two-step = 0.")
    report = "\n".join(lines)+"\n"
    (directory / "ch05-output.txt").write_text(report)
    print(report, end="")


if __name__ == "__main__":
    main()
