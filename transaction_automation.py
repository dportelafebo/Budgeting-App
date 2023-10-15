import requests
import json
from plaid import Client


# Use plaid api for banking stuff
client = Client(
    client_id="652b7439a1ae1d001c4de004",
    secret="189510c8a0d88900db6100f6942b75",
    environment="sandbox",  # Use 'development' or 'production' as you move forward
)

# Your Notion API Key
api_key = "secret_1olFgTFxP6WTZmQ5PHaGDmMKWNOLfcPsJUw8afqdWBR"

# Your Notion Database ID
database_id = "ddec9d3e96014e6184d2624423d7176a"

# API Endpoint
url = "https://api.notion.com/v1/pages"

# Headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",
}

# # Your list of transactions (Replace this with actual data)
manual_transactions = [
    {"Name": "Transaction 1", "Date": "2023-10-14", "Amount": 20.5, "Category": "Food"},
    {
        "Name": "Transaction 2",
        "Date": "2021-10-14",
        "Amount": 40.0,
        "Category": "Transport",
    },
]


# Function to get transactions
def get_transactions():
    response = client.Sandbox.public_token.create(
        "ins_109508", ["transactions"]  # A test institution ID
    )
    # Exchange the public_token for an access_token
    exchange_response = client.Item.public_token.exchange(response["public_token"])
    access_token = exchange_response["access_token"]
    return access_token


# Function to add row to Notion Database
def add_row_to_notion(transaction):
    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "type": "title",
                "title": [{"text": {"content": transaction["Name"]}}],
            },
            "Date": {"type": "date", "date": {"start": transaction["Date"]}},
            "Amount": {"type": "number", "number": transaction["Amount"]},
            "Category": {"type": "select", "select": {"name": transaction["Category"]}},
        },
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


# # Add each transaction to Notion
# for transaction in get_transactions():
#     print(add_row_to_notion(transaction))

print(get_transactions())
