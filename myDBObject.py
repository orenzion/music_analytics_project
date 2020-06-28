import MySQLdb
import pandas as pd
import datetime as dt


class MyDBObject:
    '''
    This object will handle ALL the interactions with the database(connection, querying, monitoring)
    '''

    def __init__(self, param_dict):
        '''
        create a connection and a curser
        '''
        self.datetime_now = dt.datetime.now()
        try:
            self.conn = MySQLdb.Connection(
                host=param_dict['host'],
                user=param_dict['user'],
                passwd=param_dict['password'],
                port=param_dict['port'],
                db=param_dict['db']
                )
            
            if self.conn:
                print("db connected")
                # set encoding
                self.conn.set_character_set('utf8')
        
        except MySQLdb._exceptions.Error as err:
            print("connection error:", err.args[0], err.args[1])
            exit(1) # throw

        try:
            self.cur = self.conn.cursor()
        except MySQLdb._exceptions.Error as err:
            print("create cursor error:", err.args[0], err.args[1])
            exit(1)


    def execute_query(self,query):
        '''
        execute a given query and monitor results
        '''
        try:
            res = self.cur.execute(query)
            self.conn.commit()
        except MySQLdb._exceptions.Error as err:
            print("last query executed:", self.cur._last_executed)
            print("execute query error:", err.args[0], err.args[1])
            exit(1)
        else:
            return res
            
    def fetch_query(self,query):
        '''
        fetch a given query and monitor results
        '''
        try:
            num_rows = self.cur.execute(query)
            self.conn.commit()
        except MySQLdb._exceptions.Error as err:
            print("last query executed:", self.cur._last_executed)
            print("execute query error:", err.args[0], err.args[1])
            exit(1)
        else:
            return num_rows, self.cur.fetchall()
    ###################################################################################
    ########################### CLASS METHODS #########################################
    ###################################################################################

    def insert_playlist_to_db(self,playlist):
        '''
        inserts the given playlist to 'playlists' table in the db
        '''
        q = """INSERT IGNORE INTO playlists VALUES ("%s","%s","%s",%d,%d,%d,"%s","%s",%d)""" \
            %(playlist['id'], playlist['name'], playlist['description'].replace('"',''), int(playlist['collaborative']), playlist['followers']['total'], \
            int(playlist['public']), playlist['owner']['id'], playlist['owner']['display_name'], playlist['tracks']['total'])
        
        inserted_rows = self.execute_query(q)
        print("inserted", inserted_rows, "rows to 'playlists' table")


    def insert_playlist_tracks_to_db(self,playlist_id,playlist_tracks):
        '''
        inserts the given playlist_tracks to 'playlists_tracks' table in the db
        '''
        inserted_rows = 0
        for track in playlist_tracks:
            q = """INSERT IGNORE INTO playlists_tracks VALUES ("%s","%s","%s","%s")""" \
                %(playlist_id, track['track']['id'], track['track']['name'],track['added_at'])

            inserted_rows += self.execute_query(q)
        
        print("inserted", inserted_rows, "rows to 'playlist_tracks' table")


    def insert_playlist_tracks_audio_features_to_db(self,playlist_tracks,playlist_tracks_audio_features):
        '''
        inserts the given playlist_tracks_audio_features to 'audio_features' table in the db
        '''
        inserted_rows = 0
        for i in range(len(playlist_tracks_audio_features)):
            feature = playlist_tracks_audio_features[i]
            track = playlist_tracks[i]
            q = """INSERT IGNORE INTO audio_features VALUES ('%s',%f,%f,%d,%f,%d,%f,%f,%f,%f,%f,%f,%d,%d,%d,%d,"%s")""" \
                %(feature['id'],feature['danceability'],feature['energy'],feature['key'],feature['loudness'], \
                feature['mode'], feature['speechiness'], feature['acousticness'],feature['instrumentalness'], \
                feature['liveness'],feature['valence'],feature['tempo'],feature['duration_ms'],feature['time_signature'], \
                len(track['track']['available_markets']),track['track']['popularity'],self.datetime_now)

            inserted_rows += self.execute_query(q)

        print("inserted", inserted_rows, "rows to 'audio_features' table")


    def read_sql_to_df(self,q):
        '''
        reads sql from db into pandas df and returns it
        '''
        df = pd.read_sql(q, self.conn)
        return df


    def insert_kmeans_params_and_centroids_to_db(self, clustering_datetime, random_state, k, interia_score, clustering_centroids):
        '''
        insert kmeans model params and centroids to db
        '''
        self.insert_kmeans_params_to_db(clustering_datetime, random_state, k, interia_score)
        self.insert_kmeans_centroids_to_db(clustering_datetime,k,clustering_centroids)

    def insert_kmeans_params_to_db(self, clustering_datetime, random_state, k, interia_score):
        '''
        insert kmeans model params to db
        '''
        q = """INSERT IGNORE INTO kmeans_clustering_params VALUES ("%s",%d,%d,%f)""" \
            %(clustering_datetime,random_state,k,interia_score)
        
        inserted_rows = self.execute_query(q)
        print("inserted", inserted_rows, "rows to 'kmeans_clustering_params' table")

    def insert_kmeans_centroids_to_db(self,clustering_datetime, k, clustering_centroids):
        '''
        insert kmeans model centroids to db
        '''
        inserted_rows = 0
        for i in range(k):
            cluster_centroid = clustering_centroids[i]
            q = """INSERT IGNORE INTO kmeans_clustering_centroids VALUES ("%s",%d,%f,%f,%f,%f,%f,%f,%f,%f,%f)""" \
                %(clustering_datetime,i,cluster_centroid[0],cluster_centroid[1],cluster_centroid[2],cluster_centroid[3],\
                    cluster_centroid[4],cluster_centroid[5],cluster_centroid[6],cluster_centroid[7],cluster_centroid[8])

            inserted_rows += self.execute_query(q)

        print("inserted", inserted_rows, "rows to 'kmeans_clustering_centroids' table")

    
    def insert_artist_and_artistgenres_to_db(self,artist):
        # insert to artists
        q = """INSERT IGNORE INTO artists VALUES ("%s","%s",%d,%d,"%s")""" \
            %(artist['id'],artist['name'],artist['followers']['total'],artist['popularity'],self.datetime_now)
        inserted_rows = self.execute_query(q)
        print("inserted", inserted_rows, "rows to 'artists' table")

        # insert to artist_genres
        inserted_rows = 0
        for genre in artist['genres']:
            q = """INSERT IGNORE INTO artist_genres VALUES ("%s","%s")""" \
                %(artist['id'],genre)
            inserted_rows += self.execute_query(q)
        print("inserted", inserted_rows, "rows to 'artist_genres' table")


    

    def fetch_artists_ids_without_top_tracks_by_country(self,country = 'US'):
        '''
        get a list of ids of the artists from the db that their top tracks by the given country were not extracted yet
        '''
        q = '''select a.artist_id
                from artists a 
                where a.artist_id not in (select att.artist_id
                from artists_top_tracks att
                where att.country = "%s")''' %country

        num_rows_fetched, res = self.fetch_query(q)
        
        print("fetched:",num_rows_fetched, "artists ids")

        return [item[0] for item in res]


    def insert_artists_top_tracks_and_audio_features_to_db(self,artists_ids , artists_top_tracks, artists_tracks_audio_features, country = 'US'):
        '''
        get a list of artists_top_tracks and a list of artists_tracks_audio_features and a country and insert to DB
        '''
        inserted_rows_artists_top_tracks = 0
        inserted_rows_artists_top_tracks_audio_features = 0

        for i in range(len(artists_ids)):
            artist_id = artists_ids[i]
            artist_top_tracks = artists_top_tracks[i]
            artist_tracks_audio_features = artists_tracks_audio_features[i]

            for j in range(len(artist_top_tracks['tracks'])):
                artist_top_track = artist_top_tracks['tracks'][j]
                q = """INSERT IGNORE INTO artists_top_tracks VALUES ("%s","%s","%s","%s")""" \
                    %(artist_id ,artist_top_track['id'], country, artist_top_track['name'])
                inserted_rows_artists_top_tracks += self.execute_query(q)

                track_audio_features = artist_tracks_audio_features[j]
                q = """INSERT IGNORE INTO audio_features VALUES ('%s',%f,%f,%d,%f,%d,%f,%f,%f,%f,%f,%f,%d,%d,%d,%d,"%s")""" \
                    %(track_audio_features['id'],track_audio_features['danceability'],track_audio_features['energy'],track_audio_features['key'],track_audio_features['loudness'], \
                    track_audio_features['mode'], track_audio_features['speechiness'], track_audio_features['acousticness'],track_audio_features['instrumentalness'], \
                    track_audio_features['liveness'],track_audio_features['valence'],track_audio_features['tempo'],track_audio_features['duration_ms'],track_audio_features['time_signature'], \
                    -1,artist_top_track['popularity'],self.datetime_now)
                inserted_rows_artists_top_tracks_audio_features += self.execute_query(q)

        print("inserted", inserted_rows_artists_top_tracks, "rows to 'artists_top_tracks' table")
        print("inserted", inserted_rows_artists_top_tracks_audio_features, "rows to 'audio_features' table")

        







    
        
        

