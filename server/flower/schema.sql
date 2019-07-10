DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS flower;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ip TEXT NOT NULL,
  phone_number TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  nickname TEXT NOT NULL,
  head TEXT NOT NULL,
  level INTEGER NOT NULL,
  EXPoint INTEGER NOT NULL,
  friend TEXT NOT NULL,
  personal_description TEXT NOT NULL,
  sex TEXT NOT NULL,
  age INTEGER NOT NULL,
  region TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  like INTEGER NOT NULL,
  liker TEXT NOT NULL,
  image TEXT NOT NULL,
  image_size TEXT NOT NULL,
  comment TEXT NOT NULL,
  FOREIGN KEY
(author_id) REFERENCES user
(id)
);

CREATE TABLE flower (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cn_name TEXT NOT NULL,
  en_name TEXT NOT NULL,
  type TEXT NOT NULL,  -- 主花/配花
  flower_language TEXT NOT NULL,
  image TEXT NOT NULL,  -- 用id作为名称
  description TEXT NOT NULL,
  similar TEXT NOT NULL,
  combined TEXT NOT NULL,  -- 用cn_name记录常用搭配
  price INTEGER NOT NULL
);