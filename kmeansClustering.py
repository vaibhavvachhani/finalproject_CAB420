#!/usr/bin/env python

# Imports
import os
import pandas as pd
import sklearn.cluster as sc
import matplotlib.pyplot as plt

# local functions
def doClustering(user_id, ratings):

    errors = []
    for nClusters in range(25,26):
        kmeans = sc.KMeans(n_clusters=10, random_state=0).fit(ratings)
        errors.append(kmeans.inertia_)
    print(kmeans.predict(ratings))
    return 0

# main function
if __name__ == "__main__":
    dataPath = "C:/Users/vrenn/Documents/QUT Files/CAB420/Assignment 3/Codes/CAB420 Final Project/CAB420 Final Project/"
    os.chdir(dataPath)  # Change path

    newRatings = pd.read_csv("newRating.csv", sep=',', header=0,encoding='latin-1')
    print('-------------------------------')
    print('Number of ratings: ', len(newRatings))
    print(newRatings.head(4))
    print('-------------------------------')
    print('...Data loaded.')

    user_id = newRatings['user_id']
    ratings = newRatings.drop('user_id',axis=1).values
    print(ratings)

    doClustering(user_id, ratings)
    
    