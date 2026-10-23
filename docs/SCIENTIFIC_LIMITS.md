# Scientific and data-governance notes

1. Notebook 1’s target is recorded-point-cell versus unlabelled background; the negative class is **not** an observed absence. OOF rankings reflect incomplete survey and spatial block design.
2. The selection policy is explicitly heuristic and intended for teaching. Selecting unlabelled high-ranked cells does not validate them archaeologically; nor does minimum separation establish independently meaningful locations.
3. Paths minimize a defined numerical cost surface, not real historic travel costs. Modern river distance is only an environmental proxy and the two weight sets are illustrations; neither is fitted or validated from documented ancient paths.
4. The node-selection policy is held fixed across scenarios so changes reflect path costs rather than simultaneous node changes. The 250 m graph is a candidate support, not an archaeologically finalized domain.
5. Cost sensitivity here is descriptive. Quantitative reconstruction or discovery performance requires independent, permissioned evidence and scientific validation.
6. Never publish private 250 m grid location-label combinations, out-of-fold score maps, route endpoints/trajectories, or other outputs that may reveal sensitive archaeological information without rights-holder review.
7. Original `canete-corridor-model` employs separate unsupervised environmental attractors and route ensembles. **Do not identify those attractors with the supervised RF-derived candidate nodes used here.**

## Notebook 3 addition
- Node identities and endpoint-pair topology are *fixed across scenarios by design*. Any statement that degree or unweighted betweenness change in this comparison is false; the notebook checks invariance.
- Physical-route-length-weighted betweenness may vary due to different modeled paths. It does not measure historical social influence or archaeological importance.
- An optional detour-ratio pruning exercise changes graph topology only by adding an explicitly separate threshold rule.
