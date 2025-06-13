from gui import start_gui
import random

#DEKORATOR
def lucky_number_decorator(func):
    def wrapper():
        func()
        lucky = random.randint(1, 100)
        print(f"Hej twoja szczęśliwa liczba na dziś to: {lucky}")
    return wrapper

# Funkcja z dekoratorem
@lucky_number_decorator
def greet_user():
    print("Cześć użytkowniku")

# Wywołanie
if __name__ == "__main__":
    greet_user()
    start_gui()
