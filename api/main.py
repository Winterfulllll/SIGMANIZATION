import requests
from dotenv import load_dotenv
import os
from urllib.parse import quote

load_dotenv()
X_API_KEY = os.getenv("X_API_KEY")

all_genres = ['аниме', 'биография', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'для взрослых', 'документальный', 'драма', 'игра', 'история', 'комедия', 'концерт', 'короткометражка', 'криминал',
              'мелодрама', 'музыка', 'мультфильм', 'мюзикл', 'новости', 'приключения', 'реальное ТВ', 'семейный', 'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фильм-нуар', 'фэнтези', 'церемония']
all_countries = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Американские Виргинские острова', 'Американское Самоа', 'Ангола', 'Андорра', 'Антарктида', 'Антигуа и Барбуда', 'Антильские Острова', 'Аргентина', 'Армения', 'Аруба', 'Афганистан', 'Багамы', 'Бангладеш', 'Барбадос', 'Бахрейн', 'Беларусь', 'Белиз', 'Бельгия', 'Бенин', 'Берег Слоновой кости', 'Бермуды', 'Бирма', 'Болгария', 'Боливия', 'Босния', 'Босния и Герцеговина', 'Ботсвана', 'Бразилия', 'Бруней-Даруссалам', 'Буркина-Фасо', 'Бурунди', 'Бутан', 'Вануату', 'Ватикан', 'Великобритания', 'Венгрия', 'Венесуэла', 'Виргинские Острова', 'Внешние малые острова США', 'Вьетнам', 'Вьетнам Северный', 'Габон', 'Гаити', 'Гайана', 'Гамбия', 'Гана', 'Гваделупа', 'Гватемала', 'Гвинея', 'Гвинея-Бисау', 'Германия', 'Германия (ГДР)', 'Германия (ФРГ)', 'Гибралтар', 'Гондурас', 'Гонконг', 'Гренада', 'Гренландия', 'Греция', 'Грузия', 'Гуам', 'Дания', 'Джибути', 'Доминика', 'Доминикана', 'Египет', 'Заир', 'Замбия', 'Западная Сахара', 'Зимбабве', 'Израиль', 'Индия', 'Индонезия', 'Иордания', 'Ирак', 'Иран', 'Ирландия', 'Исландия', 'Испания', 'Италия', 'Йемен', 'Кабо-Верде', 'Казахстан', 'Каймановы острова', 'Камбоджа', 'Камерун', 'Канада', 'Катар', 'Кения', 'Кипр', 'Кирибати', 'Китай', 'Колумбия', 'Коморы', 'Конго', 'Конго (ДРК)', 'Корея', 'Корея Северная', 'Корея Южная', 'Косово', 'Коста-Рика', 'Кот-д’Ивуар', 'Куба', 'Кувейт', 'Кыргызстан', 'Лаос', 'Латвия', 'Лесото', 'Либерия', 'Ливан', 'Ливия', 'Литва', 'Лихтенштейн', 'Люксембург', 'Маврикий', 'Мавритания', 'Мадагаскар', 'Макао',
                 'Македония', 'Малави', 'Малайзия', 'Мали', 'Мальдивы', 'Мальта', 'Марокко', 'Мартиника', 'Маршалловы острова', 'Мексика', 'Мозамбик', 'Молдова', 'Монако', 'Монголия', 'Монтсеррат', 'Мьянма', 'Намибия', 'Непал', 'Нигер', 'Нигерия', 'Нидерланды', 'Никарагуа', 'Новая Зеландия', 'Новая Каледония', 'Норвегия', 'ОАЭ', 'Оккупированная Палестинская территория', 'Оман', 'Остров Мэн', 'Острова Кука', 'Пакистан', 'Палау', 'Палестина', 'Панама', 'Папуа - Новая Гвинея', 'Парагвай', 'Перу', 'Польша', 'Португалия', 'Пуэрто Рико', 'Реюньон', 'Российская империя', 'Россия', 'Руанда', 'Румыния', 'СССР', 'США', 'Сальвадор', 'Самоа', 'Сан-Марино', 'Саудовская Аравия', 'Свазиленд', 'Северная Македония', 'Сейшельские острова', 'Сенегал', 'Сент-Винсент и Гренадины', 'Сент-Китс и Невис', 'Сент-Люсия ', 'Сербия', 'Сербия и Черногория', 'Сиам', 'Сингапур', 'Сирия', 'Словакия', 'Словения', 'Соломоновы Острова', 'Сомали', 'Судан', 'Суринам', 'Сьерра-Леоне', 'Таджикистан', 'Таиланд', 'Тайвань', 'Танзания', 'Тимор-Лесте', 'Того', 'Тонга', 'Тринидад и Тобаго', 'Тувалу', 'Тунис', 'Туркменистан', 'Турция', 'Уганда', 'Узбекистан', 'Украина', 'Уругвай', 'Фарерские острова', 'Федеративные Штаты Микронезии', 'Фиджи', 'Филиппины', 'Финляндия', 'Фолклендские острова', 'Франция', 'Французская Гвиана', 'Французская Полинезия', 'Хорватия', 'ЦАР', 'Чад', 'Черногория', 'Чехия', 'Чехословакия', 'Чили', 'Швейцария', 'Швеция', 'Шри-Ланка', 'Эквадор', 'Экваториальная Гвинея', 'Эритрея', 'Эстония', 'Эфиопия', 'ЮАР', 'Югославия', 'Югославия (ФР)', 'Ямайка', 'Япония']
headers = {
    "accept": "application/json",
    "X-API-KEY": X_API_KEY
}


def search_person_by_name(query_text: str):
    url = "https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10"
    encoded_query_text = quote(query_text, encoding='utf-8')
    url += f"&query={encoded_query_text}"
    response = requests.get(url, headers=headers).json()
    return response


def search_filter(filters: dict, count=10):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit={count}"
    for filter_type in filters:
        for filter_val in filters[filter_type]:
            url += f"&{filter_type}={filter_val}"
    response = requests.get(url, headers=headers).json()
    return response["docs"]


def get_full_info(id: int):
    url = f"https://api.kinopoisk.dev/v1.4/movie/{id}"
    response = requests.get(url, headers=headers).json()
    res = {
        "name": response["name"],
        "year": response["year"],
        "type": response["type"],
        "movieLength": response["movieLength"],
        "countries": [],
        "genres": [],
        "rating": [response["rating"]["kp"], response["rating"]["imdb"]],
        "trailerUrls": [],
        "shortDescription": response["shortDescription"],
        "description": response["description"],
        "similar_movies": response["similarMovies"],
        "persons": response["persons"],
        "poster": response["poster"]["url"],
        "backdrop": response["backdrop"]["url"],
        "ageRating": response["ageRating"],
        "photos": [],
        "watchability": response["watchability"]["items"],
        "5reviews": [],
        "facts": response["facts"],
    }
    for genre in response["genres"]:
        res["genres"].append(genre["name"])
    for country in response["countries"]:
        res["countries"].append(country["name"])
    for tr_url in response["videos"]["trailers"]:
        response["trailerUrls"].append(tr_url["url"])
    url = f"https://api.kinopoisk.dev/v1.4/review?page=1&limit=5&selectFields=&movieId={id}&type=%D0%9F%D0%BE%D0%B7%D0%B8%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9"
    res["5reviews"] = requests.get(url, headers=headers).json()
    return res


def get_all_reviews(id: int, page_number: int):
    url = f"https://api.kinopoisk.dev/v1.4/review?page={page_number}&limit=5&selectFields=&movieId={id}"
    return requests.get(url, headers=headers).json()


filters = {
    "type": [],
    "genres.name": [],
    "year": [],
    "query": [],
    "rating.kp": [],
    "ageRating": [],
    "countries.name": [],
    "selectFields": ["id", "name", "poster", "year", "rating", "movieLength", "genres", "countries"],
    "persons.id": []
}
