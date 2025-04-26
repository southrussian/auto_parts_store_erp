from __future__ import annotations
from yandex_cloud_ml_sdk import YCloudML
from dotenv import load_dotenv
import os

load_dotenv()


def yandex(prompt: str) -> str:
    """Функция для взаимодействия с YandexGPT.

    Args:
        prompt: Текст запроса пользователя.

    Returns:
        Ответ от YandexGPT.
    """
    sdk = YCloudML(
        folder_id=os.getenv('FOLDER_ID'),
        auth=os.getenv('AUTH'),
    )

    messages = [
        {
            "role": "system",
            "text": """Ты - поисковой ассистент магазина автозапчастей. 
            Отвечай вежливо и по делу, характеристики запрашиваемых моделей автомобилей указывай точно. 
            Не допускай использование формулировок 'Лучше обратитесь к кому-то...' или '...зависит от модификации...' 
            """
        },
        {
            "role": "user",
            "text": prompt
        }
    ]

    result = (
        sdk.models.completions("yandexgpt").configure(temperature=0.3).run(messages)
    )

    for alternative in result:
        return str(filter_text(alternative.text))

    return "Не удалось получить ответ от YandexGPT."


def filter_text(text):
    return text.replace('*', '').replace('#', '')
