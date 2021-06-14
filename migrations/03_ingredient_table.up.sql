CREATE SCHEMA ingredient;

CREATE TABLE ingredient.ingredient
(
    iid             SERIAL PRIMARY KEY,
    iname           VARCHAR(200) NOT NULL,
    creator_id      NUMERIC,
    creation_date   VARCHAR(200),
    last_updated    VARCHAR(200),
    description     VARCHAR(200)
);

CREATE UNIQUE INDEX uq_ingredient_ingredient__name ON ingredient.ingredient (LOWER(name));
