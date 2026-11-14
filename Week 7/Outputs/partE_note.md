# Task E - the note

**Message (one sentence).** The Authority's "punctuality is improving" is a mix effect (every mode got worse: the +1.73-pt headline = -1.10 within modes + +2.82 mix), and the next corridor should be argued from boardings *per resident*, not boardings.
**Reader.** The Secretary (30 seconds, top-left only) first; the finance director and the journalist second.

## Parameters, each with a reason
- **Window:** 2025 Q2 vs 2026 Q2, the latest complete quarters a year apart (the reversal also holds for first-3/last-3 and first-6/last-6 months); partial 2026-09 is never compared.
- **Unit:** departures for punctuality, boardings (legs) for map and trend, journeys only for fares; never added or on one axis (boardings / journeys = 1.30).
- **Aggregation:** sum on-time and operated, *then* divide (a mean of daily % weights a quiet Sunday like a busy Tuesday); unfiled days break lines, never zeros.
- **Denominator:** resident population from the register, in words on the legend ("per 1,000 residents").
- **Breaks:** Jenks natural breaks, k=5, edges printed; equal breaks would put one outlier in its own class.
- **Projection:** equal-area, because colouring an area makes area the encoding.

## The counterfactual
A count map of boardings is a population map: r(boardings, population) = **+0.945**, against **+0.249** for the rate. Raw counts send the corridor to **D17, D09, D13** (11.0M, 6.9M, 6.3M residents); the rate points at **D12, D21, D09**. Only **D09** (Ilyaspur) is on both lists, and *why* is the finding: it is the network hub - 17 of 36 routes serve it (tied for most) and it has the most stops - so it is large *and* intense. The count version takes the corridor away from **D12 Lashkar (1.4M) and D21 Ushkan (1.1M)**, the two small districts with the highest boardings per resident, and gives it to D17 Qilabad and D13 Mehrabad. The five most populous districts hold 59.9% of the people on 12.6% of the land, which is all a count map can see.

## Ethics clause
**Suppressed or merged: none (0 of 24).** My rule would have been to suppress a rate whose Poisson funnel interval contains the pooled rate; the funnel is only +/-0.07% wide (smallest district count 2,391,101 boardings) and **24 of 24** districts lie outside it, so noise is not what separates them - structure is. Three districts (D05, D15, D23) were filed in thousands and are *repaired*, not suppressed; the route table agrees with the repaired register to within 690 boardings. **What I would not claim:** a high rate is not "well served". Boardings are credited to where a route runs, so a hub is credited with non-residents' trips, and the rate tracks stop density almost exactly (r = +0.98). Siting infrastructure from this screen should add access (stops, income, concession share), not only rank use; the data are synthetic and the district names carry no real-world meaning.
