# -*- coding: utf-8 -*-
"""
Created on Sat May 25 11:55:06 2019

@author: Vaibhav Vachhani
"""
import numpy as np
import csv



'''
Storing ratings in an array from csv file

format:
    {['userId' 'movieId' 'rating'],['userId' 'movieId' 'rating'],['userId' 'movieId' 'rating'])
    
'''
size = 22026 # only considering first 156 users
ratingsRecords = []
f = open('ratings.csv', 'r')
for i in range(0,size):
    record = f.readline()
    arr = record.split(',')
    arr = np.asarray(arr[:3])
    ratingsRecords.append(arr)
#print(ratingsRecords[1])



'''
Storing Movies Information in an array from csv file

format:
    {['movieId' 'title' 'genres'],['movieId' 'title' 'genres'],['movieId' 'title' 'genres'])
    
'''

moviesInfo = []
with open('movies.csv', newline='', encoding='utf-8') as f:
    for row in csv.reader(f):
        moviesInfo.append(row)
print(moviesInfo)





