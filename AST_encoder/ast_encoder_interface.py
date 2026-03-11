from abc import ABC, abstractmethod

class AST_ENCODER(ABC):
    @abstractmethod
    def create_ast(self, *args, **kwargs):
        """Создание и предработка ast"""
    @abstractmethod
    def get_var_names(self, *args, **kwargs):
        """Получить имена вершин ast"""