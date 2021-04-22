CREATE TABLE users (
  id SERIAL PRIMARY KEY, 
  username TEXT UNIQUE, 
  password TEXT,
  admin BOOLEAN DEFAULT false
  );

CREATE TABLE recipes (
  id SERIAL PRIMARY KEY,
  recipename TEXT,
  visible INTEGER DEFAULT 1,
  popularity INTEGER DEFAULT 0,
  owner_id SERIAL REFERENCES users
  );

CREATE TABLE messages (
  id SERIAL PRIMARY KEY, 
  content TEXT,
  recipe_id SERIAL REFERENCES recipes,
  user_id SERIAL REFERENCES users,
  sent_at TIMESTAMP,
  edited_at TIMESTAMP
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

CREATE TABLE userrecipes (
  user_id SERIAL REFERENCES users,
  recipe_id SERIAL REFERENCES recipes
  );
