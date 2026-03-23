import base64
from core.models import Submission
from data.collectors.codeforces.CodeforcesRequest import CFRequests
from utils.file_utils import code_type_definition
import sqlite3
import os
from core.config import DB_PATH

class CodeforcesCollector:
    
    def __init__(self, cf_key: str, cf_secret: str):
        self.cf_key = cf_key
        self.cf_secret = cf_secret
        self.data = None
    
    def _convert_to_utf8(sample_string: str):
        sample_string_bytes = sample_string.encode("utf-8")
        decoded_bytes = base64.b64decode(sample_string_bytes)
        decoded_string = decoded_bytes.decode("utf-8")
        return decoded_string
    
    def _request(self, contest_id : str, group_id : str ) -> list:
        cf = CFRequests(cf_key=self.cf_key, cf_secret=self.cf_secret)
        contest = cf.contest(cf)
        data = contest.status(contest_id=contest_id, groupCode_=group_id)
        if data['status'] != 'OK':
            print(f"WARNING! CFRequest failrule with status: {data['status']}\n {data['comment']}")
            raise RuntimeError
        else:
            return data['result']

    
    def get_submissions(self):
        """
        Генератор submition
        """
        for submition in self.data:
            try:
                solution_id = submition["id"]
                author_id = submition["author"]["participantId"]
                author_name = submition["author"]["members"][0]["name"]
                problem_name = submition["problem"]["name"]
                problem_index = submition["problem"]["index"]
                code_base64 = submition["sourceBase64"]
                programming_Language = submition["programmingLanguage"]
                
                code = self._convert_to_utf8(code_base64)
                programming_Language = code_type_definition(programming_Language)
                
                new_submition = Submission(solution_id, author_id, author_name/
                                           problem_name, problem_index, code, programming_Language)
                yield new_submition
                
            except:
                print("file with soluthion not found or somthing gone wrong")

    def fetch_submissions(self, contest_id : str, group_id : str):
        """Заполнение бд Submision"""
        self.data = self._request(contest_id, group_id)

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER,
                author_id INTEGER,
                author_name TEXT,
                problem_name TEXT,
                problem_index TEXT,
                code TEXT,
                language TEXT
            )
            """)

            for sub in self.get_submissions():
                cursor.execute("""
                INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    sub.solution_id,
                    sub.user_id,
                    sub.user_name,
                    sub.problem_name,
                    sub.problem_index,
                    sub.code,
                    sub.language
                ))
            
        
    