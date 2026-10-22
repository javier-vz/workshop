# Ancient routing networks in the Andes: computations for NetSciX 2027

This repository reproduces the Chachapoyas results and the network measures in the extended abstract *Topological Optimization and Predictive Modeling of Ancient Routing Networks: A Comparative Spatial Analysis in the Andes*. The abstract is by D. S. Cornejo Meza and J. M. Vera Zúñiga and was submitted to NetSciX 2027.

The repository freezes version 0.20.0 (7 October 2026) of `camino`, the least-cost-path package written for the Leimebamba–Chachapoyas project. It adds three scripts written for the abstract.

## What it reproduces

| In the abstract | Values | Step |
| --- | --- | --- |
| Cost ratio of each registered segment against its least-cost path (Fig. 1B, Table 1) | 1.03–1.22 in five of six segments; 1.39 in Pauja–Santa Cruz | `python -m camino revisar` |
| Null model: 500 control routes per segment | p = 0.002 in five segments; p = 0.73 in Pauja–Santa Cruz | `python nulo_en_dos_partes.py` |
| The national Qhapaq Ñan registry as a network | 917 components; 17% of the 9,591 observed km lie in corridors of ≥100 km; within them, the betweenness ranking holds when gaps of up to 2 km are closed (Spearman ρ ≥ 0.70) | `python -m camino red` |
| The two networks of Fig. 1 as spatial graphs | Chachapoyas registry: 273 km in 22 components, no cycles (α = 0). Cañete corridor model: one component, α = 0.44, no bridges | `canete_paths.py`, then `red_regional.py` |

## Repository layout

```
camino/                    camino 0.20.0 (2026-10-07), frozen
config.yaml                study configuration used in the abstract
environment.yml            conda environment
nulo_en_dos_partes.py      null model split into two parallel processes
canete_paths.py            regenerates the Cañete corridor paths
red_regional.py            measures the two networks of Fig. 1
resultados_de_referencia/  outputs of the reference run, for comparison
datos/                     input data (not versioned, see below)
derivados/, resultados/    filled by the steps (not versioned)
```

The code comments and console messages are in Spanish.

## Study area and grid

- **Bounding box:** 78.05°W to 77.549°W, 6.8°S to 5.869°S.
- **Grid:** 30-m cells in UTM 18S (EPSG:32718), 6,438,705 cells (about 5,800 km²). The box was chosen so that every registered segment with at least 8 km of continuous road fits entirely inside it.

The six segments add up to 169 km and use only the observed sections of the registry:
- Chachapoyas – Jumbilla
- Leymebamba – Chilchos – Mendoza
- La Jalca – Mendoza
- Pauja – Santa Cruz
- Chachapoyas – Cochamal
- Chillo – Chachapoyas

## Requirements

Install [conda](https://docs.conda.io), then run:

```
conda env create -f environment.yml
conda activate camino
```

Tested on Windows 11 and Linux.

## Input data

The input files are not versioned, following the same policy as the development project. Put them in `datos/`:

| File | Content | How to get it |
| --- | --- | --- |
| `cop30_raw.tif` | Copernicus DEM GLO-30 | `python -m camino bajar`, through OpenTopography |
| `aw3d30_raw.tif` | ALOS World 3D 30 m (JAXA) | same step |
| `agua_osm.json` | water bodies from OpenStreetMap | same step |
| `qhapaq_nan.kmz` | Qhapaq Ñan registry of the Ministry of Culture of Peru, as distributed by [GEO GPS Perú](https://www.geogpsperu.com/2020/10/mapa-del-qhapaq-nan-camino-inca.html) | manual download |
| `qn_geocam.gpkg` | the registry clipped to the study box | `python -m camino ruta`, with the KMZ already in `datos/` |

`bajar` needs an OpenTopography API key. Set it in the `OPENTOPOGRAPHY_API_KEY` environment variable, never in `config.yaml`.

The reference run used files downloaded on 5 October 2026. OpenStreetMap and the registry change over time, so newer downloads can differ, and the results with them. Check your files against these SHA-256 hashes:

```
9a6a15bfa357c00dd5292ab3ded2cdb4ad2f9250dc2f8f8a3f86e22ec5e31bcc  cop30_raw.tif
7842c9413c89fe84f1a536651c4048987342bf210925e105a949235c4cf4faa3  aw3d30_raw.tif
6ec7366e6af34604dfa80067bf194c39c9d1943bb5ca0b3de795b028c3ddb30c  agua_osm.json
741f833af70f29f19bb2a88126421af18cc5239d3d1d8ffd3aab1088d98a3b33  qhapaq_nan.kmz
36363b902b089e2206b0a6f141e7f156ac70ff772081d643bac67b6ffc2e3b0f  qn_geocam.gpkg
```

## Running

Run the commands from the repository folder, with the environment active:

```
python -m camino preparar                                 # align the DEMs, corridor mask
python -m camino superficies                              # slope and roughness
python -m camino grafo                                    # 16-neighbour transit graph
python -m camino revisar                                  # least-cost paths and cost ratios
python nulo_en_dos_partes.py                              # null model, 500 control routes per segment
python -m camino red > resultados/red_nacional.txt        # the national registry as a network
git clone https://github.com/javier-vz/canete-corridor-model ../canete-corridor-model
python canete_paths.py ../canete-corridor-model           # Cañete corridor paths
python red_regional.py                                    # the two networks of Fig. 1
```

On a laptop, the first four steps take a few minutes in total. The null model takes 30–60 minutes, `red` about 5 minutes, and the last two steps about 3 minutes.

### About the null model script

`nulo_en_dos_partes.py` runs `camino`'s own null model, but splits it into two parallel processes of three segments each. Each process uses its own seed, derived from the one in `config.yaml` with `numpy.random.SeedSequence([seed, ord(part)])`. With the same inputs it reproduces the reference run exactly.

To check the setup first, `python nulo_en_dos_partes.py --m 5` takes a couple of minutes.

`python -m camino nulos` runs the same null model in a single process, with different random draws. It takes about twice as long and reaches the same conclusion.

### Steps you should not run

Do not run `python -m camino todo`, `barrido` or `validar` here. They need the catalog of ceremonial spaces described below.

## Reference results

`resultados_de_referencia/` holds the outputs of the reference run. The run was reproduced on Windows 11 and Linux with identical least-cost paths, cost ratios, p-values and network measures.

| Segment | Cost ratio | Control routes (p25 / median / p75) | p |
| --- | --- | --- | --- |
| Chillo – Chachapoyas | 1.03 | 1.55 / 1.73 / 2.18 | 0.002 |
| La Jalca – Mendoza | 1.07 | 1.49 / 1.62 / 1.77 | 0.002 |
| Leymebamba – Chilchos – Mendoza | 1.09 | 1.52 / 1.67 / 1.84 | 0.002 |
| Chachapoyas – Cochamal | 1.17 | 1.66 / 1.96 / 2.33 | 0.002 |
| Chachapoyas – Jumbilla | 1.22 | 1.72 / 1.87 / 2.05 | 0.002 |
| Pauja – Santa Cruz | 1.39 | 1.17 / 1.28 / 1.40 | 0.73 |

| Network | km | Components | Cycles | α | km in bridges |
| --- | --- | --- | --- | --- | --- |
| Chachapoyas registry, no gaps closed | 273 | 22 | 0 | 0.00 | 100% |
| Chachapoyas registry, gaps of up to 2 km closed | 267 | 8 | 1 | 0.02 | 98% |
| Cañete corridor model, 4 routes per pair | 617 | 1 | 624 | 0.44 | 0% |
| Cañete corridor model, best route per pair | 539 | 1 | 469 | 0.42 | 0% |

The two networks are of different kinds: the Cañete network is simulated by a model, while the Chachapoyas network is the registered road. A registry-to-registry comparison is not possible, because the Cañete province has only 23.5 km of observed registry.

## Method in brief

- **Cost.** The edge cost is the metabolic cost of walking as a function of slope (Minetti et al. 2002), computed on a 16-neighbour graph over Copernicus GLO-30. Slopes beyond ±45% are impassable, and terrain roughness (VRM, 99th percentile) acts as a barrier.
- **Cost ratio.** The cost of following the registered route, divided by the cost of the least-cost path between the same two ends.
- **Null model.** For each segment, 500 least-cost routes are traced on Gaussian random surfaces that share the spectral exponent of the real terrain (β = 2.52). Each route is then costed on the real terrain. p is the fraction of control routes that cost as little as the registered route or less, computed as (k + 1)/(M + 1). With 500 routes, its floor is 0.002.
- **Network measures.** Nodes are junctions and loose ends, and edges are the chains between them (`camino.red.construir`). The measures are:
  - the Garrison–Marble α index (meshedness: 0 for a tree, 1 for a full mesh)
  - the share of kilometres in bridges
  - edge betweenness within corridors of ≥100 km, and how stable its ranking stays (Spearman ρ) as registry gaps of up to 2 km are closed

## Not included

- **Inverse optimization of the cost weights** (`barrido`, `validar`). It needs a catalog of ceremonial spaces, filtered by archaeological criteria: sites that were identified because of the road must be left out. It has not been run.
- **The Cañete Random Forest model** (ROC-AUC 0.68–0.71), which comes from D. S. Cornejo Meza's work.
- **The scripts that draw Figure 1.**

## Versions

`camino` 0.20.0 corrects the 16-neighbour graph of 0.15.0: knight moves can no longer cross a cliff in a single step. The development repository's report of 6 October 2026 was made with 0.15.0, so its numbers differ (cost ratios 1.03–1.25, and 1.45 in Pauja–Santa Cruz).

Later versions of `camino` (0.22 and up) add a 35° slope mask and are configured for a different set of units, so they do not reproduce these numbers. Development continues in [javier-vz/leimebamba](https://github.com/javier-vz/leimebamba).

The Cañete corridor paths come from [canete-corridor-model](https://github.com/javier-vz/canete-corridor-model), commit `576993c` (17 September 2026). They use its canonical configuration: eps = 0.15, kappa = 0.03, seed 42.

## Sensitive data

The repository contains no coordinates of archaeological sites. The Cañete network uses only the 250-m aggregated site flags that canete-corridor-model already publishes. Field data from Chachapoyas are not used.

## References

- D. S. Cornejo Meza and J. M. Vera Zúñiga. Topological optimization and predictive modeling of ancient routing networks: a comparative spatial analysis in the Andes. Extended abstract submitted to NetSciX 2027.
- D. S. Cornejo Meza and J. M. Vera Zúñiga. An unsupervised corridor-based model for archaeological prospection in the Lower Cañete Valley, Peru. Submitted to *Journal of Computer Applications in Archaeology*, 2026.
- A. E. Minetti, C. Moia, G. S. Roi, D. Susta and G. Ferretti. Energy cost of walking and running at extreme uphill and downhill slopes. *Journal of Applied Physiology* 93(3):1039–1046, 2002.
