DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS rarity;

CREATE TABLE card (
  code CHARACTER(10) ,
  rarity CHARACTER(10),
  name VARCHAR(200),
  price FLOAT,
  nbcopy INT,
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
  ('SR', 'Secret Rare'),
  ('PSR', 'Prismatic Secret Rare'),
  ('GH', 'Ghost Rare'),
  ('GR', 'Gold Rare'),
  ('QCSE', 'Quarter Century Secret Rare');