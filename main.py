import os
import shutil
from AST_encoder.AST_encode import global_AST_encoder
from file_utils import get_file_paths, create_and_clear_work_dir, get_extension
from cf_request.cf_API_request import cf_requests
from pathlib import Path
from difflib import Differ
import pandas as pd


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
            
def count_diff(content_1 : str, content_2 : str):
    d = Differ()
    diff = list(d.compare(content_1, content_2))
    count = 0
    for s in diff:
        if s[0] == '+' | s[0] == '-':
            count += 1
        elif s[0] == '?':
            count += 1
    

def _Start_work():
    
    problem_names = ['A']
    
    Sc_sol_path = {
        'A' : [''],
    }
    
    AI_sol_path = {
        'A' : ['D:\AID\AID\AI_Solution\A\deepseak.py'],
        }
    
    metrics = dict()
    
    for problem in problem_names:
        for AI_path in AI_sol_path[problem]:
            ai_encode = global_AST_encoder(AI_path)
            ai_ast = ai_encode.create_ast()
            ai_name_set = ai_encode.get_var_names()
            ai_lang = get_extension(AI_sol_path)
            
            for Sc_path in Sc_sol_path:
                
                ...
            
        
    
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
    
        