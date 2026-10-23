# NetSciX 2027 — facilitator guide (180 minutes)

**Learning question:** How can we construct and critically evaluate hypothetical spatial networks from incomplete geographic observations?

| Elapsed time | Live component | Participant action | Fallback |
| --- | --- | --- | --- |
| 00:00–00:20 | Research question & source limitations | Identify what is observed vs unlabelled; inspect the pipeline | Present static workflow in README |
| 00:20–01:05 | Notebook 1 · spatial ranking | Run demo; discuss spatial folds, AP and baselines | Use executed demo screenshots locally, not real maps |
| 01:05–01:15 | Break | — | — |
| 01:15–02:00 | Notebook 2 · routing | Change a cost weight, compare LCP lengths and overlaps | Use bundled synthetic NB2 edge/route fixtures |
| 02:00–02:40 | Notebook 3 · graph analysis | Compare weighted betweenness; vary detour ratio | Use embedded synthetic NB3 inputs |
| 02:40–03:00 | Discussion | Identify an inferential limitation and a possible independent validation source | Written prompts |

**Before the event:** test GitHub notebook links in a signed-out browser, run demo mode on a fresh Google Colab session, test internet access and packages, and check accessibility. For private Cañete analysis, use only authorization-compliant restricted accounts or local execution. Never show or distribute sensitive derived maps publicly without permission.

**Suggested participant work:**
1. Notebook 1: record difference between AP and recorded-background rate, change block size and reflect on leakage.
2. Notebook 2: compare slope-dominant and river-distance-dominant paths; record the fraction of shared route cells.
3. Notebook 3: confirm invariant degree and unweighted betweenness, then test a detour threshold and explain why the graph changes.

**Exit question:** Which patterns follow from the environment, and which follow from our node-pairing and cost assumptions?
