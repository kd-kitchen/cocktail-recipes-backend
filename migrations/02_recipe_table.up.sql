CREATE SCHEMA recipe;


CREATE TABLE recipe.recipe
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(500) NOT NULL CHECK (CHAR_LENGTH(name) > 0),
    description TEXT,
    instruction TEXT
);

CREATE UNIQUE INDEX uq_recipe_recipe__name ON recipe.recipe (LOWER(name));


CREATE TABLE recipe.ingredient
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(500) NOT NULL CHECK (CHAR_LENGTH(name) > 0),
    description TEXT
);

CREATE UNIQUE INDEX uq_recipe_ingredient__name ON recipe.ingredient (LOWER(name));


CREATE TABLE recipe.recipe_ingredient_assc_table
(
    id            SERIAL PRIMARY KEY,
    recipe_id     INT         NOT NULL,
    ingredient_id INT         NOT NULL,
    quantity      FLOAT       NOT NULL,
    unit          VARCHAR(50) NOT NULL CHECK (CHAR_LENGTH(unit) > 0),
    CONSTRAINT fk_recipe_ingredient_asc_tbl__recipe_id FOREIGN KEY (recipe_id) REFERENCES recipe.recipe (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_recipe_ingredient_asc_tbl__ingredient_id FOREIGN KEY (ingredient_id) REFERENCES recipe.ingredient (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE UNIQUE INDEX uq_recipe_ingredient_assc_table__fk ON recipe.recipe_ingredient_assc_table (recipe_id, ingredient_id);

CREATE TABLE recipe.tag
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL CHECK (CHAR_LENGTH(name) > 0)
);

CREATE UNIQUE INDEX uq_recipe_tag__name ON recipe.tag (LOWER(name));


CREATE TABLE recipe.recipe_tag_assc_table
(
    id        SERIAL PRIMARY KEY,
    recipe_id INT NOT NULL,
    tag_id    INT NOT NULL,
    CONSTRAINT fk_recipe_tag_asc_tbl__recipe_id FOREIGN KEY (recipe_id) REFERENCES recipe.recipe (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_recipe_tag_asc_tbl__tag_id FOREIGN KEY (tag_id) REFERENCES recipe.tag (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE UNIQUE INDEX uq_recipe_recipe_tag_assc_table__fk ON recipe.recipe_tag_assc_table (recipe_id, tag_id);

CREATE TABLE recipe.recipe_image
(
    id        SERIAL PRIMARY KEY,
    recipe_id INT  NOT NULL,
    image_url TEXT NOT NULL,
    CONSTRAINT fk_recipe_image__recipe_id FOREIGN KEY (recipe_id) REFERENCES recipe.recipe (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE recipe.ingredient_image
(
    id            SERIAL PRIMARY KEY,
    ingredient_id INT  NOT NULL,
    image_url     TEXT NOT NULL,
    CONSTRAINT fk_ingredient_image__ingredient_id FOREIGN KEY (ingredient_id) REFERENCES recipe.ingredient (id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- ingesting initial data
INSERT INTO recipe.ingredient (name, description)
VALUES ('Lemon', 'Yellow fruit, sour taste.'),
       ('Mint', 'Leafy plant, smells fresh.'),
       ('Lime', 'Green fruit, small and sour.'),
       ('White Rum', 'Common rum such as Barcardi.'),
       ('Soda Water', 'Carbonated water, tasteless.');

INSERT INTO recipe.recipe (name, description, instruction)
VALUES ('Mojito', 'A very tasty drink', 'Instructions to make a mojito');

INSERT INTO recipe.recipe_ingredient_assc_table (recipe_id, ingredient_id, quantity, unit)
SELECT r.id,
       i.id,
       CASE
           WHEN LOWER(i.name) = 'lemon' THEN 5
           WHEN LOWER(i.name) = 'mint' THEN 4
           END,
       CASE
           WHEN LOWER(i.name) = 'lemon' THEN 'gram'
           WHEN LOWER(i.name) = 'mint' THEN 'litres'
           END
FROM recipe.recipe r,
     recipe.ingredient i
WHERE LOWER(r.name) = 'mojito'
  AND LOWER(i.name) IN ('lemon', 'mint')
