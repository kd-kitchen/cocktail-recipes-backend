CREATE SCHEMA account;

CREATE TABLE account.account
(
    id       SERIAL PRIMARY KEY,
    username VARCHAR(200) NOT NULL,
    email    VARCHAR(200) NOT NULL,
    password TEXT CHECK (CHAR_LENGTH(password) > 0),
    is_admin BOOL         NOT NULL DEFAULT FALSE
);

CREATE UNIQUE INDEX uq_account_account__username ON account.account (LOWER(username));
CREATE UNIQUE INDEX uq_account_account__email ON account.account (LOWER(email));
