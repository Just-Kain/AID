from AST_encoder.cpp_to_ast_encoder import CPP_TO_AST_ENCODER
from AST_encoder.py_to_ast_encoder import PY_TO_AST_ENCODER
from zss import Node as ZSSNode
from zss import simple_distance

def global_AST_encoder(path, code_type):
    
    if code_type == 'c++':
        return CPP_TO_AST_ENCODER(path).create_ast()
    elif code_type == 'py':
        return PY_TO_AST_ENCODER(path).create_ast()
    else:
        return ZSSNode("EmptyAST")
    
def AST_score(NodeA, NodeB):
    ASTScore = simple_distance(NodeA, NodeB)
    return ASTScore