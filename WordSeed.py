import sqlite3
import pandas as pd
import logging


class WordSeed:
    def __init__(self, name_db):
        self.conn = sqlite3.connect(name_db)
        self.cursor = self.conn.cursor()

        self.conn.commit()

        self._apdate_metods = {
            "xlsx": self.__apdate_extension_xlsx,
        }

    def apdate(self, name_sours):
        extension = name_sours.split(".")[-1]

        metod = self._apdate_metods.get(extension)

        if metod:
            metod(name_sours)
        else:
            logging.warning(f"unknown extension {extension}")

    def __del__(self):
        self.conn.close()

    def __apdate_extension_xlsx(self, name_sours):
        # Создание таблицы (если не существует)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Phrases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase_set_id INTEGER NOT NULL,
                language TEXT NOT NULL,
                phrase TEXT NOT NULL,
                UNIQUE (phrase_set_id, language)
            );
        """)
        logging.info("[INFO] Таблица проверена/создана.")

        # Чтение данных из Excel
        df = pd.read_excel(name_sours)
        logging.info("[INFO] Данные из Excel успешно загружены.")

        # Проверка структуры данных
        expected_columns = {'id', 'lang', 'text'}
        if not expected_columns.issubset(df.columns):
            logging.warning(f"Файл Excel должен содержать столбцы: {expected_columns}")
            raise ValueError(f"Файл Excel должен содержать столбцы: {expected_columns}")

        # Добавление данных в таблицу
        for _, row in df.iterrows():
            try:
                self.cursor.execute(f"""
                    INSERT OR IGNORE INTO Phrases (phrase_set_id, language, phrase)
                    VALUES (?, ?, ?);
                """, (row['id'], row['lang'], row['text']))
            except Exception as e:
                logging.warning(f"[ERROR] Ошибка при добавлении строки: {row}. Ошибка: {e}")

        # Сохранение изменений и закрытие соединения
        self.conn.commit()
        print("[INFO] Данные успешно добавлены в базу данных.")

