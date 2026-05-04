import numpy as np 
from core.models import Candidate, SimilarityResult


class Ranker:
    def rate(self, results):
        
        features = np.array([r.to_list_features() for r in results])
        weights = np.array([0.80, 0.15, 0.05])
        coef = 1 / (weights[1] + weights[2])
        
        rank = features @ weights
        candidates = []
        for r, c in zip(results, rank):
            score = c
            if r.ast_score == 0.: 
                score *= coef
            cand = Candidate(r.subID_a, r.subID_b, c)
            
            candidates.append(cand)
        
        return candidates
        
        