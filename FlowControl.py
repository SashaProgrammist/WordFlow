import sqlite3
from random import choice


class FlowControl:
    def __init__(self, name_db : str):
        self.conn = sqlite3.connect(name_db)
        self.cursor = self.conn.cursor()

        self.conn.commit()

    def getAllLanguages(self):
        languages = self.cursor.execute("""
        SELECT DISTINCT language
        FROM phrases;
        """).fetchall()

        return [lang[0] for lang in languages]

    def getAnyPhrase(self, language: str):
        result = self.cursor.execute(f"""
        SELECT id, phrase_set_id, phrase
        FROM phrases
        WHERE language='{language}';
        """).fetchall()

        result = choice(result)

        result = {
            "id" : result[0],
            "phrase_set_id" : result[1],
            "phrase" : result[2]
        }

        return result

    def getAnyTranslate(self, language: str, set_id: int):
        result = self.cursor.execute(f"""
        SELECT id, phrase, language
        FROM phrases
        WHERE phrase_set_id={set_id} AND language!='{language}';
        """).fetchone()

        result = {
            "id" : result[0],
            "phrase" : result[1],
            "language" : result[2]
        }

        return result


    def __del__(self):
        self.conn.close()
