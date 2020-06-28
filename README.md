# music_analytics_project
A project I do to learn about music, data science, DB design and python

## DB in the project - MySQL

## Main Python libraries used in the project:
* MySQLdb - MySQL python library to handle the interactions with the DB.
* Pandas - For data analytics and manipulation.
* Spotipy - Client Python library to handle requests to the Spotify API.
* SKLearn - For machine learning.
* Librosa - To help with feature extraction out of sound.

## Clustering models used in the project:
* KMeans
* DBSCAN

## Analytics folder:
The [analytics](https://github.com/orenzion/music_analytics_project/tree/master/analytics) folder contains notebooks with analytics performed on the data that was extracted from the Spotify API and stored in the MySQLdb. 

## Python programs that extract data from Spotify's Api and stores it in the MySQL DB:
* insertPlaylistToDB.py - The program takes a playlist id, extracts the data from Spotify's API and stores the data in tables: playlists, playlists_tracks, audio_features
* clusterTracksAndInsertToDB.py -   
