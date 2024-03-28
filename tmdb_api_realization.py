import requests

url = "https://api.kinopoisk.dev/v1.4/movie/random"

headers = {
    "accept": "application/json",
    "X-API-KEY": "S2F7CKC-CTEMPQ1-K4YDW4W-NJRG7KH"
}

response = requests.get(url, headers=headers)

print(response.text)