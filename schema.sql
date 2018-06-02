CREATE TABLE decks(
  id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
  title VARCHAR(100) NOT NULL,
  subject VARCHAR(100) NOT NULL,
  author VARCHAR(100) NOT NULL
);

CREATE TABLE users_decks(
  id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
  user_id INT(11) NOT NULL,
  deck_id INT(11) NOT NULL
);

CREATE TABLE users(
  id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
  username VARCHAR(100) NOT NULL,
  email VARCHAR(320) NOT NULL,
  password VARCHAR(100) NOT NULL,
  register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (USERNAME)
);

CREATE TABLE cards(
  id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
  front VARCHAR(500) NOT NULL,
  back VARCHAR(500) NOT NULL,
  deck_id INT(11) NOT NULL
);

CREATE TABLE cards_tags(
  id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
  tag_id INT(11) NOT NULL,
  card_id INT(11) NOT NULL
);

CREATE TABLE tags(
  id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
  name VARCHAR(100) NOT NULL
);
