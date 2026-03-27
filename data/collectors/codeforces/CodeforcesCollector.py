import base64
from core.models import Submission
from data.collectors.codeforces.CodeforcesRequest import CFRequests
from utils.file_utils import code_type_definition, use_comments
import sqlite3
from core.config import DB_PATH

class CodeforcesCollector:
    
    def __init__(self, cf_key: str, cf_secret: str):
        self.cf_key = cf_key
        self.cf_secret = cf_secret
        self.data = None
    
    def _convert_to_utf8(self, sample_string: str):
        sample_string_bytes = sample_string.encode("utf-8")
        decoded_bytes = base64.b64decode(sample_string_bytes)
        decoded_string = decoded_bytes.decode("utf-8")
        return decoded_string
    
    def _request(self, contest_id : str, group_id : str ) -> list:
        cf = CFRequests(cf_key=self.cf_key, cf_secret=self.cf_secret)
        contest = cf.contest(cf)
        data = contest.status(contestId_=contest_id, groupCode_=group_id, from_=None, count_=None, asManager_="true", includeSources_="true")
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
                solution_id = submition.get("id")
                contest_id = submition.get("contestId")
                author_id = submition.get("author", {}).get("participantId")
                author_name = submition.get("author", {}).get("members", [{}])[0].get("name")
                problem_name = submition.get("problem", {}).get("name")
                problem_index = submition.get("problem", {}).get("index")
                code_base64 = submition.get("sourceBase64")
                programming_Language = submition.get("programmingLanguage")
                verdict = submition.get("verdict")
                comments = 0
                
                code = self._convert_to_utf8(code_base64) if code_base64 else None
                programming_Language = code_type_definition(programming_Language) if programming_Language else None

                if code and programming_Language:
                    comments = use_comments(code, programming_Language)
                
                new_submition = Submission(
                    solution_id, 
                    contest_id, 
                    author_id, 
                    author_name,
                    problem_name, 
                    problem_index, 
                    code, 
                    programming_Language,
                    comments,
                    verdict
                )
                yield new_submition
                
            except Exception as e:
                print(f"Critical eror: You don't have manager rights\nCan't catch {e}")

    def fetch_submissions(self, contest_id : str, group_id : str):
        """Заполнение бд Submision"""
        self.data = self._request(contest_id, group_id)
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY,
                contest_id INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                author_name TEXT,
                problem_name TEXT NOT NULL,
                problem_index TEXT NOT NULL,
                code TEXT NOT NULL,
                language TEXT NOT NULL,
                comments INTEGER,
                verdict TEXT NOT NULL
            )
            """)

            for sub in self.get_submissions():
                cursor.execute("""
                                INSERT OR IGNORE INTO submissions 
                                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (
                                sub.solution_id,
                                sub.contest_id,
                                sub.user_id,
                                sub.user_name,
                                sub.problem_name,
                                sub.problem_index,
                                sub.code,
                                sub.language,
                                sub.comment,
                                sub.verdict
                                ))
            
        
    