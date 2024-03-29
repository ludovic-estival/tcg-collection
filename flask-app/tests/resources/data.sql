INSERT OR REPLACE INTO user(username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f');

INSERT OR REPLACE INTO collection
VALUES
  (1, 'collection1', 'test'),
  (2, 'collection2', 'test');

INSERT OR REPLACE INTO contain
VALUES
  (1, 'MP23-001', 'PSE', 2),
  (1, 'MP23-002', 'GR', 1);

INSERT OR REPLACE INTO card
VALUES
  ('MP23-001', 'PSE', 'Lovely Labrynth', '5'),
  ('MP23-002', 'GR', 'Lady Labrynth', '2'); 

INSERT OR REPLACE INTO snapshot(idCollection, snapDate, cardsNumber, totalValue)
VALUES
  (1, datetime('now'), 5, 10.1),
  (1, datetime('now'), 10, 20.5);
  
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