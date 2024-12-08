import unittest
import sqlite3
from Stock import Stock
from Items import Items

conn = sqlite3.connect('sql.db')
cursor = conn.cursor()

class TestStock(unittest.TestCase):
    def test_update_stock(self):
        stock = Stock(True)
        items = Items(True)
        item = "Iphone 12"
        new_amount = 5
        stock.update_stock(item, new_amount)
        item_id = items.fetch_id(item)
        cursor.execute("SELECT quantity FROM stock WHERE item_id = {}".format(item_id))
        amount = cursor.fetchone()[0]
        self.assertEqual(new_amount, amount)

if __name__ == '__main__':
    unittest.main()