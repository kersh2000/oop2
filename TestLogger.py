import os
import os.path
from datetime import date, datetime
import unittest
from Logger import Logger
from Sections import Sections

class TestLogger(unittest.TestCase):
    def test_create_file(self):
        log = Logger('test1')
        filepath = f"test1-{str(date.today())}.log"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, filepath)
        log.write("Test Message")
        self.assertTrue(os.path.exists(path))

    def test_append_file(self):
        log = Logger('test2')
        filepath = f"test2-{str(date.today())}.log"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, filepath)
        log.write("Test Message")
        size1 = os.path.getsize(path)
        log.write("Test Message 2")
        size2 = os.path.getsize(path)
        self.assertGreater(size2, size1)

    def test_write(self):
        log = Logger('test3')
        filepath = f"test3-{str(date.today())}.log"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, filepath)
        log.write("Test Message")
        log.write("Test Message 33!")
        message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Test Message 33!\n"
        with open(path, "r") as file:
            lastline = (list(file)[-1])
        self.assertEqual(message, lastline)
    
    def test_logger_inherited(self):
        sections = Sections(True)
        filepath = f"system-{str(date.today())}.log"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, filepath)
        message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Section Tables Seeded!\n"
        with open(path, "r") as file:
            lastline = (list(file)[-1])
        self.assertEqual(message, lastline)

if __name__ == '__main__':
    unittest.main()