
from pathlib import Path
import pandas as pd
import sqlite3

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_DIR = DATA_DIR / "processed"


def load_database(df):
    """Load cleaned records into SQLite."""
    db_path = DATA_DIR.parent / "gender_pay_gap.db"

    with sqlite3.connect(db_path) as conn:
        df.to_sql(
            "gender_pay_gap",
            conn,
            if_exists="replace",
            index=False
        )

        count = pd.read_sql_query(
            "SELECT COUNT(*) AS total FROM gender_pay_gap",
            conn
        )

    print(f"\nDatabase: {db_path}")
    print(f"Rows loaded: {count['total'].iloc[0]:,}")

def extract():
    """Read annual CSV files and add their reporting year."""
    frames = []

    for csv_file in sorted(DATA_DIR.glob("*.csv")):
        df = pd.read_csv(csv_file)

        # Extract reporting year from filename
        year = csv_file.stem.split(" - ")[-1]
        df["ReportingYear"] = year

        frames.append(df)
        print(f"Extracted {len(df):,} rows for {year}")

    return pd.concat(frames, ignore_index=True)


def transform(df):
    """Clean and validate the combined dataset."""
    df = df.copy()

    # Remove duplicate employer submissions within each year
    before = len(df)
    df = df.drop_duplicates(subset=["EmployerId", "ReportingYear"])
    print(f"Removed {before - len(df)} duplicate employer/year records")

    # Convert dates to datetime
    for column in ["DueDate", "DateSubmitted"]:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    # Ensure key pay gap fields are numeric
    for column in ["DiffMeanHourlyPercent", "DiffMedianHourlyPercent"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def load(df):
    """Export the cleaned dataset."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "gender_pay_gap_clean.csv"
    df.to_csv(output_file, index=False)

    print(f"Saved {len(df):,} rows to {output_file}")


def validate(df):
    """Report data quality issues."""
    print("\n--- Data Quality Report ---")

    # Check missing values in important fields
    columns = [
        "EmployerId",
        "EmployerName",
        "ReportingYear",
        "DiffMeanHourlyPercent",
        "DiffMedianHourlyPercent",
    ]

    print("\nMissing values:")
    print(df[columns].isna().sum())

    # Check duplicate employer/year combinations
    duplicates = df.duplicated(
        subset=["EmployerId", "ReportingYear"]
    ).sum()
    print(f"\nDuplicate employer/year records: {duplicates}")

    # Check hourly pay gap values
    for column in [
        "DiffMeanHourlyPercent",
        "DiffMedianHourlyPercent",
    ]:
        invalid = (~df[column].between(-100, 100) & df[column].notna()).sum()
        print(f"{column} outside -100% to 100%: {invalid}")

    # Check reporting year counts
    print("\nRecords by reporting year:")
    print(df.groupby("ReportingYear").size())

    print("\n--- Hourly Pay Gap Outliers ---")

    for column in [
        "DiffMeanHourlyPercent",
        "DiffMedianHourlyPercent",
    ]:
        outliers = df.loc[
            ~df[column].between(-100, 100) & df[column].notna(),
            ["EmployerName", "ReportingYear", column]
        ]

        print(f"\n{column}:")
        print(outliers.to_string(index=False))

if __name__ == "__main__":
    raw_data = extract()
    clean_data = transform(raw_data)
    validate(clean_data)
    load(clean_data)
    load_database(clean_data)