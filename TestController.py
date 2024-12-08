import unittest
import sqlite3
from Controller import Controller

conn = sqlite3.connect('sql.db')
cursor = conn.cursor()

class TestController(unittest.TestCase):
    def setUp(self):
        self.ctr = Controller(True)

    def test_add_section_empty(self):
        response = self.ctr.add_section('', 'nothing')
        self.assertEqual(response, "Section must have a name!")
    
    def test_add_section_exists(self):
        response = self.ctr.add_section('Electronics', "gadgets")
        self.assertEqual(response, "Section already exists!")

    def test_add_item_empty(self):
        response = self.ctr.add_item('', 'Electronics', '2024-11-10')
        self.assertEqual(response, "Item must have a name!")

    def test_add_item_section(self):
        response = self.ctr.add_item('Gold', 'Metals', '2024-11-10')
        self.assertEqual(response, "Section does not exist!")

    def test_add_item_exists(self):
        response = self.ctr.add_item('Iphone 12', 'Electronics', '2024-11-10')
        self.assertEqual(response, "Item already exists!")

    def test_add_stock_zero(self):
        response = self.ctr.add_stock('Laptop', 0)
        self.assertEqual(response, "Quantity cannot be 0!")

    def test_add_stock_item(self):
        response = self.ctr.add_stock('Apples', 12)
        self.assertEqual(response, "Item does not exist!")

    def test_add_stock_over(self):
        response = self.ctr.add_stock('Laptop', -100)
        self.assertEqual(response, "Quantity over stock amount!")

    def test_add_stock_new(self):
        response = self.ctr.add_stock('DVD Player', -5)
        self.assertEqual(response, "Cannot remove stock on new item!")

if __name__ == '__main__':
    unittest.main()