CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    device_id TEXT UNIQUE NOT NULL,
    status TEXT,
    last_command TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
