import sqlite3
from core.config import DB_PATH

class SimilarityCandidateRepository:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def save_many(self, candidate):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidate( 
                    sub_id_a INTEGER,
                    sub_id_b INTEGER,
                    score INTEGER
                )
            """)

            cursor.executemany("""
                INSERT INTO candidate (
                    sub_id_a,
                    sub_id_b,
                    score
                )
                VALUES (?, ?, ?)
            """, [
                (
                    c.subID_a,
                    c.subID_b,
                    c.score
                )
                for c in candidate
            ])
