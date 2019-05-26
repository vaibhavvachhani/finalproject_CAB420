# -*- coding: utf-8 -*-
"""
Created on Sat May 25 11:55:06 2019

@author: Vaibhav Vachhani
"""
import numpy as np
import csv



'''
Storing ratings in an arrays from csv file
ratingRecords_X Structre: [[userId, movieId], [userId, movieId], [userId, movieId], [userId, movieId]....[userId, movieId]]
ratingRecords_y Structre: [rating, rating, rating, rating, rating....rating]

    
'''

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
        moviesInfo_y.append(row[2])
print(moviesInfo_X)
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

