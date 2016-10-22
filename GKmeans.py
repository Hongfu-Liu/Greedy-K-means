# ===================================================================================================================================
# Greedy K-means
# Python version 1.0 July-22-2016
# This code is used for Greedy Kmeans, for more details please see
# Likas, A., Vlassis, N., & Verbeek, J. J. (2003). The global k-means clustering algorithm. Pattern recognition, 36(2), 451-461.
# For questions and comments, please feel free to contact Hongfu Liu (liu.hongf@husky.neu.edu) and Nikos Vlassis (vlassis@adobe.com)
# ===================================================================================================================================
from __future__ import print_function
import sys

import numpy as np
from pyspark import SparkContext

def parseVector(line):
    return np.array([float(x) for x in line.split(',')])

def closestPoint(p, centers):
    bestIndex = 0
    closest = float("+inf")
    for i in range(len(centers)):
        tempDist = np.sum((p - centers[i]) ** 2)
        if tempDist < closest:
            closest = tempDist
            bestIndex = i
    return bestIndex

def CandidateCenter(p):
	return np.vstack((kCenters,p))  

# Users can replace the BasicKmeans with a fast version
def BasicKmeans(kCenters):
    totalsum = 0
    for iter in range(1, maxIter):  
        index = data.map(
            lambda p: (closestPoint(p, kCenters), (p, 1)))
        pointStats = index.reduceByKey(
            lambda p1_c1, p2_c2: (p1_c1[0] + p2_c2[0], p1_c1[1] + p2_c2[1]))
        kCenters = pointStats.map(
            lambda st: (st[1][0] / st[1][1])).collect()
        # The objective function is $\sum_k |C_k| ||m_k||^2$ ranther than the standard K-means
        # where $|C_k|$ and $m_k$ are are the size and center of k-th cluster, respectively 
        # To minimize the standard Kmeans objecitve function is equal to maximize $\sum_k |C_k| ||m_k||^2$
        objValue = sum(pointStats.map(
            lambda st: (sum((st[1][0]**2 / st[1][1])))).collect())

        while len(kCenters)<k:
        	kCenters = np.vstack((kCenters,data.takeSample(False,1,1)))  

        if abs(totalsum - objValue) < threshold:
            break
        else:
            totalsum = objValue    
    return index, kCenters, totalsum

if __name__ == "__main__":

	# Input: data & the cluster number
    if len(sys.argv) != 3:
        print("Usage: GKmeans <file> <k>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="Python_GKMeans")
    lines = sc.textFile(sys.argv[1])
    data = lines.map(parseVector).cache()
    K = int(sys.argv[2])

    # Set the stop criteria
    # Soft criterion: the difference of objective function value between two consecutive iterations
    # Hard criterion: the max number of iterations
    threshold = 0.01
    maxIter = 100
    output = {}
    
    # Start with one center
    kCenters = data.reduce(lambda x, y : x + y)/data.count()

    # The cluster number varies from 2 to K
    for k in range(2,K+1):
    	# Randomly pick up 59 points, which combines with the centers in previous stage as the new centers
    	CandidateCenters = sc.parallelize(data.takeSample(False, 59, 1)).map(CandidateCenter).collect()
    	# Run Kmeans with the new centers and this process is repeated 59 times
    	result = map(BasicKmeans, CandidateCenters)
    	# Select the result with the minimum objective function value and return the centers, assignments
    	best = result[np.argmax(result[i][2] for i in range(0,59))]
    	
    	index = best[0].map(lambda p : p[0]).collect()
    	kCenters = best[1]
    	objValue = best[2]
    	output[k] = (kCenters, index, objValue)

    sc.stop()
    # The ouput is formulized as a dictionary, where the key is the cluster number, the value consists of
    # the centers, assignments and new objective function value according to the specific cluster number 
    print(output)
