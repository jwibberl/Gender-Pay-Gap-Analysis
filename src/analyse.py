from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = Path(__file__).resolve().parent.parent / "gender_pay_gap.db"

def plot_results(results):
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        results["ReportingYear"],
        results["MeanPayGap"],
        marker="o",
        label="Mean hourly pay gap"
    )

    ax.plot(
        results["ReportingYear"],
        results["MedianPayGap"],
        marker="o",
        label="Median hourly pay gap"
    )

    ax.set_title("Average Reported Gender Pay Gap by Year")
    ax.set_ylabel("Pay gap (%)")
    ax.set_xlabel("Reporting year")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    output = DB_PATH.parent / "gender_pay_gap_trends.png"
    fig.savefig(output, dpi=150)
    plt.close(fig)

    print(f"Chart saved to {output}")

def analyse():
    with sqlite3.connect(DB_PATH) as conn:
        query = """
            SELECT
                ReportingYear,
                COUNT(*) AS EmployerCount,
                ROUND(AVG(DiffMeanHourlyPercent), 2) AS MeanPayGap,
                ROUND(AVG(DiffMedianHourlyPercent), 2) AS MedianPayGap
            FROM gender_pay_gap
            GROUP BY ReportingYear
            ORDER BY ReportingYear
        """

        results = pd.read_sql_query(query, conn)

    print("\n--- Gender Pay Gap by Reporting Year ---")
    print(results.to_string(index=False))
    plot_results(results)

if __name__ == "__main__":
    analyse()