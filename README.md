UK Gender Pay Gap Analysis

A Python data engineering project analysing UK gender pay gap data across three reporting years: 2022–2023, 2023–2024 and 2024–2025.

Overview

This project uses publicly available data from the UK Government's Gender Pay Gap Service to explore changes in reported gender pay gaps over time.

It demonstrates a basic ETL (Extract, Transform, Load) pipeline using Python, Pandas, SQLite and SQL.

Data Pipeline

Extract – Read the three annual CSV datasets and identify their reporting years.

Transform – Clean and standardise the data, handle duplicates and validate records.

Load – Export the processed data to CSV and load it into a SQLite database.

Analyse – Use SQL queries to calculate statistics, including average mean and median hourly pay gaps by reporting year.

Visualise – Use Matplotlib to present the results graphically.

Technologies Used

Python

Pandas

SQLite / SQL

Matplotlib

Data Source

UK Government Gender Pay Gap Service:

https://gender-pay-gap.service.gov.uk/

The project uses employer-submitted gender pay gap data for three consecutive reporting years.

Purpose

This project was developed to practise data engineering techniques, including working with real-world datasets, building ETL pipelines, data validation, SQL analysis and visualisation.

Notes

The SQLite database (gender_pay_gap.db) is generated locally and is not included in the repository.

The analysis is based on published employer submissions and should not be interpreted as a direct measure of unequal pay for equivalent work.
