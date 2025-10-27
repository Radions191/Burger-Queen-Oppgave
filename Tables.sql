DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS burgers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS burger_ingredients;

CREATE TABLE users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_employee INTEGER NOT NULL CHECK (is_employee IN (0,1))
);

CREATE TABLE burgers (
    burgerID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE ingredients (
    ingredientID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    quantity INTEGER NOT NULL
);

CREATE TABLE orders (
    orderID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER NOT NULL,
    burgerID INTEGER NOT NULL,
    produced INTEGER NOT NULL CHECK (produced IN (0,1)),
    FOREIGN KEY(userID) REFERENCES users(userID),
    FOREIGN KEY(burgerID) REFERENCES burgers(burgerID)
);

CREATE TABLE burger_ingredients (
    burgerID INTEGER NOT NULL,
    ingredientID INTEGER NOT NULL,
    quantity_per_burger INTEGER DEFAULT 1,
    FOREIGN KEY(burgerID) REFERENCES burgers(burgerID),
    FOREIGN KEY(ingredientID) REFERENCES ingredients(ingredientID)
);

INSERT INTO users (name, password, is_employee) VALUES
('Lukas', 'solsikke123', 0),
('Bent', 'fjellrose', 0),
('Ilja', 'sjokolade', 0),
('Kateryna', 'himmelbla', 1);

INSERT INTO burgers (name) VALUES
('Whopper Queen'),
('Triple Cheesy Princess');

INSERT INTO ingredients (name, quantity) VALUES
('Burgerbrød', 9001),
('Burgerkjøtt', 10),
('Salat', 8008),
('Tomat', 1337),
('Ost', 42),
('Agurk', 666),
('Potet', 420);

INSERT INTO burger_ingredients (burgerID, ingredientID)
SELECT 1, ingredientID FROM ingredients WHERE name IN ('Burgerbrød','Burgerkjøtt','Salat','Tomat');

INSERT INTO burger_ingredients (burgerID, ingredientID)
SELECT 2, ingredientID FROM ingredients WHERE name IN ('Burgerbrød','Burgerkjøtt','Salat','Tomat','Ost','Potet');

INSERT INTO orders (userID, burgerID, produced) VALUES
(1, 1, 1),
(1, 1, 0),
(4, 2, 0),
(3, 1, 0);