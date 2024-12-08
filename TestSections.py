import unittest
import sqlite3
from Sections import Sections

conn = sqlite3.connect('sql.db')
cursor = conn.cursor()

class TestSections(unittest.TestCase):
    def setUp(self):
        self.sections = Sections(True)

    def test_create_table(self):
        cursor.execute("DROP TABLE IF EXISTS sections")
        conn.commit()
        self.sections.create_table()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        self.assertIn("sections", tables)
    
    def test_init_seed(self):
        cursor.execute("SELECT * FROM sections")
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 4)

    def test_fetch_id(self):
        id = self.sections.fetch_id('Electronics')
        cursor.execute("SELECT id FROM sections WHERE name = 'Electronics'")
        real_id = cursor.fetchone()
        self.assertEqual(id, real_id[0])

if __name__ == '__main__':
    unittest.main()