# logger_config.py
import logging
import os
from datetime import datetime

def setup_logger(name: str, log_level=logging.INFO, log_to_file=True, log_to_console=True):
    """
    Настройка логгера для модуля
    
    Args:
        name: имя логгера (обычно __name__)
        log_level: уровень логирования
        log_to_file: писать в файл
        log_to_console: выводить в консоль
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Очищаем существующие обработчики, чтобы не дублировать
    if logger.handlers:
        logger.handlers.clear()
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Консольный обработчик
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Файловый обработчик
    if log_to_file:
        # Создаем папку для логов, если её нет
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Разные файлы для разных модулей
        log_file = os.path.join(log_dir, f"{name.replace('.', '_')}.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str):
    """Получить уже настроенный логгер"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        return setup_logger(name)
    
    return logger