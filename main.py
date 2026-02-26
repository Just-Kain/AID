import os
import shutil
from py_to_ast_encoder import PY_TO_AST_ENCODER 
from cpp_to_ast_encoder import CPP_TO_AST_ENCODER
from abc import ABC, abstractmethod
from import_and_space_constructor import Get_file_paths, Code_type_definition
from zss import Node as ZSSNode 
from zss import simple_distance

encoder='utf-8'  

def Global_AST_encoder(path, code_type):
    
    if code_type == 'c++':
        return CPP_TO_AST_ENCODER(path).create_ast()
    elif code_type == 'py':
        return PY_TO_AST_ENCODER(path).create_ast()
    else:
        return ZSSNode("EmptyAST")
    
def AST_score(NodeA, NodeB):
    ASTScore = simple_distance(NodeA, NodeB)
    return ASTScore

AST_boundery = 0

def _Start_work():
    dir_path = os.path.join("..", "657023")
    file_names = Get_file_paths(folder_path=dir_path)

    AST_lib = []
    AST_Score_list = []
    for file_name in file_names:
        
        path_work_file = os.path.join(dir_path, file_name)
        work_file = file_name.split('.')
        print('start work on :', path_work_file)

        code_type = Code_type_definition(work_file[1])
        AST = Global_AST_encoder(path_work_file, code_type)
        isPlagiat = False
        for i in AST_lib:
            sco = AST_score(AST, i)
            AST_Score_list.append(sco)
            
        if not(isPlagiat):
            AST_lib.append(AST)
            
        print(simple_distance(AST, AST))
                
    
    
if __name__ == '__main__':
    _Start_work()
        