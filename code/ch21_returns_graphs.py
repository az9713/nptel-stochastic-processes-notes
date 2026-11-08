"""Renewal probabilities and exact finite-gasket backward equations."""
from pathlib import Path
import json

import numpy as np
from scipy.special import gammaln
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

ROOT = Path(__file__).resolve().parents[1]


def gasket(generation):
    edges = {((0, 0), (1, 0)), ((0, 0), (0, 1)), ((0, 1), (1, 0))}
    side = 1
    for level in range(generation):
        new = set()
        for dx, dy in ((0, 0), (side, 0), (0, side)):
            for a, b in edges:
                new.add(tuple(sorted(((a[0]+dx, a[1]+dy),
                                      (b[0]+dx, b[1]+dy)))))
        edges = new
        side *= 2
    adjacency = {}
    for a, b in edges:
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)
    return adjacency, edges, side


graph_checks = []
for generation in range(7):
    graph, edges, side = gasket(generation)
    traps = {(side, 0), (0, side)}
    states = sorted(set(graph)-traps)
    index = {x: j for j, x in enumerate(states)}
    row, col, values = [], [], []
    for x, j in index.items():
        row.append(j)
        col.append(j)
        values.append(1.)
        for y in graph[x]-traps:
            row.append(j)
            col.append(index[y])
            values.append(-1/len(graph[x]))
    matrix = csr_matrix((values, (row, col)), shape=(len(states),)*2)
    times = spsolve(matrix, np.ones(len(states)))
    apex = float(times[index[(0, 0)]])
    assert abs(apex/5**generation-1) < 1e-10
    assert len(graph) == (3**(generation+1)+3)//2
    graph_checks.append({'generation': generation, 'side': side,
                         'vertices': len(graph), 'mean_exit_steps': apex})
m = np.arange(1, 10001)
log_choose = gammaln(2*m+1)-2*gammaln(m+1)
returns = []
for p in (.5, .6):
    first = np.exp(log_choose+m*np.log(p*(1-p)))/(2*m-1)
    u = np.r_[1., np.exp(log_choose[:100]+m[:100]*np.log(p*(1-p)))]
    for n in range(1, 101):
        assert abs(u[n]-sum(first[k-1]*u[n-k] for k in range(1, n+1))) < 1e-12
    returns.append({'p': p, 'exact_return_probability': 1-abs(2*p-1),
                    'partial_probability': float(first.sum()),
                    'partial_first_moment': float(np.dot(2*m, first)),
                    'first_return_even': first[:500].tolist()})
graph, edges, side = gasket(3)
result = {'gaskets': graph_checks, 'return_checks': returns,
          'walk_dimension': float(np.log(5)/np.log(2)),
          'fractal_dimension': float(np.log(3)/np.log(2)),
          'm_plot': m[:500].tolist(),
          'graph_edges': [[list(a), list(b)] for a, b in sorted(edges)]}
(ROOT/'code/ch21-results.json').write_text(json.dumps(result, indent=2)+'\n')
report = '\n'.join(f"side={g['side']}: vertices={g['vertices']}; "
                   f"mean exit={g['mean_exit_steps']:.6f} steps" for g in graph_checks)
report += f"\nwalk dimension={result['walk_dimension']:.8f}\n"
report += '\n'.join(f"p={r['p']}: return={r['exact_return_probability']:.6f}; "
                    f"partial mass={r['partial_probability']:.8f}; "
                    f"partial moment={r['partial_first_moment']:.6f}"
                    for r in returns)+'\n'
(ROOT/'code/ch21-output.txt').write_text(report)
print(report, end='')
