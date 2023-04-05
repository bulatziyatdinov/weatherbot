import sqlite3


# Класс БД
class Database:
    def __init__(self, db_name):
        try:
            self.con = sqlite3.connect(db_name)
            self.create_users_table()
        except Exception as ex:
            print('Ошибка на этапе создания БД!', ex)

    # Создание таблицы users
    def create_users_table(self):
        try:
            with self.con as cur:
                cur.execute("""CREATE TABLE IF NOT EXISTS users (
                                   id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                   city CHAR NOT NULL DEFAULT NONE,
                                   nums_using INTEGER NOT NULL DEFAULT 0
                                );"""
                            )
        except Exception as ex:
            print('Ошибка на этапе создания таблицы в БД!', ex)

    # Добавляет пользователя в БД
    def add_user_to_db(self, user_id):
        with self.con as cur:
            t = cur.execute(f"""SELECT id FROM users WHERE id = {user_id}""").fetchone()
            if not t:
                cur.execute(f"""INSERT INTO users (id) VALUES ({user_id})""")

    # Увеличивает кол-во использований бота в БД
    def update_nums_of_using(self, user_id):
        with self.con as cur:
            n = cur.execute(f"""SELECT nums_using FROM users WHERE id = {user_id}""").fetchone()
            cur.execute(f"""UPDATE users SET nums_using = '{int(n[0]) + 1}' WHERE id = '{user_id}'""")

    # Установка города пользователю
    def set_user_city(self, user_id, city):
        # Не пустая ли строка
        if not city:
            return False
        # Проверка на установку города
        try:
            with self.con as cur:
                cur.execute(f"""UPDATE users SET city = '{city}' WHERE id = '{user_id}'""")
            return True
        except Exception as ex:
            print('Ошибка в установки города', ex)
            return False

    # Возврат названия города пользователя
    def get_user_city(self, user_id) -> str | None:
        try:
            with self.con as cur:
                res = cur.execute(f"""SELECT city FROM users WHERE id = {user_id}""").fetchone()[0]
                return res
        except Exception as ex:
            print('Ошибка в запросе города', ex)

    # Возвращает кол-во использований бота пользователем
    def get_user_nums(self, user_id) -> int | None:
        try:
            with self.con as cur:
                res = cur.execute(f"""SELECT nums_using FROM users WHERE id = {user_id}""").fetchone()[0]
            return res
        except Exception as ex:
            print('Ошибка в запросе nums', ex)

    # Удаляет пользователя
    def delete_user(self, user_id):
        pass
