# From Incomplete Spatial Data to Networks

**A hands-on tutorial in predictive modeling and routing · NetSciX 2027**  
**Javier M. Vera Zúñiga** (UTP) · **Dina S. Cornejo Meza** (PUCP)

Three independent Google Colab notebooks demonstrate how to go from **incomplete spatial observations → candidate locations → least-cost corridors → network analysis**. The case-study methodology was developed with reference to archaeological research in the Cañete Valley, Peru. **Public demo data are fictional; real archaeology-derived data are not published here.**

## Start here: open in Google Colab

| Order | Notebook | What you learn | Open after publication |
| --- | --- | --- | --- |
| 1 | [Spatial prediction](notebooks/01_spatial_prediction.ipynb) | Random Forest; spatial folds; ranking vs unlabelled background | [Open in Colab](https://colab.research.google.com/github/javier-vz/netscix2027-spatial-networks/blob/main/notebooks/01_spatial_prediction.ipynb) |
| 2 | [Network construction](notebooks/02_network_construction.ipynb) | Select candidates; build grid cost surfaces and LCP corridors | [Open in Colab](https://colab.research.google.com/github/javier-vz/netscix2027-spatial-networks/blob/main/notebooks/02_network_construction.ipynb) |
| 3 | [Network analysis](notebooks/03_network_analysis.ipynb) | Connectivity, degree, betweenness and sensitivity | [Open in Colab](https://colab.research.google.com/github/javier-vz/netscix2027-spatial-networks/blob/main/notebooks/03_network_analysis.ipynb) |

The Colab links work **after you publish this repository** under that name. Before publishing, in Colab choose **File → Upload notebook** and select the `.ipynb` from your computer.

### Run modes

- **`DATA_MODE="demo"` (default):** each notebook runs independently, with embedded/generated synthetic inputs. No uploads, account keys or prior execution are needed (apart from Colab access).
- **`DATA_MODE="real"` (restricted):** use the **separately delivered private ZIP** on an approved computing environment. Notebook 1 uses `canete_250m_PRIVATE.csv`; Notebook 2 uses this file plus `nb1_oof_scores_PRIVATE.csv`; Notebook 3 uses `nb2_nodes_PRIVATE.csv` and `nb2_edges_PRIVATE.csv`. These are provided in the offline private package; the notebooks also support controlled generation and export of intermediate CSVs. **Never upload that private package to GitHub.**

Running demo mode in each notebook is intentionally self-contained. In demo mode Notebook 2 *reproduces the ranking algorithm* from Notebook 1 on the same synthetic grid; Notebook 3 embeds the synthetic output of Notebook 2. The public `data/sample` folder preserves synthetic NB2 outputs for independent inspection.

## Research logic and limits

1. **Spatial ranking:** classify *previously recorded points in a cell* vs *unlabelled cells* with four environmental predictors, comparing predictive discrimination under grouped spatial folds. Labels 0 represent **unknown status**, not verified site absences. Scores are **not calibrated site-presence probabilities**.
2. **Candidate connections:** select at most 12 high-ranked unlabelled cells separated by 3 km and pair each with its 2 nearest candidate neighbors (undirected, deduplicated). This rule is heuristic.
3. **LCP routes:** on a 250 m 8-neighbor grid, compute two alternative scenario-specific least-cost paths via Dijkstra. Compare routes and physical lengths under different slope and distance-to-modern-river penalties.
4. **Networks:** make candidate-node graphs from those pairs. With fixed pairs, degree, connectivity, and *unweighted* betweenness do **not** vary between cost scenarios. Length-weighted betweenness can vary; an explicitly separate detour-filtering rule can alter topology.

**Archaeological interpretation:** Candidate nodes are not confirmed sites or the unsupervised attractors from the original Cañete corridor model. Modeled routes are not documented ancient roads. Independent field validation, historical hydrology checks and source/permission audits are needed for archaeological conclusions. The candidate common domain of 12,826 250 m cells (~801.625 km²) still requires scientific boundary review. See [Methods and assumptions](docs/METHODS_AND_ASSUMPTIONS.md).

## Workshop structure (three hours)

20 min introduction · 45 min Notebook 1 · 10 min break · 45 min Notebook 2 · 40 min Notebook 3 · 20 min discussion. See [Facilitator guide](docs/FACILITATOR_GUIDE.md).

## Repository map

- `notebooks/`: three notebooks, ready for default public demo Colab sessions.
- `data/sample/`: fictional synthetic outputs for inspection.
- `docs/`: methods, data dictionary, ethics, scientific limits and teaching guide.
- `scripts/smoke_test.py`: local automatic code checks (demo runs and fixture consistency).
- `requirements.txt`: libraries for normal notebook operation.

## Credits and licenses

Joint development: Javier M. Vera Zúñiga and Dina S. Cornejo Meza. See [CITATION.cff](CITATION.cff). Code is MIT-licensed (`LICENSE`); fictional teaching tables in `data/sample` are CC0. **These permissions do not cover any unpublished or rights-restricted real archaeological dataset.**
