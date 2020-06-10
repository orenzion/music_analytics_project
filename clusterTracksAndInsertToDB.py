import myenvvar
import myDBObject
import kmeansObj
import pandas as pd


if __name__ == '__main__':
    '''
    this program clusters the tracks in the db and inserts the results to a new table  
    '''

    # create DB object to handle ALL interactions with database
    db = myDBObject.MyDBObject(myenvvar.db_vars)

    # create a kmeans modeler
    km = kmeansObj.KmeansObj(3)

    km.create_features_df(db.read_sql_to_df("SELECT * FROM audio_features"))

    km.determine_k()

    km.fit_kmeans_model()

    db.insert_kmeans_params_and_centroids_to_db(km.clustering_datetime,km.random_state,km.k,km.kmeans_model.inertia_,km.kmeans_model.cluster_centers_)


    