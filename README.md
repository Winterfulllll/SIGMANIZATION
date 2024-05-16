# RECO - Recommendation Web Service 🔎

WEB-сервис, который использует передовые технологии искусственного интеллекта для анализа и генерации рекомендаций фильмов на основе предпочтений пользователя! 🎯

![Баннер](data/images/banner.png)

## *Состав команды разработчиков* 👨🏻‍💻

- **Горячкин Владимир Олегович** - Тимлид, архитектор, дизайнер
- **Павлюшин Максим Кириллович** - Backend-разработчик
- **Прокофьев Илья Алексеевич** - Backend-разработчик
- **Ситников Илья Александрович** - Frontend-разработчик

## *Стек используемых технологий* ✨

### Backend 🔧

- [**Python**](https://www.python.org) - Основной язык программирования для backend-части проекта;
- [**Flask**](https://flask.palletsprojects.com/en/3.0.x/) - Микрофреймворк Python для создания веб-приложений и API;
- [**Connexion**](https://connexion.readthedocs.io/en/latest/) - Расширение Flask для создания OpenAPI-совместимых API;
- [**SQLAlchemy**](https://www.sqlalchemy.org) - ORM (Object-Relational Mapper) для работы с базами данных;
- [**Marshmallow**](https://marshmallow.readthedocs.io/en/stable/) - Библиотека для сериализации/десериализации данных;
- [**Flask-JWT-Extended**](https://flask-jwt-extended.readthedocs.io/en/stable/api.html) - Расширение Flask для работы с JWT (JSON Web Tokens) для аутентификации.

### Frontend 🎨

- [**JavaScript**](https://js-documentation.netlify.app) - Основной язык программирования для frontend-части проекта;
- [**HTML/CSS**](https://html.spec.whatwg.org) - Для создания структуры и стиля веб-страниц.

### Другие инструменты 🧩

- [**Swagger**](https://docs.swagger.io) - Для документирования и удобного тестирования собственного API;
- База данных [**SQLite**](https://www.sqlite.org) - Лёгкая БД, подходящая для небольших проектов.

## *Процесс установки и запуска* ⚙️

Для начала, **установите** [***Python***](https://ekohl.github.io/tutorial/en/python_installation/) и [***GIT***](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) на свой компьютер 🐍

После этого, [**скопируйте**](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) репозиторий *(Сделать это можно в терминале ОС с помощью `git clone https://github.com/Winterfulllll/SIGMANIZATION.git`)*

**Перейдите** в скопированную директорию - `cd SIGMANIZATION`

Затем, **создайте** и **войдите** в [*виртуальное окружение*](https://github.com/AndrewVolkova/Python/blob/master/Visual/venv/instruction.ipynb) *(опционально)*

```shell
python -m venv venv # создание venv
venv\Scripts\activate # или другая команда, см. гипер-ссылку
```

**Установите** необходимые для работоспособности сервиса *python-библиотеки*

```shell
pip install -r requirements.txt # установка библиотек из requirements.txt
```

**Настройте** файл с название `.env` по инструкции

[*Подробная инструкция по настройке `.env` файла*](./data/env_instruction.md)

В конце концов, запустите код с помощью команды `uvicorn main:app --reload`
