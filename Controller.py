from datetime import date
from Audit import Audit
from Sections import Sections
from Items import Items
from Stock import Stock

class Controller:
    def __init__(self, recreate = False):
        self.sections_db = Sections(recreate)
        self.items_db = Items(recreate)
        self.stock_db = Stock(recreate)
        self.audit_db = Audit(recreate)

    # Fetch table from sections
    def fetch_sections_table(self):
        return self.sections_db.select_table()
    
    # Fetch all sections
    def fetch_all_sections(self):
        return self.sections_db.select_column('name')

    # Fetch table from items
    def fetch_items_table(self):
        return self.items_db.select_table()
    
    # Fetch all items
    def fetch_all_items(self):
        return self.items_db.select_column('name')
    
    # Fetch table from stock
    def fetch_stock_table(self):
        return self.stock_db.select_table()

    # Add new section
    def add_section(self, section_name, section_description):
        if len(section_name) == 0:
            return "Section must have a name!"
        existing_section = self.sections_db.fetch_id(section_name)
        if existing_section:
            return "Section already exists!"
        self.sections_db.insert_table([section_name, section_description])
        return "ok"
    
    # Add new item
    def add_item(self, item_name, section_name, date):
        if len(item_name) == 0:
            return "Item must have a name!"
        section = self.sections_db.select_row('name', section_name)
        if not section:
            return "Section does not exist!"
        existing_item = self.items_db.fetch_id(item_name)
        if existing_item:
            return "Item already exists!"
        self.items_db.insert_table([item_name, section[0], date])
        return "ok"
    
    # Add new stock
    def add_stock(self, item_name, quantity_change):
        if quantity_change == 0:
            return "Quantity cannot be 0!"
        item = self.items_db.select_row('name', item_name)
        if not item:
            return "Item does not exist!"
        existing_stock = self.stock_db.select_row('item_id', item[0])
        if existing_stock:
            quantity = existing_stock[2]
            if quantity_change < 0 and quantity < (quantity_change * -1):
                return "Quantity over stock amount!"
            self.stock_db.update_stock(item_name, quantity + quantity_change)
        else:
            if quantity_change < 0:
                return "Cannot remove stock on new item!"
            self.stock_db.insert_table([item[0], quantity_change, str(date.today())])
        self.audit_db.insert_table([item[1], quantity_change, str(date.today())])
        return "ok"

    # Fetch table from audit
    def fetch_audit_table(self):
        return self.audit_db.select_table('id', 'DESC')