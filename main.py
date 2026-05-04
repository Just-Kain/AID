from core.pipeline import Pipeline
import logging.config
from core.config import LOG_DIR
import json
import os

def init_logging():
    """Инициализация логирования для всего проекта"""
    
    if os.path.exists("config/logging_config.json"):
        with open("config/logging_config.json") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.info("logger configuration lost!")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("logs/app.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

init_logging()

#todo: * Необходимо реализовать коллектор для подгрузки файлов из локального репозитория пользователя 
# * Необходимо собрать весь проект в Docker и сделать порты для будущего API
"""
Референс портов:
PUT:
        Login - CF (принимает CF_KEY, CF_SECRET)
        Contest - (принимает contestID и groupID(при необходимости)) 
        Including Languages - (принимает кортеж сокращений языков программирования прописанные в коде (сейчас py, c++))
        Set treshold - (задает пороговое значение)
GET:
        start - (инициализирует полный piepline)
        status - (получает текущее состояние piepline)
        log - (выгружает логи в хронологической последовательности) 
POST: 
        new solution - (Загружает картеж кодов для проверки на схожесть. Начинает проверку с уже проверенными кодами)
"""
# * Нужно сделать упрощеное API для фронта
# * Необходимо седлать вывод ссылок на код в формате 
"""
Совпадение кодов:
root link       child link      ast_score   diff_score  delta_len
url_1   like    url_2           1           1           0
                url_3           1           1           0
                url_4           1           1           0
                ...
url_99  like    url_100         1           1           0
                url_101         1           1           0
                ...
Коды с комментариями в них:
url_1
url_2
url_3
"""
# При необходимости стоит допилить возможность вывода списков всех очков отношений 
# Необязательно: @ Сделать клиентское оконное приложение для более простой работы с проектом
# @ Сделать мульти задачный код что бы он мог запускаться как API и как клиентское консольное приложение
if __name__ == '__main__':
    work = Pipeline()
    work.run(contest_id="657023", group_id="b4hWjnSy2p")
    
        