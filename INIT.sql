CREATE SCHEMA IF NOT EXISTS relational;
CREATE SCHEMA IF NOT EXISTS timescale;

CREATE TABLE IF NOT EXISTS relational.users(
    id              SERIAL PRIMARY KEY,
    firstname       TEXT,
    lastname        TEXT,
    phone           TEXT,
    address         TEXT,
    iban            TEXT,
    company_id      INT4
);

CREATE TABLE IF NOT EXISTS relational.files(
    id              SERIAL PRIMARY KEY,
    filename        TEXT UNIQUE,
    created         timestamp
);

CREATE TABLE IF NOT EXISTS relational.file_access(
    user_id     INT4 REFERENCES relational.users(id) ON DELETE CASCADE,
    file_id     INT4 REFERENCES relational.files(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id,file_id)
);

CREATE TABLE IF NOT EXISTS timescale.tokens (
    id BIGSERIAL,
    token TEXT,
    user_id  INT4,
    created TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, created)
);

CREATE TABLE IF NOT EXISTS relational.tokens (
    id BIGSERIAL,
    token TEXT,
    user_id  INT4,
    created TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, created)
);

SELECT create_hypertable('timescale.tokens', 'created');