CREATE TABLE users (
  id SERIAL PRIMARY KEY, 
  username TEXT, 
  password TEXT
  );

CREATE TABLE messages (
  id SERIAL PRIMARY KEY, 
  content TEXT
  );

CREATE TABLE recipes (
  id SERIAL PRIMARY KEY,
  recipename TEXT,
  );

CREATE TABLE incredients (
  id SERIAL PRIMARY KEY, 
  incredientname TEXT,
  incredientamount TEXT
  );

CREATE TABLE recipeincredients (
    incredient_id INTEGER REFERENCES incredients,
    recipe_id SERIAL REFERENCES recipes
  );

