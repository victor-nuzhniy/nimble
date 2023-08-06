"""Module for manual testing code for 'nimble' project."""


import requests

url = "http://127.0.0.1:8000/api/contacts/search/"

response = requests.post(
    url=url,
    headers={"Content-Type": "application/json"},
    json={"search_data": "oleg or ken or kari"},
)

print(response.json())
