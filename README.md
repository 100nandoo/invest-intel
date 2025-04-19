# 🏦 Invest Intel

A simple script to fetch historical dividend data from Investing.com using their (undocumented) GraphQL API. It can export dividend data for individual or multiple stock assets as CSV files — great for analysis, dashboards, or further automation.

## 🧰 Requirements

- Python 3.13+
- [UV](https://github.com/astral-sh/uv)
- Dependencies:
  - requests
  - argparse
  - pathlib

## 📄 Scripts

### `dividend.py`

Fetch dividend data for a single asset using its Investing.com asset ID.

#### 🔧 Usage

`uv run dividend.py <asset_id> <output_csv>`

#### Example

`uv run dividend.py 101342 output.csv`

This will fetch dividends for asset ID `101342` and save them to `output.csv`.

### `combine.py`

Fetch dividend data for multiple assets listed in a CSV file.

#### 🔧 CSV Input Format

The input file must be a CSV with the following columns:

```csv
id,ticker
101233,GEMS
101281,ADRO
101289,AKRA
```

`id`: Investing.com asset ID

`ticker`: Your chosen label or stock ticker (used in filenames and CSV output)

#### 🛠 Basic Usage

`uv run combine.py investing.csv output_directory`

This fetches and saves individual CSVs to the specified directory.

#### 📦 With Combined Output

To also save a combined CSV with all dividend data:

`uv run combine.py investing.csv output_directory --combined all_dividends.csv`

The combined output will include all tickers in a single CSV.

## 📝 Output CSV Format

Each output file contains the following columns:

- ticker
- div_date
- div_amount
- div_payment_type
- pay_date
- yield

## 🚨 Notes

Uses Investing.com’s unofficial GraphQL API, which may change without notice.

Requires a stable internet connection.

HTTP errors or failed asset IDs will be logged to console.
