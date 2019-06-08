# Import libraries
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Reading ratings file
ratings = pd.read_csv('ml-20m/ratings.csv', sep=',', 
                      usecols=['userId', 'movieId', 'rating'])
max_userid = ratings['userId'].drop_duplicates().max()
max_movieid = ratings['movieId'].drop_duplicates().max()

# Reading ratings file
movies = pd.read_csv('ml-20m/movies.csv', sep=',', 
                     usecols=['movieId', 'title', 'genres'])


# Define model
from keras.layers import Input, Dense, Dropout, Flatten, Lambda
from keras.models import Model
from keras.layers import Embedding, Reshape, dot, multiply, concatenate
from keras import backend as BK

K_FACTORS = 100 # The number of dimensional embeddings for movies and users


input_1 = Input(shape=(1,))
input_2 = Input(shape=(1,))


P = Reshape((K_FACTORS,))(Embedding(max_userid, K_FACTORS, input_length=1)(input_1))
Q = Reshape((K_FACTORS,))(Embedding(max_userid, K_FACTORS, input_length=1)(input_2))
P_dot_Q = dot([P, Q], axes = 1, normalize = True)
scaled = Lambda(lambda x: x * 5)(P_dot_Q)


model = Model(inputs=[input_1,input_2], outputs=scaled)
#print(model.summary())
# model.compile(loss = 'MSE', optimizer='adamax',metrics = ['accuracy'])

model.load_weights('weights_RSME_1,1919.h5')

# Function to predict the ratings given User ID and Movie ID
def predict_rating(userId, movieId):
    return model.predict([np.array([userId - 1]),np.array([movieId - 1])])[0][0]

TEST_USER = 1560
print('\n\nMovies rated by user {}'.format(TEST_USER))
user_ratings = ratings[ratings['userId'] == TEST_USER][['userId', 'movieId', 'rating']]
# user_ratings['prediction'] = user_ratings.apply(lambda x: predict_rating(TEST_USER, x['movieId']), axis=1)
print(user_ratings.sort_values(by='rating', ascending=False).merge(movies, 
                                                on='movieId', 
                                                how='inner', 
                                                suffixes=['_u', '_m']).head(20))


print('\n\n Movies predicted for user {}'.format(TEST_USER))
recommendations = ratings[ratings['movieId'].isin(user_ratings['movieId']) == False][['movieId']].drop_duplicates()
recommendations['prediction'] = recommendations.apply(lambda x: predict_rating(TEST_USER, x['movieId']), axis=1)
print(recommendations.sort_values(by='prediction',
                          ascending=False).merge(movies,
                                                 on='movieId',
                                                 how='inner',
                                                 suffixes=['_u', '_m']).head(20))