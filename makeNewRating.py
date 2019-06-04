#!/usr/bin/env python

# Purpose of the function - to create a new csv file that has all the ratings for a user

# Imports
import numpy as np
import os
import pandas as pd


# Local functions

# loadData - loads data of user rating and movies.
#   - no inputs (was designed to have one such as which file to use but not right now)
#   - loads movie id to get total movies
#   - returns the data in ratings and movies
def loadData():
    print('Loading data of 156 users...')
    r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
    ratings = pd.read_csv("ratingsLimited.csv", sep=',', names=r_cols, encoding='latin-1')
    print('-------------------------------')
    print('Number of ratings: ', len(ratings))
    print(ratings.head(4))
    print('-------------------------------')
    print('...Data loaded.')
    
    print('Now loading movie_ids...')
    r_cols = ['movieId', 'title', 'genres']
    movies = pd.read_csv("movies.csv", sep=',', names=r_cols, encoding='latin-1', header=None, skiprows=1)
    #movies.drop([1], axis=0)
    print('-------------------------------')
    print('Number of movies: ', len(movies))
    print(movies.tail(4))
    print('-------------------------------')
    print('...Data loaded.')

    return ratings, movies

# Creates a new dataframe based on the new data and 

# This function takes the ratings and movies and transforms it into a new data frame.
# In addition, it will create a new csv file for this.
def processData(ratings, movies):

    # Number of unique items in both rating and movie
    userNum = 702
    movieNum = len(movies)

    # data
    newData = np.zeros((userNum,movies.loc[movieNum-1,'movieId']))
    
    # fill in ratings of a user.
    for idx in range(len(ratings)):
        newData[ratings.loc[idx,'user_id']-1][ratings.loc[idx,'movie_id']-1] = ratings.loc[idx,'rating']

    hasCol = []
    for colIdx in range(movies.loc[movieNum-1,'movieId']):
        if len(set(newData[:,colIdx])) != 1:
            hasCol.append(colIdx)
            for idx, eachRow in enumerate(newData):
                if eachRow[colIdx] is 10:
                    newData[idx, colIdx] = 0
        else:
            newData[:, colIdx] = 0
    newData = newData[:, hasCol]

    return newData, hasCol

def makeDF(newData, hasCol):

    a = np.array(list(range(1,703)))
    a = a.reshape(len(a), 1)
    
    newestData = np.hstack((a, newData))
    
    tags = ['user_id']
    tags.extend([str(id+1) for id in hasCol])
    
    newDf = pd.DataFrame(data=newestData,columns=tags)
    
    return newDf

# Main function

if __name__ == "__main__":
    
    # File pathing
    dataPath = "C:/Users/vrenn/Documents/QUT Files/CAB420/Assignment 3/Codes/CAB420 Final Project/CAB420 Final Project/"
    os.chdir(dataPath)  # Change path
    
    # Load data.
    ratings, movies = loadData()

    # create new matrix
    newData, hasCol = processData(ratings, movies)

    # create new dataframe
    newDF = makeDF(newData, hasCol)
   
    newDF.to_csv("newRating.csv",index=False, encoding='latin-1')