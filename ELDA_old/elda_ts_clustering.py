## time series clustering algorithm ##

# coding: utf-8

# default lib
import random
# required lib #
import numpy as np


def k_means_clust(data, num_clust, num_iter, w):
    dataset = list(data.values())
    centroids = random.sample(dataset,num_clust) # 랜덤하게 중심점 선택
    data_len = len(dataset[0][:])

    for n in range(num_iter):   # 10회 반복

    # assign data points to clusters
        assignments = {}

        # ex) ind: 0, i: time series data 1
        for ind, i in enumerate(data.values()):
            # replace index to node ID
            ind = list(data)[ind]

            min_dist = float('inf')
            closest_clust = None

            # calculate with random centroid
            for c_ind, j in enumerate(centroids):

                if LB_Keogh(i, j, 5) < min_dist:
                    cur_dist = float(DTWDistance(i, j, w))

                    if cur_dist < min_dist:
                        min_dist = cur_dist
                        closest_clust = c_ind

            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust] = []


        # recalculate centroids of clusters
        for key in assignments:

            # clust_sum 리스트로 초기화
            clust_sum = [0 for _ in range(data_len)]

            # 클러스터의 중심값 계산
            for k in assignments[key]:
                clust_sum = [x + y for x, y in zip(clust_sum, data[k])]

            # 클러스터가 비어있다면.. -1로 초기화
            if all(v == 0 for v in clust_sum):
            #if not assignments[key]:
                print("There is no cluster")
                #centroids[key] = [0 for _ in range(data_len)]
                centroids[key] = [-1 for _ in range(data_len)]
            else:
                centroids[key] = [m/len(assignments[key]) for m in clust_sum]

    ## print(assignments) #Result of Clustering


    return centroids, assignments


def DTWDistance(s1, s2, w):

    DTW = {}

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
                dist = float((s1[i] - s2[j]))**2
                DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])
        else:
            for j in range(len(s2)):
                dist = (s1[i]-s2[j])**2
                DTW[(i, j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])

    return np.sqrt(DTW[len(s1)-1, len(s2)-1])


def LB_Keogh(s1, s2, r):

    LB_sum = 0

    for ind, i in enumerate(s1):

        lower_bound = min(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])
        upper_bound = max(s2[(ind-r if ind-r >= 0 else 0):(ind+r)])

        if float(i) > float(upper_bound):
            LB_sum = LB_sum+(float(i)-upper_bound)**2
        elif float(i) < lower_bound:
            LB_sum = LB_sum+(float(i)-lower_bound)**2

    return np.sqrt(LB_sum)

##########################
if __name__ == '__main__':
    pass
