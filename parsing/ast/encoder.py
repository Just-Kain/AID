from parsing.ast.cpp_to_ast_encoder import CPP_TO_AST_ENCODER
from parsing.ast.py_to_ast_encoder import PY_TO_AST_ENCODER
from zss import simple_distance
import sqlite3
from core.config import DB_PATH, INCLUDING_LANGUAGE


class ASTEncoder:
        
    def take_submissions(self):
        
        with sqlite3.connect(DB_PATH) as conn:

            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT problem_name FROM submissions')
            problem_names = cursor.fetchall()
            problem_names = [x[0] for x in problem_names]
            
            cursor.execute('SELECT DISTINCT language FROM submissions')
            languages = cursor.fetchall()
            languages = [x[0] for x in languages]
            
            submissions = dict()
            for name in problem_names:
                submissions[name] = dict()
                for language in languages:
                    cursor.execute('SELECT id, code FROM submissions WHERE problem_name = ? AND language = ?', (name, language))
                    recall = cursor.fetchall()
                    id = [x[0] for x in recall]
                    code = [x[1] for x in recall]
                    submissions[name][language] = dict()
                    submissions[name][language]['id'] = id    
                    submissions[name][language]['code'] = code  
            
            return problem_names, submissions
        
    def gen_ast(self, lang: str, code_list: list):
        if lang == 'py':
            for code in code_list:
                try: 
                    encoder = PY_TO_AST_ENCODER(code)
                    ast = encoder.create_ast()
                    yield ast
                except:
                    print("WARNING: The code is not interpreted in Python or something went wrong.")
                    yield None
             
        # elif lang == 'c++':
        #     for code in code_list:
        #         try: 
        #             encoder = CPP_TO_AST_ENCODER(code)
        #             ast = encoder.create_ast()
        #             yield ast
        #         except:
        #             print("WARNING: The code doesn't compile in C++ or something went wrong")
        #             yield None
                
        else:
            for code in code_list:
                yield None
        
    def gen_ast_list(self, lang: str, code_list: list):
        ast_list = list()
        
        for ast in self.gen_ast(lang, code_list):
            ast_list.append(ast)
            
        return ast_list
                
    def ASTEncoder(self):
        
        problem_names, submissions = self.take_submissions()
            
        for name in problem_names:   
            print(f"DEBUG: work with {name}") 
            for lang, sub in submissions[name].items():
                print(f"DEBUG: work on {lang}") 
                submissions[name][lang]['ast'] = self.gen_ast_list(lang, sub['code'])
        
        return submissions

    def AST_score(NodeA, NodeB):
        ASTScore = simple_distance(NodeA, NodeB)
        return ASTScore