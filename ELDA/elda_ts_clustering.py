## time series clustering algorithm ##

# coding: utf-8

# default lib
import random
# required lib #
import numpy as np


def k_means_clust(data, num_clust, num_iter, w):
    centroids = random.sample(list(data.values()),num_clust) # 랜덤하게 중심점 선택
    #centroids = random.sample(list(data),num_clust) # 랜덤하게 중심점 선택
    #centroids = [0,0,0,0,0]
    ##print(list(data.values()))
    ##print("-----------------")
    ##print(centroids)

    counter = 0

    for n in range(num_iter):   # 10회 반복
        counter += 1
        #print(counter)

    #assign data points to clusters
        assignments = {}

        for ind, i in enumerate(data.values()):  #ex) ind: 0, i: ts_1
            ind = list(data)[ind]
            
            min_dist = float('inf')
            closest_clust = None

            #print(ind)
            #print("----------")
            #print(type(i))
            #print("----------")
            #print(min_dist)
            #print("----------")
            #print(closest_clust)

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
        #print(assignments) #Result of Clustering
        #print(type(assignments))

        #recalculate centroids of clusters 
        for key in assignments:
            #print(key)
            #print("-------------")
            #print(assignments[key])

            clust_sum = 0

            if not assignments[key]:
                print("============== Null Cluster ============")
                #centroids[key] = 0
            else:
                for k in assignments[key]:
                    clust_sum = clust_sum+np.asarray(data[k])
                    #print("clust_sum : ", clust_sum)
                    #print("data[k]", data[k])
                ########## null 값으로 처리해야함 ########
                centroids[key] = [m/len(assignments[key]) for m in clust_sum]

    print(assignments) #Result of Clustering


    return centroids, assignments


def DTWDistance(s1, s2, w):
    ''' 
    Calculates dynamic time warping Euclidean distance between two 
    sequences. Option to enforce locality constraint for window size w. 
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
#    print(s1)
#    print("-----------------------")
#    print(s2)


    LB_sum = 0
    for ind, i in enumerate(s1):
          
        lower_bound = min(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        upper_bound = max(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        
#        print(ind, i, lower_bound, upper_bound)

        if float(i) > float(upper_bound):
            LB_sum = LB_sum+(float(i)-upper_bound)**2
        elif float(i) < lower_bound:
            LB_sum = LB_sum+(float(i)-lower_bound)**2
      
    return np.sqrt(LB_sum) 

##########################
if __name__ == '__main__':
    pass