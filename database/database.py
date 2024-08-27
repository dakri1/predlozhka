import sqlite3
from typing import List, Optional

class Admin:
    def __init__(self, id: int, user_id: str):
        self.id = id
        self.user_id = user_id

    def __repr__(self):
        return f"Admin(id={self.id}, user_id='{self.user_id}')"

class User:
    def __init__(self, id: int, user_id: str, username: str, message_count, reset_date):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.message_count = message_count
        self.reset_date = reset_date

    def __repr__(self):
        return f"User(id={self.id}, user_id='{self.user_id}', username='{self.username}', message_count={self.message_count}, reset_data={self.reset_date})"

class AdminRepository:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def create_admin(self, user_id: str) -> Admin:
        self.cursor.execute('INSERT INTO admin (user_id) VALUES (?)', (user_id,))
        self.connection.commit()
        return Admin(self.cursor.lastrowid, user_id)

    def get_admin(self, user_id: str) -> Optional[Admin]:
        self.cursor.execute('SELECT * FROM admin WHERE user_id = ?', (user_id,))
        row = self.cursor.fetchone()
        return Admin(*row) if row else None

    def get_all_admins(self) -> List[Admin]:
        self.cursor.execute('SELECT * FROM admin')
        rows = self.cursor.fetchall()
        return [Admin(*row) for row in rows]

    def delete_admin(self, user_id: str) -> bool:
        self.cursor.execute('DELETE FROM admin WHERE user_id = ?', (user_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.connection.close()

class UserRepository:
    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()


    def create_user(self, user_id: str, username: str) -> User:
        self.cursor.execute('INSERT INTO user (user_id, username) VALUES (?, ?)', (user_id, username))
        self.connection.commit()
        return User(self.cursor.lastrowid, user_id, username, 0, '')

    def get_user(self, user_id: str) -> Optional[User]:
        self.cursor.execute('SELECT * FROM user WHERE user_id = ?', (user_id,))
        row = self.cursor.fetchone()
        return User(*row) if row else None

    def get_all_users(self) -> List[User]:
        self.cursor.execute('SELECT * FROM user')
        rows = self.cursor.fetchall()
        return [User(*row) for row in rows]

    def change_username(self, user_id: str, username: str) -> Optional[User]:
        self.cursor.execute('UPDATE user SET username = ? WHERE user_id = ?', (username, user_id))
        self.connection.commit()
        return self.get_user(user_id)

    def delete_user(self, user_id: int) -> bool:
        self.cursor.execute('DELETE FROM user WHERE id = ?', (user_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def increment_message_count(self, user_id: str) -> Optional[User]:
        """Увеличить счетчик отправленных сообщений на 1."""
        self.cursor.execute('UPDATE user SET message_count = message_count + 1 WHERE user_id = ?', (user_id,))
        self.connection.commit()
        return self.get_user(user_id)

    def set_reset_date(self, user_id: str, date: str) -> Optional[User]:
        """Установить указанную дату."""
        self.cursor.execute('UPDATE user SET reset_date = ? WHERE user_id = ?', (date, user_id))
        self.connection.commit()
        return self.get_user(user_id)

    def reset_message_count_and_date(self, user_id: str) -> Optional[User]:
        self.cursor.execute('UPDATE user SET message_count = 0, reset_date = "" WHERE user_id = ?', (user_id,))
        self.connection.commit()
        return self.get_user(user_id)


    def get_reset_date(self, user_id: str) -> Optional[str]:
        self.cursor.execute('SELECT reset_date FROM user WHERE user_id = ?', (user_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_message_count(self, user_id: str) -> Optional[int]:
        self.cursor.execute('SELECT message_count FROM user WHERE user_id = ?', (user_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def close(self):
        self.connection.close()
