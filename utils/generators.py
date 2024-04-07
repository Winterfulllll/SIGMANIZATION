from langchain.schema import HumanMessage, SystemMessage
from configuration import giga


def generate_film_plot(film: str) -> str:
    """
    Generates a film plot using GigaChat.

    Args:
        film (str): The name of the film.

    Returns:
        str: The generated film plot.
    """
    prompt = SystemMessage(content=f"Ты - полезный помощник с искусственным интеллектом, обладающий обширными знаниями о фильмах. Я сообщу тебе название фильма, а ты кратко изложите сюжет.")
    human_message = HumanMessage(content=f"Какой сюжет у фильма: {film}")
    response = giga([prompt, human_message])
    plot = response.content
    return plot
