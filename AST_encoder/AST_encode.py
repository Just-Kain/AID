from AST_encoder.cpp_to_ast_encoder import CPP_TO_AST_ENCODER
from AST_encoder.py_to_ast_encoder import PY_TO_AST_ENCODER
from file_utils import get_extension, code_type_definition
from zss import simple_distance

def global_AST_encoder(path):
    
    file_extension = get_extension(path)
    code_type = code_type_definition(file_extension)
    
    if code_type == 'c++':
        return CPP_TO_AST_ENCODER(path)
    elif code_type == 'py':
        return PY_TO_AST_ENCODER(path)
    else:
        return None
    
def AST_score(NodeA, NodeB):
    ASTScore = simple_distance(NodeA, NodeB)
    return ASTScore