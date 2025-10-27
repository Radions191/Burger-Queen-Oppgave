import sqlite3
from argon2 import PasswordHasher


ph = PasswordHasher()

DB_NAME = "Databaser.db"

def connect_db():
    return sqlite3.connect(DB_NAME)