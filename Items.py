from Database import Database

class Items(Database):
    def __init__(self, recreate = True):
        super().__init__("items", ["name", "section_id", "expiration_date"])
        if recreate:
            self.delete_table()
            self.create_table()
            self.seed_table()

    def create_table(self):
        q = '''
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            section_id INTEGER NOT NULL,
            expiration_date TEXT,
            FOREIGN KEY (section_id)
                REFERENCES sections (id)
                    ON DELETE CASCADE
        )
        '''
        self.query(q, commit=True)
        self.log.write("Items Tables Created!")
    
    def seed_table(self):
        q = '''
        INSERT INTO items (name, section_id, expiration_date)
        VALUES
            ('Laptop', 1, null),
            ('Iphone 12', 1, null),
            ('DVD Player', 1, null),
            ('Pasta', 2, '2026-07-01'),
            ('Beans', 2, '2025-09-11'),
            ('Cheddar Cheese', 2, '2025-02-05'),
            ('Socks', 3, null),
            ('Hat', 3, null),
            ('Wooden Chair', 4, null),
            ('Leather Couch', 4, null)
        '''
        self.query(q, commit=True)
        self.log.write("Items Tables Seeded!")

    def select_table(self):
        q = '''
        SELECT 
            items.id,
            items.name,
            sections.name as section,
            expiration_date
        FROM
            items,
            sections
        WHERE
            items.section_id = sections.id
        '''
        results = self.query(q, force_cols=True)
        self.log.write("Items Table Selected!")
        return results
    
    def fetch_id(self, item):
        row = self.select_row('name', item)
        self.log.write("Items ID Fetched!")
        return row[0] if row else None