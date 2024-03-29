import requests
from urllib.parse import quote


headers = {
    "accept": "application/json",
    "X-API-KEY": "S2F7CKC-CTEMPQ1-K4YDW4W-NJRG7KH"
}

# Пример получения фильма по следующим параметрам: комедия, 2018, рейтинг >= 6