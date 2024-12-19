import tkinter as tk
from tkinter import messagebox
import os
import unicodedata

# Meniul restaurantului
menu = {
    "Feluri principale": {
        "Pizza Margherita": 25.0,
        "Burger": 20.0,
        "Lasagna": 30.0,
    },
    "Deserturi": {
        "Tiramisu": 15.0,
        "Cheesecake": 12.0,
        "Înghețată": 10.0,
    },
    "Bauturi": {
        "Coca Cola": 6.0,
        "Apă plată": 4.0,
        "Bere": 8.0,
    }
}

def save_order(selected_items, total):
    orders_dir = os.path.join(os.getcwd(), "orders") 
    if not os.path.exists(orders_dir):
        os.makedirs(orders_dir)

    order_file_path = os.path.join(orders_dir, "order.txt")
    with open(order_file_path, "a", encoding="utf-8") as file:
        file.write("Comandă:\n")
        for item, price in selected_items:
            file.write(f"- {item} - {price} RON\n")
        file.write(f"Total: {total} RON\n")
        file.write("\n")

# Funcție pentru calcularea totalului comenzii
def calculate_total(selected_items):
    return sum(price for item, price in selected_items)

# Funcție pentru a elimina diacriticele
def remove_diacritics(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Interfața grafică principală
class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meniu Restaurant")
        self.root.geometry("600x700")
        self.root.config(bg="#f2f2f2")
        self.selected_items = []

        # Titlul aplicației
        self.title_label = tk.Label(root, text="Meniu Restaurant", font=("Arial", 18, "bold"), bg="#f2f2f2")
        self.title_label.pack(pady=10)

        # Panoul pentru categorii
        self.category_frame = tk.Frame(root, bg="#f2f2f2")
        self.category_frame.pack(pady=10, fill=tk.X)

        # Dicționar pentru a reține starea de vizibilitate a preparatelor
        self.category_visibility = {}
        self.last_category = None  # Variabilă pentru a reține ultima categorie deschisă

        # Adăugarea butoanelor pentru fiecare categorie
        self.category_buttons = {}
        for category in menu:
            button = tk.Button(self.category_frame, text=category, font=("Arial", 12), bg="#4CAF50", fg="white", 
                               command=lambda c=category: self.toggle_items(c))
            self.category_buttons[category] = button
            button.pack(side=tk.LEFT, padx=5)
            self.category_visibility[category] = False  # Inițial, preparatele din fiecare categorie sunt ascunse

        # Panoul pentru preparate
        self.items_frame = tk.Frame(root, bg="#f2f2f2")
        self.items_frame.pack(pady=10, fill=tk.X)

        # Butoanele pentru funcțiile suplimentare
        self.add_item_button = tk.Button(root, text="Adaugă Produs în Meniu", font=("Arial", 14), bg="#FF9800", fg="white", 
                                         command=self.add_item_to_menu)
        self.add_item_button.pack(pady=10)

        self.view_order_button = tk.Button(root, text="Vizualizează Comanda", font=("Arial", 14), bg="#2196F3", fg="white", 
                                           command=self.view_order)
        self.view_order_button.pack(pady=10)

        # Butonul pentru a finaliza comanda
        self.finalize_button = tk.Button(root, text="Finalizează Comanda", font=("Arial", 14), bg="#FF5722", fg="white", 
                                         command=self.finalize_order)
        self.finalize_button.pack(pady=20)

        # Eticheta pentru total
        self.total_label = tk.Label(root, text="Total: 0 RON", font=("Arial", 14), bg="#f2f2f2")
        self.total_label.pack()

    # Funcția pentru a toggla vizibilitatea preparatelor dintr-o categorie
    def toggle_items(self, category):
        # Dacă există o categorie deschisă, o închidem
        if self.last_category and self.last_category != category:
            self.hide_items(self.last_category)
        
        # Dacă categoria aleasă nu este deja vizibilă, o deschidem
        if not self.category_visibility[category]:
            self.show_items(category)
        else:
            self.hide_items(category)
        
        # Actualizează ultima categorie deschisă
        self.last_category = category

    # Funcția pentru a arăta preparatele dintr-o categorie
    def show_items(self, category):
        # Arată preparatele din categoria respectivă
        for item, price in menu[category].items():
            button = tk.Button(self.items_frame, text=f"{item} - {price} RON", font=("Arial", 12), bg="#2196F3", fg="white",
                               command=lambda i=item, p=price: self.add_to_order(i, p))
            button.pack(pady=5)
        
        # Actualizează starea ca fiind vizibilă
        self.category_visibility[category] = True

    # Funcția pentru a ascunde preparatele dintr-o categorie
    def hide_items(self, category):
        # Ascunde toate preparatele din categoria respectivă
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # Actualizează starea ca fiind ascunsă
        self.category_visibility[category] = False

    # Funcția pentru a adăuga preparate în comandă
    def add_to_order(self, item, price):
        self.selected_items.append((item, price))
        total = calculate_total(self.selected_items)
        self.total_label.config(text=f"Total: {total} RON")
        messagebox.showinfo("Adăugat", f"{item} a fost adăugat la comandă!")

    # Funcția pentru a finaliza comanda
    def finalize_order(self):
        if not self.selected_items:
            messagebox.showwarning("Eroare", "Nu ai adăugat nimic în comandă!")
        else:
            total = calculate_total(self.selected_items)
            save_order(self.selected_items, total)
            messagebox.showinfo("Comandă Finalizată", f"Comanda ta a fost salvată.\nTotal: {total} RON")
            self.reset_order()

    # Funcția pentru a reseta comanda
    def reset_order(self):
        self.selected_items = []
        self.total_label.config(text="Total: 0 RON")

        # Ascunde toate preparatele
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # Reinițializează starea de vizibilitate pentru fiecare categorie
        self.category_visibility = {category: False for category in menu}
        self.last_category = None

    # Funcția pentru a adăuga un produs în meniu
    def add_item_to_menu(self):
        def add_product():
            category = category_entry.get()
            item = item_entry.get()
            price = price_entry.get()
            
            if category and item and price:
                try:
                    price = float(price)
                    # Normalizează categoria pentru a nu depinde de diacritice
                    normalized_category = remove_diacritics(category).capitalize()

                    if normalized_category not in menu:
                        menu[normalized_category] = {}

                    menu[normalized_category][item] = price
                    messagebox.showinfo("Succes", f"Produsul '{item}' a fost adăugat în meniu!")
                    add_window.destroy()
                except ValueError:
                    messagebox.showerror("Eroare", "Prețul trebuie să fie un număr valid!")
            else:
                messagebox.showwarning("Eroare", "Te rugăm să completezi toate câmpurile!")

        # Fereastra pentru adăugarea unui produs
        add_window = tk.Toplevel(self.root)
        add_window.title("Adăugare Produs")
        add_window.geometry("400x300")

        tk.Label(add_window, text="Categorie:", font=("Arial", 12)).pack(pady=5)
        category_entry = tk.Entry(add_window, font=("Arial", 12))
        category_entry.pack(pady=5)

        tk.Label(add_window, text="Preparat:", font=("Arial", 12)).pack(pady=5)
        item_entry = tk.Entry(add_window, font=("Arial", 12))
        item_entry.pack(pady=5)

        tk.Label(add_window, text="Preț:", font=("Arial", 12)).pack(pady=5)
        price_entry = tk.Entry(add_window, font=("Arial", 12))
        price_entry.pack(pady=5)

        add_button = tk.Button(add_window, text="Adaugă Produs", font=("Arial", 12), bg="#4CAF50", fg="white", command=add_product)
        add_button.pack(pady=20)

    # Funcția pentru a vizualiza comanda
    def view_order(self):
        if not self.selected_items:
            messagebox.showwarning("Comandă Goală", "Nu ai adăugat niciun produs în comandă!")
        else:
            order_text = "Comanda ta:\n"
            for item, price in self.selected_items:
                order_text += f"- {item} - {price} RON\n"
            total = calculate_total(self.selected_items)
            order_text += f"\nTotal: {total} RON"
            messagebox.showinfo("Vizualizare Comandă", order_text)

# Crearea și rularea aplicației
if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()
