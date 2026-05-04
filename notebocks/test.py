from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "storage" / "aid.db"

submissions = dict()

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT problem_name FROM submissions')
    problem_names = cursor.fetchall()
    problem_names = [x[0] for x in problem_names]
    
    cursor.execute('SELECT DISTINCT language FROM submissions')
    languages = cursor.fetchall()
    languages = [x[0] for x in languages]
    
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


for name in problem_names:
    
    for lang, sub in submissions[name].items():
        
        if lang == 'c++':
            print('c++')
            print(sub['id'])
        elif lang == 'py':
            print('py')
            print(sub['id'])
        else:
            print('lol')
            print(sub['id'])

if __name__ == "__main__":
    from rich import print

    print("Посетите [link=https://example.com]наш сайт[/link]!")
