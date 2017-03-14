#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database cursor."""
    connection = psycopg2.connect("dbname=tournament")
    # connection = psycopg2.connect("dbname={}".format(database_name))
    cursor = connection.cursor()
    return connection, cursor

def deleteMatches():
    """Remove all the match records from the database."""
    connection, cursor = connect()
    query = "DELETE FROM matches;"
    cursor.execute(query)
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection, cursor = connect()
    query = "DELETE FROM players;"
    cursor.execute(query)
    connection.commit()
    connection.close()
    
def countPlayers():
    """Returns the number of players currently registered."""
    connection, cursor = connect()
    query = "SELECT count(id) AS total FROM players;"
    cursor.execute(query)
    num_of_players = cursor.fetchone()
    connection.close()
    if num_of_players:
        return int(num_of_players[0])
    else:
        return 0

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection, cursor = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    param = (name,)
    cursor.execute(query, param)
    connection.commit()
    connection.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection, cursor = connect()
    query = """
        SELECT players.id, players.name, v_win_count.wins, v_match_count.matches
        FROM players 
        LEFT JOIN v_win_count
        ON players.id=v_win_count.id
        RIGHT JOIN v_match_count
        ON players.id=v_match_count.id
        ORDER BY v_win_count.wins DESC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection, cursor = connect()

    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);" 
    params = (winner, loser)
    cursor.execute(query, params)
    connection.commit()
    connection.close()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    player_list = playerStandings()
    player1_id = [tuple[0] for tuple in player_list[::2]]
    player2_id = [tuple[0] for tuple in player_list[1::2]]
    player1_name = [tuple[1] for tuple in player_list[::2]]
    player2_name = [tuple[1] for tuple in player_list[1::2]]
    next_round = zip(player1_id, player1_name, player2_id, player2_name)
    return next_round