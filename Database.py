import sqlite3

CREATE_SONG_TABLE = "CREATE TABLE IF NOT EXISTS songs (id INTEGER PRIMARY KEY, name TEXT, path TEXT);"

INSERT_SONG = "INSERT INTO songs (name, path) VALUES (?, ?);"

GET_ALL_SONGS = "SELECT * FROM songs;"

GET_SONGS_BY_NAME = "SELECT path FROM songs WHERE name = ?;"

DELETE_SONG = "DELETE FROM songs WHERE name = ?;"


def connect():
    return sqlite3.connect("music.db")


def create_table(connection):
    with connection:
        connection.execute(CREATE_SONG_TABLE)


def add_song(connection, name, path):
    with connection:
        connection.execute(INSERT_SONG, (name, path))


def delete_song(connection, name):
    with connection:
        connection.execute(DELETE_SONG, (name,))


def get_all_songs(connection):
    with connection:
        return connection.execute(GET_ALL_SONGS).fetchall()


def get_songs_by_name(connection, name):
    with connection:
        return connection.execute(GET_SONGS_BY_NAME, (name,)).fetchone()