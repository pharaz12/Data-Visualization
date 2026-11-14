# Task C — interaction contract

**View:** `partC_interactive.html` (Plotly; built by `partC_interactive.ipynb`) — Task B chart 1, daily boardings by mode. Static default: `partC_default.png`. No-install fallback: `LinkedBrush` demo, `partC_brush_demo.png`.

## The default state
Before anyone touches it the view says one sentence: **Metro boardings per day have nearly doubled since April 2025 while Bus has fallen by about two-fifths** — all four modes, the full period, with the partial month and Metro's 14-day gap already shaded.

## The controls
| Control | What it changes | What it does **not** change | Way back |
|---|---|---|---|
| Legend click / double-click | Which modes are *visible* (double-click isolates one) | The data, the smoothing, the unit, the shaded bands | Click again; double-click the legend again to show all; "Reset" button |
| Zoom by drag, or the range slider | The visible date window and the y-scale | The 7-day smoothing; the bands; the values | **"Reset: full period"** button, double-click on the plot, or the modebar home icon |
| Three range buttons (full / complete months / last 3 complete months) | The visible window only | Everything else | They *are* the reset: "Reset: full period" |
| Hover | Reads one date: value and how many of the 7 days in that window were actually filed | Nothing | — |

Always on, not controllable: the **partial September 2026** band, the **Metro 9-22 Feb** band, the unit "boardings (legs), not journeys", and a live warning line under the chart that names any of those two periods that the current window includes.

## The thing the control must not invite
**Two wrong conclusions were easy, and I dealt with both.**
1. *"Bus and Ferry collapsed in September / Metro fell to zero in February."* A date zoom onto either window makes a missing-data hole look like a crash. I did not make it impossible to zoom there — I made it impossible to misread: lines **break** (never drop to zero), the periods are shaded and labelled permanently, and the warning line under the chart says "partial month / missing data, not zero" whenever the window touches them.
2. *"Add up the filtered views."* A mode filter is safe in this chart — every row is one mode on one day, so the visible modes add up to the network (checked: no duplicated date-mode). It would **not** be safe on `routes.csv` by district: a route is credited to every district it serves, and summing the filtered district views gives **3.096×** the true total (28 of 36 routes serve more than one district). So the district view is not offered as a filter on the Plotly chart; in the `LinkedBrush` demo the sum and its multiple are printed *on the figure* beside the bars.
