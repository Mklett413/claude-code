---
description: Transcribe and format a handwritten butcher cut sheet into a clean digital record
argument-hint: Customer name and cut data (or describe/paste the sheet)
---

# Cut Sheet Typist

You are processing a beef cut sheet for a butcher shop. Your goal is to produce a clean, accurate digital record from handwritten or dictated data.

## Input

$ARGUMENTS

If no arguments are provided, ask the user to:
1. Describe or paste the cut sheet data (customer name, date, animal number, list of cuts and weights)
2. Or provide a file path to a photo/scan

## Steps

1. Parse all cut names and weights from the input
2. Identify the customer, animal ID, and processing date
3. Note any special packaging (sausage links, breakfast sausage, 2# ground beef packages, etc.)
4. Launch the **cut-sheet-typist** agent to format the data
5. Write the output to `cut-sheets/[customer]-[animal]-[date].md`
6. Confirm the file was created and display the formatted sheet

## Quality check

Before saving, verify:
- All cut weights are plausible (single cuts rarely exceed 30 lbs)
- The customer name and date are present
- Ground beef / chili grind package totals are included if provided
- Any uncertain readings are flagged with `*`
