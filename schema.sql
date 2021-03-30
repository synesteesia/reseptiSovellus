CREATE TABLE users (
  id SERIAL PRIMARY KEY, 
  username TEXT, 
  password TEXT
  );

CREATE TABLE recipes (
  id SERIAL PRIMARY KEY,
  recipename TEXT,
  visible INTEGER DEFAULT 1
  );

CREATE TABLE messages (
  id SERIAL PRIMARY KEY, 
  content TEXT,
  username TEXT,
  recipe_id SERIAL REFERENCES recipes,
  user_id SERIAL REFERENCES users
  );

CREATE TABLE ingredients (
  id SERIAL PRIMARY KEY, 
  ingredientname TEXT,
  ingredientamount TEXT,
  recipe_id SERIAL REFERENCES recipes
  );

CREATE TABLE recipecontents (
  id SERIAL PRIMARY KEY, 
  content TEXT,
  recipe_id SERIAL REFERENCES recipes
  );

