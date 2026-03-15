import ast
from AST_encoder.ast_encoder_interface import AST_ENCODER
from zss import Node as ZSSNode
from functools import lru_cache

class ASTZSSNode(ZSSNode):
    """
    Адаптер совместимые с zss
    """
    def __init__(self, ast_node: ast.AST):
        super().__init__(ast_node.__class__.__name__)
        self.ast_node = ast_node
        self.children = []
    
    def add_child(self, child: 'ASTZSSNode'):
        self.children.append(child)
    

class PY_TO_AST_ENCODER(AST_ENCODER):
    
    def __init__(self, path):
        with open(path , 'r', encoding='utf-8') as f:
            content = f.read()
        self.ast =  ast.parse(content)
        self.name_set = set()
        
    def create_ast(self):
        return self.ast_to_zss_tree(self.ast)
    
    @lru_cache(maxsize=512)
    def ast_to_zss_tree(self, node: ast.AST):

        if node is None:
            return None
        
        zss_node = ASTZSSNode(node)
        
        for child_name, child_value in ast.iter_fields(node):
            if isinstance(child_value, ast.AST):
                child_node = self.ast_to_zss_tree(child_value)
                if child_node:
                    zss_node.add_child(child_node)
            
            elif isinstance(child_value, list):
                for item in child_value:
                    if isinstance(item, ast.AST):
                        child_node = self.ast_to_zss_tree(item)
                        if child_node:
                            zss_node.add_child(child_node)
        
        return zss_node

    def get_var_names(self):
        for node in ast.walk(self.ast):
            if isinstance(node, ast.Name):
                self.name_set.add(f"{node.id}")
        return self.name_set
