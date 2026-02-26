import ast
import os
from zss import simple_distance
from zss import Node as ZSSNode

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
    
    def get_children(self):
        return self.children


class PY_TO_AST_ENCODER:
    def __init__(self, path):
        with open(path , 'r') as f:
            content = f.read()
        self.ast =  ast.parse(content)
        
    def create_ast(self):
        return self.ast_to_zss_tree(self.ast)
    
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
            
            elif child_value is not None and not isinstance(child_value, (str, int, float, bool)):
                pass
        
        return zss_node

if __name__ == "__main__":
    path = os.path.join("..", "657023", "352515686.py3")
    with open(path, 'r') as f:
        print()
        a = PY_TO_AST_ENCODER(f.read())
        asn = a.create_ast()
        print(simple_distance(asn, asn))
        print(asn)
    