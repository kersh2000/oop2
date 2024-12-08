import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Controller import Controller

class GUI:
    
    def __init__(self, recreate_db = False):
        self.ctr = Controller(recreate_db)
        self.window = tk.Tk()
        self.frames = {}
        self.entries = {}
        self.tables = {}
        self.options = {}

    def addFrames(self, frame_names):
        menu = tk.Menu(self.window)
        for name in frame_names:
            self.frames[name] = tk.Frame(self.window)
            menu.add_command(label=name.title(), command=lambda n=name: self.showFrame(n))
        self.window.config(menu=menu)

        self.showFrame(frame_names[0])

    def showFrame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[frame_name].pack(fill="both", expand=True)

    def addLabel(self, frame, label_text):
        label = tk.Label(frame, text=label_text)
        label.pack()

    def addEntry(self, frame_name, prompt, key):
        frame = self.frames[frame_name]
        self.addLabel(frame, prompt)
        self.entries[key] = tk.Entry(frame)
        self.entries[key].pack()

    def addButton(self, frame_name, text, command):
        frame = self.frames[frame_name]
        button = tk.Button(frame, text=text, command=command)
        button.pack()
    
    def addTable(self, frame_name, cols, rows, key):
        frame = self.frames[frame_name]
        self.tables[key] = ttk.Treeview(frame, columns=cols, show = 'headings')
        self.tables[key].pack(fill='both', expand=True)
        for col in cols:
            self.tables[key].heading(col, text = col.replace("_", " ").title())

        index = 0
        for row in rows:
            self.tables[key].insert(parent = '', index = index, values = row)
            index += 1
    
    def addOptions(self, frame_name, prompt, selections, key):
        frame = self.frames[frame_name]
        self.addLabel(frame, prompt)
        self.options["{}_var".format(key)] = tk.StringVar()
        self.options[key] = tk.OptionMenu(frame, self.options["{}_var".format(key)], *selections)
        self.options[key].pack()

    def updateOptions(self, new_selections, key):
        self.options[key]['menu'].delete(0, 'end')
        for selection in new_selections:
            self.options[key]['menu'].add_command(
                label = selection,
                command = lambda value=selection: self.options["{}_var".format(key)].set(value)
            )

    def createSections(self):
        frame = "sections"
        self.addEntry(frame, "Section Name", "sections_name")
        self.addEntry(frame, "Section Description", "sections_description")
        self.addButton(frame, "Add Section", self.updateSections)
        cols, rows = self.ctr.fetch_sections_table()
        self.addTable(frame, cols, rows, "sections")

    def updateSections(self):
        response = self.ctr.add_section(self.entries["sections_name"].get(), self.entries["sections_description"].get())
        if response != "ok":
            messagebox.showerror('Database Error', response)
            return 0
        self.tables["sections"].destroy()
        cols, rows = self.ctr.fetch_sections_table()
        self.addTable("sections", cols, rows, "sections")
        self.updateOptions(self.ctr.fetch_all_sections(), "items_section")

    def createItems(self):
        frame = "items"
        self.addEntry(frame, "Item Name", "items_name")
        self.addOptions(frame, "Section Name", self.ctr.fetch_all_sections(), "items_section")
        self.addEntry(frame, "Expiration Date (Optional, YYYY-MM-DD)", "items_date")
        self.addButton(frame, "Add Item", self.updateItems)
        cols, rows = self.ctr.fetch_items_table()
        self.addTable(frame, cols, rows, "items")
    
    def updateItems(self):
        date = self.entries["items_date"].get() if self.entries["items_date"].get() != "" else None
        response = self.ctr.add_item(self.entries["items_name"].get(), self.options["items_section_var"].get(), date)
        if response != "ok":
            messagebox.showerror('Database Error', response)
            return 0
        self.tables["items"].destroy()
        cols, rows = self.ctr.fetch_items_table()
        self.addTable("items", cols, rows, "items")
        self.updateOptions(self.ctr.fetch_all_items(), "stock_item")

    def createStock(self):
        frame = "stock"
        self.addOptions(frame, "Item Name", self.ctr.fetch_all_items(), "stock_item")
        self.addEntry(frame, "Quantity", "stock_quantity")
        self.addButton(frame, "Add Stock", lambda: self.updateStock(1))
        self.addButton(frame, "Remove Stock", lambda: self.updateStock(-1))
        cols, rows = self.ctr.fetch_stock_table()
        self.addTable(frame, cols, rows, "stock")

    def updateStock(self, factor):
        quantity_entered = self.entries["stock_quantity"].get()
        if quantity_entered == '':
            messagebox.showerror('GUI Error', "Quantity cannot be empty!")
            return 0
        quantity_change = int(quantity_entered) * factor
        response = self.ctr.add_stock(self.options["stock_item_var"].get(), quantity_change)
        if response != "ok":
            messagebox.showerror('Database Error', response)
            return 0
        self.tables["stock"].destroy()
        cols, rows = self.ctr.fetch_stock_table()
        self.addTable("stock", cols, rows, "stock")
        self.updateAudit()

    def createAudit(self):
        frame = "audit"
        cols, rows = self.ctr.fetch_audit_table()
        self.addTable(frame, cols, rows, "audit")
    
    def updateAudit(self):
        self.tables["audit"].destroy()
        cols, rows = self.ctr.fetch_audit_table()
        self.addTable("audit", cols, rows, "audit")

    def startWindow(self, width, height):
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry("{}x{}+{}+{}".format(width, height, x, y))
        self.window.title("New Warehouse Management System")
        self.window.mainloop()
    

if __name__ == "__main__":
    gui = GUI(True)
    frames = ["sections", "items", "stock", "audit"]
    gui.addFrames(frames)
    gui.createSections()
    gui.createItems()
    gui.createStock()
    gui.createAudit()
    gui.startWindow(800, 500)