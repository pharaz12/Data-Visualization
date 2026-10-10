| Element | Marks | Load type | Why |
|---|---|---|---|
| Bars (height = total) | 51 | intrinsic | this IS the data: 51 numbers |
| Bar drop shadows | 51 | extraneous | decoration, encodes nothing |
| 51 different bar colours | - | extraneous | x position already says which state; colour repeats it (attribute of the bars, no extra marks counted) |
| State labels on x axis (rotated 90) | 51 | extraneous | needed information, but rotated and tiny so the reader must tilt their head and squint |
| x tick marks | 51 | extraneous | one per bar, adds nothing the labels don't |
| Vertical gridlines | 51 | extraneous | there is nothing to read off along x |
| Horizontal gridlines | 6 | germane | help turn bar height into a number, but far too heavy here |
| y tick labels | 6 | germane | let the reader decode the value |
| y tick marks | 6 | extraneous | gridlines already do this job |
| Box frame (4 spines) | 4 | extraneous | borders hold nothing |
| Legend swatches | 51 | extraneous | colour -> state lookup that x labels already provide |
| Legend text entries | 51 | extraneous | 51 items to hold in working memory |
| Legend title | 1 | extraneous |  |
| Chart title (names the axes) | 1 | extraneous | says what the axes already say |
| Axis labels (2) | 2 | germane | units / meaning for the reader (the y one is too terse: 'total') |

### Data-ink estimate (marks counted, not ink area)
- Marks that encode a number: the 51 bars (one number each).
- All marks: 51 bars + 51 shadows + 51 x labels + 51 x ticks + 51 x grid + 6 y grid + 6 y labels + 6 y ticks + 4 frame + 51 legend swatches + 51 legend text + 1 legend title + 1 title + 2 axis labels = 383.
- Data-ink ratio = 51 / 383 = **0.13**.
- If I also count the 6 y tick labels as 'encoding' (they let you decode the bars) it is 57 / 383 = 0.15. Either way most of the marks carry no data.
- This counts marks, not ink area, so the shadows, thick frame and heavy grid are underweighted. It is a rough estimate.