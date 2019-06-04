# -*- coding: utf-8 -*-
#!/usr/bin/env python3.7
"""
Created on Sat May 25 11:55:06 2019
@author: Vaibhav Vachhani - pre-processing of raw data.
         Vrenn Umipig - clustering analysis
"""
import numpy as np
import csv
import statistics
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sklearn.cluster

def getSimMovie(moviesInfo_X, moviesInfo_y, selectedGenre):
    # This finds the movie with the selectedGenre
    # Uses moviesInfo_y then returns movieID in moviesInfor_X
    # returns [movieID, ..., movieID]
    movies = []
    for ii, genre in enumerate(moviesInfo_y):
        for aGenre in genre:
            if aGenre == selectedGenre:
                movies.append(moviesInfo_X[ii][0])
                break # its a romantic movie - stop looking for other tag.
    
    return movies

def getUserRating(ratingsRecords_X, ratingsRecords_y, movieIDList):
    # places the all scores into one user.
    #    - [User id, all their ratings for the genre]
    # returns [[userID, rating, ..., rating], ..., [userID, rating, ..., rating]]
    userRating = []
    uniqueRating = set()
    for ii, eachRating in enumerate(ratingsRecords_X):
        if eachRating[1] in movieIDList:
            if eachRating[0] not in uniqueRating:
                uniqueRating.add(eachRating[0])
                userRating.append([int(eachRating[0]), float(ratingsRecords_y[ii])])
            else:
                userRating[int(eachRating[0])-1].append( float(ratingsRecords_y[ii]))
    return userRating

def getAvg(genreScore):
    # Gives mean of scores
    # returns [avgRating, ..., avgRating] in the order of input so movieScore[0] would be for scores[0].
    movieScore = [statistics.mean(scores[1:]) for scores in genreScore]
    return movieScore

def getErrors(clusterObj, dataPoints):
    # Sum of squared difference in distance between a point to cluster centre
    # Returns total distance between points and assigned cluster.
    prediction = clusterObj.predict(dataPoints)
    clusterCentre = clusterObj.cluster_centers_
    dist = 0
    for ii, eachData in enumerate(dataPoints):
        dist += sum(np.square(clusterCentre[prediction[ii]] - eachData))
    return dist

def doRatingsClustering(ratingsRecords_X, ratingsRecords_y, moviesInfo_X, moviesInfo_y):
    '''
    This function does clustering: So far i've been testing it on a few genre.
    Purpose is to find similar users based on their ratings
    Inputs: data input kept the same as VaibhavVachhani's work.
       - ratingRecords_X/y : Same structure as below.
       - movieInfo_X/y : same structure as below.
    '''

    # Test with a few ratings
    romanticMovies = getSimMovie(moviesInfo_X,moviesInfo_y, 'Romance')
    romanticMoviesScore = getUserRating(ratingsRecords_X,ratingsRecords_y, romanticMovies)
    avgRomanticScore = getAvg(romanticMoviesScore)
    print(romanticMovies)
    print(romanticMoviesScore)
    print(avgRomanticScore)
    scifiMovies = getSimMovie(moviesInfo_X,moviesInfo_y,'Sci-Fi')
    scifiMoviesScore = getUserRating(ratingsRecords_X,ratingsRecords_y, scifiMovies)
    avgScifiScore = getAvg(scifiMoviesScore)

    actionMovies = getSimMovie(moviesInfo_X,moviesInfo_y,'Action')
    actionMoviesScore = getUserRating(ratingsRecords_X,ratingsRecords_y, actionMovies)
    avgActionScore = getAvg(actionMoviesScore)

    # Testing data can come after the whole thing is created.
    trainData = list(zip(avgRomanticScore,avgScifiScore,avgActionScore))
    trainData = [list(score) for score in trainData]

    # Change the number of clusters. If you do, you might have to comment out the plotting bc its for 2D classes
    kTrain = sklearn.cluster.KMeans(n_clusters=2,random_state=1).fit(trainData)
    prediction = kTrain.predict(trainData)
    class1_X = [avgRomanticScore[idx] for idx in range(len(trainData)) if prediction[idx] == 0]
    class1_y = [avgScifiScore[idx] for idx in range(len(trainData)) if prediction[idx] == 0]
    class2_X = [avgRomanticScore[idx] for idx in range(len(trainData)) if prediction[idx] == 1]
    class2_y = [avgScifiScore[idx] for idx in range(len(trainData)) if prediction[idx] == 1]
    plt.scatter(class1_X, class1_y,c='green')
    plt.scatter(class2_X, class2_y,c='red')
    plt.show()
    
           
if __name__ == "__main__":
    '''
    Storing ratings in an arrays from csv file
    ratingRecords_X Structre: [[userId, movieId], [userId, movieId], [userId, movieId], [userId, movieId]....[userId, movieId]]
    ratingRecords_y Structre: [rating, rating, rating, rating, rating....rating]
    
    '''
    # At the moment only this much works. Increasing it will break it - I have to fix.
    size = 22026 # only considering first 156 users
    ratingsRecords_X = []
    ratingsRecords_y = []
    f = open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/ratings.csv", 'r')
    for i in range(0,size):
        record = f.readline()
        arr_data = record.split(',')
        arr = arr_data[:2]
        arr1 = arr_data[2]
        ratingsRecords_X.append(arr)
    
        ratingsRecords_y.append(arr1)
    #print(ratingsRecords_X)
    #print(ratingsRecords_y)

    '''
    Storing Movies Information in an arrays from csv file
    movieInfo_X Structre: [[movieId, title], [movieId, title], [movieId, title],[movieId, title] ......[movieId, title]] 
    movieInfo_y Structre: [[Genres], [Genres], [Genres], [Genres], [Genres].....[Genres]] 
    '''

    moviesInfo_X = []
    moviesInfo_y = []

    with open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/movies.csv", newline='', encoding='utf-8') as f:
        for row in csv.reader(f):
            moviesInfo_X.append(row[:2])
            moviesInfo_y.append(row[2].split('|'))
    #print(moviesInfo_X)
    #print(moviesInfo_y)

    '''
    Storing Tags Information in an arrays from csv file
    tagsInfo_X Structure : [[userId, movieId], [userId, movieId], [userId, movieId], [userId, movieId]....[userId, movieId]]
    tagsInfo_y Structure : [tag, tag, tag, tag......tag, tag]
    '''

    tagsInfo_X = []
    tagsInfo_y = []

    with open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/tags.csv", newline='', encoding='utf-8') as f:
        for row in csv.reader(f):
            tagsInfo_X.append(row[:2])
            tagsInfo_y.append(row[2])
    #print(tagsInfo_X)
    #print(tagsInfo_y)

    doRatingsClustering(ratingsRecords_X, ratingsRecords_y, moviesInfo_X, moviesInfo_y)
