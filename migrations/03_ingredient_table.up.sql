CREATE SCHEMA ingredient;

CREATE TABLE ingredient.ingredient
(
    iid             SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    creator_id      NUMERIC,
    creation_date   TIMESTAMP [ (p) ] [ without time zone ],
    last_updated    TIMESTAMP [ (p) ] [ without time zone ],
    description     VARCHAR(200)
);

CREATE UNIQUE INDEX uq_ingredient_ingredient__name ON ingredient.ingredient (LOWER(name));
