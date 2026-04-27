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
         
if __name__ == '__main__':
    work = Pipeline()
    work.run(contest_id="657023", group_id="b4hWjnSy2p")
    
        