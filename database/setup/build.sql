CREATE TABLE IF NOT EXISTS warns (
    user_id int,
    guild_id,
    reason TEXT,
    warned_at NOT NULL DEFAULT CURRENT_TIMESTAMP
);


