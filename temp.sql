/*
EXPLAIN ANALYZE SELECT u.id, u.firstname, f.*, COUNT(*) OVER () AS total_users
FROM relational.users u
LEFT JOIN relational.file_access fa ON fa.user_id = u.id
LEFT JOIN relational.files f ON f.id = fa.file_id
WHERE u.firstname = 'Mark';

DELETE FROM timescale.tokens
WHERE created > NOW();

CREATE TABLE timescale.tokensr AS 
SELECT * FROM timescale.tokens;

ALTER TABLE timescale.tokens RENAME TO oldtokens;
ALTER TABLE timescale.tokensr RENAME TO tokens;

SELECT u.id, u.firstname, t.*, COUNT(*) OVER () AS total_users
FROM relational.users u
LEFT JOIN timescale.tokens t ON t.user_id = u.id
WHERE u.firstname = 'Mark' and  u.lastname = 'James';

EXPLAIN ANALYZE SELECT u.id, u.firstname, t.*, COUNT(*) OVER () AS total_users
FROM relational.users u
LEFT JOIN timescale.tokens t ON t.user_id = u.id
WHERE u.firstname = 'Mark' and t.created < NOW() and t.created > NOW() - INTERVAL '1 hours';


PREPARE get_last_token (INTEGER) AS
SELECT * FROM timescale.tokens
WHERE user_id = $1 and created < NOW() ORDER BY created LIMIT 1;

PREPARE get_last_token (INTEGER) AS
SELECT * FROM timescale.tokens
WHERE user_id = $1 and created < NOW() ORDER BY created LIMIT 1;
SELECT pg_prewarm('timescale.tokens');



execute get_last_token(449)
CREATE OR REPLACE FUNCTION get_last_token(uid INTEGER)
RETURNS TABLE(token_id INTEGER, token_created TIMESTAMP) AS
$$
BEGIN
    RETURN QUERY
    SELECT id, created
    FROM timescale.tokens
    WHERE user_id = uid AND created < NOW()
    ORDER BY created DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

EXPLAIN ANALYZE SELECT
    u.id,
    u.firstname,
    COUNT(*) OVER () AS total_users,
    t.token_id,
    t.token_created
FROM relational.users u
LEFT JOIN LATERAL get_last_token(u.id) t ON true
WHERE u.firstname = 'Mark' limit 100;

EXPLAIN ANALYZE SELECT u.id, u.firstname, t.*, COUNT(*) OVER () AS total_users
FROM relational.users u
LEFT JOIN timescale.tokens t ON t.user_id = u.id
WHERE u.firstname = 'Mark' and t.created < NOW() and t.created > NOW() - INTERVAL '1 hours';



SELECT u.id, u.firstname, u.company_id, COUNT(*) OVER () AS total_users
FROM relational.users u
LEFT JOIN timescale.tokens t ON t.user_id = u.id
WHERE u.company_id = 15 and t.created < NOW() and t.created > NOW() - INTERVAL '10 hours';

SET log_statement_stats = 'off';
SET log_parser_stats = 'on';
SET log_planner_stats = 'on';
SET log_executor_stats = 'on';


explain analyze INSERT INTO timescale.tokens_ht (token, user_id, created)
SELECT token, user_id, created
FROM timescale.tokens;
*/


BEGIN;

DO $$
BEGIN
    INSERT INTO relational.tokens (token, created, user_id)
    SELECT * FROM (VALUES
        ('John Doe', '2020-12-12 20:30:12'::timestamp, 60000),
        ('Jane Smith', '2020-12-12 20:30:12'::timestamp, 55000),
        ('Emily Davis', '2020-12-12 20:30:12'::timestamp, 50000),
        ('Michael Brown', '2020-12-12 20:30:12'::timestamp, 52000),
        ('Linda Johnson', '2020-12-12 20:30:12'::timestamp, 57000),
        ('Robert Wilson', NULL, 62000),
        ('BOBBYYYYY', '2020-12-12 20:30:12'::timestamp, 53000),
        ('James Martinez', '2020-12-12 20:30:12'::timestamp, 54000),
        ('Patricia Hernandez', '2020-12-12 20:30:12'::timestamp, 48000),
        ('William Clark', '2020-12-12 20:30:12'::timestamp, 45000)
    ) AS t(token, created, user_id)
    ON CONFLICT do NOTHING;
END;
$$;

COMMIT;