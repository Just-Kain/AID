from core.models import SimilarityResult
from difflib import Differ
from zss import simple_distance

class SimilarityEngine:
    def __init__(self, features):
        self.features = features
    
    def diff_gen(self, code_1 : str, code_2 : str):
        """Получаем разницу кодов по строкам"""
        d = Differ()
        diff = list(d.compare(code_1, code_2))
        return diff
    
    def count_diff(self, diff : list):
        """Подсчёт разницы между строками"""
        count = 0
        
        for s in diff:
            if s[0] == '+' or s[0] == '-':
                count += 1
            elif s[0] == '?':
                count -= 1
        
        return count 
    
    def AST_score(self, NodeA, NodeB):
        """Получаем расстояне между деревьями через zss"""
        ASTScore = simple_distance(NodeA, NodeB)
        return ASTScore
    
    def delta_len(self, code_1 : str, code_2 : str):
        return len(code_1, code_2)
    
    def gen_similitary(self, features):
        for i in range(0, len(features)):
            
            yield
    
    def similitary_extrude(self):
        ...