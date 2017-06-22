## time series clustering algorithm ##

# coding: utf-8

# default lib
import random
# required lib #
import numpy as np
from pprint import pprint
from collections import OrderedDict
import json
import ast

###########################################
def k_means_clust(data, num_clust, num_iter, w):
    centroids = random.sample(list(data.values()),num_clust) # 랜덤하게 중심점 선택
    #centroids = random.sample(list(data),num_clust) # 랜덤하게 중심점 선택
    #centroids = [0,0,0,0,0]
    ##print(list(data.values()))
    ##print("-----------------")
    #print(centroids)
    #pprint(len(data.keys())) #--> 56개 노드수

    #counter = 0

    for n in range(num_iter):   # 10회 반복
        #counter += 1
        #print(counter)

    #assign data points to clusters
        assignments = {}

        for ind, i in enumerate(data.values()):  #ex) ind: 0, i: ts_1
            ind = list(data)[ind]
            
            min_dist = float('inf')
            closest_clust = None

#            print(ind)
#            print("----------")
#            print(i)
#            print("----------")
#            print(min_dist)
#            print("----------")
#            print(closest_clust)


            for c_ind, j in enumerate(centroids): #random centroid 
                
                #print(c_ind, j) ###############

                if LB_Keogh(i, j, 5) < min_dist:
                    cur_dist = float(DTWDistance(i, j, w))
                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        closest_clust = c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust] = []

        #print(type(assignments))

        #recalculate centroids of clusters 
        for key in assignments:
            print(key)
            #print("-------------")
            #print(assignments[key])
            #print("888888888")
            #print(data['0001.0000001C'])

            #clust_sum = 0

            clust_sum = [0.0 for _ in range(len(data.keys()))]

            for k in assignments[key]:
                #print("k ==> {}".format(k))
                #print(data[k])
                #print("$$$$$$$")
                #print(data[k][1:5])


                clust_sum = [x + y for x,y in zip(clust_sum, data[k])]
                #print(clust_sum)


                #print(type(data[k]))
                #clust_sum = clust_sum+np.asarray(data[k])
                #clust_sum = clust_sum+data[k]
                #print("clust_sum : ", clust_sum)
                #print("data[k]", data[k])
                ########## null 값으로 처리해야함 ########

            if all(v == 0 for v in clust_sum):
                print("There is no cluster")
                centroids[key] = [-1 for _ in range(len(data.keys()))]
                print(centroids[key])
            else:
                centroids[key] = [m/len(assignments[key]) for m in clust_sum]
                print(centroids[key])


            #print("========================")
            #print(centroids[key])

    print(assignments) #Result of Clustering
    import pdb; pdb.set_trace()  # breakpoint 9a6e6008 //

    return centroids, assignments

#################################################
def DTWDistance(s1, s2, w=None):

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
                dist = (s1[i] - s2[j])**2
                DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
        else: 
            for j in range(len(s2)): 
                dist = (s1[i]-s2[j])**2 
                DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)]) 
              
    return np.sqrt(DTW[(len(s1)-1), (len(s2)-1)])

############################################################
def LB_Keogh(s1, s2, r):

    LB_sum = 0

    for ind, i in enumerate(s1):

        lower_bound = min(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        upper_bound = max(s2[(ind-r if ind-r >= 0 else 0):(ind+r)]) 

        if i > upper_bound:
            LB_sum = LB_sum + (i-upper_bound)**2
        elif i < lower_bound:
            LB_sum = LB_sum + (i-lower_bound)**2

    return np.sqrt(LB_sum)

##########################
if __name__ == '__main__':

    f = open('testdata.txt', 'r')
    data = f.read()
    data = ast.literal_eval(data)

    pf_ls = OrderedDict(sorted(data.items(), key=lambda x:x[1], reverse=True))
    
    k_means_clust(pf_ls, 4, 1, 5)