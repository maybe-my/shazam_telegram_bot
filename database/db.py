import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `telegram_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `telegram_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, username):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`telegram_id`, `username`) VALUES (?,?)", (user_id,'@' + username,))
        return self.conn.commit()

    def add_record(self, user_id, operation, value):
        """Создаем запись о доходах/расходах"""
        self.cursor.execute("INSERT INTO `records` (`users_id`, `operation`, `value`) VALUES (?, ?, ?)",
            (self.get_user_id(user_id),
            operation == "+",
            value))
        return self.conn.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()