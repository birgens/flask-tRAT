DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS test_taker;
DROP TABLE IF EXISTS taker_answer;
DROP TABLE IF EXISTS answer;


CREATE TABLE user (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL
);


CREATE TABLE test_taker (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  test_id INTEGER NOT NULL,
  url TEXT NOT NULL,
  FOREIGN KEY (test_id) REFERENCES test (id)
);


CREATE TABLE test (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE question (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  test_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  prompt TEXT NOT NULL,
  FOREIGN KEY (test_id) REFERENCES test (id)
);


CREATE TABLE answer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER NOT NULL,
  body TEXT NOT NULL,
  weight REAL NOT NULL,
  FOREIGN KEY (question_id) REFERENCES question (id)
);

CREATE TABLE taker_answer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  answer_id INTEGER NOT NULL,
  testtaker_id INTEGER NOT NULL,
  FOREIGN KEY (testtaker_id) REFERENCES test_taker (id),
  FOREIGN KEY (answer_id) REFERENCES answer (id)
);
