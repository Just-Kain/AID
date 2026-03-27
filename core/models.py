from typing import Any

class Submission:
    def __init__(self, solution_id: int, contest_id: int, user_id: int, user_name: str, problem_name: str, problem_index: str, code: str, language: str, comment: str, verdict: str):
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

class SimilarityResult:
    def __init__(self, sub_a: Submission, sub_b: Submission, ast_score: float, diff_score: float, delta_len: float):
        self.sub_a = sub_a
        self.sub_b = sub_b
        self.ast_score = ast_score
        self.diff_score = diff_score
        self.delta_len = delta_len
        
class Candidate:
    def __init__(self, sub_a: Submission, sub_b: Submission, score: float, confidence: float):
        self.sub_a = sub_a
        self.sub_b = sub_b
        self.score = score
        self.confidence = confidence