import requests
from urllib.parse import quote


headers = {
    "accept": "application/json",
    "X-API-KEY": "S2F7CKC-CTEMPQ1-K4YDW4W-NJRG7KH"
}

# Пример получения фильма по следующим параметрам: комедия, 2018, рейтинг >= 6

# genre = "комедия"
# year = "2018"
# rate = "6"

# url = "https://api.kinopoisk.dev/v1.4/movie?page=1&limit=10"
# url += f"&genres.name={genre}"
# url += f"&year={year}"
# url += f"&rating.kp=6-10"
# url += f"&selectFields=id"

# response = requests.get(url, headers=headers)

# response_arr = response.json()
# print(type(response_arr))

url = "https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10&selectFields="
encoded_query_text = quote("Секс", encoding='utf-8')  # Кодировка текста под URL
url += f"&query={encoded_query_text}"
response = requests.get(url, headers=headers).json()
print(response["docs"][0])