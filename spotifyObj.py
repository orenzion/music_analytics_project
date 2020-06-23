from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import myenvvar
import os

class SpotifyObj:
    '''
    this class will handle the interactions with spotify's api and the data extraction process
    '''

    def __init__(self):

        # set env van
        myenvvar.setVar()

        # get env var
        client_id = os.environ.get('s_client_id')
        client_secret = os.environ.get('s_client_secret')

        # init spotify client
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    def get_playlist(self,playlist_id):
        playlist = self.sp.playlist(playlist_id)
        return playlist


    def get_playlist_tracks(self,playlist_id):
        playlist = self.sp.playlist(playlist_id)
        playlist_tracks = playlist['tracks']['items']
        return playlist_tracks


    def get_playlist_tracks_audio_features(self,playlist_id):
        playlist = self.sp.playlist(playlist_id)
        playlist_tracks = playlist['tracks']['items']

        tids = []
        for t in playlist_tracks:
            tids.append(t['track']['id'])

        # extract audio features from tracks
        playlist_tracks_audio_features = self.sp.audio_features(tids)
        return playlist_tracks_audio_features

    
    def get_artist(self, artist_id):
        artist = self.sp.artist(artist_id)
        return artist


