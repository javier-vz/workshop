"""Las rutas de la red de corredores de Canete (Fig. 1A), guardadas una por una.

Corre la configuracion canonica de canete-corridor-model (eps = 0.15,
kappa = 0.03, semilla 42) con la misma logica que `compute_traffic_field` en
scripts/regen_figures_with_scalebar.py, pero ademas guarda cada ruta. Las
necesita red_regional.py para armar la red de Canete como grafo.

Uso, con el entorno activado:

    python canete_paths.py RUTA_A_canete-corridor-model [SALIDA.pkl]

Ejemplo en Windows:

    python canete_paths.py C:\\Users\\jvera\\Documents\\canete-corridor-model

Por omision deja canete_paths.pkl en esta carpeta. Tarda unos 2 o 3 minutos.
"""
import pathlib
import pickle
import sys
import time
from copy import deepcopy

import networkx as nx
import numpy as np

if len(sys.argv) < 2:
    sys.exit(__doc__)

REPO = pathlib.Path(sys.argv[1]).resolve()
SALIDA = (pathlib.Path(sys.argv[2]) if len(sys.argv) > 2
          else pathlib.Path(__file__).resolve().parent / "canete_paths.pkl")
CSV = REPO / "data" / "grilla_con_W_hidrica.csv"
if not CSV.exists():
    sys.exit(f"No encuentro {CSV}. El primer argumento tiene que ser la carpeta del repositorio "
             "canete-corridor-model.")

sys.path.insert(0, str(REPO / "src"))
from ca_kernel import (apply_congestion_update, apply_perceptual_noise, build_state,  # noqa: E402
                       k_simple_paths_weighted, path_cost)

t0 = time.time()
state = build_state(str(CSV))
print(f"estado listo en {time.time() - t0:.0f} s: {len(state.attractors)} atractores, "
      f"{len(state.pair_candidates)} pares, {state.n_sites} celdas con sitio", flush=True)

eps, kappa, seed = 0.15, 0.03, 42
G = deepcopy(state.G_template)
rng = np.random.default_rng(seed)

recs = []
for a, b in state.pair_candidates:
    i1, j1 = state.attractors[a]
    i2, j2 = state.attractors[b]
    try:
        cmin = nx.shortest_path_length(G, source=(i1, j1), target=(i2, j2), weight="weight_base")
        wab = (np.exp(2.0 * state.E_grid[i1, j1]) * np.exp(2.0 * state.E_grid[i2, j2])
               * np.exp(-3.0 * cmin))
        recs.append((a, b, wab, cmin))
    except nx.NetworkXNoPath:
        continue
recs.sort(key=lambda r: r[2], reverse=True)

traffic = np.zeros_like(state.E_grid, dtype=float)
rutas = []
for a, b, wab, _ in recs:
    i1, j1 = state.attractors[a]
    i2, j2 = state.attractors[b]
    apply_perceptual_noise(G, eps, rng)
    paths = k_simple_paths_weighted(G, (i1, j1), (i2, j2), n_paths=4)
    if not paths:
        continue
    costs = np.array([path_cost(G, p) for p in paths], dtype=float)
    c0 = costs.min()
    boltz = np.exp(-1.5 * (costs - c0))
    boltz /= boltz.sum() + 1e-12
    pw = (np.exp(2.0 * state.E_grid[i1, j1]) * np.exp(2.0 * state.E_grid[i2, j2])
          * np.exp(-3.0 * c0))
    visitas = {}
    for path, pprob in zip(paths, boltz):
        wpath = pw * pprob
        rutas.append((list(path), float(wpath)))
        for i, j in path:
            traffic[i, j] += wpath
        for u, v in zip(path[:-1], path[1:]):
            clave = tuple(sorted([u, v]))
            visitas[clave] = visitas.get(clave, 0) + 1
    apply_congestion_update(G, visitas, kappa=kappa, cap=2.0)

lat = state.lattice
pickle.dump(dict(xs=list(lat["xs"]), ys=list(lat["ys"]), valid=state.valid_mask,
                 site=state.site_mask, attractors=list(state.attractors), paths=rutas,
                 traffic=traffic), open(SALIDA, "wb"))
print(f"{len(rutas)} rutas guardadas en {SALIDA} ({time.time() - t0:.0f} s)")
