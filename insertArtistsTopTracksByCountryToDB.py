import myenvvar
import myDBObject
import spotifyObj
import sys


if __name__ == '__main__':
    '''
    this program takes a country (like 'US', 'IL'), looks for the artists that their top tracks were not inserted and
    inserts their top tracks and audio features to the db. 
    '''

    # check if artist_id was given by user
    if len(sys.argv) == 2:
        # fetch artist_id
        county = sys.argv[1]
    else:
        print("country was not given")
        exit(1)

    # create DB object to handle ALL interactions with database
    db = myDBObject.MyDBObject(myenvvar.db_vars)

    # create a spotify object to Handle ALL requests to the spotify api
    sp = spotifyObj.SpotifyObj()


    artists_ids = db.fetch_artists_ids_without_top_tracks_by_country(county)

    for id in artists_ids:
        print(id)

    


