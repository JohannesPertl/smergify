import logging
import sqlite3


class DB:
    def __init__(self, file_location):
        self.file_location = file_location
        self.conn = self.get_connection()

    ########## helper functions ##########

    def get_connection(self):
        """Return the connection to the given database file"""
        conn = None
        try:
            conn = sqlite3.connect(self.file_location)
        except Exception as e:
            logging.error("AT dbaccess.get_connection %s", e)
        return conn

    def switch_timerange(self, timerange_string):
        """return the defined int number for the given timerange_string"""
        switcher = {
            "long_term": 1,
            "short_term": 2,
            "mid_term": 3
        }
        return switcher.get(timerange_string)

    def objects_to_list(self, object_list):
        """create an attribute list of the given objects"""
        object_attribute_list = []
        for object in object_list:
            object_attribute_list.append(object.to_tuple())

        return object_attribute_list

    def extract(self, lst):
        """return every first element of a more dimensional list"""
        return [item[0] for item in lst]

    ########## user functions ##########

    def get_user_id_by_name(self, user):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT user_id FROM user WHERE user_name = ?", (user.user_name,))
            user_id = cursor.fetchone()
        except BaseException as e:
            logging.error("AT dbaccess.get_user_id_by_name: %s", e)

        cursor.close()
        return user_id[0]

    def insert_users(self, users):
        """insert a list of users - given by a object list"""
        cursor = self.conn.cursor()
        users_list = self.objects_to_list(users)
        try:
            cursor.executemany("INSERT OR IGNORE INTO user ('user_id', 'user_name' ) VALUES (?, ?)", users_list)
            self.conn.commit()
        except BaseException as e:
            logging.error("AT insert_users: %s", e)
        cursor.close()
        self.assign_users_to_group(users)
        self.assign_artists_to_users(users)

    ########## artist and user_has_artist functions ##########

    def insert_artists(self, artists):
        """map the artists array and prepare a new one with a null value of the AI primary key"""
        cursor = self.conn.cursor()
        artist_list = self.objects_to_list(artists)
        try:
            cursor.executemany("INSERT OR IGNORE INTO artist ('artist_id', 'artist_name') VALUES (?,?)", artist_list)
            self.conn.commit()
        except BaseException as e:
            logging.error("AT insert_artists: %s", e)

        cursor.close()

    def get_artist_ids_by_name(self, artists):
        """return the ids to the given artists"""
        cursor = self.conn.cursor()
        # prepare the sql statement, that every object in the array
        # has one placeholder in the "in function"
        sql = "SELECT artist_id FROM artist WHERE artist_name in({seq})".format(
            seq=','.join(['?'] * len(artists)))

        try:
            cursor.execute(sql, artists)
        except BaseException as e:
            logging.error("AT dbaccess.get_artist_id_by_name_array %s", e)

        ids = cursor.fetchall()
        cursor.close()
        return ids

    def get_artist_id_by_name(self, artist):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT artist_id FROM artist WHERE artist_name = ?", (artist.artist_name,))
            artist_id = cursor.fetchone()
        except BaseException as e:
            logging.error("AT dbaccess.get_artist_id_by_name %s", e)

        cursor.close()
        return artist_id[0]

    def get_timeranges_of_user_artists(self, user):
        """get every artist id of the given user object"""
        timeranges_multiple = []
        for artist in user.artists:
            timeranges_multiple.append(artist.time_range)

        # remove the duplicate entries of the time range ids
        return list(set(timeranges_multiple))

    def delete_artists_by_timeranges(self, user):
        """delete all the current artists which have the same time ranges as the artists in the user.artists list"""
        cursor = self.conn.cursor()
        time_ranges = self.get_timeranges_of_user_artists(user)
        for time_range in time_ranges:
            try:
                cursor.execute("DELETE FROM user_has_artist WHERE timerange = ? AND user_id = ?",
                               (time_range, user.user_id,))
                self.conn.commit()
            except BaseException as e:
                logging.error("AT dbaccess.delete_artists_by_timeranges %s", e)

        cursor.close()

    def assign_artists_to_users(self, users):
        """Delete the users artists in the given time range and assign the new ones"""
        cursor = self.conn.cursor()

        for user in users:
            self.delete_artists_by_timeranges(user)
            # map the artist array and create a new array with just the ids
            prepared_data = []
            for artist in user.artists:
                prepared_data.append((artist.time_range, artist.artist_id, user.user_id))

            try:
                cursor.executemany(
                    "INSERT OR IGNORE INTO user_has_artist ('timerange', 'artist_id', 'user_id') VALUES (?, ?, ?)",
                    prepared_data)
                self.conn.commit()
            except BaseException as e:
                logging.error("AT dbaccess.assign_artists_to_users %s", e)

        cursor.close()

    ########## group and group has user functions ##########

    def get_group_id_by_name(self, group):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT group_id FROM user_group WHERE group_name = ?", (group.group_name,))
            group_id = cursor.fetchone()
        except BaseException as e:
            logging.error("AT dbaccess.get_group_id_by_name %s", e)

        cursor.close()
        return group_id[0]

    def insert_groups(self, groups):
        cursor = self.conn.cursor()
        groups_list = self.objects_to_list(groups)
        try:
            cursor.executemany("INSERT OR IGNORE INTO user_group ('group_id', 'group_name') VALUES (?, ?)", groups_list)
            self.conn.commit()
        except BaseException as e:
            logging.error("AT dbaccess.insert_groups %s", e)

        cursor.close()

    def assign_users_to_group(self, users):
        """assign the user to the group - attribute given in the user object"""
        cursor = self.conn.cursor()
        prepared_data = []
        for user in users:
            prepared_data.append((self.get_group_id_by_name(user.user_group), user.user_id))
        try:
            cursor.executemany("INSERT OR IGNORE INTO group_has_user ('group_id', 'user_id') VALUES (?, ?)",
                               prepared_data)
            self.conn.commit()
        except BaseException as e:
            logging.error("AT dbaccess.assign_users_to_group %s", e)

        cursor.close()

    ########## song functions ##########

    def insert_songs(self, songs):
        cursor = self.conn.cursor()

        prepared_data = self.objects_to_list(songs)

        try:
            cursor.executemany("INSERT OR IGNORE INTO  song ('song_id', 'song_title', 'artist_id') VALUES (?, ?, ?)",
                               prepared_data)
            self.conn.commit()
        except BaseException as e:
            logging.error("AT dbaccess.insert_songs %s", e)

        cursor.close()

    def get_matched_song_ids_for_two_users(self, group):
        """get all artists which are in both libraries of the users
        and fetch the songs from these artist - only works with two users"""
        cursor = self.conn.cursor()
        # get the members of the group
        try:
            cursor.execute("SELECT user_id "
                           "FROM user_group AS g JOIN group_has_user AS ghu ON g.group_id = ghu.group_id "
                           "WHERE g.group_name = ?", (group.group_name,))
        except BaseException as e:
            logging.error("AT dbaccess.get_matched_songs_for_two_users %s", e)

        users = cursor.fetchall()
        # get the songs
        matched_songs = []
        if len(users) == 2:
            try:
                cursor.execute("SELECT song.song_id, song.song_title "
                               "FROM song WHERE song.artist_id IN "
                               "( SELECT uha1.artist_id "
                               "FROM user_has_artist as uha1 JOIN user_has_artist as uha2 ON uha1.artist_id = uha2.artist_id "
                               "WHERE (uha1.user_id = ? AND uha2.user_id = ?))", (users[0][0], users[1][0]))
                matched_songs = cursor.fetchall()
            except BaseException as e:
                logging.error("AT dbaccess.get_matched_songs_for_two_users %s", e)

        cursor.close()
        return self.extract(matched_songs)

    def get_matched_song_ids_for_group(self, group):
        """get all artists from the users in the list - and their songs"""
        cursor = self.conn.cursor()
        user_list = []
        for user in group.users:
            user_list.append(user.user_id)

        try:
            sql_artist_ids = ("SELECT artist.artist_id FROM user_has_artist "
                              "JOIN artist on user_has_artist.artist_id = artist.artist_id "
                              "WHERE user_has_artist.user_id in ({seq}) GROUP BY artist.artist_name".format(
                seq=','.join(['?'] * len(user_list))))

            cursor.execute(sql_artist_ids, user_list)
            artists = cursor.fetchall()
        except BaseException as e:
            logging.error("AT dbaccess.get_matched_songs_for_group %s", e)

        artist_ids = self.extract(artists)

        try:
            sql_song_ids = ("SELECT song.song_id FROM song "
                            "WHERE song.artist_id in ({seq})".format(
                seq=','.join(['?'] * len(artist_ids))))

            cursor.execute(sql_song_ids, artist_ids)
        except BaseException as e:
            logging.error("AT dbaccess.get_matched_songs_for_group %s", e)

        songs = cursor.fetchall()
        return self.extract(songs)
