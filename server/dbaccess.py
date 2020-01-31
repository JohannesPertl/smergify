import sqlite3
import logging
import sys


CONST_DB_FILE = "data.db"


########## helper functions ##########

def get_connection():
    """Return the connection to the given database file"""
    conn = None
    try:
        conn = sqlite3.connect(CONST_DB_FILE)
    except BaseException as e:
        logging.error("AT dbaccess.get_connection %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    return conn


def switch_timerange(timerange_string):
    """return the defined int number for the given timerange_string"""
    switcher = {
        "long_term": 1,
        "short_term": 2,
        "mid_term": 3
    }
    return switcher.get(timerange_string)


def objects_to_list(object_list):
    """create an attribute list of the given objects"""
    object_attribute_list = []
    for object in object_list:
        object_attribute_list.append(object.to_tuple())

    return object_attribute_list


########## user functions ##########

def get_user_id_by_name(conn, user):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id FROM user WHERE user_name = ?", (user.user_name,))
        user_id = cursor.fetchone()
    except BaseException as e:
        logging.error("AT dbaccess.get_user_id_by_name: %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    cursor.close()
    return user_id[0]


def insert_users(conn, users):
    cursor = conn.cursor()
    users_list = objects_to_list(users)
    try:
        cursor.executemany("INSERT OR IGNORE INTO user ('user_id', 'user_name' ) VALUES (?, ?)", users_list)
        conn.commit()
    except BaseException as e:
        logging.error("AT insert_user: %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    cursor.close()


########## artist and user_has_artist functions ##########

def insert_artists(conn, artists):
    """map the artists array and prepare a new one with a null value of the AI primary key"""
    cursor = conn.cursor()
    artist_list = objects_to_list(artists)
    try:
        cursor.executemany("INSERT OR IGNORE INTO artist ('artist_id', 'artist_name') VALUES (?,?)", artist_list)
        conn.commit()
    except BaseException as e:
        logging.error("AT insert_artist: %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    # print(artist_list)
    cursor.close()


# def get_artist_ids_by_name(conn, artists):
#     """return the ids to the given artists"""
#     cursor = conn.cursor()
#     # prepare the sql statement, that every object in the array
#     # has one placeholder in the "in function"
#     sql = "SELECT artist_id FROM artist WHERE artist_name in({seq})".format(
#         seq=','.join(['?'] * len(artists)))
#
#     try:
#         cursor.execute(sql, artists)
#         ids = cursor.fetchall()
#     except BaseException as e:
#         logging.error("AT dbaccess.get_artist_id_by_name_array %s", e)
#         print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")
#     cursor.close()
#     return ids


def get_artist_id_by_name(conn, artist):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT artist_id FROM artist WHERE artist_name = ?", (artist.artist_name,))
        artist_id = cursor.fetchone()
    except BaseException as e:
        logging.error("AT dbaccess.get_artist_id_by_name %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    cursor.close()
    return artist_id[0]


def get_timeranges_of_user_artists(user):
    timeranges_multiple = []
    for artist in user.artists:
        timeranges_multiple.append(artist.time_range)

    #filter the multiple time ranges
    return list(set(timeranges_multiple))


def delete_artists_by_timeranges(conn, user):
    """delete all the current artists which have the same time ranges as the artists in the user.artists list"""
    cursor = conn.cursor()
    timeranges = get_timeranges_of_user_artists(user)
    for timerange in timeranges:
        try:
            cursor.execute("DELETE FROM user_has_artist WHERE timerange = ? AND user_id = ?", (timerange, user.user_id,))
            conn.commit()
        except BaseException as e:
            logging.error("AT dbaccess.delete_artists_by_timeranges %s", e)
            print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    cursor.close()


def assign_artists_to_users(conn, users):
    """Delete the users artists in the given time range and assign the new ones"""
    cursor = conn.cursor()

    for user in users:
        delete_artists_by_timeranges(conn, user)
        # map the artist array and create a new array with just the ids
        prepared_data = []
        for artist in user.artists:
            prepared_data.append((artist.time_range, artist.artist_id, user.user_id))

        try:
            cursor.executemany("INSERT OR IGNORE INTO user_has_artist ('timerange', 'artist_id', 'user_id') VALUES (?, ?, ?)", prepared_data)
            conn.commit()
        except BaseException as e:
            logging.error("AT dbaccess.assign_artists_to_users %s", e)
            print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    cursor.close()


########## group and group has user functions ##########

def get_group_id_by_name(conn, group):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT group_id FROM user_group WHERE group_name = ?", (group.group_name,))
        group_id = cursor.fetchone()
    except BaseException as e:
        logging.error("AT dbaccess.get_group_id_by_name %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    cursor.close()
    return group_id[0]


def insert_groups(conn, groups):
    cursor = conn.cursor()
    groups_list = objects_to_list(groups)
    # print(groups_list)
    try:
        cursor.executemany("INSERT OR IGNORE INTO user_group ('group_id', 'group_name') VALUES (?, ?)", groups_list)
        conn.commit()
    except BaseException as e:
        logging.error("AT dbaccess.insert_groups %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")
    cursor.close()


def assign_users_to_group(conn, users):
    cursor = conn.cursor()
    prepared_data = []
    for user in users:
        prepared_data.append((get_group_id_by_name(conn, user.user_group), user.user_id))
    try:
        cursor.executemany("INSERT OR IGNORE INTO group_has_user ('group_id', 'user_id') VALUES (?, ?)", prepared_data)
        conn.commit()
    except BaseException as e:
        logging.error("AT dbaccess.assign_user_to_group %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    cursor.close()


########## song functions ##########

def insert_songs(conn, songs):
    cursor = conn.cursor()

    prepared_data = objects_to_list(songs)

    try:
        cursor.executemany("INSERT INTO song ('song_id', 'song_title', 'artist_id') VALUES (?, ?, ?)", prepared_data)
        conn.commit()
    except BaseException as e:
        logging.error("AT dbaccess.insert_songs %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")
    cursor.close()


def get_matched_songs_for_group(conn, group, timerange):
    cursor = conn.cursor()
    # get the members of the group
    try:
        cursor.execute("SELECT user_id "
                       "FROM user_group AS g JOIN group_has_user AS ghu ON g.group_id = ghu.group_id "
                       "WHERE g.group_name = ?", (group.group_name,))
        users = cursor.fetchall()
    except BaseException as e:
        logging.error("AT dbaccess.get_songs_for_group %s", e)
        print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    # get the songs
    matched_songs = []
    if len(users) == 2:
        try:
            cursor.execute("SELECT song.song_id, song.song_title "
                           "FROM song WHERE song.artist_id IN "
                           "( SELECT uha1.artist_id "
                           "FROM user_has_artist as uha1 JOIN user_has_artist as uha2 ON uha1.artist_id = uha2.artist_id "
                           "WHERE (uha1.user_id = ? AND uha2.user_id = ?) "
                           "AND uha1.timerange = ?)", (users[0][0], users[1][0], timerange))
            matched_songs = cursor.fetchall()
        except BaseException as e:
            logging.error("AT dbaccess.get_songs_for_group %s", e)
            print("Ein Fehler ist aufgetreten - ueberpruefen Sie das Log-File")

    cursor.close()
    return matched_songs