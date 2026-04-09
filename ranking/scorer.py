import numpy as np 
from core.models import Candidate

class Ranker:
    def rate(self, results):
        
        features = np.array([r.to_list_features() for r in results])
        weights = np.array([0.4, 0.55, 0.05])
        
        rank = features @ weights
        candidates = []
        for r, c in zip(results, rank):
            cand = Candidate(r.subID_a, r.subID_b, c)
            candidates.append(cand)
        
        return candidates
        
        