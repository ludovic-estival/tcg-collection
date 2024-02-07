-- DROP dans le sens inverse de création

DROP TABLE IF EXISTS contain;
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS collection;
DROP TABLE IF EXISTS rarity;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE collection (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  user TEXT NOT NULL,
  FOREIGN KEY (user) REFERENCES user(username)
);

CREATE TABLE contain (
  idCollection INTEGER,
  cardCode CHARACTER(10),
  rarity CHARACTER(10),
  nbcopy INT,
  FOREIGN KEY (idCollection) REFERENCES collection(id),
  FOREIGN KEY (cardCode, rarity) REFERENCES carte(code, rarity)
);

CREATE TABLE card (
  code CHARACTER(10) ,
  rarity CHARACTER(10),
  name VARCHAR(200),
  price FLOAT,
  FOREIGN KEY (rarity) REFERENCES rarity(code),
  PRIMARY KEY (code, rarity)
);

CREATE TABLE rarity (
  code CHARACTER(10) PRIMARY KEY,
  label VARCHAR(50)
);

INSERT OR REPLACE INTO rarity
VALUES
  ('C', 'Common'),
  ('R', 'Rare'),
  ('SR', 'Super Rare'),
  ('UR', 'Ultra Rare'),
  ('UL', 'Ultimate Rare'),
  ('SE', 'Secret Rare'),
  ('PSE', 'Prismatic Secret Rare'),
  ('GH', 'Ghost Rare'),
  ('GR', 'Gold Rare'),
  ('QCSE', 'Quarter Century Secret Rare');

INSERT OR REPLACE INTO card
VALUES
  ('code1', 'C', 'Carte1', 10.2),
  ('code2', 'C', 'Carte2', 10.5);

INSERT OR REPLACE INTO user(username, password)
VALUES ('Trahald', 'test');

INSERT OR REPLACE INTO collection(name, user)
VALUES ('Nom1', 'Trahald');

INSERT OR REPLACE INTO contain 
VALUES
  (1, 'code1', 'C', 1),
  (1, 'code2', 'C', 3);