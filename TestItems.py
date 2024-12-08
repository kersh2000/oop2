import unittest
import sqlite3
from Items import Items

conn = sqlite3.connect('sql.db')
cursor = conn.cursor()

class TestItems(unittest.TestCase):
    def setUp(self):
        self.items = Items(True)

    def test_create_table(self):
        cursor.execute("DROP TABLE IF EXISTS items")
        conn.commit()
        self.items.create_table()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        self.assertIn("items", tables)
    
    def test_select_table(self):
        cols = self.items.select_table()[0]
        self.assertIn('section', cols)
    
    def test_fetch_id(self):
        id = self.items.fetch_id('Laptop')
        cursor.execute("SELECT id FROM items WHERE name = 'Laptop'")
        real_id = cursor.fetchone()
        self.assertEqual(id, real_id[0])

if __name__ == '__main__':
    unittest.main()