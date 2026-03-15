import os
import shutil
from AST_encoder.AST_encode import global_AST_encoder, AST_score
from file_utils import get_file_paths, create_and_clear_work_dir, get_extension, code_type_definition
from cf_request.cf_API_request import cf_requests
from pathlib import Path
from difflib import Differ
import pandas as pd
from collections import defaultdict

def create_space(req:dict, dir_path : str, work_dir_name="shcool_solution_space"):
     
    result = req["result"]

    create_and_clear_work_dir(work_dir_name)
    path_to_file = Path(dir_path)
    now_path = os.path.join('.', work_dir_name)
    for submition in result:
        try:
            index_problem = submition["problem"]["index"]
            need_path = os.path.join(now_path, index_problem)
            file_path = str(list(path_to_file.glob(f"{submition["id"]}.*"))[0])
            if submition["verdict"] == "OK" or submition["verdict"] == "PARTIAL":
                if os.path.isdir(need_path):
                    shutil.copy(file_path, need_path)
                else:
                    os.mkdir(need_path)
                    shutil.copy(file_path, need_path)
        except:
            print("file with soluthion not found or somthing gone wrong")
        
        
        
def diff_gen(content_1 : str, content_2 : str):
    d = Differ()
    diff = list(d.compare(content_1, content_2))
    return diff
            
def count_diff(diff : list):
    count = 0
    
    for s in diff:
        if s[0] == '+' or s[0] == '-':
            count += 1
        elif s[0] == '?':
            count -= 1
    
    return count 
    
def count_var_diff(vars_1 : set, vars_2 : set):
    return len(vars_1 - vars_2) + len(vars_2 - vars_1)

def use_comments(content : str, code_type : str):
    comment_sing = list()
    if code_type == 'py':
        comment_sing = ['"""', '#']
    else:
        comment_sing = ['//', '/*', '*/']
    
    for sing in comment_sing:
        if sing in content:
            return 1
    
    return 0


def code_map(path : str):
    """
    Получаем словарь с ключем в виде имени файла (без расширения) и 
    внутренней словарем с текстом кода, ast, языком
    """    
    
    ...
    

def metrics_collector(problem_names : list, sc_solutions_path : dict, AI_sol_path : dict):
    
    # problem_names = ['A']
    
    # sc_solutions_path = {
    #     'A' : os.path.join('.', 'scool_solution_space', 'A')
    # }
    
    # AI_sol_path = {
    #     'A' : [os.path.join('.', 'AI_Solution', 'A', 'deepseak.py')]
    #     }
    
    metrics = defaultdict(list)
    
    for problem in problem_names:
        
        solutions_paths = get_file_paths(sc_solutions_path[problem])
        
        for AI_path in AI_sol_path[problem]:
            
            with open(AI_path, 'r', encoding='utf-8') as f:
                ai_content = f.read()
                
            ai_len = len(ai_content)
            ai_encode = global_AST_encoder(AI_path)
            ai_ast = ai_encode.create_ast()
            ai_name_set = ai_encode.get_var_names()
            ai_lang = code_type_definition(get_extension(AI_path))
            filename = os.path.basename(AI_path)
            
            for sc_path in solutions_paths:
                print(sc_path)
                sc_lang = code_type_definition(get_extension(sc_path))
                if sc_lang != ai_lang:
                    continue
                else:
                    with open(sc_path, 'r', encoding='utf-8') as f:
                        sc_content = f.read()
                        
                    sc_len = len(sc_content)
                    sc_encode = global_AST_encoder(sc_path)
                    sc_ast = sc_encode.create_ast()
                    sc_name_set = sc_encode.get_var_names()
                    
                    diff = diff_gen(ai_content, sc_content)
                    str_diff_score = count_diff(diff)
                    score = AST_score(ai_ast, sc_ast)
                    var_diff_score = count_var_diff(sc_name_set, ai_name_set)
                    comments = use_comments(sc_content, sc_lang)
                    sol_fname = os.path.basename(sc_path)
                    
                    metrics[f'id'].append(f'{sol_fname}')
                    metrics[f'delt_lenght_"{filename}"'].append(abs(ai_len - sc_len))
                    metrics[f'ast_score_"{filename}"'].append(score)
                    metrics[f'str_diff_score_"{filename}"'].append(str_diff_score)
                    metrics[f'var_diff_score_"{filename}"'].append(var_diff_score)
                    metrics[f'use_cooments"{filename}"'].append(comments)
                    
    dt = pd.DataFrame(metrics) 

def _Start_work():
    
    problem_names = ['A']
    
    sc_solutions_path = {
        'A' : os.path.join('.', 'scool_solution_space', 'A')
    }
    
    AI_sol_path = {
        'A' : [os.path.join('.', 'AI_Solution', 'A', 'deepseak.py')]
        }
    
    metrics = defaultdict(list)
    
    for problem in problem_names:
        
        solutions_paths = get_file_paths(sc_solutions_path[problem])
        
        for AI_path in AI_sol_path[problem]:
            
            with open(AI_path, 'r', encoding='utf-8') as f:
                ai_content = f.read()
                
            ai_len = len(ai_content)
            ai_encode = global_AST_encoder(AI_path)
            ai_ast = ai_encode.create_ast()
            ai_name_set = ai_encode.get_var_names()
            ai_lang = code_type_definition(get_extension(AI_path))
            filename = os.path.basename(AI_path)
            
            for sc_path in solutions_paths:
                print(sc_path)
                sc_lang = code_type_definition(get_extension(sc_path))
                if sc_lang != ai_lang:
                    continue
                else:
                    with open(sc_path, 'r', encoding='utf-8') as f:
                        sc_content = f.read()
                        
                    sc_len = len(sc_content)
                    sc_encode = global_AST_encoder(sc_path)
                    sc_ast = sc_encode.create_ast()
                    sc_name_set = sc_encode.get_var_names()
                    
                    diff = diff_gen(ai_content, sc_content)
                    str_diff_score = count_diff(diff)
                    score = AST_score(ai_ast, sc_ast)
                    var_diff_score = count_var_diff(sc_name_set, ai_name_set)
                    comments = use_comments(sc_content, sc_lang)
                    sol_fname = os.path.basename(sc_path)
                    
                    metrics[f'id'].append(f'{sol_fname}')
                    metrics[f'delt_lenght_"{filename}"'].append(abs(ai_len - sc_len))
                    metrics[f'ast_score_"{filename}"'].append(score)
                    metrics[f'str_diff_score_"{filename}"'].append(str_diff_score)
                    metrics[f'var_diff_score_"{filename}"'].append(var_diff_score)
                    metrics[f'use_cooments"{filename}"'].append(comments)
                    
    dt = pd.DataFrame(metrics) 
    dt.to_excel('output.xlsx', index=False)    
            
            
            
        
    
    # dir_path = os.path.join("..", "657023")
    # file_paths = get_file_paths(folder_path=dir_path)
    # for file in file_paths:
    #     try:
    #         print(file)
    #         new_ast = global_AST_encoder(file)
    #         new_ast.create_ast()
    #         print(new_ast.get_var_names())
    #     except:
    #         print("lol")
            
    
if __name__ == '__main__':
    _Start_work()
    
    # cf_requests.contest.status()
    
        