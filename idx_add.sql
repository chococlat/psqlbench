/*
SELECT create_hypertable('sensor_data', 'time', 'sensor_id', 4);

*/

CREATE INDEX idx_users_firstname ON relational.users (firstname);
CREATE INDEX idx_users_lastname ON relational.users (lastname);

SELECT create_hypertable('timescale.tokens', 'created');

CREATE INDEX idx_tokens_user_id ON timescale.tokens (user_id);

