import sqlite3


class FlowControl:
    def __init__(self, name_db):
        self.conn = sqlite3.connect(name_db)
        self.cursor = self.conn.cursor()

        self.conn.commit()

    def getAllLanguages(self):
        languages = self.cursor.execute("""
        SELECT DISTINCT language
        FROM phrases;
        """).fetchall()

        return [lang[0] for lang in languages]

    def __del__(self):
        self.conn.close()
