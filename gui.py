import tkinter as tk
from tkinter import messagebox
import pandas as pd
import csv
import os

def validate_login(email, password):
    """Funkcja sprawdzająca dane logowania w pliku customer.csv"""
    file_path = os.path.join("data", "customer.csv")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['E-MAIL'] == email and row['PASSWORD'] == password:
                    return True, row['NAME'] 
        return False, None
    except FileNotFoundError:
        messagebox.showerror("Błąd", "Plik z danymi klientów nie został znaleziony!")
        return False, None
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem przy sprawdzaniu danych: {str(e)}")
        return False, None

def login_window(callback):
    login_root = tk.Tk()
    login_root.title("Logowanie - Sklep Żabka")
    login_root.geometry("400x400")
    login_root.resizable(False, False)
    
    # Centrowanie okna
    login_root.eval('tk::PlaceWindow . center')
    
    # Główny label
    title_label = tk.Label(login_root, text="Sklep Żabka", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)
    
    subtitle_label = tk.Label(login_root, text="Zaloguj się do swojego konta", font=("Arial", 12))
    subtitle_label.pack(pady=5)
    
    # Frame na formularz
    form_frame = tk.Frame(login_root)
    form_frame.pack(pady=30)
    
    email_label = tk.Label(form_frame, text="Email:", font=("Arial", 12))
    email_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
    
    email_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
    email_entry.grid(row=0, column=1, padx=10, pady=10)
    email_entry.focus()  
    
    password_label = tk.Label(form_frame, text="Hasło:", font=("Arial", 12))
    password_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
    
    password_entry = tk.Entry(form_frame, font=("Arial", 12), width=20, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    
    def attempt_login():
        """Funkcja obsługująca próbę logowania"""
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Ostrzeżenie", "Wprowadź email i hasło!")
            return
        
        is_valid, user_name = validate_login(email, password)
        
        if is_valid:
            messagebox.showinfo("Sukces", f"Witaj {user_name}!")
            login_root.destroy()  
            callback(user_name)  
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy email lub hasło!")
            password_entry.delete(0, tk.END)  
    
    login_button = tk.Button(
        form_frame, 
        text="Zaloguj się", 
        command=attempt_login,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12),
        padx=20,
        pady=5
    )
    login_button.grid(row=2, column=0, columnspan=2, pady=20)
    
    # Obsługa klawisza Enter 
    def handle_login_enter(event):
        attempt_login()
    
    login_root.bind('<Return>', handle_login_enter)
    email_entry.bind('<Return>', lambda e: password_entry.focus())
    password_entry.bind('<Return>', handle_login_enter)
    

    def close_login():
        try:
            login_root.quit()
        except:
            pass
        finally:
            login_root.destroy()
    
    close_button = tk.Button(login_root, text="Zamknij", command=close_login)
    close_button.pack(side="bottom", pady=10)
    
    login_root.mainloop()

def main_shop_window(user_name="Użytkowniku"):
    """Główne okno aplikacji sklepu"""
    root = tk.Tk()
    root.title("Sklep Żabka")
    root.geometry("1200x700") 
    
    cart = {}
    
    label = tk.Label(root, text=f"Witaj w sklepie Żabka, {user_name}!", font=("Arial", 16))
    label.pack(pady=20)
    
    main_frame = tk.Frame(root)
    main_frame.pack(pady=10, fill="both", expand=True)
    
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5))
    
    products_label = tk.Label(left_frame, text="Produkty", font=("Arial", 14, "bold"))
    products_label.pack(pady=5)
    
    right_frame = tk.Frame(main_frame, width=300, bg="#f0f0f0")
    right_frame.pack(side="right", fill="y", padx=(5, 10))
    right_frame.pack_propagate(False)
    
    cart_label = tk.Label(right_frame, text="Koszyk", font=("Arial", 14, "bold"), bg="#f0f0f0")
    cart_label.pack(pady=10)
    
    cart_content_frame = tk.Frame(right_frame, bg="#f0f0f0")
    cart_content_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    canvas = tk.Canvas(left_frame)
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def update_cart_display():
        for widget in cart_content_frame.winfo_children():
            widget.destroy()
        
        if not cart:
            empty_label = tk.Label(cart_content_frame, text="Koszyk jest pusty", 
                                 font=("Arial", 10), bg="#f0f0f0", fg="gray")
            empty_label.pack(pady=20)
        else:
            for product_id, (product_name, quantity) in cart.items():
                item_frame = tk.Frame(cart_content_frame, bg="#ffffff", relief=tk.RAISED, bd=1)
                item_frame.pack(fill="x", pady=2, padx=5)
                
                item_label = tk.Label(item_frame, text=f"{product_name}\nIlość: {quantity}", 
                                    font=("Arial", 9), bg="#ffffff", justify="left")
                item_label.pack(pady=5, padx=5, anchor="w")
    
    def validate_quantity(quantity_str):
        try:
            quantity = int(quantity_str)
            if quantity < 1 or quantity > 99:
                return False, "Ilość musi być między 1 a 99!"
            return True, quantity
        except ValueError:
            return False, "Podaj prawidłową liczbę!"
    
    def buy_product(product_id, product_name, quantity_entry):
        quantity_str = quantity_entry.get().strip()
        
        if not quantity_str:
            messagebox.showwarning("Ostrzeżenie", "Podaj ilość produktu!")
            return
        
        is_valid, result = validate_quantity(quantity_str)
        
        if not is_valid:
            messagebox.showerror("Błąd", result)
            return
        
        quantity = result
        
        # Dodaj do koszyka
        if product_id in cart:
            current_quantity = cart[product_id][1]
            new_quantity = current_quantity + quantity
            cart[product_id] = (product_name, new_quantity)
        else:
            cart[product_id] = (product_name, quantity)
                
        # Aktualizuj wyświetlanie koszyka
        update_cart_display()
        
        messagebox.showinfo("Sukces", f"Dodano {quantity} szt. '{product_name}' do koszyka!")
    
    file_path = os.path.join("data", "products.xlsx")
    
    try:
        # Wczytanie danych z pliku Excel
        df = pd.read_excel(file_path, header=None, skiprows=1)
        
        # Dodanie produktów do interfejsu
        for index, row in df.iterrows():
            # Rozdzielenie danych po przecinkach
            data = str(row[0]).split(',')
            if len(data) >= 3:  # Upewnienie się, że mamy przynajmniej ID, nazwę i ilość
                product_id = data[0]
                product_name = data[1]
                product_available = data[2]
                
                # Ramka dla jednego produktu
                product_frame = tk.Frame(scrollable_frame, bd=1, relief=tk.RAISED)
                product_frame.pack(fill="x", padx=10, pady=5)
                

                product_label = tk.Label(
                    product_frame, 
                    text=f"{product_name} - Dostępnych: {product_available}",
                    font=("Arial", 12),
                    padx=10
                )
                product_label.pack(side="left", pady=10)
                
                # Frame na kontrolki po prawej stronie
                controls_frame = tk.Frame(product_frame)
                controls_frame.pack(side="right", padx=10, pady=10)
                

                quantity_label = tk.Label(controls_frame, text="Ilość:", font=("Arial", 10))
                quantity_label.pack(side="left", padx=(0, 5))
                
                quantity_entry = tk.Entry(controls_frame, width=5, font=("Arial", 10))
                quantity_entry.pack(side="left", padx=(0, 10))
                quantity_entry.insert(0, "1")  # Domyślna wartość

                buy_button = tk.Button(
                    controls_frame, 
                    text="Dodaj do koszyka", 
                    command=lambda id=product_id, name=product_name, entry=quantity_entry: buy_product(id, name, entry),
                    bg="#4CAF50",
                    fg="white",
                    font=("Arial", 10),
                    padx=15
                )
                buy_button.pack(side="left")
    
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem przy wczytywaniu pliku: {str(e)}")
        print(f"Błąd: {str(e)}")
    
    # Frame na przyciski na dole
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    def close_app():
        try:
            root.quit()
        except:
            pass
        finally:
            root.destroy()
    
    close_button = tk.Button(button_frame, text="Zamknij", command=close_app)
    close_button.pack(padx=10)
    
    update_cart_display()
    
    root.mainloop()

def start_gui():
    login_window(main_shop_window)


if __name__ == "__main__":
    start_gui()
