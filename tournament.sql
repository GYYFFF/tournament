/* Table definitions for the tournament project.
Create a tournament database including two tables
table players and table matches;
Table Players assign unique key id to each players and also includes player names;
Table Matches contains all matches info, assign each match a unique id and each match 
has a winner and a loser, stores winner's id and loser's id in matches table
*/

-- Drop previous database tournament if it already exist. 
DROP DATABASE tournament;
-- Create a tournament database
CREATE DATABASE tournament;
-- connect to tournament databse
\c tournament;

-- create a players table in tournament database
CREATE TABLE players(
        id serial PRIMARY KEY, 
        name text
        );

-- create a mathes table in tournament database
CREATE TABLE matches(
        id serial PRIMARY KEY,
        winner serial REFERENCES players(id),
        loser serial REFERENCES players(id));

/*
Create a view to store total wins for all players
*/
CREATE VIEW v_win_count AS
    SELECT players.id, players.name, count(matches.winner) 
    AS wins
    FROM players
    LEFT JOIN matches
    ON players.id = matches.winner
    GROUP BY players.id;

/*
Create a view to store total matches for all players
*/
CREATE VIEW v_match_count AS
    SELECT players.id, players.name, count(matches.*) 
    AS matches
    FROM players 
    LEFT JOIN matches 
    ON players.id = matches.winner OR players.id = matches.loser
    GROUP BY players.id;

