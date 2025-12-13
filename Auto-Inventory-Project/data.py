import requests
headers = {"X-API-KEY": "339068c025e4592ac0c7294b7cf830c2b9730c89"}
payload = {
        "q": "Search about smartWatches trend in pakistan",
}
res = requests.post("https://google.serper.dev/search", json=payload, headers=headers)
print(res.json().get("organic", []))