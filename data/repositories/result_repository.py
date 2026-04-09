import sqlite3
from core.config import DB_PATH

class SimilarityResultRepository:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def save_many(self, results):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS similarity_results ( 
                    sub_id_a INTEGER,
                    sub_id_b INTEGER,
                    ast_score INTEGER,
                    differ TEXT,
                    diff_score INTEGER,
                    delta_len INTEGER
                )
            """)

            cursor.executemany("""
                INSERT INTO similarity_results (
                    sub_id_a,
                    sub_id_b,
                    ast_score,
                    differ,
                    diff_score,
                    delta_len
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (
                    r.subID_a,
                    r.subID_b,
                    r.ast_score,
                    r.differ,
                    r.diff_score,
                    r.delta_len
                )
                for r in results
            ])
