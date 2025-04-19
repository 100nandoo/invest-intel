# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "argparse",
#     "requests",
# ]
# ///
import requests
import csv
import argparse

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

def save_to_csv(dividends, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["div_date", "div_amount", "div_payment_type", "pay_date", "yield"])
        writer.writeheader()
        for dividend in dividends:
            writer.writerow(dividend)

def main():
    parser = argparse.ArgumentParser(description="Fetch historical dividends from Investing.com and save them as a CSV")
    parser.add_argument("asset_id", help="The asset ID to fetch dividend data for")
    parser.add_argument("output_file", help="The CSV file to save dividend data")
    args = parser.parse_args()

    data = fetch_dividends(args.asset_id)
    dividends = data['data']['investingAsset']['dividends']['dividends']['data']

    save_to_csv(dividends, args.output_file)
    print(f"Data saved to {args.output_file}")

if __name__ == "__main__":
    main()
