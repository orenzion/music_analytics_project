# music_analytics_project
A project I do to learn about music, data science, DB design and python

## Main Python libraries used in the project:
* MySQLdb - MySQL python library to handle the interactions with the DB.
* Pandas - For data analytics and manipulation.
* [Spotipy](https://spotipy.readthedocs.io/en/2.13.0/) - Client Python library to handle requests to the Spotify API.
* SKLearn - For machine learning.
* Librosa - To help with feature extraction out of sound.

## Clustering models used in the project:
* KMeans - clustering tracks based on their audio features.
* DBSCAN - clustering tracks based on their audio features.

## Python programs that extract data from Spotify's Api and stores it in the MySQL DB:
* insertPlaylistToDB.py - The program takes a playlist id, extracts the data from Spotify's API and stores the data in tables: playlists, playlists_tracks, audio_features.
* clusterTracksAndInsertToDB.py - cluster all tracks from audio_features tables using sklearn and store the results in kmeans_clustering_params table and in kmeans_clustering_centroids.
* insertArtistAndGenresRoDB.py - the program takes an artist id, extracts its data and inserts it into tables: artists, artist_genres.
* insertArtistsTopTracksByCountryToDB.py - the program looks for the artists their top tracks were not yet extracted and inserted into the db. Then, it taks those artists, extracts their top tracks and inserts them into the tables: artists_top_tracks, audio_features

## Analytics folder:
The [analytics](https://github.com/orenzion/music_analytics_project/tree/master/analytics) folder contains notebooks with analytics performed on the data that was extracted from the Spotify API and stored in the MySQLdb.

### Notebooks:
* [EDA_spotify_audio_features.ipynb](https://github.com/orenzion/music_analytics_project/blob/master/analytics/EDA_spotify_audio_features.ipynb) - 

## DataBase:
* DB used in this project - MySQL
* Tables and schema can be found in DB folder 
* Check out [query_examples.sql](https://github.com/orenzion/music_analytics_project/blob/master/DB/query_examples.sql) to get a better understanting of the DB.

