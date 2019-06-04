# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:32:48 2019

@author: Vaibhav Vachhani
"""
size = 423
finalRatings = []
users = []
ratings = []
def ratingData():
    f = open("C:/Users/Vaibhav Vachhani/Downloads/SEM-5/CAB420/final project/ml-20m/ml-20m/ratings.csv", 'r')
    record = f.readline()
    for i in range(0,size):
        record = f.readline()
        record = record.strip('\n')
        arr_data = record.split(',')
        
        currentUserId = arr_data[0]
        currentRating = arr_data[2]
        
        users.append(currentUserId)
        ratings.append(currentRating)
       
       
            
    uniqueUsers = list(set(users))
    return uniqueUsers
        
    
    #print(uniquesUsers)
if __name__ == "__main__":
    uniqueUsers = ratingData()
    
    index = 0
    for x in uniqueUsers:        
        index1 = users.count(x)
        lastIndex = index1+ index
        finalRatings.append(ratings[index:lastIndex])
        index = lastIndex
    print(finalRatings)
    print(len(uniqueUsers))