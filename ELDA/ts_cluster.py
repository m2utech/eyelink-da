# coding: utf-8

import pandas as pd

### test library ###
import numpy as np
import matplotlib.pyplot as plt
import random

def k_means_clust(data, num_clust, num_iter, w):
    centroids = random.sample(list(data),num_clust) # 랜덤하게 중심점 선택
    #centroids = random.sample(list(data),num_clust) # 랜덤하게 중심점 선택
    #centroids = [0,0,0,0,0]
    print(list(data))
    import pdb; pdb.set_trace()  # breakpoint 82d50c1b //

    print(centroids)

    counter = 0

    for n in range(num_iter):   # 10회 반복
        counter += 1
        #print(counter)

    #assign data points to clusters
        assignments = {}

        for ind, i in enumerate(data):  #ex) ind: 0, i: ts_1
            min_dist = float('inf')
            closest_clust = None
            print(ind, i, min_dist, closest_clust)##########################

            for c_ind, j in enumerate(centroids): #random centroid 
                
                print(c_ind, j) ###############
                if LB_Keogh(i, j, 5) < min_dist:
                    cur_dist = float(DTWDistance(i, j, w))
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        closest_clust = c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust] = []
        print(assignments)

        #recalculate centroids of clusters 
        for key in assignments:
            clust_sum = 0
            for k in assignments[key]:
                clust_sum = clust_sum+data[k]

            centroids[key] = [m/len(assignments[key]) for m in clust_sum]
    return centroids


def DTWDistance(s1, s2, w):
    ''' 
    Calculates dynamic time warping Euclidean distance between two 
    sequences. Option to enforce locality constraint for window w. 
    ''' 
    
    DTW={} 
 
    if w: 
        w = max(w, abs(len(s1)-len(s2))) 
 
        for i in range(-1,len(s1)): 
            for j in range(-1,len(s2)): 
                DTW[(i, j)] = float('inf') 
      
    else: 
        for i in range(len(s1)): 
            DTW[(i, -1)] = float('inf') 
        for i in range(len(s2)): 
            DTW[(-1, i)] = float('inf') 
  
    DTW[(-1, -1)] = 0 

    for i in range(len(s1)): 
        if w: 
            for j in range(max(0, i-w), min(len(s2), i+w)):
                dist = float((s1[i] - s2[j]))**2
                DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)]) 
        else: 
            for j in range(len(s2)): 
                dist = (s1[i]-s2[j])**2 
                DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)]) 
      
    return np.sqrt(DTW[len(s1)-1, len(s2)-1]) 


def LB_Keogh(s1, s2, r):
    ''' 
    Calculates LB_Keough lower bound to dynamic time warping. Linear 
    complexity compared to quadratic complexity of dtw. 
    ''' 
    LB_sum = 0
    for ind, i in enumerate(s1):
          
        lower_bound = min(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        upper_bound = max(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        
        if i > upper_bound:
            LB_sum = LB_sum+(i-upper_bound)**2
        elif i < lower_bound:
            LB_sum = LB_sum+(i-lower_bound)**2
      
    return np.sqrt(LB_sum) 


test = pd.read_csv("../data/train.csv", sep=',')
#test = np.genfromtxt("../data/train.csv", delimiter=',')
#test = test.T
#test = test.values.tolist()
#print(type(test))
#print(list(test))

centroids = k_means_clust(test, 5, 10, 4)

for i in centroids:
    plt.plot(i)

plt.show()
