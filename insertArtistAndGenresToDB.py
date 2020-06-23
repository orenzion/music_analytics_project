import myenvvar
import myDBObject
import spotifyObj
import sys


if __name__ == '__main__':
    '''
    this program takes a spotify artist uri/id, extracts the data of it and populates the tables in the db  
    '''

    # check if artist_id was given by user
    if len(sys.argv) == 2:
        # fetch artist_id
        artist_id = sys.argv[1]
    else:
        print("artist_id was not given")
        exit(1)

    # create DB object to handle ALL interactions with database
    db = myDBObject.MyDBObject(myenvvar.db_vars)

    # create a spotify object to Handle ALL requests to the spotify api
    sp = spotifyObj.SpotifyObj()


    db.insert_artist_and_artistgenres_to_db(sp.get_artist(artist_id))

    


