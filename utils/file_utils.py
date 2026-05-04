import os
import shutil
from pathlib import Path
from logger_config import get_logger

logger = get_logger(__name__)

encoder='utf-8' 

code_lang_lib = {       'c' : 'c++',
                        'cpp' : 'c++',
                        'C++17 (GCC 7-32)' : 'c++',
                        'C++20 (GCC 13-64)' : 'c++',
                        'C++23 (GCC 14-64, msys2)' : 'c++',
                        'GNU C11' : 'c++',
                        'py' : 'py',
                        'py3' : 'py',
                        'py2' : 'py',
                        'pypy3' : 'py',
                        'pypy2' : 'py',
                        'pypy3-64' : 'py',
                        'PyPy 2' : 'py',
                        'PyPy 3' : 'py',
                        'PyPy 3-64' : 'py',
                        'Python 2' : 'py',
                        'Python 3' : 'py',
                        }
    # Здесь прописаны все поддерживаемые языки для шифрования 
    # На данный момент c++, py

def get_file_paths(folder_path="."):
    file_names = []
    
    for file_name in os.listdir(folder_path):
        file_names.append(os.path.join(folder_path, file_name))
            
    return file_names

def create_and_clear_work_dir(new_dir_name="work_dir"):

    folder_exist = os.path.exists(new_dir_name)
    
    if not folder_exist:
        os.mkdir(new_dir_name)
    else:
        shutil.rmtree(new_dir_name)
        os.mkdir(new_dir_name)
            
def get_extension(path):
    root, extension = os.path.splitext(path)
    extension = extension[1::]
    return extension

def code_type_definition(code_type):
    try:  
        return code_lang_lib[code_type]
    except KeyError:
        logger.warning('Warning this code type not supported to encoding!')
        return code_type
    
    
def use_comments(code: str, code_type: str):
        """проверка на использование комментариев в коде"""
        comment_sing = list()
        if code_type == 'py':
            comment_sing = ['"""', '#']
        else:
            comment_sing = ['//', '/*', '*/']
        
        for sing in comment_sing:
            if sing in code:
                return 1
        
        return 0
    
#todo : сделать возможность доставать из реквеста задачи

def sort_solution_to_dirs(req:dict, dir_path : str, work_dir_name="shcool_solution_space"):
    """
    Копирует все решения из dir_path в work_dir_name и сортирует их по задачам из cf_request\n
    Возвращает все литерралы проблем из cf_request
    """
    result = req["result"]
    problem_set = set()
    create_and_clear_work_dir(work_dir_name)
    path_to_file = Path(dir_path)
    now_path = os.path.join('.', work_dir_name)

    
    for submition in result:
        try:
            index_problem = submition["problem"]["index"]
            problem_set.add(index_problem)

            need_path = os.path.join(now_path, index_problem)
            file_path = str(list(path_to_file.glob(f"{submition["id"]}.*"))[0])
            if submition["verdict"] == "OK" or submition["verdict"] == "PARTIAL":
                if os.path.isdir(need_path):
                    shutil.copy(file_path, need_path)
                else:
                    os.mkdir(need_path)
                    shutil.copy(file_path, need_path)
        except:
            logger.warning("file with soluthion not found or somthing gone wrong")
    
    logger.debug(f"RETURNING {now_path}")
    logger.debug(f"RETURNING {problem_set}")
    
    return now_path, problem_set

