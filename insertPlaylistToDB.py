import myenvvar
import myDBObject
import spotifyObj
import sys


if __name__ == '__main__':
    '''
    this program takes a spotify playlist uri/id, extracts the data of it and populates the tables in the db  
    '''
    # p_id spotify:track:0IxOHOLbmlO2VdYsI441Kj spotify:playlist:37i9dQZF1E8Ht7BWpkQiTf

    # check if playlist_id was given by user
    if len(sys.argv) == 2:
        # fetch playlist_id
        playlist_id = sys.argv[1]
    else:
        print("playlist_id was not given")
        exit(1)

    # create DB object to handle ALL interactions with database
    db = myDBObject.MyDBObject(myenvvar.db_vars)

    # create a spotify object to Handle ALL requests to the spotify api
    sp = spotifyObj.SpotifyObj()


    db.insert_playlist_to_db(sp.get_playlist(playlist_id))
    db.insert_playlist_tracks_to_db(playlist_id,sp.get_playlist_tracks(playlist_id))
    db.insert_playlist_tracks_audio_features_to_db(sp.get_playlist_tracks(playlist_id),sp.get_playlist_tracks_audio_features(playlist_id))

    


