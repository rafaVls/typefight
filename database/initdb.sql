CREATE TABLE IF NOT EXISTS highscores(
    highscore_uid UUID PRIMARY KEY,
    score NUMERIC(6, 2) NOT NULL CHECK (score > 0)
);

CREATE TABLE IF NOT EXISTS players(
    player_uid UUID PRIMARY KEY,
    player_name CHAR(3) UNIQUE NOT NULL,
    highscore_uid UUID REFERENCES highscores(highscore_uid) ON DELETE CASCADE NOT NULL,
    CONSTRAINT FK_Highscores UNIQUE (highscore_uid)
);
