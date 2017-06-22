## time series clustering algorithm ##

# coding: utf-8

# default lib
import random
# required lib #
import numpy as np


def k_means_clust(data, num_clust, num_iter, w):
    
    centroids = random.sample(list(data.values()), num_clust) # 랜덤하게 중심점 선택
    
    print(centroids)
    
    counter = 0
    
    for n in range(num_iter):   # num_iter회 반복
        # assign data points to clusters
        counter += 1
        assignments = {}

        for ind, i in enumerate(data.values()):  #ex) index: 0~n, i: ts_0~n
            ind = list(data)[ind]   # replace index to node ID
            print("i====> {}".format(len(i)))

            min_dist = float('inf')
            closest_clust = None

            for c_ind, j in enumerate(centroids): #random centroid 

                print("j====> {}".format(len(j)))               

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

        # recalculate centroids of clusters 
        for key in assignments:

            # clust_sum = 0
            # clust_sum 리스트로 초기화
            clust_sum = [0 for _ in range(len(data.keys()))]

            # 클러스터의 중심값 계산
            for k in assignments[key]:
                clust_sum = [x + y for x, y in zip(clust_sum, data[k])]

            # 클러스터가 빙있다면.. -1로 초기화
            if all(v == 0 for v in clust_sum):
                print("There is no cluster")
                centroids[key] = [-1 for _ in range(len(data.keys()))]
            else:
                centroids[key] = [m/len(assignments[key]) for m in clust_sum]

    return centroids, assignments


def DTWDistance(s1, s2, w):

    DTW={}

    if w:
        w = max(w, abs(len(s1)-len(s2)))

        for i in range(-1, len(s1)):
            for j in range(-1, len(s2)):
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
                DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])
        else:
            for j in range(len(s2)):
                dist = (s1[i]-s2[j])**2
                DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])

    return np.sqrt(DTW[len(s1)-1, len(s2)-1])


def LB_Keogh(s1, s2, r):
    print("===== debug =====")
    print("s1 len == {} | s2 len == {}".format(len(s1), len(s2)))
    print("s1==== {}".format(s1))
    print("s2==== {}".format(s2))

    LB_sum = 0.0
    #LB_sum = 0
    for ind, i in enumerate(s1):
        print("ind==== {}".format(ind))
        print("i==== {}".format(i))
        print(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])

        lower_bound = min(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        upper_bound = max(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        print(ind, i, lower_bound, upper_bound)

        if float(i) > float(upper_bound):
            LB_sum = LB_sum + (float(i)-upper_bound)**2
        elif float(i) <= float(lower_bound):
            LB_sum = LB_sum + (float(i)-lower_bound)**2

    return np.sqrt(LB_sum)

##########################
if __name__ == '__main__':
    pass