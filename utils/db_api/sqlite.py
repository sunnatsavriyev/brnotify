import datetime
import sqlite3


class Database:
    def __init__(self, path_to_db):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, first_name: str, last_name: str, tg_id: str, birthday: datetime.date ):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO TgUser(first_name, last_name, tg_id, birthday) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(first_name, last_name, tg_id, birthday), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM TgUser
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, tg_id):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM TgUser WHERE tg_id = ?"

        return self.execute(sql, parameters=(tg_id, ), fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM TgUser;", fetchone=True)

    def update_user_data(self, month, day, tg_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE TgUser SET birthday=? WHERE id=?
        """
        date = datetime.date(year=1900, month=month, day=day)
        return self.execute(sql, parameters=(date, tg_id), commit=True)

    def delete_user(self, tg_id):
        self.execute("DELETE FROM TgUser WHERE tg_id=?", parameters=(tg_id, ), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM TgUser WHERE TRUE", commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")