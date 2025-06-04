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
                    return True, row['NAME']  # Zwracamy True i imię użytkownika
        return False, None
    except FileNotFoundError:
        messagebox.showerror("Błąd", "Plik z danymi klientów nie został znaleziony!")
        return False, None
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem przy sprawdzaniu danych: {str(e)}")
        return False, None

def login_window(callback):
    """Okno logowania"""
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
    
    # Email
    email_label = tk.Label(form_frame, text="Email:", font=("Arial", 12))
    email_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
    
    email_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
    email_entry.grid(row=0, column=1, padx=10, pady=10)
    email_entry.focus()  # Ustawienie fokusa na pole email
    
    # Hasło
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
            login_root.destroy()  # Zamknięcie okna logowania
            callback(user_name)  # Wywołanie głównej aplikacji z imieniem użytkownika
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy email lub hasło!")
            password_entry.delete(0, tk.END)  # Wyczyszczenie pola hasła
    
    # Przycisk logowania
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
    def on_enter(event):
        attempt_login()
    
    login_root.bind('<Return>', on_enter)
    email_entry.bind('<Return>', lambda e: password_entry.focus())
    password_entry.bind('<Return>', on_enter)
    
    # Przycisk zamknięcia
    close_button = tk.Button(login_root, text="Zamknij", command=login_root.quit)
    close_button.pack(side="bottom", pady=10)
    
    login_root.mainloop()

def main_shop_window(user_name="Użytkowniku"):
    """Główne okno aplikacji sklepu"""
    root = tk.Tk()
    root.title("Sklep Żabka")
    root.geometry("800x600")  # Szerokość x wysokość
    
    # Główny label z powitaniem użytkownika
    label = tk.Label(root, text=f"Witaj w sklepie Żabka, {user_name}!", font=("Arial", 16))
    label.pack(pady=20)
    
    # Ramka na produkty
    products_frame = tk.Frame(root)
    products_frame.pack(pady=10, fill="both", expand=True)
    
    # Frame na przyciski
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    # Przycisk zamknięcia
    close_button = tk.Button(button_frame, text="Zamknij", command=root.quit)
    close_button.pack(padx=10)
    
    # Canvas do scrollowania
    canvas = tk.Canvas(products_frame)
    scrollbar = tk.Scrollbar(products_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    products_frame.pack(fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Funkcja do obsługi kliknięcia przycisku "Kup"
    def buy_product(product_id, product_name):
        messagebox.showinfo("Zakup", f"Produkt '{product_name}' (ID: {product_id}) został dodany do koszyka!")
    
    # Ścieżka do pliku Excel
    file_path = os.path.join("data", "products.xlsx")
    
    try:
        # Wczytanie danych z pliku Excel
        # skiprows=1 pomija pierwszy wiersz z nagłówkami
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
                
                # Informacje o produkcie
                product_label = tk.Label(
                    product_frame, 
                    text=f"{product_name} - Dostępnych: {product_available}",
                    font=("Arial", 12),
                    padx=10
                )
                product_label.pack(side="left", pady=10)
                
                # Przycisk "Kup"
                buy_button = tk.Button(
                    product_frame, 
                    text="Dodaj do koszyka", 
                    command=lambda id=product_id, name=product_name: buy_product(id, name),
                    bg="#4CAF50",  # Zielony kolor tła
                    fg="white",    # Biały kolor tekstu
                    padx=20
                )
                buy_button.pack(side="right", padx=10, pady=10)
    
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem przy wczytywaniu pliku: {str(e)}")
        print(f"Błąd: {str(e)}")
    
    root.mainloop()

def start_gui():
    """Główna funkcja uruchamiająca aplikację - zaczyna od logowania"""
    login_window(main_shop_window)