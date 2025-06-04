import os
import csv
import pytz
import re
import random
from datetime import datetime
from tkinter import messagebox
import tkinter as tk  # potrzebne do .END

def add_user(email_entry, password_entry, name_entry, phone_entry):
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()

    if email and password and name and phone:
        # Walidacja e-maila
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            messagebox.showerror("Nieprawidłowy e-mail", f"'{email}' nie jest poprawnym adresem e-mail.")
            return

        file_path = os.path.join("data", "customer.csv")

        if not os.path.exists(file_path):
            messagebox.showerror("Błąd", f"Plik {file_path} nie istnieje.")
            return

        with open(file_path, mode="r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            # Sprawdź czy email już istnieje
            for row in rows:
                if row["E-MAIL"].strip().lower() == email.lower():
                    messagebox.showerror("Błąd", f"Użytkownik z emailem '{email}' już istnieje.")
                    return

            # Pobierz istniejące ID
            existing_ids = {row["ID"] for row in rows}

        # Generuj unikalne 4-cyfrowe ID
        while True:
            new_id = str(random.randint(1000, 9999))
            if new_id not in existing_ids:
                break

        # Aktualna data w strefie Warszawa
        warsaw = pytz.timezone("Europe/Warsaw")
        now = datetime.now(warsaw).strftime("%Y-%m-%d")

        new_user = {
            "ID": new_id,
            "NAME": name,
            "E-MAIL": email,
            "PASSWORD": password,
            "PHONE": phone,
            "CREATED": now,
            "UPDATED": now,
        }

        # Dopisz do pliku CSV 
        with open(file_path, mode="a", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["ID", "NAME", "E-MAIL", "PASSWORD", "PHONE", "CREATED", "UPDATED"])
            writer.writerow(new_user)

        # Tworzenie pliku w folderze DATABASE
        database_dir = "DATABASE"
        os.makedirs(database_dir, exist_ok=True)
        txt_file_path = os.path.join(database_dir, f"{new_id}.txt")
        open(txt_file_path, "w").close()  # Tworzy pusty plik

        messagebox.showinfo("Sukces", f"Dodano użytkownika: {name} (ID: {new_id})")

        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)

    else:
        messagebox.showwarning("Brak danych", "Wprowadź poprawnie wszystkie dane dla nowego użytkownika.")


def delete_user(delete_entry):
    email_to_delete = delete_entry.get().strip().lower()

    if not email_to_delete:
        messagebox.showwarning("Brak danych", "Wprowadź e-mail użytkownika do usunięcia.")
        return

    file_path = os.path.join("data", "customer.csv")

    if not os.path.exists(file_path):
        messagebox.showerror("Błąd", f"Plik {file_path} nie istnieje.")
        return

    with open(file_path, mode="r", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Szukamy użytkownika do usunięcia
    user_to_delete = None
    for row in rows:
        if row["E-MAIL"].strip().lower() == email_to_delete:
            user_to_delete = row
            break

    if not user_to_delete:
        messagebox.showerror("Nie znaleziono", f"Użytkownik o e-mailu '{email_to_delete}' nie istnieje.")
        return

    # Usuń użytkownika z listy
    filtered_rows = [row for row in rows if row["E-MAIL"].strip().lower() != email_to_delete]

    # Zapisz przefiltrowaną listę z powrotem do pliku 
    with open(file_path, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "NAME", "E-MAIL", "PASSWORD", "PHONE", "CREATED", "UPDATED"])
        writer.writeheader()
        writer.writerows(filtered_rows)

    # Przygotuj dane do archiwizacji
    user_id = user_to_delete["ID"]
    txt_file_path = os.path.join("DATABASE", f"{user_id}.txt")

    txt_content = ""
    if os.path.exists(txt_file_path):
        with open(txt_file_path, "r", encoding="utf-8") as f:
            txt_content = f.read()

    # DODANO PASSWORD DO ARCHIWIZACJI
    archive_data = f"ID: {user_to_delete['ID']}\n" \
                   f"NAME: {user_to_delete['NAME']}\n" \
                   f"E-MAIL: {user_to_delete['E-MAIL']}\n" \
                   f"PASSWORD: {user_to_delete.get('PASSWORD', '[brak hasła]')}\n" \
                   f"PHONE: {user_to_delete['PHONE']}\n" \
                   f"CREATED: {user_to_delete['CREATED']}\n" \
                   f"UPDATED: {user_to_delete['UPDATED']}\n" \
                   f"PLIK: {txt_content if txt_content else '[brak zawartości]'}\n" \
                   f"{'-' * 40}\n"

    # Zapisz do pliku Archivum
    archivum_dir = os.path.join("DATABASE", "ARCHIVUM")
    os.makedirs(archivum_dir, exist_ok=True)

    archivum_path = os.path.join(archivum_dir, "Archivum.txt")
    with open(archivum_path, "a", encoding="utf-8") as arch_file:
        arch_file.write(archive_data)

    # Usuń plik txt z DATABASE po archiwizacji
    if os.path.exists(txt_file_path):
        try:
            os.remove(txt_file_path)
        except Exception as e:
            messagebox.showwarning("Uwaga", f"Nie udało się usunąć pliku {txt_file_path}: {e}")

    messagebox.showinfo("Sukces", f"Użytkownik o e-mailu '{email_to_delete}' został usunięty i zarchiwizowany.")
    delete_entry.delete(0, tk.END)