DROP TABLE IF EXISTS card;

CREATE TABLE card (
  code CHARACTER(10) ,
  rarity CHARACTER(10),
  name VARCHAR(100),
  price FLOAT,
  nbcopy INT,
  PRIMARY KEY (code, rarity)
);