import sqlite3

CONST_DB_FILE = "data.db"


def get_connection():
    """Return the connection to the given database file"""
    conn = None
    try:
        conn = sqlite3.connect(CONST_DB_FILE)
    except Error as e:
        print(e)

    return conn


def get_user_id(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM user WHERE user_name = ?", (username,))
    user_id = cursor.fetchone()
    cursor.close()
    return user_id[0]


def insert_artists(conn, artists):
    """map the artists array and prepare a new one with a null value of the AI primary key"""
    cursor = conn.cursor()

    prepared_artists = []
    for i in artists:
        prepared_artists.append((None, i))

    cursor.executemany("INSERT OR IGNORE INTO artist VALUES (?,?)", prepared_artists)
    conn.commit()
    cursor.close()


def get_artist_id_by_name(conn, artists):
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


def assign_artist_to_user(conn, artists, user, timerange_string):
    """Delete the users artists in the given time range and assign the new ones"""
    cursor = conn.cursor()
    user_id = get_user_id(conn, user)
    timerange_int = switch_timerange(timerange_string)
    cursor.execute("DELETE FROM user_has_artist WHERE timerange = ? AND user_id = ?", (timerange_int, user_id,))
    conn.commit()

    artist_id_array = get_artist_id_by_name(conn, artists)
    # map the artist id array and push it to the insert data array
    prepared_data = []
    for id in artist_id_array:
        prepared_data.append((None, timerange_int, id[0], user_id))

    cursor.executemany("INSERT INTO user_has_artist VALUES (?, ?, ?, ?)", prepared_data)
    conn.commit()
    cursor.close()


def switch_timerange(timerange_string):
    """return the defined int number for the given timerange_string"""
    switcher = {
        "long_term": 1,
        "short_term": 2,
        "mid_term": 3
    }
    return switcher.get(timerange_string)
