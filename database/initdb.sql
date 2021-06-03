CREATE TABLE IF NOT EXISTS players(
    player_uid UUID PRIMARY KEY,
    player_name VARCHAR(15) NOT NULL,
    country VARCHAR,
    salt CHAR(16) NOT NULL,
    pass_hash VARCHAR NOT NULL,
    UNIQUE(player_name)
);

CREATE TABLE IF NOT EXISTS sentences(
    sentence_uid UUID PRIMARY KEY,
    sentence VARCHAR NOT NULL,
    UNIQUE(sentence)
);

CREATE TABLE IF NOT EXISTS scores(
player_uid UUID REFERENCES players(player_uid) ON DELETE CASCADE,
sentence_uid UUID REFERENCES sentences(sentence_uid) ON DELETE CASCADE,
score NUMERIC(6,2) NOT NULL CHECK(score > 0),
PRIMARY KEY(player_uid, sentence_uid)
);