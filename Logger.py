import os
import os.path
from datetime import date, datetime

class Logger:
    def __init__(self, name):
        formatted_name = f"{name}-{str(date.today())}.log"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.local_path = formatted_name
        self.__path = os.path.join(current_dir, formatted_name)

    def __create_file(self, msg):
        file = open(self.local_path, "w")
        file.write(f"{msg}\n")
        file.close()

    def __append_file(self, msg):
        file = open(self.local_path, "a")
        file.write(f"{msg}\n")
        file.close()

    def write(self, msg):
        message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {msg}"
        if os.path.isfile(self.__path):
            self.__append_file(message)
        else:
            self.__create_file(message)