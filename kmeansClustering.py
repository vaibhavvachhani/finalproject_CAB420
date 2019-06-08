#!/usr/bin/env python

# Imports
import statistics
import math
import os
import pandas as pd
import numpy as np
import sklearn.cluster as sc
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy.ma as ma

# local functions
# Train a kmeans model using ratings as data with a default number of clusters as 10
def ktrain(ratings, nClusters=10):
    return sc.KMeans(n_clusters=nClusters, random_state=1).fit(ratings)

# Get users within the same cluster as the rating
# Accepts kmeans object and a single input.
# Returns idx of similar users
def getSimilarUser(rating, clusters):
    # Expected rating structure is a [[data]], must reshape
    rating = rating.reshape(1, -1)

    # predict which cluster this single input would be in.
    # returns [pred]
    pred = clusters.predict(rating)

    # collect training labels
    ylabel = clusters.labels_
    
    # find similar users
    simUserIdx = [idx for idx in range(len(ylabel)) if ylabel[idx] == pred[0]]

    return simUserIdx

# 
def doClustering(user_id, ratings):
    clusterError = []
    #[1, 5, 10, 20, 40, 80]
    for nCluster in [1, 5, 10, 20, 40, 80]:
        print('Starting...')
        print('Using ', nCluster, ' clusters')
        kmeans = sc.KMeans(n_clusters=nCluster, random_state=1).fit(ratings)
        pred = kmeans.predict(ratings)
        errors = []
        for idx in range(len(pred)):
            #errors.append(kmeans.inertia_)
            #dist = [math.pow(movieRating - kmeans.cluster_centers_[pred[idx], j],2) for j, movieRating in enumerate(ratings[idx]) if movieRating != 0]
            #print('Method 1: SUM( (Xa - Ya)^2 + ... + (Xn - Yn)^2 ) ')
            #print('Distance Calculated: ', sum(dist))
            #print('--------------------------------')
            idxNZ = [j for j in range(len(ratings[idx])) if ratings[idx, j] !=0]
            vectorX = np.linalg.norm(ratings[idx, idxNZ], ord=2)
            vectorY = np.linalg.norm(kmeans.cluster_centers_[pred[idx], idxNZ], ord=2)
            #prediction = statistics.mean(vectorY)
            dist = math.pow(vectorX - vectorY, 2)
            #print('Method 2: SUM( (SQRT( Xa^2 + ... + Xn^2) - SQRT( Ya^2 + ... + Yn^2 ) )^2 )')
            #print('Distance Calculated: ', test)
            #dist = sum(dist)
            errors.append(dist)
        clusterError.append(sum(errors))
        print('...Done')
        
    #print(clusterError, kmeans.inertia_)
    #idxNZ = [j for j in range(len(ratings[0])) if ratings[0, j] !=0]
    #print(ratings[1,idxNZ])
    #print(kmeans.cluster_centers_[pred[1],idxNZ])
    plt.plot([1, 5, 10, 20, 40, 80], clusterError)
    plt.show()    
    #print(kmeans.labels_)
    #print(kmeans.predict(ratings))
    return pred

def clusterAVG(rating):

    size = rating.shape
    movieAVG = []
    # for each movie
    for i in range(size[1]):
        #find the non zero values
        aMovie = rating[:,i]

        # need the index to keep track of the rows
        idxNZ = [j for j in range(len(aMovie)) if aMovie[j] !=0]        

        # otherwise find average
        if idxNZ:
            movieAVG.append(statistics.mean(aMovie[idxNZ]))
        else:
            movieAVG.append(0)
        
    return np.array(movieAVG)

def doCluster(user_id, ratings):
    pred = sc.KMeans(n_clusters=11, random_state=1).fit_predict(ratings)

    movieAVGs = []
    
    for n in list(set(pred)):
        groupRatings = ratings[pred==n]
        movieAVG = clusterAVG(groupRatings)
        clusterError = []
        for i in groupRatings:
            vectorX = np.linalg.norm(i, ord=2) 
            vectorY = np.linalg.norm(movieAVG, ord=2)
            dist = math.pow(vectorX - vectorY, 2)
            clusterError.append(dist)
        movieAVGs.append(sum(clusterError))

    print(movieAVGs)
    return np.array(movieAVGs)
         
# main function
if __name__ == "__main__":
    # Change paths
    dataPath = "C:/Users/vrenn/Documents/QUT Files/CAB420/Assignment 3/Codes/CAB420 Final Project/CAB420 Final Project/"
    os.chdir(dataPath)  # Change path

    # The path to the data is here
    newRatings = pd.read_csv("topRated.csv", sep=',', header=0,encoding='latin-1')
    print('-------------------------------')
    print('Number of ratings: ', len(newRatings))
    print(newRatings.head(4))
    print('-------------------------------')
    print('...Data loaded.')

    # Pseudo-user ID.
    user_id = list(range(0,len(newRatings.iloc[:,1])))
    
    # Convert movieID into np array
    movieId = newRatings.columns.values
    

    # convert data into np array
    ratings = newRatings.values
    
    #ratings = newRatings.drop('user_id',axis=1).values
    #print(ratings)
    #kmodel = ktrain(ratings)
    #simUsers = getSimilarUser(ratings[0,:], kmodel)
    #simUser = doCluster(user_id, ratings)
    
    doClustering(user_id,ratings)