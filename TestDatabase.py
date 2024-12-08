import unittest
import sqlite3
from Database import Database

conn = sqlite3.connect('sql.db')
cursor = conn.cursor()

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("test", ["name", "age"])
        cursor.execute("DROP TABLE IF EXISTS test")
        conn.commit()
        self.db.query("CREATE TABLE IF NOT EXISTS test(id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")

    def test_query(self):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        self.assertIn("test", tables)
    
    def test_select_table(self):
        cursor.execute("INSERT INTO test (name, age) VALUES ('Jake', 22), ('John', 34), ('Jasmine', 19)")
        conn.commit()
        rows = self.db.select_table()[1]
        self.assertEqual(len(rows), 3)

    def test_select_table_ordered(self):
        cursor.execute("INSERT INTO test (name, age) VALUES ('Jake', 22), ('John', 34), ('Jasmine', 19)")
        conn.commit()
        rows = self.db.select_table('age')[1]
        self.assertEqual(rows[0][0], 3)
    
    def test_select_column(self):
        cursor.execute("INSERT INTO test (name, age) VALUES ('Jake', 22), ('John', 34), ('Jasmine', 19)")
        conn.commit()
        names = self.db.select_column('name')
        self.assertEqual(names, ['Jake', 'John', 'Jasmine'])

    def test_select_row(self):
        cursor.execute("INSERT INTO test (name, age) VALUES ('Jake', 22), ('John', 34), ('Jasmine', 19)")
        conn.commit()
        row = self.db.select_row('name', 'Jasmine')
        self.assertEqual(row, (3, 'Jasmine', 19))

    def test_insert_table(self):
        self.db.insert_table(['Jake', 22])
        cursor.execute("SELECT name FROM test WHERE id = 1")
        names = cursor.fetchall()
        self.assertEqual(names[0][0], "Jake")

if __name__ == '__main__':
    unittest.main()