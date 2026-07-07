"""
EVM (Earned Value Management) Basic Calculator
------------------------------------------------
A teaching script. Read the comments -- they explain WHY, not just WHAT.
"""

import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------
# STEP 1: Load the data
# -----------------------------------------------------------------------
def load_data(csv_path):
    """
    pandas.read_csv turns a CSV file into a DataFrame -- think of it like
    an Excel sheet living inside Python, where every column is a Series
    (basically a labeled array).
    """
    df = pd.read_csv(csv_path, parse_dates=["period"])
    return df


# -----------------------------------------------------------------------
# STEP 2: Define the Total Project Budget (BAC = Budget At Completion)
# -----------------------------------------------------------------------
# In our sample data, each row's 'budgeted_cost' is the SAME ($20,000)
# because it's the monthly planned budget slice. The TOTAL project budget
# (BAC) is the sum across all planned periods.
def get_bac(df):
    return df["budgeted_cost"].sum()


# -----------------------------------------------------------------------
# STEP 3: Calculate the core EVM metrics
# -----------------------------------------------------------------------
def calculate_evm(df, bac):
    """
    PV (Planned Value)  = % planned complete  x  BAC
    EV (Earned Value)   = % actually complete x  BAC
    AC (Actual Cost)    = money actually spent (given directly in data)

    CPI (Cost Performance Index)     = EV / AC
        > 1.0 means you're getting MORE value than you're spending (good)
        < 1.0 means you're spending MORE than the value you're getting (bad)

    SPI (Schedule Performance Index) = EV / PV
        > 1.0 means you're AHEAD of schedule
        < 1.0 means you're BEHIND schedule

    EAC (Estimate At Completion) = BAC / CPI
        "If we keep performing at this same cost efficiency, this is
        what the WHOLE project will actually cost."
    """
    df = df.copy()

    df["PV"] = (df["percent_planned"] / 100) * bac
    df["EV"] = (df["percent_complete"] / 100) * bac
    df["AC"] = df["actual_cost"]

    df["CPI"] = df["EV"] / df["AC"]
    df["SPI"] = df["EV"] / df["PV"]

    df["CV"] = df["EV"] - df["AC"]   # Cost Variance (positive = under budget)
    df["SV"] = df["EV"] - df["PV"]   # Schedule Variance (positive = ahead)

    df["EAC"] = bac / df["CPI"]

    return df


# -----------------------------------------------------------------------
# STEP 4: Print a readable summary table
# -----------------------------------------------------------------------
def print_summary(df):
    print("\n--- EVM Summary ---\n")
    display_cols = ["period", "PV", "EV", "AC", "CPI", "SPI", "CV", "SV", "EAC"]
    print(df[display_cols].round(2).to_string(index=False))

    latest = df.iloc[-1]
    print("\n--- Latest Period Health Check ---")
    print(f"CPI: {latest['CPI']:.2f}  ->", "Under budget" if latest['CPI'] > 1 else "Over budget")
    print(f"SPI: {latest['SPI']:.2f}  ->", "Ahead of schedule" if latest['SPI'] > 1 else "Behind schedule")
    print(f"Forecasted Final Cost (EAC): ${latest['EAC']:,.2f}")


# -----------------------------------------------------------------------
# STEP 5: Build the chart and export it as a PDF
# -----------------------------------------------------------------------
def make_chart(df, output_path):
    plt.figure(figsize=(9, 5.5))

    plt.plot(df["period"], df["PV"], label="Planned Value (PV)", marker="o")
    plt.plot(df["period"], df["EV"], label="Earned Value (EV)", marker="o")
    plt.plot(df["period"], df["AC"], label="Actual Cost (AC)", marker="o")

    plt.title("EVM Curve: Planned vs Earned vs Actual")
    plt.xlabel("Reporting Period")
    plt.ylabel("Cumulative Cost ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(output_path)  # saving as .pdf triggers matplotlib's PDF backend
    plt.close()
    print(f"\nChart saved to: {output_path}")


# -----------------------------------------------------------------------
# STEP 6: Tie it all together
# -----------------------------------------------------------------------
if __name__ == "__main__":
    df = load_data("data/sample_evm.csv")
    bac = get_bac(df)

    result = calculate_evm(df, bac)
    print_summary(result)
    make_chart(result, "evm_report.pdf")
