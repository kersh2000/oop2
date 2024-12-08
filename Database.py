import sqlite3
from Logger import Logger

class Database:
    def __init__(self, table_name, cols):
        self.table_name = table_name
        self.cols = cols
        self.log = Logger("system")
        self.__query_log = Logger("sql")

    def connect_to_db(self):
        conn = sqlite3.connect('sql.db')
        cursor = conn.cursor()
        return (conn, cursor)
    
    def query(self, query, binds = [], commit=False, force_cols=False):
        conn, cursor = self.connect_to_db()
        cursor.execute(query, binds)

        if commit:
            conn.commit()

        rows = cursor.fetchall()
        cols = [description[0] for description in cursor.description] if rows or force_cols else []

        cursor.close()
        self.__query_log.write(f"QUERY: \n{query}") if len(binds) > 0 else self.__query_log.write(f"QUERY: \n{query}\nBINDS: {binds}")

        return cols, rows
    
    def create_table(self):
        raise NotImplementedError

    def seed_table(self):
        raise NotImplementedError
    
    def delete_table(self):
        self.query('DROP TABLE IF EXISTS {}'.format(self.table_name), commit=True)

    def select_table(self, order_col = 'id', order = 'ASC'):
        return self.query(f'SELECT * FROM {self.table_name} ORDER BY {order_col} {order}', force_cols=True)
    
    def select_column(self, col):
        rows = self.query(f'SELECT {col} FROM {self.table_name}')[1]
        row = [col[0] for col in rows]
        return row
    
    def select_row(self, col, val):
        row = self.query(f'SELECT * FROM {self.table_name} WHERE {col} = ?', [val])[1]
        return row[0] if row else []
    
    def insert_table(self, row):
        columns = ', '.join(self.cols)
        binds = ', '.join("?" * len(row))
        self.query(f'INSERT INTO {self.table_name} ({columns}) VALUES ({binds})', row, True)

    def insert_table(self, row):
        columns = ', '.join(self.cols)
        binds = ', '.join("?" * len(row))
        self.query(f'INSERT INTO {self.table_name} ({columns}) VALUES ({binds})', row, True)