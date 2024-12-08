from Database import Database

class Sections(Database):
    def __init__(self, recreate = True):
        super().__init__("sections", ["name", "description"])
        if recreate:
            self.delete_table()
            self.create_table()
            self.seed_table()

    def create_table(self):
        q = '''
        CREATE TABLE IF NOT EXISTS sections(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL
        )
        '''
        self.query(q, commit=True)
        self.log.write("Section Tables Created!")
    
    def seed_table(self):
        q = '''
        INSERT INTO sections (name, description)
        VALUES
            ('Electronics', 'This contains all electronic gadgets, like phone and laptops.'),
            ('Food', 'All food including fresh, canned, and preserved produce.'),
            ('Clothing', 'Examples include footwear, accessories, or other clothes.'),
            ('Furniture', 'Furniture like tables, chairs, and sofas.')
        '''
        self.query(q, commit=True)
        self.log.write("Section Tables Seeded!")

    def fetch_id(self, section):
        row = self.select_row('name', section)
        self.log.write("Section ID Fetched!")
        return row[0] if row else None