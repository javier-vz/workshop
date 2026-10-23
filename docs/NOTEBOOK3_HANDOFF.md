# Notebook 3 input handoff

The default demo is fully stand-alone and embeds synthetic candidate-node and edge tables **regenerated from Notebook 2 v1.0 demo mode**. The same tables are in `data/sample/` for auditing. To use restricted Cañete-derived data, choose `DATA_MODE="real"` and privately upload `nb2_nodes_PRIVATE.csv` and `nb2_edges_PRIVATE.csv` from the offline package. Notebook 3 does not require the detailed route geometry file. An authorized fresh Notebook 2 run can generate the same handoff schema by setting `EXPORT_RESULTS=True` and keeping the files private.

All unweighted topological measures are invariant between cost scenarios because node pairs were fixed. Route-length-weighted betweenness and weighted distances may change; detour-threshold edge filtering is a **separate** operation which can change topology.
