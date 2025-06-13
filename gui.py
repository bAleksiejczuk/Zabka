import tkinter as tk
from tkinter import messagebox
import pandas as pd
import csv
import os
from datetime import datetime

# Funkcja wyższego rzędu do tworzenia message handlers
def create_message_handler(default_title="Informacja"):
    """Funkcja wyższego rzędu tworząca różne handlery wiadomości"""
    def message_handler(message_type="info"):
        def show_message(message):
            if message_type == "info":
                messagebox.showinfo(default_title, message)
            elif message_type == "warning":
                messagebox.showwarning(default_title, message)
            elif message_type == "error":
                messagebox.showerror(default_title, message)
            elif message_type == "question":
                return messagebox.askyesno(default_title, message)
        return show_message
    return message_handler

# Tworzenie różnych message handlers dla różnych sekcji aplikacji
login_messages = create_message_handler("Logowanie")
show_login_error = login_messages("error")
show_login_warning = login_messages("warning")
show_login_success = login_messages("info")

cart_messages = create_message_handler("Koszyk")
show_cart_info = cart_messages("info")
show_cart_warning = cart_messages("warning")
show_cart_error = cart_messages("error")
ask_cart_question = cart_messages("question")

shop_messages = create_message_handler("Sklep")
show_shop_error = shop_messages("error")
show_shop_info = shop_messages("info")

payment_messages = create_message_handler("Płatność")
show_payment_info = payment_messages("info")
show_payment_error = payment_messages("error")
show_payment_warning = payment_messages("warning")
ask_payment_question = payment_messages("question")

points_messages = create_message_handler("Sklep za punkty")
show_points_error = points_messages("error")

def validate_login(email, password):
    """Funkcja sprawdzająca dane logowania w pliku customer.csv"""
    file_path = os.path.join("data", "customer.csv")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['E-MAIL'] == email and row['PASSWORD'] == password:
                    return True, row['NAME'], row['ID']  # Zwracaj NAME i ID
        return False, None, None
    except FileNotFoundError:
        show_login_error("Plik z danymi klientów nie został znaleziony!")
        return False, None, None
    except Exception as e:
        show_login_error(f"Wystąpił problem przy sprawdzaniu danych: {str(e)}")
        return False, None, None

def check_product_availability(cart):
    """Sprawdza dostępność produktów w koszyku względem pliku xlsx"""
    file_path = os.path.join("data", "products.xlsx")
    
    try:
        df = pd.read_excel(file_path)
        
        # Słownik do przechowywania dostępnych ilości {product_id: available_quantity}
        available_products = {}
        
        # Pobierz nazwę pierwszej kolumny
        first_col_name = df.columns[0]
        
        # Parsuj dane rozdzielone przecinkami
        for index, row in df.iterrows():
            try:
                data_str = str(row[first_col_name])
                
                if ',' in data_str:
                    data_parts = data_str.split(',')
                    if len(data_parts) >= 4:
                        product_id = data_parts[0].strip()
                        try:
                            available = int(data_parts[3].strip())
                            available_products[product_id] = available
                        except:
                            available_products[product_id] = 0
                    
            except Exception as e:
                continue
        
        # Sprawdź każdy produkt w koszyku
        unavailable_products = []
        
        for product_id, (product_name, cart_quantity, unit_price) in cart.items():
            available_quantity = available_products.get(product_id, 0)
            
            if cart_quantity > available_quantity:
                unavailable_products.append({
                    'name': product_name,
                    'cart_quantity': cart_quantity,
                    'available_quantity': available_quantity
                })
        
        return unavailable_products
        
    except Exception as e:
        show_shop_error(f"Wystąpił problem przy sprawdzaniu dostępności: {str(e)}")
        return []

def get_user_points(user_id):
    """Pobiera punkty użytkownika z pliku customer.csv"""
    file_path = os.path.join("data", "customer.csv")
    
    try:
        customers_df = pd.read_csv(file_path)
        user_row = customers_df[customers_df['ID'] == int(user_id)]
        
        if not user_row.empty:
            return int(user_row.iloc[0]['POINTS'])
        else:
            return 0
    except Exception as e:
        print(f"Błąd przy pobieraniu punktów: {e}")
        return 0

def points_shop_window(user_name, user_id):
    """Okno sklepu za punkty"""
    points_root = tk.Tk()
    points_root.title("Sklep za punkty - Żabka")
    points_root.geometry("600x400")
    
    # Centrowanie okna
    points_root.eval('tk::PlaceWindow . center')
    
    # Tytuł
    title_label = tk.Label(points_root, text="Sklep za punkty", font=("Arial", 20, "bold"))
    title_label.pack(pady=30)
    
    # Pobierz i wyświetl punkty użytkownika
    user_points = get_user_points(user_id)
    
    points_label = tk.Label(
        points_root, 
        text=f"Twoje punkty: {user_points} pkt", 
        font=("Arial", 16),
        fg="#4CAF50"
    )
    points_label.pack(pady=20)
    
    # Przycisk zamknij
    def close_points_shop():
        points_root.destroy()
    
    close_button = tk.Button(
        points_root,
        text="Zamknij",
        command=close_points_shop,
        font=("Arial", 12),
        padx=20,
        pady=5
    )
    close_button.pack(pady=30)
    
    points_root.mainloop()

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
            show_login_warning("Wprowadź email i hasło!")
            return
        
        is_valid, user_name, user_id = validate_login(email, password)  # Pobierz też ID
        
        if is_valid:
            show_login_success(f"Witaj {user_name}!")
            login_root.destroy()  
            callback(user_name, user_id)  # Przekaż zarówno NAME jak i ID
        else:
            show_login_error("Nieprawidłowy email lub hasło!")
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

def payment_window(cart, user_name, user_id, refresh_callback=None):
    """Okno płatności z podsumowaniem zamówienia"""
    payment_root = tk.Tk()
    payment_root.title("Płatność - Sklep Żabka")
    payment_root.geometry("1000x800")
    
    title_label = tk.Label(payment_root, text="Podsumowanie zamówienia", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)
    
    user_label = tk.Label(payment_root, text=f"Klient: {user_name}", font=("Arial", 12))
    user_label.pack(pady=5)
    
    # Frame na listę produktów
    products_frame = tk.LabelFrame(payment_root, text="Zamówione produkty", font=("Arial", 12, "bold"))
    products_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Canvas i scrollbar dla listy produktów
    canvas = tk.Canvas(products_frame)
    scrollbar = tk.Scrollbar(products_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    scrollbar.pack(side="right", fill="y")
    
    # Wyświetl produkty z koszyka
    total_amount = 0.0
    for product_id, (product_name, quantity, unit_price) in cart.items():
        item_total = quantity * unit_price
        total_amount += item_total
        
        item_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, bd=1, bg="#f9f9f9")
        item_frame.pack(fill="x", padx=5, pady=2)
        
        item_info = tk.Label(
            item_frame,
            text=f"{product_name}\nIlość: {quantity} szt. × {unit_price:.2f} zł = {item_total:.2f} zł",
            font=("Arial", 11),
            bg="#f9f9f9",
            justify="left",
            padx=10,
            pady=5
        )
        item_info.pack(anchor="w")
    
    # Frame na podsumowanie
    summary_frame = tk.Frame(payment_root, bg="#e0e0e0")
    summary_frame.pack(fill="x", padx=20, pady=10)
    
    total_label = tk.Label(
        summary_frame,
        text=f"SUMA CAŁKOWITA: {total_amount:.2f} zł",
        font=("Arial", 16, "bold"),
        bg="#e0e0e0"
    )
    total_label.pack(pady=10)
    
    # Frame na metody płatności
    payment_method_frame = tk.LabelFrame(payment_root, text="Metoda płatności", font=("Arial", 12, "bold"))
    payment_method_frame.pack(fill="x", padx=20, pady=10)
    
    # Globalna zmienna dla metody płatności
    selected_payment = {"method": "blik"}
    
    def select_blik():
        selected_payment["method"] = "blik"
        print("Wybrano BLIK")
    
    def select_cash_on_delivery():
        selected_payment["method"] = "cash_on_delivery"
        print("Wybrano płatność przy odbiorze")
    
    # Radio buttony
    payment_choice = tk.IntVar(value=1)
    
    blik_radio = tk.Radiobutton(
        payment_method_frame,
        text="BLIK",
        variable=payment_choice,
        value=1,
        command=select_blik,
        font=("Arial", 11)
    )
    blik_radio.pack(anchor="w", padx=10, pady=5)
    
    cash_on_delivery_radio = tk.Radiobutton(
        payment_method_frame,
        text="Płatność przy odbiorze",
        variable=payment_choice,
        value=2,
        command=select_cash_on_delivery,
        font=("Arial", 11)
    )
    cash_on_delivery_radio.pack(anchor="w", padx=10, pady=5)
    
    blik_radio.select()
    
    # Frame na adres dostawy
    address_frame = tk.LabelFrame(payment_root, text="Adres dostawy", font=("Arial", 12, "bold"))
    address_frame.pack(fill="x", padx=20, pady=10)
    
    address_label = tk.Label(address_frame, text="Adres dostawy:", font=("Arial", 11))
    address_label.pack(anchor="w", padx=10, pady=(10,5))
    
    address_entry = tk.Entry(address_frame, font=("Arial", 11), width=70)
    address_entry.pack(padx=10, pady=(0,10), fill="x")
    
    def finalize_order():
        """Finalizuje zamówienie"""
        
        # Pobierz adres z pola Entry
        delivery_address = address_entry.get().strip()
        
        # Sprawdź czy adres został wprowadzony
        if not delivery_address:
            show_cart_error("Proszę wprowadzić adres dostawy.")
            return
        
        # Sprawdzenie dostępności produktów przed finalizacją
        unavailable_products = check_product_availability(cart)
        
        if unavailable_products:
            # Stwórz szczegółowy komunikat o błędzie
            error_message = "Błąd dostępności produktów:\n\n"
            for product in unavailable_products:
                error_message += f"• {product['name']}\n"
                error_message += f"  W koszyku: {product['cart_quantity']} szt.\n"
                error_message += f"  Dostępne: {product['available_quantity']} szt.\n\n"
            
            error_message += "Zmniejsz ilość produktów w koszyku lub usuń niedostępne produkty."
            
            show_cart_error(error_message)
            return
        
        # Jeśli wszystkie produkty są dostępne, kontynuuj finalizację
        payment_method = selected_payment["method"]
        
        # Oblicz punkty - za każdą pełną złotówkę 1 punkt
        earned_points = int(total_amount)
        
        print(f"Finalizacja z metodą: {payment_method}")
        print(f"Adres dostawy: {delivery_address}")
        print(f"Zdobyte punkty: {earned_points}")
        
        method_names = {
            "blik": "BLIK",
            "cash_on_delivery": "Płatność przy odbiorze"
        }
        
        result = ask_payment_question(
            f"Czy chcesz sfinalizować zamówienie?\n\n"
            f"Kwota: {total_amount:.2f} zł\n"
            f"Metoda płatności: {method_names[payment_method]}\n"
            f"Adres dostawy: {delivery_address}\n"
            f"Zdobędziesz punktów: {earned_points}"
        )
        
        if result:
            # Aktualizuj dostępność produktów w pliku
            try:
                file_path = os.path.join("data", "products.xlsx")
                df = pd.read_excel(file_path)
                
                # Pobierz nazwę pierwszej kolumny
                first_col_name = df.columns[0]
                
                # Aktualizuj dane w każdym wierszu
                for index, row in df.iterrows():
                    try:
                        data_str = str(row[first_col_name])
                        
                        if ',' in data_str:
                            data_parts = data_str.split(',')
                            if len(data_parts) >= 4:
                                product_id = data_parts[0].strip()
                                
                                # Sprawdź czy ten produkt jest w koszyku
                                if product_id in cart:
                                    product_name, cart_quantity, unit_price = cart[product_id]
                                    try:
                                        current_available = int(data_parts[3].strip())
                                        new_available = current_available - cart_quantity
                                        
                                        # Upewnij się, że nie zejdziemy poniżej 0
                                        new_available = max(0, new_available)
                                        
                                        # Aktualizuj wiersz
                                        data_parts[3] = str(new_available)
                                        updated_data = ','.join(data_parts)
                                        df.at[index, first_col_name] = updated_data
                                        
                                        print(f"Zaktualizowano produkt {product_id}: {current_available} -> {new_available}")
                                        
                                    except Exception as e:
                                        print(f"Błąd przy aktualizacji produktu {product_id}: {e}")
                                        continue
                        
                    except Exception as e:
                        continue
                
                # Zapisz zaktualizowany plik
                df.to_excel(file_path, index=False)
                print("Dostępność produktów została zaktualizowana w pliku")
                
            except Exception as e:
                print(f"Błąd przy aktualizacji pliku produktów: {e}")
                show_payment_error(f"Zamówienie zostało złożone, ale wystąpił problem z aktualizacją dostępności produktów: {str(e)}")
            
            # Dodaj punkty do bazy klientów
            try:
                
                customers_file = os.path.join("data", "customer.csv")
                
                # Wczytaj plik z klientami
                customers_df = pd.read_csv(customers_file)
                
                # Znajdź użytkownika po ID - używaj user_id zamiast user_name
                user_row = customers_df[customers_df['ID'] == int(user_id)]
                
                if not user_row.empty:
                    # Użytkownik znaleziony - dodaj punkty
                    user_index = user_row.index[0]
                    current_points = int(customers_df.at[user_index, 'POINTS'])
                    new_points = current_points + earned_points
                    
                    # Aktualizuj punkty i datę
                    customers_df.at[user_index, 'POINTS'] = new_points
                    customers_df.at[user_index, 'UPDATED'] = datetime.now().strftime('%Y-%m-%d')
                    
                    # Zapisz plik
                    customers_df.to_csv(customers_file, index=False)
                    
                    print(f"Zaktualizowano punkty użytkownika {user_name} (ID: {user_id}): {current_points} -> {new_points}")
                    
                    points_info = f"Twoje punkty: {current_points} + {earned_points} = {new_points} pkt"
                else:
                    print(f"Nie znaleziono użytkownika o ID {user_id} w bazie klientów")
                    points_info = f"Zdobyte punkty: {earned_points} pkt"
                
            except Exception as e:
                print(f"Błąd przy aktualizacji punktów: {e}")
                points_info = f"Zdobyte punkty: {earned_points} pkt (błąd zapisu do bazy)"
            
            # Przygotuj treść do wyświetlenia i zapisania
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Utwórz szczegółową listę produktów w koszyku
            cart_details = "ZAMÓWIONE PRODUKTY:\n"
            cart_details += "-" * 50 + "\n"
            
            for product_id, (product_name, cart_quantity, unit_price) in cart.items():
                item_total = cart_quantity * unit_price
                cart_details += f"• {product_name}\n"
                cart_details += f"  Ilość: {cart_quantity} szt.\n"
                cart_details += f"  Cena za sztukę: {unit_price:.2f} zł\n"
                cart_details += f"  Wartość: {item_total:.2f} zł\n"
                cart_details += "-" * 24 + "\n"
            
            cart_details += f"SUMA CAŁKOWITA: {total_amount:.2f} zł\n"
            cart_details += "-" * 24 + "\n\n"
            
            order_info = (
                f"=== ZAMÓWIENIE z {current_time} ===\n"
                f"Zamówienie zostało złożone!\n\n"
                f"{cart_details}"
                f"SZCZEGÓŁY ZAMÓWIENIA:\n"
                f"Kwota całkowita: {total_amount:.2f} zł\n"
                f"Metoda płatności: {method_names[payment_method]}\n"
                f"Adres dostawy: {delivery_address}\n\n"
                f"🎉 PUNKTY LOJALNOŚCIOWE 🎉\n"
                f"{points_info}\n"
                f"==============================\n"
            )
            
            # Zapisz zamówienie do pliku użytkownika (dopisz)
            try:
                # Stwórz folder DATABASE jeśli nie istnieje
                database_folder = "DATABASE"
                if not os.path.exists(database_folder):
                    os.makedirs(database_folder)
                
                # Ścieżka do pliku użytkownika
                user_file_path = os.path.join(database_folder, f"{user_id}.txt")
                
                # Dopisz treść zamówienia do pliku
                with open(user_file_path, 'a', encoding='utf-8') as file:
                    file.write(order_info + "\n")
                
                print(f"Zamówienie dopisane do pliku: {user_file_path}")
                
            except Exception as e:
                print(f"Błąd przy zapisywaniu zamówienia do pliku: {e}")
            
            # Wyświetl informację użytkownikowi (bez daty w wyświetlaniu)
            display_info = (
                f"Zamówienie zostało złożone!\n\n"
                f"Kwota: {total_amount:.2f} zł\n"
                f"Metoda płatności: {method_names[payment_method]}\n"
                f"Adres dostawy: {delivery_address}\n\n"
                f"🎉 PUNKTY LOJALNOŚCIOWE 🎉\n"
                f"{points_info}\n"
            )
            
            show_payment_info(display_info)
            
            # Odśwież panel produktów w głównym oknie
            if refresh_callback:
                refresh_callback()
            
            payment_root.destroy()
    
    def go_back():
        """Powrót do sklepu bez finalizowania"""
        payment_root.destroy()
    
    # Frame na przyciski
    buttons_frame = tk.Frame(payment_root)
    buttons_frame.pack(pady=20)
    
    finalize_button = tk.Button(
        buttons_frame,
        text="Finalizuj zamówienie",
        command=finalize_order,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=10
    )
    finalize_button.pack(side="left", padx=10)
    
    back_button = tk.Button(
        buttons_frame,
        text="Powrót do sklepu",
        command=go_back,
        bg="#2196F3",
        fg="white",
        font=("Arial", 12),
        padx=20,
        pady=10
    )
    back_button.pack(side="left", padx=10)
    
    payment_root.mainloop()
    
def main_shop_window(user_name="Użytkowniku", user_id=None):
    """Główne okno aplikacji sklepu"""
    root = tk.Tk()
    root.title("Sklep Żabka")
    root.geometry("1200x700") 
    
    # Koszyk: {product_id: (product_name, quantity, unit_price)}
    cart = {}
    
    label = tk.Label(root, text=f"Witaj w sklepie Żabka, {user_name}!", font=("Arial", 16))
    label.pack(pady=20)
    
    main_frame = tk.Frame(root)
    main_frame.pack(pady=10, fill="both", expand=True)
    
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5))
    
    products_label = tk.Label(left_frame, text="Produkty", font=("Arial", 14, "bold"))
    products_label.pack(pady=5)
    
    right_frame = tk.Frame(main_frame, width=350, bg="#f0f0f0")
    right_frame.pack(side="right", fill="y", padx=(5, 10))
    right_frame.pack_propagate(False)
    
    cart_label = tk.Label(right_frame, text="Koszyk", font=("Arial", 14, "bold"), bg="#f0f0f0")
    cart_label.pack(pady=10)
    
    cart_content_frame = tk.Frame(right_frame, bg="#f0f0f0")
    cart_content_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Frame na sumę
    total_frame = tk.Frame(right_frame, bg="#f0f0f0")
    total_frame.pack(side="bottom", fill="x", padx=10, pady=5)
    
    total_label = tk.Label(total_frame, text="Suma: 0.00 zł", font=("Arial", 12, "bold"), bg="#f0f0f0")
    total_label.pack()
    
    # Frame na przycisk płatności
    payment_button_frame = tk.Frame(right_frame, bg="#f0f0f0")
    payment_button_frame.pack(side="bottom", fill="x", padx=10, pady=5)
    
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
    
    def create_product_widget(parent, product_id, product_name, price, available):
        """Tworzy widget produktu"""
        # Ramka dla jednego produktu
        product_frame = tk.Frame(parent, bd=1, relief=tk.RAISED)
        product_frame.pack(fill="x", padx=10, pady=5)
        
        # Informacje o produkcie
        product_info = tk.Label(
            product_frame, 
            text=f"{product_name}\nCena: {price:.2f} zł\nDostępnych: {available} szt.",
            font=("Arial", 11),
            padx=10,
            justify="left"
        )
        product_info.pack(side="left", pady=10)
        
        # Frame na kontrolki po prawej stronie
        controls_frame = tk.Frame(product_frame)
        controls_frame.pack(side="right", padx=10, pady=10)
        
        # Kontrolki ilości tylko jeśli produkt jest dostępny
        if available > 0:
            quantity_label = tk.Label(controls_frame, text="Ilość:", font=("Arial", 10))
            quantity_label.pack(side="left", padx=(0, 5))
            
            quantity_entry = tk.Entry(controls_frame, width=5, font=("Arial", 10))
            quantity_entry.pack(side="left", padx=(0, 10))
            quantity_entry.insert(0, "1")  # Domyślna wartość

            buy_button = tk.Button(
                controls_frame, 
                text="Dodaj do koszyka", 
                command=lambda: buy_product(product_id, product_name, price, quantity_entry),
                bg="#4CAF50",
                fg="white",
                font=("Arial", 10),
                padx=15
            )
            buy_button.pack(side="left")
        else:
            # Jeśli produkt niedostępny
            unavailable_label = tk.Label(controls_frame, text="Niedostępny", 
                                       font=("Arial", 10), fg="red")
            unavailable_label.pack(side="left")
    
    def load_products():
        """Wczytuje i wyświetla produkty"""
        # Usuń wszystkie istniejące produkty
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        file_path = os.path.join("data", "products.xlsx")
        
        try:
            df = pd.read_excel(file_path)
            first_col_name = df.columns[0]
            
            # Parsuj dane rozdzielone przecinkami
            for index, row in df.iterrows():
                try:
                    data_str = str(row[first_col_name])
                    
                    if ',' in data_str:
                        data_parts = data_str.split(',')
                        if len(data_parts) >= 4:
                            product_id = data_parts[0].strip()
                            product_name = data_parts[1].strip()
                            try:
                                price = float(data_parts[2].strip())
                            except:
                                price = 0.0
                            try:
                                available = int(data_parts[3].strip())
                            except:
                                available = 0
                            
                            create_product_widget(scrollable_frame, product_id, product_name, price, available)
                        
                except Exception as e:
                    continue
        
        except Exception as e:
            show_shop_error(f"Wystąpił problem przy wczytywaniu pliku: {str(e)}")
    
    def refresh_products():
        """Funkcja odświeżająca panel produktów"""
        print("Odświeżanie panelu produktów...")
        load_products()
        # Wyczyść koszyk po zakupie
        cart.clear()
        update_cart_display()
    
    def go_to_payment():
        """Przejście do okna płatności z sprawdzeniem dostępności"""
        if not cart:
            show_cart_warning("Koszyk jest pusty! Dodaj produkty przed przejściem do płatności.")
            return
        
        # Przekaż user_id zamiast user_name
        payment_window(cart.copy(), user_name, user_id, refresh_products)
    
    def open_points_shop():
        """Otwiera okno sklepu za punkty"""
        points_shop_window(user_name, user_id)
    
    payment_button = tk.Button(
        payment_button_frame,
        text="Przejdź do płatności",
        command=go_to_payment,
        bg="#FF9800",
        fg="white",
        font=("Arial", 12, "bold"),
        pady=8
    )
    payment_button.pack(fill="x")
    
    def calculate_total():
        """Oblicza całkowitą sumę koszyka"""
        total = 0.0
        for product_id, (product_name, quantity, unit_price) in cart.items():
            total += quantity * unit_price
        return total
    
    def update_cart_display():
        # Czyść zawartość koszyka
        for widget in cart_content_frame.winfo_children():
            widget.destroy()
        
        if not cart:
            empty_label = tk.Label(cart_content_frame, text="Koszyk jest pusty", 
                                 font=("Arial", 10), bg="#f0f0f0", fg="gray")
            empty_label.pack(pady=20)
            payment_button.config(state="disabled")
        else:
            for product_id, (product_name, quantity, unit_price) in cart.items():
                item_frame = tk.Frame(cart_content_frame, bg="#ffffff", relief=tk.RAISED, bd=1)
                item_frame.pack(fill="x", pady=2, padx=5)
                
                item_total = quantity * unit_price
                
                item_label = tk.Label(item_frame, 
                                    text=f"{product_name}\nIlość: {quantity}\nCena jedn.: {unit_price:.2f} zł\nRazem: {item_total:.2f} zł", 
                                    font=("Arial", 9), bg="#ffffff", justify="left")
                item_label.pack(pady=5, padx=5, anchor="w")
            
            payment_button.config(state="normal")
        
        total = calculate_total()
        total_label.config(text=f"Suma: {total:.2f} zł")
    
    def validate_quantity(quantity_str):
        try:
            quantity = int(quantity_str)
            if quantity < 1 or quantity > 99:
                return False, "Ilość musi być między 1 a 99!"
            return True, quantity
        except ValueError:
            return False, "Podaj prawidłową liczbę!"
    
    def buy_product(product_id, product_name, unit_price, quantity_entry):
        quantity_str = quantity_entry.get().strip()
        
        if not quantity_str:
            show_cart_warning("Podaj ilość produktu!")
            return
        
        is_valid, result = validate_quantity(quantity_str)
        
        if not is_valid:
            show_cart_error(result)
            return
        
        quantity = result
        
        if product_id in cart:
            current_quantity = cart[product_id][1]
            new_quantity = current_quantity + quantity
            cart[product_id] = (product_name, new_quantity, unit_price)
        else:
            cart[product_id] = (product_name, quantity, unit_price)
                
        update_cart_display()
        show_cart_info(f"Dodano {quantity} szt. '{product_name}' do koszyka!")
    
    def clear_cart():
        """Funkcja czyszcząca koszyk"""
        if cart:
            result = ask_cart_question("Czy na pewno chcesz wyczyścić koszyk?")
            if result:
                cart.clear()
                update_cart_display()
                show_cart_info("Koszyk został wyczyszczony!")
        else:
            show_cart_info("Koszyk jest już pusty!")
    
    # Wczytaj produkty przy starcie
    load_products()
    
    # Frame na przyciski na dole
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    clear_cart_button = tk.Button(button_frame, text="Wyczyść koszyk", command=clear_cart,
                                 bg="#f44336", fg="white", font=("Arial", 10), padx=15)
    clear_cart_button.pack(side="left", padx=5)
    
    points_shop_button = tk.Button(button_frame, text="Sklep za punkty", command=open_points_shop,
                                  bg="#9C27B0", fg="white", font=("Arial", 10), padx=15)
    points_shop_button.pack(side="left", padx=5)
    
    def close_app():
        try:
            root.quit()
        except:
            pass
        finally:
            root.destroy()
    
    close_button = tk.Button(button_frame, text="Zamknij", command=close_app)
    close_button.pack(side="left", padx=5)
    
    update_cart_display()
    
    root.mainloop()

def start_gui():
    login_window(main_shop_window)
