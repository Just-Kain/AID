import os
import shutil
import json
from AST_encoder.AST_encode import global_AST_encoder, AST_score
from file_utils import get_file_paths, sort_solution_to_dirs, get_extension, code_type_definition
from cf_request.cf_API_request import cf_requests
from difflib import Differ
from collections import defaultdict
from functools import lru_cache

class code_map():
    """
    Получаем класс с метриками по коду\n
    _gast_encoder -> global_AST_encoder\n
    ast -> ast представленное в виде ZSSNode\n
    var_names -> имена используеммых классов, переменных и операторов\n
    lang -> язык написания кода\n
    solution_name -> имя файла кода (с расширением)\n
    string_lenght -> количество строк кода\n
    comment -> присутствуют ли комментарии в коде\n
    """
    
    def __init__(self, path : str):
        self.code_path = path
        with open(path, 'r', encoding='utf-8') as f:
            self.content = f.read()

        self._gast_encoder = global_AST_encoder(path)
        self.ast = self._gast_encoder.create_ast()
        self.var_names = self._gast_encoder.get_var_names()
        self.lang = code_type_definition(get_extension(path))
        self.solution_name = os.path.basename(path)
        self.string_lenght = len(self.content.split('\n'))
        self.comment = self.use_comments()
        
    @lru_cache
    def diff_metrics(self, other):
        """
        Получение разницы между думя code_map (self и другой) одного языка\n
        diff_content, str_diff, ast_score, delta_str_len\n
        """
        if self.lang != other.lang or self.solution_name == other.solution_name:
            return 'None', 'None', 'None', 'None'
        
        delta_str_len = abs(self.string_lenght - other.string_lenght)
        ast_score = AST_score(self.ast, other.ast)
        diff_content = self.diff_gen(self.content, other.content)
        str_diff = self.count_diff(diff_content)
        
        return diff_content, str_diff, ast_score, delta_str_len
    
    def diff_gen(content_1 : str, content_2 : str):
        """Получаем разницу кодов по строкам"""
        d = Differ()
        diff = list(d.compare(content_1, content_2))
        return diff
                
    def count_diff(diff : list):
        """Подсчёт разницы между строками"""
        count = 0
        
        for s in diff:
            if s[0] == '+' or s[0] == '-':
                count += 1
            elif s[0] == '?':
                count -= 1
        
        return count 
        
    def count_var_diff(vars_1 : set, vars_2 : set):
        """Подсчитывает количество уникальных имен"""
        return len(vars_1 - vars_2) + len(vars_2 - vars_1)

    def use_comments(self):
        """проверка на использование комментариев в коде"""
        comment_sing = list()
        if self.lang == 'py':
            comment_sing = ['"""', '#']
        else:
            comment_sing = ['//', '/*', '*/']
        
        for sing in comment_sing:
            if sing in self.content:
                return 1
        
        return 0
    
        
def collect_code_map(dir_path):
    dict_code_map = dict()
    
    paths = get_file_paths(dir_path)
    
    for path in paths:
        try:
            dict_code_map[f'{os.path.basename(path)}'] = code_map(path)
        except:
            print("code type note supported")
    
    return dict_code_map
        
def collector(problems, work_path):
    """Проходит по всем задачам и собирает списки codemap разбитые в словарь"""
    problem_dict = dict()
    
    for problem in problems:
        problem_path = os.path.join(work_path, problem)
        dict_solution = collect_code_map(problem_path)
        problem_dict[problem] = dict_solution
    
    return problem_dict
    

def _Start_work():
    q_ans_path = os.path.join('.', 'cf_request', 'quary_ans.json')
    scul_path_ans = os.path.join('..', 'school_solv')
    with open(q_ans_path, 'r', encoding='utf-8') as f:
        q_ans = json.load(f)
    print('сортировка')
    work_space, problem_set_name = sort_solution_to_dirs(q_ans, scul_path_ans)
    problem_to_test = {'A'}
    print('собираем')
    test = collector(problems=problem_to_test, work_path=work_space)
    print('сборка прошла успешно')
    
    pass
            
    
if __name__ == '__main__':
    _Start_work()
    
    # cf_requests.contest.status()
    
        