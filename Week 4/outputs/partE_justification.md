# Week 4 - Part E: Justification of the e-commerce review figure
*CDB601220 Data Visualization. All data are synthetic course data (Superior University Lahore), not findings about a real business.*

## 1. Per panel: the question, the chart type, the Week 2 channel rule
Panel 1 - 'Where is traffic really heading?' A line over time: time on the x axis and sessions on a common aligned scale, i.e. position, the most accurate channel (position > length > angle > area). Raw daily totals stay in grey for context; the 7-day rolling mean is the single coloured pop-out, so the eye finds the trajectory, not the weekend rhythm.

Panel 2 - 'When in the week do people visit?' A day-of-week x hour heatmap: two categorical axes give position, magnitude goes to colour lightness. Colour is a weaker channel than position, so it is used for the pattern (where is the dark band?), not for exact values. One-hue sequential colormap because there is no midpoint (Week 3).

Panel 3 - 'Where is the mass?' A treemap: containment shows category -> sub-category and area (the 4th-best channel, read to about +/-20%) shows size, so every block carries its value in text. One hue per parent category and only 4 parents respect the 4 +/- 1 chunk limit.

Panel 4 - 'By how much?' The same eight numbers as sorted horizontal bars: position on a common scale, values printed, rank readable top to bottom. Panels 3 and 4 answer different questions about the same data: where the mass is, and by how much.

## 2. Every time decision, named and defended
Parse. The file mixes 9,019 ISO timestamps and 3,651 slash timestamps. Each is parsed with its own explicit format. The slash format is day-first: its first field reaches 31 while its second never exceeds 12, so month-first is impossible. format='mixed' parses every row without an error but moves 1,382 rows to a wrong date and stretches the span from 528 to 704 days. I checked min and max, not just the row count: 2024-04-01 to 2025-09-11.

Resolution and aggregation. Hourly rows are resampled to daily with sum, because sessions are a flow (visits that began during the hour); a flow is never resampled with last(). The axis says 'Sessions per day (sum of hourly)'. Gaps were counted on the hourly index before resampling, and sum(min_count=24) makes an incomplete day NaN rather than a silent short total or a zero.

Window. 7 days, centred, requiring at least 5 of 7 days present. It cancels the weekly cycle exactly (Part B.1: removes 31.7% of raw variation, loses 3 days at each end; 28 days would cost 14, 91 days 45). Centred, not trailing, because this is a retrospective Monday review: a centred mean puts turns on the right date, while a trailing mean would report them about half a window (3 days) late. A live dashboard would need the trailing version and a caption saying so.

Ethics clause. The window was fixed at 7 days before plotting, because the cycle being removed is weekly (Part B.1). The series is shown from its first recorded day (1 April 2024); no start date was selected. A 28-day version is in the appendix and does not change the direction (the 7- and 28-day lines correlate 0.96). Part B.5 shows why this matters: on the same series 34 of 60 start-and-window combinations rise and 26 fall. Symmetry test: I would have kept the same 7-day window if it had weakened my conclusion, because the weekly cycle, not the picture, sets it.

## 3. Every row removed (rule, count, what moved)
| Item | Rule | Count | What moved |
|---|---|---|---|
| Duplicate hours | keep first row per timestamp; every pair verified value-identical | 286 rows (12,670 -> 12,384) | total sessions -2.36% |
| Sentinel sessions = -1 | set to NaN; daily totals refilled with same weekday-hour median, flagged | 0 rows removed; 287 hours refilled | adds 2.33% to daily total; excluded from heatmap |
| Days never recorded | left as gaps (NaN), never zero-filled | 0 rows; 13 days / 312 hours absent | line breaks at 13 places |
| Partial month (2025-09) | kept, shaded and labelled partial; never compared as a total | 0 rows; 11 of 30 days | excluded from monthly-median statements |
| Duplicate SKU (SKU-0127) | keep the copy whose sku_name prefix matches its sub-category | 1 row (345 -> 344) | Wearables share 10.13% -> 9.35%; Audio 14.86% -> 14.99% |
| Negative net revenue | never drawn as area; netted inside sub-category totals and reported | 0 rows; 7 SKUs, -1.07m in total | all 8 sub-category totals stay positive |
## 4. Every level rolled up
No 'Other' bucket was needed: 0 categories folded, value 0m, because the smallest sub-category (Drones) is still 2.4% of the total. The depth was cut at sub-category: 344 SKUs were summed into 8 sub-categories (total net revenue 1,711.4m), because 344 blocks would be unreadable. Tree checks passed: every sub-category has exactly one parent and the children sum to their parents. Self-check against shares_eight.csv: every sub-category share is within 0.3 percentage points. In Panel 2, 168 weekday-hour cells are shown unrolled.
