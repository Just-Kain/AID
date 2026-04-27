from parsing.ast.cpp_to_ast_encoder import CPP_TO_AST_ENCODER
from parsing.ast.py_to_ast_encoder import PY_TO_AST_ENCODER
import sqlite3
from core.config import DB_PATH, INCLUDING_LANGUAGE
from logger_config import get_logger

class ASTEncoder:
    
    def __init__(self):
        self.logger = get_logger(__name__) 
        self.logger.info("initialization successful")
        
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
        
        if lang in INCLUDING_LANGUAGE:
            if lang == 'py':
                for code in code_list:
                    try: 
                        encoder = PY_TO_AST_ENCODER(code)
                        ast = encoder.create_ast()
                        yield ast
                    except Exception as e:
                        self.logger.warning(f"This code is not interpreted in Python or something went wrong. { e }")
                        yield None
                
            elif lang == 'c++':
                for code in code_list:
                    try: 
                        encoder = CPP_TO_AST_ENCODER(code)
                        ast = encoder.create_ast()
                        yield ast
                    except Exception as e:
                        self.logger.warning(f"This code doesn't compile in C++ or something went wrong. { e }")
                        yield None     
        else:
            for code in code_list:
                yield None
        
    def gen_ast_list(self, lang: str, code_list: list):
        ast_list = list()
        
        for ast in self.gen_ast(lang, code_list):
            ast_list.append(ast)
            
        return ast_list
                
    def encode(self):
        
        problem_names, submissions = self.take_submissions()
            
        for name in problem_names:   
            self.logger.info(f"Work with {name} problem") 
            for lang, sub in submissions[name].items():
                self.logger.info(f"Start work on {lang} code") 
                submissions[name][lang]['ast'] = self.gen_ast_list(lang, sub['code'])
        
        return submissions

