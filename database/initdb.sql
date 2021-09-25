CREATE TABLE IF NOT EXISTS players(
    player_uid UUID PRIMARY KEY,
    player_name VARCHAR(15) NOT NULL,
    country VARCHAR,
    salt CHAR(16) NOT NULL,
    pass_hash VARCHAR NOT NULL,
    UNIQUE(player_name)
);

CREATE TABLE IF NOT EXISTS quotes(
    quote_uid UUID PRIMARY KEY,
    quote VARCHAR NOT NULL,
    UNIQUE(quote)
);

CREATE TABLE IF NOT EXISTS scores(
    player_uid UUID REFERENCES players(player_uid) ON DELETE CASCADE,
    quote_uid UUID REFERENCES quotes(quote_uid) ON DELETE CASCADE,
    score NUMERIC(6,2) NOT NULL CHECK(score > 0),
    PRIMARY KEY(player_uid, quote_uid)
);

CREATE TABLE IF NOT EXISTS sessions(
    player_uid UUID REFERENCES players(player_uid) ON DELETE CASCADE PRIMARY KEY,
    session_hash CHAR(128) NOT NULL,
    login_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(session_hash)
);
