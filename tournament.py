#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    delete_cmd = "DELETE FROM matches"
    cursor.execute(delete_cmd)
    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    delete_cmd = "DELETE FROM players"
    cursor.execute(delete_cmd)
    connection.commit()
    connection.close()
    
def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    count_cmd = "SELECT count(id) AS total FROM players"
    cursor.execute(count_cmd)
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
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO players (name) VALUES(%s)" , (name,))
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
    connection = connect()
    cursor = connection.cursor()
    query = """
        SELECT players.id, players.name, v_win_counts.wins, v_match_count.matches
        FROM players 
        LEFT JOIN v_win_counts
        ON players.id=v_win_counts.id
        RIGHT JOIN v_match_count
        ON players.id=v_match_count.id
        ORDER BY v_win_counts.wins DESC;
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
    connection = connect()
    cursor = connection.cursor()

    new_match = "INSERT INTO matches (winner, loser) VALUES (%d, %d)" % (winner, loser)

    cursor.execute(new_match)
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
    next_round = []
    i = 0
    while i < len(player_list):
        id1 = player_list[i][0]
        name1 = player_list[i][1]
        id2 = player_list[i+1][0]
        name2 = player_list[i+1][1]
        i = i + 2
        next_round.append([id1, name1, id2, name2])
    return next_round





