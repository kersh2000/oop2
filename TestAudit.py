import unittest
import sqlite3
from Audit import Audit

conn = sqlite3.connect('sql.db')
cursor = conn.cursor()

class TestAudit(unittest.TestCase):
    def test_select_table(self):
        audit = Audit(True)
        rows = audit.select_table()[1]
        cursor.execute("SELECT * FROM audit")
        real_rows = cursor.fetchall()
        self.assertEqual(len(rows), len(real_rows))

if __name__ == '__main__':
    unittest.main()