# Cut Sheet Agent

Transcribe and format handwritten butcher cut sheets into clean, structured digital records.

## What it does

The `/cut-sheet` command accepts raw cut sheet data — dictated, typed, or described from a photo — and produces a formatted Markdown file with a cut table, packaging notes, ground beef package breakdown, and totals.

## Usage

```
/cut-sheet Haldeman Cow 2, 4-30-26 — Chuck Eye 5.430, Flatiron 4.395 ...
```

Or run with no arguments and follow the prompts.

## Output

Saves to `cut-sheets/[customer]-[animal]-[date].md` in the current project directory.

## Included components

| Component | Purpose |
|-----------|---------|
| `/cut-sheet` command | Entry point — parses input and drives the workflow |
| `cut-sheet-typist` agent | Formats raw cut data into a clean Markdown table |
