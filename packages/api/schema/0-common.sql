CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY,
  bot BOOL NOT NULL DEFAULT FALSE,

  name TEXT NOT NULL,
  discriminator TEXT NOT NULL,

  avatar TEXT
);

CREATE TABLE IF NOT EXISTS guilds (
  id BIGINT PRIMARY KEY,

  name TEXT NOT NULL,
  icon TEXT,

  removed_at TIMESTAMP  -- Used to delete data after an inactivity timeout
);

CREATE TABLE IF NOT EXISTS roles (
  id BIGINT PRIMARY KEY,
  guild_id BIGINT NOT NULL REFERENCES guilds (id) ON DELETE CASCADE,

  name TEXT NOT NULL,

  position INT NOT NULL,
  permissions BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS channels (
  id BIGINT PRIMARY KEY,
  guild_id BIGINT NOT NULL REFERENCES guilds (id) ON DELETE CASCADE,

  name TEXT NOT NULL,
  type INT NOT NULL
);
