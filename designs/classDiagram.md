``` mermaid
classDiagram
    class Logger {
        +local_path: string
        -__path: string
        +__init__(self, name): void
        -__create_file(self, msg): void
        -__append_file(self, msg): void
        +write(self, msg): void
    }

    class Database {
        +table_name: string
        +cols: array
        +log: Logger
        -__query_log: Logger
        +connect_to_db(self)
        +query(self, query, binds, commit, force_cols)
        +create_table(self)
        +seed_table(self)
        +delete_table(self)
        +select_table(self, order_col, order)
        +select_column(self, col)
        +select_row(self, col, val)
        +insert_table(self, row)
    }

    class Sections {
        +create_table(self)
        +seed_table(self)
        +fetch_id(self, section)
    }

    class Items {
        +create_table(self)
        +seed_table(self)
        +select_table(self)
        +fetch_id(self, section)
    }

    class Stock {
        +create_table(self)
        +seed_table(self)
        +select_table(self)
        +update_stock(self, item_name, new_quantity)
    }
    
    class Audit {
        +create_table(self)
    }

    class Controller {
        +sections_db: Sections
        +items_db: Items
        +stock_db: Stock
        +audit_db: Audit
        +fetch_sections_table(self)
        +add_section(self, section_name, section_description)
        +fetch_all_sections(self)
        +fetch_items_table(self)
        +add_item(self, item_name, section_name, date)
        +fetch_all_items(self)
        +fetch_stock_table(self)
        +add_stock(self, item_name, quantity_change)
        +fetch_audit_table(self)
    }

    class GUI {
        +ctr: Controller
        +window: tkinter
        +frames: dict
        +entries: dict
        +tables: dict
        +options: dict
        +addFrames(self, frame_names)
        +showFrame(self, frame_name)
        +addLabel(self, frame, label_text)
        +addEntry(self, frame_name, prompt, key)
        +addButton(self, frame_name, text, command)
        +addTable(self, frame_name, cols, rows, key)
        +addOptions(self, frame_name, prompt, selections, key)
        +updateOptions(self, new_selections, key)
        +createSections(self)
        +updateSections(self)
        +createItems(self)
        +updateItems(self)
        +createStock(self)
        +updateStock(self, factor)
        +createAudit(self)
        +updateAudit(self)
        +startWindow(self, width, height)
    }

    Database *-- Logger

    Database <|-- Sections
    Database <|-- Items
    Database <|-- Stock
    Database <|-- Audit

    Controller *-- Sections
    Controller *-- Items
    Controller *-- Stock
    Controller *-- Audit

    GUI *-- Controller
```