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
    burger_amount INTEGER DEFAULT 1,
    FOREIGN KEY(burgerID) REFERENCES burgers(burgerID),
    FOREIGN KEY(ingredientID) REFERENCES ingredients(ingredientID)
);  

INSERT INTO users (name, password, is_employee) VALUES
('Geralt', 'hesterbest', 0),
('Yennefer', 'qwerty', 0),
('Roach', 'pizza', 0),
('Jaskier', 'nyttpassord', 1);

INSERT INTO burgers (name) VALUES
('Whopper Queen'),
('Triple Cheesy Princess');

INSERT INTO ingredients (name, quantity) VALUES
('Burgerbrød', 230),
('Burgerkjøtt', 30),
('Salat', 8008),
('Tomat', 1337),
('Ost', 52),
('Agurk', 666),
('Potet', 420);

INSERT INTO burger_ingredients (burgerID, ingredientID) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4);

INSERT INTO burger_ingredients (burgerID, ingredientID) VALUES
(2, 1),
(2, 2),
(2, 3),
(2, 4),
(2, 5),
(2, 7);

INSERT INTO orders (userID, burgerID, produced) VALUES
(1, 1, 1),
(1, 1, 0),
(4, 2, 0),
(3, 1, 0);