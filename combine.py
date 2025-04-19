# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "argparse",
#     "requests",
#     "pathlib"
# ]
# ///

import requests
import csv
import argparse
from pathlib import Path

def fetch_dividends(asset_id):
    url = 'https://gql.api.investing.com/graphql'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept': 'application/graphql-response+json, application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.investing.com/',
        'content-type': 'application/json',
        'Origin': 'https://www.investing.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-GPC': '1',
        'Priority': 'u=4',
        'TE': 'trailers',
    }

    payload = {
        "query": """query HistoricalDividends($investingAssetId:ID!,$idType:AssetIDType,$cursor:String,$limit:Int){
            investingAsset(id:$investingAssetId,idType:$idType){
                dividends{
                    dividends(cursor:$cursor,limit:$limit){
                        cursor 
                        data{
                            div_date 
                            div_amount 
                            div_payment_type 
                            pay_date 
                            yield
                        }
                    }
                }
            }
        }""",
        "variables": {
            "investingAssetId": asset_id,
            "idType": "INVESTING",
            "limit": 50
        },
        "operationName": "HistoricalDividends"
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def save_to_csv(dividends, filename, ticker=None):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["ticker", "div_date", "div_amount", "div_payment_type", "pay_date", "yield"])
        writer.writeheader()
        for dividend in dividends:
            if ticker:
                dividend["ticker"] = ticker
            writer.writerow(dividend)

def process_assets(input_file, output_dir, combined_output=None):
    # Read input CSV
    with open(input_file, mode='r') as file:
        reader = csv.DictReader(file)
        assets = list(reader)
    
    # Prepare output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    all_dividends = []
    
    for asset in assets:
        asset_id = asset['id']
        ticker = asset.get('ticker', asset_id)  # Use ticker if available, otherwise use ID
        
        print(f"Fetching dividends for {ticker} (ID: {asset_id})...")
        try:
            data = fetch_dividends(asset_id)
            dividends = data['data']['investingAsset']['dividends']['dividends']['data']
            
            # Add ticker to each dividend record
            for dividend in dividends:
                dividend['ticker'] = ticker
            
            # Save individual file
            output_file = Path(output_dir) / f"{ticker}_dividends.csv"
            save_to_csv(dividends, output_file)
            print(f"Saved {len(dividends)} dividends to {output_file}")
            
            # Collect for combined output
            all_dividends.extend(dividends)
            
        except Exception as e:
            print(f"Error processing {ticker} (ID: {asset_id}): {str(e)}")
    
    # Save combined file if requested
    if combined_output:
        combined_path = Path(output_dir) / combined_output
        save_to_csv(all_dividends, combined_path)
        print(f"\nCombined data saved to {combined_path}")
        print(f"Total dividends fetched: {len(all_dividends)}")

def main():
    parser = argparse.ArgumentParser(description="Fetch historical dividends from Investing.com for multiple assets")
    parser.add_argument("input_file", help="CSV file containing asset IDs and tickers (columns: id,ticker)")
    parser.add_argument("output_dir", help="Directory to save dividend CSV files")
    parser.add_argument("--combined", help="Filename for combined output (optional)", default=None)
    args = parser.parse_args()

    process_assets(args.input_file, args.output_dir, args.combined)

if __name__ == "__main__":
    main()