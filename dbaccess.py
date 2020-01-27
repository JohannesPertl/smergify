import sqlite3

CONST_DB_FILE = "data.db"


########## helper functions ##########

def get_connection():
    """Return the connection to the given database file"""
    conn = None
    try:
        conn = sqlite3.connect(CONST_DB_FILE)
    except Error as e:
        print(e)

    return conn


def switch_timerange(timerange_string):
    """return the defined int number for the given timerange_string"""
    switcher = {
        "long_term": 1,
        "short_term": 2,
        "mid_term": 3
    }
    return switcher.get(timerange_string)


########## user functions ##########

def get_user_id_by_name(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM user WHERE user_name = ?", (username,))
    user_id = cursor.fetchone()
    cursor.close()
    return user_id[0]


def insert_user(conn, user_name, first_login):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user ('user_id', 'user_name', 'first_login') VALUES (?, ?, ?)", (None, user_name, first_login,))
    conn.commit()
    cursor.close()


########## artist and user_has_artist functions ##########

def insert_artists(conn, artists):
    """map the artists array and prepare a new one with a null value of the AI primary key"""
    cursor = conn.cursor()

    prepared_artists = []
    for artist in artists:
        prepared_artists.append((None, artist))

    cursor.executemany("INSERT OR IGNORE INTO artist ('artist_id', 'artist_name') VALUES (?,?)", prepared_artists)
    conn.commit()
    cursor.close()


def get_artist_id_by_name_array(conn, artists):
    """return the ids to the given artist names"""
    cursor = conn.cursor()
    # prepare the sql statement, that every object in the array
    # has one placeholder in the "in function"
    sql = "SELECT artist_id FROM artist WHERE artist_name in({seq})".format(
        seq=','.join(['?'] * len(artists)))

    cursor.execute(sql, artists)
    ids = cursor.fetchall()
    cursor.close()
    return ids


def get_artist_id_by_name(conn, artist):
    cursor = conn.cursor()
    cursor.execute("SELECT artist_id FROM artist WHERE artist_name = ?", (artist,))
    artist_id = cursor.fetchone()
    cursor.close()
    return artist_id[0]


def assign_artist_to_user(conn, artists, user, timerange_string):
    """Delete the users artists in the given time range and assign the new ones"""
    cursor = conn.cursor()
    user_id = get_user_id_by_name(conn, user)
    timerange_int = switch_timerange(timerange_string)
    cursor.execute("DELETE FROM user_has_artist WHERE timerange = ? AND user_id = ?", (timerange_int, user_id,))
    conn.commit()

    artist_id_array = get_artist_id_by_name_array(conn, artists)
    # map the artist id array and push it to the insert data array
    prepared_data = []
    for id in artist_id_array:
        prepared_data.append((None, timerange_int, id[0], user_id))

    cursor.executemany("INSERT INTO user_has_artist ('id', 'timerange', 'artist_id', 'user_id') VALUES (?, ?, ?, ?)", prepared_data)
    conn.commit()
    cursor.close()


########## group and group has user functions ##########

def get_group_id_by_name(conn, group_name):
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM user_group WHERE group_name = ?", (group_name,))
    group_id = cursor.fetchone()
    cursor.close()
    return group_id[0]


def insert_group(conn, group_name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_group ('group_id', 'group_name') VALUES (?, ?)", (None, group_name,))
    conn.commit()
    cursor.close()


def assign_user_to_group(conn, group_name, user_name):
    cursor = conn.cursor()
    user_id = get_user_id_by_name(conn, user_name)
    group_id = get_group_id_by_name(conn, group_name)
    cursor.execute("INSERT INTO group_has_user ('group_id', 'user_id') VALUES (?, ?)", (group_id, user_id,))
    conn.commit()
    cursor.close()


########## song functions ##########

def insert_songs(conn, artist_name, songs):
    cursor = conn.cursor()

    artist_id = get_artist_id_by_name(conn, artist_name)
    prepared_songs = []
    for song in songs:
        prepared_songs.append((None, song, artist_id))

    cursor.executemany("INSERT INTO song ('song_id', 'song_title', 'artist_id') VALUES (?, ?, ?)", prepared_songs)
    conn.commit()
    cursor.close()



########## !! just for testing !! ##########
artists = ["Camo & Krooked", "Billy Talent", "Muse", "Odesza", "Korn", "Foo Fighters", "Delta Heavy", "Mac Miller",
           "Genetikk", "Jack Garrat"]
songs = ['Set It Off', 'Watch It Burn', 'Atlas VIP', 'Loa', 'Kallisto', 'Sidewinder', 'Good Times Bad Times - Document One Remix', 'Atlas', 'Broken Pieces (feat. Nihils) - Culture Shock Remix', 'Good Times Bad Times']
# insert_artists(get_connection(), artists)
# assign_artist_to_user(get_connection(), artists, "manu", "long_term")
# insert_group(get_connection(), "bestGroup")
# assign_user_to_group(get_connection(), "testgruppe", "manu")
# insert_songs(get_connection(), "Camo & Krooked", songs)
insert_user(get_connection(), "Julia", "0000")
