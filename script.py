import sqlite3
from argon2 import PasswordHasher

ph = PasswordHasher()
DB_NAME = "Databaser.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def hash_existing_passwords():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT userID, password FROM users")
    users = cur.fetchall()
    for user_id, pwd in users:
        if not pwd.startswith("$argon2"):   
            hashed = ph.hash(pwd)
            cur.execute("UPDATE users SET password = ? WHERE userID = ?", (hashed, user_id))
    con.commit()
    con.close()

def register_user():
    con = connect_db()
    cur = con.cursor()
    navn = input("Skriv inn brukernavn: ")
    passord = input("Skriv inn passord: ")
    hashed = ph.hash(passord)
    try:
        cur.execute("INSERT INTO users (name, password, is_employee) VALUES (?, ?, 0)", (navn, hashed))
        con.commit()
        print("Bruker registrert")
    except sqlite3.IntegrityError:
        print("Brukernavn eksisterer allerede")
    finally:
        con.close()

def login():
    con = connect_db()
    cur = con.cursor()
    navn = input("Brukernavn: ")
    passord = input("Passord: ")
    cur.execute("SELECT userID, password, is_employee FROM users WHERE name = ?", (navn,))
    bruker = cur.fetchone()
    con.close()
    if not bruker:
        print("Bruker ikke funnet")
        return None
    user_id, stored_hash, is_employee = bruker
    try:
        ph.verify(stored_hash, passord)
        print("Innlogging vellykket")
        return (user_id, bool(is_employee))
    except:
        print("Feil passord")
        return None

def show_burgers():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT burgerID, name FROM burgers")
    burgere = cur.fetchall()
    con.close()
    print("\nTilgjengelige burgere:")
    for b in burgere:
        print(str(b[0]) + ". " + b[1])

def create_order(user_id):
    show_burgers()
    burger_id = input("Velg burger-ID å bestille: ")
    try:
        burger_id = int(burger_id)
    except:
        print("Ugyldig ID")
        return
    con = connect_db()
    cur = con.cursor()
    cur.execute("INSERT INTO orders (userID, burgerID, produced) VALUES (?, ?, 0)", (user_id, burger_id))
    con.commit()
    con.close()
    print("Bestilling registrert")

def show_my_orders(user_id):
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        SELECT o.orderID, b.name, o.produced
        FROM orders o
        JOIN burgers b ON o.burgerID = b.burgerID
        WHERE o.userID = ?
    """, (user_id,))
    ordre = cur.fetchall()
    con.close()
    print("\nMine ordre:")
    for o in ordre:
        status = "Produsert" if o[2] else "Ikke produsert"
        print("Ordre " + str(o[0]) + ": " + o[1] + " - " + status)

def show_all_orders():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        SELECT o.orderID, u.name, b.name, o.produced
        FROM orders o
        JOIN users u ON o.userID = u.userID
        JOIN burgers b ON o.burgerID = b.burgerID
    """)
    ordre = cur.fetchall()
    con.close()
    print("\nAlle ordre:")
    for o in ordre:
        status = "Produsert" if o[3] else "Ikke produsert"
        print("Ordre " + str(o[0]) + ": " + o[1] + " - " + o[2] + " - " + status)

def show_inventory():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT name, quantity FROM ingredients")
    ingredienser = cur.fetchall()
    con.close()
    print("\nInventar:")
    for i in ingredienser:
        print(i[0] + ": " + str(i[1]) + " stk")

def mark_order_done():
    show_all_orders()
    order_id = input("Velg ordre-ID å markere som fullført: ")
    try:
        order_id = int(order_id)
    except:
        print("Ugyldig ID")
        return

    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT burgerID FROM orders WHERE orderID = ?", (order_id,))
    res = cur.fetchone()
    if not res:
        print("Ordre ikke funnet")
        con.close()
        return
    burger_id = res[0]

    cur.execute("SELECT ingredientID, quantity_per_burger FROM burger_ingredients WHERE burgerID = ?", (burger_id,))
    ingredienser = cur.fetchall()
    for ing in ingredienser:
        cur.execute("UPDATE ingredients SET quantity = quantity - ? WHERE ingredientID = ?", (ing[1], ing[0]))

    cur.execute("UPDATE orders SET produced = 1 WHERE orderID = ?", (order_id,))
    con.commit()
    con.close()
    print("Ordre markert som fullført")

def customer_menu(user_id):
    while True:
        print("\n1. Se burgere")
        print("2. Lag ny ordre")
        print("3. Mine ordre")
        print("4. Logg ut")
        valg = input("Velg handling: ")
        if valg == "1":
            show_burgers()
        elif valg == "2":
            create_order(user_id)
        elif valg == "3":
            show_my_orders(user_id)
        elif valg == "4":
            break
        else:
            print("Ugyldig valg")

def employee_menu():
    while True:
        print("\n1. Se alle ordre")
        print("2. Marker ordre som fullført")
        print("3. Se inventar")
        print("4. Logg ut")
        valg = input("Velg handling: ")
        if valg == "1":
            show_all_orders()
        elif valg == "2":
            mark_order_done()
        elif valg == "3":
            show_inventory()
        elif valg == "4":
            break
        else:
            print("Ugyldig valg")

def main():
    hash_existing_passwords()  
    print("Velkommen til Burger Queen")
    while True:
        print("\n1. Logg inn")
        print("2. Registrer bruker")
        print("3. Avslutt")
        valg = input("Velg handling: ")
        if valg == "1":
            bruker = login()
            if bruker:
                user_id, is_employee = bruker
                if is_employee:
                    employee_menu()
                else:
                    customer_menu(user_id)
        elif valg == "2":
            register_user()
        elif valg == "3":
            print("Ha det bra")
            break
        else:
            print("Ugyldig valg")

if __name__ == "__main__":
    main()
