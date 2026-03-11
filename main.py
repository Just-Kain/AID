import os
import shutil
from AST_encoder.AST_encode import global_AST_encoder
from file_utils import get_file_paths, create_and_clear_work_dir
from cf_request.cf_API_request import cf_requests
from pathlib import Path

"""
"contestId" : "657023" ,
"groupCode" : "b4hWjnSy2p",
"""


def _Start_work():
    
    req = cf_requests.contest.status(contestId_=657023, groupCode_="b4hWjnSy2p", from_=None, count_=None)
    
    result = list()
    if req["status"] == 'OK':
        print("request complete")
        result = req["result"]
    else:
        print("request faild")
        return
    
    create_and_clear_work_dir("shcool_solution_space")
    dir_path = os.path.join("..", "657023")
    path_to_file = Path(dir_path)
    now_path = os.path.join('.', 'shcool_solution_space')
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
    
        