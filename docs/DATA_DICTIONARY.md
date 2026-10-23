# Data dictionary and handoffs

| Variable | Type | Meaning |
| --- | --- | --- |
| `cell_id` | str | Identifier of analysis-grid cell |
| `x`, `y` | float | Planar grid-cell centre (metres; real dataset EPSG:32718) |
| `registered_point_cell` | int {0,1} | 1 if at least one prior recorded point occupies the cell, 0 if unlabelled (not a verified absence) |
| `background_status` | str | Indicates unlabeled/record status or synthetic nature where supplied |
| `altitud_m` | float | Elevation proxy (metres) |
| `pendiente_grados` | float | Slope proxy (degrees) |
| `dist_acequia_m_aprox` | float | Approximate mapped canal distance (metres) |
| `dist_rio_m_aprox` | float | Approximate mapped river distance (metres) |
| `oof_rank_score` | float | Out-of-fold ranking score from Notebook 1 (not calibrated probability) |
| `node_id` | str | Identifier of candidate node N01... |
| `source`, `target` | str | Selected candidate pair (undirected edge) |
| `scenario` | str | Named cost-surface scenario |
| `physical_length_m` | float | Physical distance along modeled minimum-cost route |
| `accumulated_model_cost` | float | Numerical Dijkstra cost, with within-scenario meaning |

**Files:** Notebook 1 privately exports `nb1_oof_scores_PRIVATE.csv` when enabled. Notebook 2 takes that plus `canete_250m_PRIVATE.csv`; it can privately export `nb2_nodes_PRIVATE.csv`, `nb2_edges_PRIVATE.csv`, and optionally `nb2_route_cells_PRIVATE.csv`. Notebook 3 needs only the node and edge tables. The offline private delivery already includes all five inputs/outputs, so each notebook can run without exporting anything in Colab.

The demo run is entirely fictional. For real-data workflows, private Colab uploads are not public GitHub publication but still involve transferring data to a cloud computing service; use only where permitted by your data agreements.
