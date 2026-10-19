# Functional Design Questions — U2 playground-ui

Answer each question by replacing the `[Answer]:` line with the letter of your choice (or `X` and your own words).

### Q1: Empty result panels when the shared list is empty

When the shared list is empty, FR6.1 requires the warning and no sorting. Should the three result columns still show headings, or be hidden entirely?

A. Hide the three columns; show only the warning
B. Show the three column headings with a "no result" hint under each
X. Other (please specify)

[Answer]: A

### Q2: Order of typed entries and picked words

When the user types entries and also picks words from the bundled list, how should the shared list be ordered?

A. Typed entries first, then picked words (in the order picked)
B. Picked words first, then typed entries
C. Combined and de-duplicated before sorting
X. Other (please specify)

[Answer]: C

### Q3: Presentation of the metrics

How should each algorithm's comparisons and swaps be shown next to its sorted list?

A. Two plain lines under each column heading: "Comparisons: N" and "Swaps: N"
B. A small table below the three columns with one row per algorithm
X. Other (please specify)

[Answer]: A

### Q4: Accuracy result display

How should the accuracy check result appear for each algorithm?

A. A plain text line: "Accuracy: pass" or "Accuracy: fail"
B. A check mark or cross followed by the word "pass" or "fail"
X. Other (please specify)

[Answer]: A
