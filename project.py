# -*- coding: utf-8 -*-
"""
Created on Sat May 25 11:55:06 2019

@author: Vaibhav Vachhani
"""
import numpy as np
import csv
import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn import linear_model
from sklearn import preprocessing
from sklearn import utils
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import math

moviesInfo_X = []
moviesInfo_y = []
movies = {}
with open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/movies.csv", newline='', encoding='utf-8') as f:
    for row in csv.reader(f):
        movies[row[0]] = row[2]
        moviesInfo_X.append(row)
        moviesInfo_y.append(row[2])
#print(moviesInfo_X[27278])
#print(movies)
        
'''       
tags_data = {}

with open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/genome-scores.csv", newline='', encoding='utf-8') as f:
    for row in csv.reader(f):
        if(tags_data.__contains__(row[0])):
            data = [tags_data[row[0]]]
            data.append(tags_data[row[0]])
            tags_data[row[0]] = data
        else:
            tags_data[row[0]] = (row[1:])
        #tags_data.append(row)
        
print(tags_data)  
'''  


'''
Storing ratings in an arrays from csv file
ratingRecords_X Structre: [[userId, movieId], [userId, movieId], [userId, movieId], [userId, movieId]....[userId, movieId]]
ratingRecords_y Structre: [rating, rating, rating, rating, rating....rating]

    
'''
def ratingData():
    
    size = 10000 # only considering first 156 users
    ratingsRecords_X = []
    ratingsRecords_y = []
    moviesID = []
    #users = []
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'  ]
    genresScores = { 'Action' : 0,
                     'Adventure' : 0,
                     'Animation' : 0,
                     'Children' : 0,
                     'Comedy' : 0,
                     'Crime' : 0,
                     'Documentary' : 0,
                     'Drama' : 0,
                     'Fantasy' : 0,
                     'Film-Noir' : 0,
                     'Horror' : 0,
                     'Musical' : 0,
                     'Mystery' : 0,
                     'Romance' : 0,
                     'Sci-Fi' : 0,
                     'Thriller' : 0,
                     'War' : 0,
                     'Western' : 0   
            
            
                    }
    f = open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/ratings.csv", 'r')
    for i in range(0,size):
        record = f.readline()
        arr_data = record.split(',')
        #if(i!=0 and users.__contains__(arr_data[0])==False):
            
            #users.append(arr_data[0]) #mark user as visited
        if(i!=0):
            d = arr_data[:2]
            arr1 = arr_data[2]
            '''
            Action = 0;
            Adventure = 0;
            Animation = 0;
            Children = 0;
            Comedy = 0;
            Crime = 0;
            Documentary = 0;
            Drama = 0;
            Fantasy = 0;
            Film-Noir = 0;
            Horror = 0;
            Musical = 0;
            Mystery = 0;
            Romance = 0;
            Sci-Fi = 0;
            Thriller = 0;
            War = 0;
            Western = 0;
            '''
            
            #find movie title from movies list using movieId
            
            movieId = d[1]
            moviesID.append(movieId)
            arr=[]
            movieGenres = movies.get(movieId)
            for genre in genres:
                if (genre in movieGenres):
                    genresScores[genre] = 1
            for g, gScore in genresScores.items():
                arr.append(gScore)
            for genre in genres:
                    genresScores[genre] = 0
            
        
        
        
        #movieGenres = movieGenres.replace('|', ',')
        #arr.append(movieGenres)
                
            ratingsRecords_X.append(arr)
                
            ratingsRecords_y.append((float(arr1)))
            
            
            
            
    ratingsRecords_X = np.array(ratingsRecords_X)
    ratingsRecords_y = np.array(ratingsRecords_y)
    
    ratingsRecords_X = ratingsRecords_X.astype(np.float64)
        
    ratingsRecords_y = ratingsRecords_y.astype(np.float64)
    #lab_enc = preprocessing.LabelEncoder()
    #ratingsRecords_y = lab_enc.fit_transform(ratingsRecords_y)
    print(ratingsRecords_X[:50])
    print(ratingsRecords_y) 
    print(ratingsRecords_X.shape)  
    print(ratingsRecords_y.shape) 
    print(utils.multiclass.type_of_target(ratingsRecords_y))
    print(ratingsRecords_y)
    return ratingsRecords_X, ratingsRecords_y, moviesID


'''
Storing Movies Information in an arrays from csv file

movieInfo_X Structre: [[movieId, title], [movieId, title], [movieId, title],[movieId, title] ......[movieId, title]] 
movieInfo_y Structre: [[Genres], [Genres], [Genres], [Genres], [Genres].....[Genres]] 
'''
'''
moviesInfo_X = []
moviesInfo_y = []

with open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/movies.csv", newline='', encoding='utf-8') as f:
    for row in csv.reader(f):
        moviesInfo_X.append(row[:2])
        moviesInfo_y.append(row[2])
#print(moviesInfo_X)
#print(moviesInfo_y)
'''

'''
Storing Tags Information in an arrays from csv file

tagsInfo_X Structure : [[userId, movieId], [userId, movieId], [userId, movieId], [userId, movieId]....[userId, movieId]]
tagsInfo_y Structure : [tag, tag, tag, tag......tag, tag]
'''

tags_data = []
with open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/genome-scores.csv", newline='', encoding='utf-8') as f:
    for row in csv.reader(f):
        #print(row)
        tags_data.append(row)
        
#print(tagsInfo_y)

if __name__ == "__main__":
    X, y, m = ratingData()
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    print(len(m))
    print(len(y))
    n = 9999
    r = 2 * np.random.rand(n)
    theta = 2 * np.pi * np.random.rand(n)
    area = 200 * r**2 * np.random.rand(n)
    colors = theta
    plt.scatter(m, y, c=colors, s=area, cmap=plt.cm.gist_heat)
    
    #plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='x')
        
    plt.title('Data points and cluster centroids')
    plt.show()
    