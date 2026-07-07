"""
EVM Interactive Tool
--------------------
Instead of editing a CSV by hand, this version ASKS the user for data,
validates it, then reuses the same calculation and charting functions
from evm_basic.py.
"""

import pandas as pd

# We're REUSING code we already wrote and tested, instead of rewriting it.
# This is called "importing from a local module" -- as long as this file
# sits in the SAME folder as evm_basic.py, this works.
from evm_basic import calculate_evm, print_summary, make_chart


# -----------------------------------------------------------------------
# STEP 1: Ask ONE question, safely, and keep asking until it's valid
# -----------------------------------------------------------------------
def ask_for_number(prompt):
    """
    Keeps asking the user for a number until they give a valid one.
    This is a 'while True' loop -- it repeats FOREVER, until something
    inside it explicitly stops it (here, a 'return' when input is valid).
    """
    while True:
        raw_value = input(prompt)
        try:
            return float(raw_value)   # if this line fails, we jump to except
        except ValueError:
            print("  -> That's not a valid number. Please try again.")


# -----------------------------------------------------------------------
# STEP 2: Collect ONE period's full set of data
# -----------------------------------------------------------------------
def collect_one_period(period_number):
    print(f"\n--- Period {period_number} ---")
    budgeted_cost = ask_for_number("Budgeted cost for this period: ")
    percent_planned = ask_for_number("Cumulative % planned complete: ")
    percent_complete = ask_for_number("Cumulative % actually complete: ")
    actual_cost = ask_for_number("Cumulative actual cost spent: ")

    # A "dictionary" bundles related values together under labeled keys --
    # think of it like a mini spreadsheet row with column names attached.
    return {
        "period": f"Period {period_number}",
        "budgeted_cost": budgeted_cost,
        "percent_planned": percent_planned,
        "percent_complete": percent_complete,
        "actual_cost": actual_cost,
    }


# -----------------------------------------------------------------------
# STEP 3: Loop to collect however many periods the user wants
# -----------------------------------------------------------------------
def collect_all_periods():
    num_periods = int(ask_for_number("How many periods (months) of data do you have? "))

    all_periods = []  # an empty LIST -- we'll add each period's dictionary into it

    for i in range(1, num_periods + 1):   # range(1, n+1) counts 1,2,3...n
        period_data = collect_one_period(i)
        all_periods.append(period_data)   # add this period onto the end of the list

    return all_periods


# -----------------------------------------------------------------------
# STEP 4: Tie it together
# -----------------------------------------------------------------------
if __name__ == "__main__":
    print("=== EVM Interactive Data Entry ===")

    periods_list = collect_all_periods()

    # Convert our list of dictionaries into a real pandas DataFrame --
    # this is the SAME kind of table evm_basic.py builds from a CSV.
    df = pd.DataFrame(periods_list)

    bac = df["budgeted_cost"].sum()

    result = calculate_evm(df, bac)
    print_summary(result)
    make_chart(result, "evm_interactive_report.pdf")
