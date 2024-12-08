from Database import Database

class Audit(Database):
    def __init__(self, recreate = True):
        super().__init__("audit", ["item_name", "quantity_change", "created_at"])
        if recreate:
            self.delete_table()
            self.create_table()
    
    def create_table(self):
        q = '''
        CREATE TABLE IF NOT EXISTS audit(
            id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            quantity_change INTEGER NOT NULL,
            created_at TEXT
        )
        '''
        self.query(q, commit=True)
        self.log.write("Audit Tables Selected!")