from difflib import SequenceMatcher, Differ
from zss import simple_distance
from itertools import combinations
from core.models import SimilarityResult
from core.config import DB_PATH
import sqlite3
from multiprocessing import Pool, cpu_count
from itertools import combinations
from functools import lru_cache
from difflib import SequenceMatcher
from core.models import SimilarityResult

def compare_pair(args):
    
        a, b = args

        # if a.ast == None or b.ast == None:
        #     ast_score = 10e10
        # else:
            
        #     size_a = len(str(a.ast))
        #     size_b = len(str(b.ast))

        #     if abs(size_a - size_b) > 0.2 * max(size_a, size_b):
        #         ast_score = 10e10
        #     else:
        #         ast_score = simple_distance(a.ast, b.ast)
        
        if a.ast == None or b.ast == None:
            simple_ast_score = 0.
        else: 
            simple_ast_score = SequenceMatcher(None, str(a.ast), str(b.ast)).ratio()

        # differ = Differ()
        # diff = "".join(list(differ.compare(a.code, b.code)))
        
        matcher = SequenceMatcher(None, a.code, b.code)
        ratio = matcher.ratio()
        
        diff = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != "equal":
                diff.append(
                    f"{tag}: A[{i1}:{i2}] -> B[{j1}:{j2}]"
                )

        diff = "\n".join(diff)
    
        delta_len = 1 - abs(a.length - b.length) / max(a.length, b.length)

        return SimilarityResult(
            subID_a=a.solution_id,
            subID_b=b.solution_id,
            ast_score=simple_ast_score,
            differ=diff,
            diff_score=ratio,
            delta_len=delta_len
        )


class SimilarityEngine:
    def __init__(self):
        self.results = []

    def extract(self, features):
        results = []

        for problem in features.keys():
            print(f"DEBUG: start work with {problem}")
            for lang in features[problem].keys():
                print(f"DEBUG: start work with {lang}")
                vectors = features[problem][lang]
                
                pairs = list(combinations(vectors, 2))
                
                with Pool(cpu_count()) as pool:
                    sub_results = pool.map(compare_pair, pairs)
                    
                results.extend(sub_results)

        self.results = results
        return results
    
    
