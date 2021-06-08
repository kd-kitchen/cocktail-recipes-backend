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
    id   SERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL CHECK (CHAR_LENGTH(name) > 0)
);

CREATE UNIQUE INDEX uq_recipe_ingredient__name ON recipe.ingredient (LOWER(name));


CREATE TABLE recipe.recipe_ingredient_assc_table
(
    id            SERIAL PRIMARY KEY,
    recipe_id     SERIAL      NOT NULL,
    ingredient_id SERIAL      NOT NULL,
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
    recipe_id SERIAL NOT NULL,
    tag_id    SERIAL NOT NULL,
    CONSTRAINT fk_recipe_tag_asc_tbl__recipe_id FOREIGN KEY (recipe_id) REFERENCES recipe.recipe (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_recipe_tag_asc_tbl__tag_id FOREIGN KEY (tag_id) REFERENCES recipe.tag (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE UNIQUE INDEX uq_recipe_recipe_tag_assc_table__fk ON recipe.recipe_tag_assc_table (recipe_id, tag_id);
