import tkinter as tk
import pandas as pd
import os
from add_delete_products import add_product, delete_product
from add_delete_user import add_user, delete_user

# Ścieżka do pliku
file_path = os.path.join("data", "products.xlsx")
users_file_path = os.path.join("data", "customer.csv")

# Globalna lista referencji do widgetów z produktami (do czyszczenia)
product_widgets = []

def validate_length(text):
    """Walidacja długości tekstu - maksymalnie 50 znaków"""
    return len(text) <= 50

def show_users():
    """Otwiera nowe okno z listą wszystkich użytkowników"""
    users_window = tk.Toplevel()
    users_window.title("Lista Użytkowników")
    users_window.geometry("500x500")
    
  
    main_frame = tk.Frame(users_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
  
    header_label = tk.Label(main_frame, text="Lista Wszystkich Użytkowników", 
                           font=("Arial", 16, "bold"))
    header_label.pack(pady=(0, 15))
    
    # Frame dla canvas i scrollbar
    canvas_frame = tk.Frame(main_frame)
    canvas_frame.pack(fill="both", expand=True)
    
    # Canvas z scrollbarem
    canvas = tk.Canvas(canvas_frame, highlightthickness=0)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    # Konfiguracja scrollowania
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pakowanie canvas i scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Bind scrollowania myszką
    def bind_mousewheel_users(event):
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def unbind_mousewheel_users(event):
        canvas.unbind_all("<MouseWheel>")
    
    canvas.bind('<Enter>', bind_mousewheel_users)
    canvas.bind('<Leave>', unbind_mousewheel_users)
    
    try:
        # Wczytaj dane z CSV
        df = pd.read_csv(users_file_path)
        
        if df.empty:
            no_users_label = tk.Label(scrollable_frame, text="Brak użytkowników w bazie danych", 
                                    font=("Arial", 12), fg="gray")
            no_users_label.pack(pady=20)
        else:
            # Wyświetl każdego użytkownika
            for index, row in df.iterrows():
                user_frame = tk.Frame(scrollable_frame, bd=2, relief=tk.RIDGE, bg="#f0f0f0")
                user_frame.pack(fill="x", padx=5, pady=5)
                
                # ID i Imię (główny nagłówek)
                name_label = tk.Label(user_frame, text=f"#{row['ID']} - {row['NAME']}", 
                                    font=("Arial", 14, "bold"), bg="#f0f0f0")
                name_label.pack(anchor="w", padx=10, pady=(8, 2))
                
                # Email
                email_label = tk.Label(user_frame, text=f"📧 Email: {row['E-MAIL']}", 
                                     font=("Arial", 10), bg="#f0f0f0")
                email_label.pack(anchor="w", padx=20, pady=1)
                
                # DODANO HASŁO
                password_text = row.get('PASSWORD', 'Brak') if pd.notna(row.get('PASSWORD')) and str(row.get('PASSWORD')) != 'NULL' else "Brak"
                password_label = tk.Label(user_frame, text=f"🔐 Hasło: {password_text}", 
                                        font=("Arial", 10), bg="#f0f0f0")
                password_label.pack(anchor="w", padx=20, pady=1)
                
                # Telefon
                phone_text = row['PHONE'] if pd.notna(row['PHONE']) and str(row['PHONE']) != 'NULL' else "Brak"
                phone_label = tk.Label(user_frame, text=f"📞 Telefon: {phone_text}", 
                                     font=("Arial", 10), bg="#f0f0f0")
                phone_label.pack(anchor="w", padx=20, pady=1)
                
                # Daty
                created_label = tk.Label(user_frame, text=f"📅 Utworzono: {row['CREATED']}", 
                                       font=("Arial", 10), bg="#f0f0f0", fg="gray")
                created_label.pack(anchor="w", padx=20, pady=1)
                
                updated_label = tk.Label(user_frame, text=f"🔄 Zaktualizowano: {row['UPDATED']}", 
                                       font=("Arial", 10), bg="#f0f0f0", fg="gray")
                updated_label.pack(anchor="w", padx=20, pady=(1, 8))
                
    except FileNotFoundError:
        error_label = tk.Label(scrollable_frame, text="Plik customer.csv nie został znaleziony!", 
                             font=("Arial", 12), fg="red")
        error_label.pack(pady=20)
    except Exception as e:
        error_label = tk.Label(scrollable_frame, text=f"Błąd wczytywania danych: {str(e)}", 
                             font=("Arial", 12), fg="red")
        error_label.pack(pady=20)
    

    close_button = tk.Button(main_frame, text="Zamknij", command=users_window.destroy,
                           bg="#757575", fg="white", font=("Arial", 10))
    close_button.pack(pady=(10, 0))
    
def load_products(products_scrollable_frame, canvas):
    # Usuń istniejące widgety
    for widget in product_widgets:
        widget.destroy()
    product_widgets.clear()

    try:
        df = pd.read_excel(file_path, header=None, skiprows=1)
        for index, row in df.iterrows():
            data = str(row[0]).split(',')
            if len(data) >= 4:  
                product_id = data[0]
                product_name = data[1]
                product_price = data[2]  
                product_available = data[3]  

                product_frame = tk.Frame(products_scrollable_frame, bd=1, relief=tk.RAISED)
                product_frame.pack(fill="x", padx=5, pady=5)

                product_label = tk.Label(
                    product_frame,
                    text=f"{product_name} - Dostępnych: {product_available} - Cena: {product_price} zł",
                    font=("Arial", 12),
                    padx=10
                )
                product_label.pack(side="left", pady=10)

                product_widgets.append(product_frame)

    except Exception as e:
        error_label = tk.Label(products_scrollable_frame, text=f"Błąd wczytywania pliku: {e}")
        error_label.pack()
        product_widgets.append(error_label)
    
    products_scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def configure_canvas_scroll(event, canvas):
    """Konfiguruje szerokość scrollable frame aby wypełnić canvas"""
    canvas_width = event.width
    canvas.itemconfig(canvas.scrollable_window, width=canvas_width)

def main():
    root = tk.Tk()
    root.title("Sklep Żabka")
    root.geometry("800x700")
    
    # Rejestracja funkcji walidacji
    vcmd = (root.register(validate_length), '%P')

    # Główna ramka
    main_container = tk.Frame(root)
    main_container.pack(fill="both", expand=True, padx=10, pady=10)

   
    products_container = tk.Frame(main_container)
    products_container.pack(side="left", fill="both", expand=True)

   
    products_header = tk.Label(products_container, text="Lista Produktów", font=("Arial", 14, "bold"))
    products_header.pack(pady=(0, 10))

    # Frame dla canvas i scrollbar
    canvas_frame = tk.Frame(products_container)
    canvas_frame.pack(fill="both", expand=True)

    # Canvas z scrollbarem
    canvas = tk.Canvas(canvas_frame, highlightthickness=0)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    products_scrollable_frame = tk.Frame(canvas)

    # Konfiguracja scrollowania
    products_scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Tworzenie okna w canvas z zapisaniem referencji
    canvas.scrollable_window = canvas.create_window((0, 0), window=products_scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Bind do zmiany rozmiaru canvas - zapewnia wypełnienie szerokości
    canvas.bind('<Configure>', lambda e: configure_canvas_scroll(e, canvas))

    # Pakowanie canvas i scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Bind scrollowania myszką
    def bind_mousewheel(event):
        canvas.bind_all("<MouseWheel>", lambda e: on_mousewheel(e, canvas))

    def unbind_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    canvas.bind('<Enter>', bind_mousewheel)
    canvas.bind('<Leave>', unbind_mousewheel)

    input_frame = tk.Frame(main_container)
    input_frame.pack(side="right", fill="y", padx=20)

    
    load_products(products_scrollable_frame, canvas)

    
    tk.Label(input_frame, text="Zarządzanie Produktami", font=("Arial", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(10, 10)
    )


    tk.Label(input_frame, text="Nazwa produktu:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    name_entry = tk.Entry(input_frame, validate='key', validatecommand=vcmd)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Ilość:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    count_entry = tk.Entry(input_frame, validate='key', validatecommand=vcmd)
    count_entry.grid(row=2, column=1, padx=5, pady=5)

    
    tk.Label(input_frame, text="Cena (XX.XX):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    price_entry = tk.Entry(input_frame)
    price_entry.grid(row=3, column=1, padx=5, pady=5)

    def on_add_product():
        add_product(name_entry, count_entry, price_entry)
        load_products(products_scrollable_frame, canvas)

    tk.Button(
        input_frame,
        text="Dodaj Produkt",
        command=on_add_product,
        bg="#2196F3",
        fg="white",
        padx=10
    ).grid(row=4, column=0, columnspan=2, pady=10)

    
    tk.Label(input_frame, text="Nazwa do usunięcia:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    delete_entry = tk.Entry(input_frame, validate='key', validatecommand=vcmd)
    delete_entry.grid(row=5, column=1, padx=5, pady=5)

    def on_delete_product():
        delete_product(delete_entry)
        load_products(products_scrollable_frame, canvas)

    tk.Button(
        input_frame,
        text="Usuń Produkt",
        command=on_delete_product,
        bg="#F44336",
        fg="white",
        padx=10
    ).grid(row=6, column=0, columnspan=2, pady=10)

   
    tk.Label(input_frame, text="Zarządzanie Użytkownikami", font=("Arial", 14, "bold")).grid(
        row=7, column=0, columnspan=2, pady=(20, 10)
    )


    tk.Label(input_frame, text="Email:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
    email_entry = tk.Entry(input_frame, validate='key', validatecommand=vcmd)
    email_entry.grid(row=8, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Hasło:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
    password_entry = tk.Entry(input_frame, validate='key', validatecommand=vcmd, show="*")
    password_entry.grid(row=9, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Imię:").grid(row=10, column=0, padx=5, pady=5, sticky="w")
    name_entry_2 = tk.Entry(input_frame, validate='key', validatecommand=vcmd)
    name_entry_2.grid(row=10, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Telefon:").grid(row=11, column=0, padx=5, pady=5, sticky="w")
    phone_entry = tk.Entry(input_frame, validate='key', validatecommand=vcmd)
    phone_entry.grid(row=11, column=1, padx=5, pady=5)

    tk.Button(
        input_frame,
        text="Dodaj Użytkownika",
        command=lambda: add_user(email_entry, password_entry, name_entry_2, phone_entry),
        bg="#1976D2",
        fg="white",
        padx=10
    ).grid(row=12, column=0, columnspan=2, pady=10)

    
    tk.Button(
        input_frame,
        text="Pokaż Użytkowników",
        command=show_users,
        bg="#4CAF50",
        fg="white",
        padx=10
    ).grid(row=13, column=0, columnspan=2, pady=5)


    tk.Label(input_frame, text="Email do usunięcia:").grid(row=14, column=0, padx=5, pady=5, sticky="w")
    delete_user_entry = tk.Entry(input_frame, validate='key', validatecommand=vcmd)
    delete_user_entry.grid(row=14, column=1, padx=5, pady=5)

    tk.Button(
        input_frame,
        text="Usuń Użytkownika",
        command=lambda: delete_user(delete_user_entry),
        bg="#D32F2F",
        fg="white",
        padx=10
    ).grid(row=15, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
