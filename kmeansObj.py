from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
import pandas as pd
import datetime as dt

class KmeansObj:
    '''
    This object will handle ALL the modeling and clustering of the tracks by their features
    '''

    def __init__(self, randomState):
        self.model_for_elbow = KMeans(random_state=randomState)
        self.random_state = randomState
        self.clustering_datetime = dt.datetime.now()


    def create_features_df(self, df):
        '''
        create a features df that is ready to cluster
        '''
        cols_to_drop = ['track_id', 'key', 'time_signature', 'total_available_markets', 'mode', 'duration_ms','popularity','added_datetime']
        features_df = df.drop(cols_to_drop, axis=1)

        # normalyze / scale features
        for col in ['loudness', 'tempo']:
            features_df[col] = ((features_df[col] - features_df[col].min()) / (features_df[col].max() - features_df[col].min()))

        self.tracks_features_df_to_cluster = features_df


    def determine_k(self):
        '''
        determine the number of clusters using the 'elbow method' and 'interia' criteria. k is between 2-12
        '''
        visualizer = KElbowVisualizer(self.model_for_elbow, k=(2,12))
        visualizer.fit(self.tracks_features_df_to_cluster)
        self.k = visualizer.elbow_value_


    def fit_kmeans_model(self):
        '''
        fit kmeans model in order to get the model params and centroids to store in DB
        '''
        self.kmeans_model = KMeans(n_clusters=self.k,random_state=self.random_state).fit(self.tracks_features_df_to_cluster)
        


    



