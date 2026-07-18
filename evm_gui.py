"""
EVM GUI
-------
A simple desktop window (instead of the terminal) for the multi-project
EVM tool. Uses Tkinter -- included with Python already, no extra install.

NEW CONCEPTS
------------
- A GUI is "event-driven": instead of running top-to-bottom once, it sits
  open and waits, running small functions ONLY when you click something.
- Widgets: buttons, labels, tables -- visual building blocks you arrange
  on the window.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
from evm_basic import calculate_evm
from evm_multi_project import load_data, summarize_all_projects, export_to_excel


class EVMApp:
    """
    A CLASS bundles related data and functions together into one object --
    here, "the whole app" (its window, its buttons, its current data) is
    one EVMApp object. This is a new concept (object-oriented programming),
    but you can read it simply as: "everything the app needs, in one place."
    """

    def __init__(self, root):
        self.root = root
        self.root.title("EVM Portfolio Dashboard")
        self.root.geometry("800x500")

        self.summary_df = None  # will hold the calculated results once loaded

        self._build_widgets()

    def _build_widgets(self):
        # --- Top control bar ---
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill="x")

        self.file_label = tk.Label(top_frame, text="No file selected", anchor="w")
        self.file_label.pack(side="left", padx=10)

        browse_btn = tk.Button(top_frame, text="Browse for CSV...", command=self.browse_file)
        browse_btn.pack(side="left", padx=5)

        calculate_btn = tk.Button(top_frame, text="Calculate", command=self.calculate)
        calculate_btn.pack(side="left", padx=5)

        export_btn = tk.Button(top_frame, text="Export to Excel", command=self.export_excel)
        export_btn.pack(side="left", padx=5)

        # --- Results table ---
        columns = ("project_id", "project_name", "CPI", "SPI", "EAC", "status")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Color tags -- rows get colored based on which tag we assign them
        self.tree.tag_configure("at_risk", background="#FFC7CE")
        self.tree.tag_configure("healthy", background="#C6EFCE")

        # --- Status bar ---
        self.status_label = tk.Label(self.root, text="Ready.", anchor="w", fg="#555555")
        self.status_label.pack(fill="x", padx=10, pady=(0, 10))

        self.csv_path = None

    # -----------------------------------------------------------------
    # Each of these methods runs ONLY when its matching button is clicked.
    # This is the "event-driven" idea: the app waits, then reacts.
    # -----------------------------------------------------------------
    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select a project CSV file",
            filetypes=[("CSV files", "*.csv")],
        )
        if path:  # empty string if the user cancels the dialog
            self.csv_path = path
            self.file_label.config(text=path)
            self.status_label.config(text="File selected. Click Calculate.")

    def calculate(self):
        if not self.csv_path:
            messagebox.showwarning("No file", "Please select a CSV file first.")
            return

        try:
            df = load_data(self.csv_path)
            self.summary_df = summarize_all_projects(df)
        except Exception as e:
            messagebox.showerror("Error", f"Could not process the file:\n{e}")
            return

        # Clear any previous rows before showing new ones
        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in self.summary_df.iterrows():
            tag = "at_risk" if row["status"] == "AT RISK" else "healthy"
            self.tree.insert("", "end", values=list(row), tags=(tag,))

        self.status_label.config(text=f"Calculated {len(self.summary_df)} projects.")

    def export_excel(self):
        if self.summary_df is None:
            messagebox.showwarning("Nothing to export", "Run Calculate first.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="portfolio_summary.xlsx",
        )
        if save_path:
            export_to_excel(self.summary_df, save_path)
            self.status_label.config(text=f"Saved to {save_path}")


# -----------------------------------------------------------------------
# Entry point: create the window and start the app's event loop
# -----------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EVMApp(root)
    root.mainloop()   # keeps the window open, waiting for clicks, until closed
