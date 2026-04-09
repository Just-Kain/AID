from typing import Any

class Submission:
    def __init__(self, solution_id: int, contest_id: int, user_id: int, user_name: str, problem_name: str, \
        problem_index: str, code: str, language: str, comment: str, verdict: str, points):
        self.solution_id = solution_id
        self.contest_id = contest_id
        self.user_id = user_id
        self.user_name = user_name
        self.problem_index = problem_index
        self.problem_name = problem_name
        self.code = code
        self.language = language
        self.verdict = verdict
        self.comment = comment
        self.points = points

class FeatureVector:
    def __init__(self, solution_id: int, ast: Any, code: str, length: int):
        self.solution_id = solution_id
        self.ast = ast
        self.code = code
        self.length = length
    
class SimilarityResult:
    def __init__(self, subID_a: int, subID_b: int, ast_score: float, differ: str, diff_score: float, delta_len: float):
        self.subID_a = subID_a
        self.subID_b = subID_b
        self.ast_score = ast_score
        self.differ = differ
        self.diff_score = diff_score
        self.delta_len = delta_len
    
    def to_list_features(self):
        return [self.ast_score, self.diff_score, self.delta_len]  
        
class Candidate:
    def __init__(self, subID_a: int, subID_b: int, score: float):
        self.subID_a = subID_a
        self.subID_b = subID_b
        self.score = score
        # self.confidence = confidence