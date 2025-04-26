from gigachat import GigaChat
from dotenv import load_dotenv
import os

load_dotenv()


def gigachat_prompt(prompt_text: str) -> str:
    """Функция для отправки запросов к GigaChat API"""
    try:
        with GigaChat(credentials=os.getenv("SBER"), verify_ssl_certs=False, model='GigaChat') as giga:
            prompt = f"""
            Ты - интеллектуальный ассистент магазина автозапчастей. Будь учтив и внимателен к запросам.
            {prompt_text}

            Пожалуйста, предоставь подробный и структурированный ответ на этот запрос.
            Если вопрос неясен, уточни, что именно нужно объяснить.
            """
            response = giga.chat(prompt)
            return str(filter_text(response.choices[0].message.content))
    except Exception as e:
        raise Exception(f"Ошибка при обращении к GigaChat: {str(e)}")


def filter_text(text):
    return text.replace('*', '').replace('#', '')
