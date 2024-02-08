-- DROP dans le sens inverse de création

DROP TABLE IF EXISTS snapshot;
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

CREATE TABLE snapshot (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  idCollection INTEGER NOT NULL,
  snapDate DATE NOT NULL,
  cardsNumber INT NOT NULL,
  totalValue FLOAT NOT NULL,
  FOREIGN KEY (idCollection) REFERENCES collection(id)
);

CREATE TABLE contain (
  idCollection INTEGER NOT NULL,
  cardCode CHARACTER(10) NOT NULL,
  rarity CHARACTER(10) NOT NULL,
  nbcopy INT NOT NULL,
  FOREIGN KEY (idCollection) REFERENCES collection(id),
  FOREIGN KEY (cardCode, rarity) REFERENCES carte(code, rarity)
);

CREATE TABLE card (
  code CHARACTER(10) NOT NULL,
  rarity CHARACTER(10) NOT NULL,
  name VARCHAR(200) NOT NULL,
  price FLOAT NOT NULL,
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