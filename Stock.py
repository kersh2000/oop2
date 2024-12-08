from Database import Database

class Stock(Database):
    def __init__(self, recreate = True):
        super().__init__("stock", ["item_id", "quantity", "edited_at"])
        if recreate:
            self.delete_table()
            self.create_table()
            self.seed_table()
    
    def create_table(self):
        q = '''
        CREATE TABLE IF NOT EXISTS stock(
            id INTEGER PRIMARY KEY,
            item_id INTEGER UNIQUE,
            quantity INTEGER NOT NULL DEFAULT 0,
            edited_at TEXT NOT NULL DEFAULT CURRENT_DATE,
            FOREIGN KEY (item_id)
                REFERENCES items (id)
                    ON DELETE CASCADE
        )
        '''
        self.query(q, commit=True)
        self.log.write("Stock Tables Created!")
    
    def seed_table(self):
        q = '''
        INSERT INTO stock (item_id, quantity, edited_at)
        VALUES
            (1, 11, '2024-11-18'),
            (2, 8, '2024-12-02'),
            (5, 100, '2024-11-27'),
            (7, 25, '2024-11-22'),
            (8, 32, '2024-11-29'),
            (10, 3, '2024-10-02')
        '''
        self.query(q, commit=True)
        self.log.write("Stock Tables Seeded!")

    def select_table(self):
        q = '''
        SELECT 
            stock.id,
            items.name as item,
            sections.name as section,
            quantity,
            edited_at as last_edited
        FROM
            stock,
            sections,
            items
        WHERE
            stock.item_id = items.id
            AND items.section_id = sections.id
        ORDER BY date(edited_at) DESC
        '''
        result = self.query(q, force_cols=True)
        self.log.write("Stock Tables Selected!")
        return result

    def update_stock(self, item_name, new_quantity):
        q = '''
        UPDATE stock
        SET 
            quantity = ?,
            edited_at = CURRENT_DATE
        WHERE stock.item_id = (
            SELECT id
            FROM items
            WHERE name = ?
        )
        '''
        self.query(q, [new_quantity, item_name], True)
        self.log.write("Stock Tables Updated!")