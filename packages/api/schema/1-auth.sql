CREATE TABLE IF NOT EXISTS authorization_tokens (
  idx BIGSERIAL PRIMARY KEY,
  user_id BIGINT REFERENCES users (id) ON DELETE CASCADE
);
