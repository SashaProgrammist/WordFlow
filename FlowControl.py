import sqlite3


class FlowControl:
    def __init__(self, name_db):
        self.conn = sqlite3.connect(name_db)
        self.cursor = self.conn.cursor()

        self.conn.commit()


    def __del__(self):
        self.conn.close()
