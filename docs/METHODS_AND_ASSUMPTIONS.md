# Methodological contract

## Step 1 — predictive ranking

**Observations:** previously recorded archaeological points aggregated to 250 m cells in the 12,826-cell candidate support. A point may share a cell with another point. The target is `registered_point_cell=1` versus `unlabelled=0`, **not presence vs confirmed absence**. Predictors: elevation, slope, approximate distance to rivers and irrigation lines. No coordinates or distance-to-site features are used as predictors. GroupKFold on 3 km spatial blocks produces out-of-fold rankings. Spatial blocking mitigates, but does not eliminate, spatial leakage or survey bias.

**Limitation:** out-of-fold scores are discriminative ranking proxies, not calibrated chances of undiscovered archaeology. The exact historical and coverage sources require separate rights/quality review.

## Step 2 — connectivity and movement

Take up to twelve unlabelled high-ranked cells, at least 3 km apart (greedy rule). Add undirected pairs to each candidate's two nearest selected neighbors, then remove duplicates. This *fixes the endpoint topology*. It is a workshop pairing heuristic, **not** a historically inferred interaction network.

On an 8-neighbor 250 m grid, a diagonal move is legal only when the two adjacent orthogonal cells exist; the move length is 250 m or 250√2 m. For each traversable cell i, define cost `c_i=1+w_s*S_i+w_r*R_i` with nonnegative slope and distance-to-present-river penalties clipped/normalized to the 95th percentile. Grid edge `(i,j)` receives weight `step_length * (c_i+c_j)/2`. Dijkstra minimizes the sum of edge costs. The illustration uses scenarios `(w_s,w_r)=(2.0,0.4)` and `(0.6,2.0)`. Neither is calibrated to historic routes. Modern rivers and irrigation geometry may not represent archaeological-period hydrology.

The original Cañete corridor study used separate unsupervised attractors and a more complex pipeline. Those attractors are **not** the supervised score-selected candidate nodes of this workshop.

## Step 3 — analyze two spatial graphs

Each selected candidate becomes a graph node. Each fixed nearest-neighbor pair becomes an undirected edge; its attribute `length_m` is physical length of the modeled minimum-cost grid path. Different scenarios can produce different spatial routes and lengths, **but identical unweighted topology** by construction. Compare weighted shortest-path lengths and betweenness by route length. As an optional independent exercise, prune edges above a specified route-length/Euclidean-distance ratio; that explicitly changes topology by adding another heuristic.

## What the exercise cannot establish

It does **not** demonstrate that any selected candidate is a site, that any inferred edge is an ancient road, that model accuracy equals archaeological discovery performance, or that weighted betweenness measures historical significance. Actual validation requires independent, permissioned field or route evidence.
