import typing
import clang.cindex
from AST_encoder.ast_encoder_interface import AST_ENCODER
from setings import clang_path
from zss import Node as ZSSNode

clang.cindex.Config.set_library_file(clang_path)

class CPP_TO_AST_ENCODER(AST_ENCODER):
    
    def __init__(self, path):
        self.path = path
        self.index = clang.cindex.Index.create()
        self.name_set = set()
    
    def filter_node_list_by_file(
        self,
        nodes: typing.Iterable[clang.cindex.Cursor],
        file_name: str
    ) -> typing.Iterable[clang.cindex.Cursor]:
        result = []
        
        for node in nodes:
            if node.location.file and node.location.file.name == file_name:
                result.append(node)
        
        return result

    def create_ast(self):
        translation_unit = self.index.parse(self.path)
        
        all_nodes = []
        
        def traverse(node):
            all_nodes.append(node)
            for child in node.get_children():
                traverse(child)
        
        traverse(translation_unit.cursor)
        
        filtered_nodes = self.filter_node_list_by_file(all_nodes, translation_unit.spelling)
        
        node_to_zss = {}
        
        for node in filtered_nodes:
            label = f"{node.kind.name}"
            
            self.name_set.add(f"{node.spelling}")
            zss_node = ZSSNode(label)
            
            node_to_zss[node] = zss_node
        
        for node in filtered_nodes:
            zss_node = node_to_zss[node]
            
            parent = node.semantic_parent
            while parent and parent not in node_to_zss:
                parent = parent.semantic_parent
            
            if parent and parent in node_to_zss:
                parent_zss = node_to_zss[parent]
                parent_zss.children.append(zss_node)  
        
        root_nodes = []
        for node, zss_node in node_to_zss.items():
            has_parent_in_filtered = False
            parent = node.semantic_parent
            while parent:
                if parent in node_to_zss:
                    has_parent_in_filtered = True
                    break
                parent = parent.semantic_parent
            
            if not has_parent_in_filtered:
                root_nodes.append(zss_node)
        
        if len(root_nodes) > 1:
            root = ZSSNode(f"main_root")
            for node in root_nodes:
                root.children.append(node)
            return root
        elif root_nodes:
            return root_nodes[0]
        else:
            return ZSSNode("Empty AST")
        
    def get_var_names(self):
        return self.name_set
    