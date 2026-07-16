# EVM Forecasting Tool

A Python command-line tool that automates **Earned Value Management (EVM)** calculations — the same cost and schedule performance metrics used in professional project management (PMI/PMP frameworks) — replacing manual spreadsheet tracking with instant, repeatable calculations.

## The Problem

Project managers routinely need to answer questions like:
- Are we over or under budget, right now?
- Are we ahead or behind schedule?
- If current trends continue, what will this project actually cost by the end?

Answering these by hand in a spreadsheet is slow and error-prone, especially across multiple reporting periods. This tool automates the entire calculation and produces a visual report in seconds.

## What It Does

Given project data (either a CSV file or live user input), the tool calculates:

- **PV (Planned Value)** — the value of work that *should* be done by now
- **EV (Earned Value)** — the value of work *actually* done
- **AC (Actual Cost)** — money *actually* spent
- **CPI (Cost Performance Index)** — cost efficiency (`EV / AC`); above 1 = under budget, below 1 = over budget
- **SPI (Schedule Performance Index)** — schedule efficiency (`EV / PV`); above 1 = ahead of schedule, below 1 = behind
- **EAC (Estimate at Completion)** — forecasted final project cost based on current performance

It then exports a line chart (PV vs EV vs AC over time) as a PDF report.

## Project Versions

| File | Description |
|---|---|
| `evm_basic.py` | Reads project data from a CSV file (`data/sample_evm.csv`) |
| `evm_interactive.py` | Prompts the user directly in the terminal for each period's data, with input validation |
| `evm_multi_project.py` | Ingests a single CSV containing **multiple projects** (`data/multi_project.csv`), automatically calculates CPI/SPI/EAC for each one, flags at-risk projects, and exports a color-coded Excel dashboard |

## How to Run It

**Requirements:** Python 3.10+, pandas, matplotlib
```
pip install pandas matplotlib
```

**CSV-driven version:**
```
python evm_basic.py
```

**Interactive version:**
```
python evm_interactive.py
```
You'll be asked how many reporting periods you have, then prompted for budgeted cost, % planned complete, % actually complete, and actual cost spent — for each period.

**Multi-project portfolio dashboard:**
```
python evm_multi_project.py
```
Point it at a CSV containing multiple projects (each row tagged with a `project_id`), and it will calculate CPI/SPI/EAC for every project, sort them worst-performing first, and generate:
- `portfolio_summary.csv` — the raw summary data
- `portfolio_summary.xlsx` — a formatted Excel report with red/green health-status shading

## Example Output

```
--- Latest Period Health Check ---
CPI: 0.93  -> Over budget
SPI: 0.85  -> Behind schedule
Forecasted Final Cost (EAC): $107,058.82
```

A PDF chart (`evm_report.pdf` or `evm_interactive_report.pdf`) is generated automatically, visualizing how Planned Value, Earned Value, and Actual Cost diverge over time.

## Why I Built This

As an aspiring project manager, I wanted to deeply understand EVM — a core PMI concept — by building a tool that calculates it, rather than just reading about the formulas. This project reflects both my grasp of project management fundamentals and my growing ability to build practical tools with Python.

## Possible Future Improvements

- Color-coded health warnings (red/green flags for at-risk metrics)
- Support for tracking multiple projects simultaneously
- A simple graphical interface instead of command-line only
