# Greedy-K-means
Greedy K-means Spark Package in Python
Version 1.0,  2016-July-29

Copyright (c) 2016 Hongfu Liu & Nikos Vlassis.
=============================================================================================

1. Introduction
===============
GKCC is a Python package for Greedy K-means in the Spark environment.
Reference:
[1] Likas, A., Vlassis, N., & Verbeek, J. J. (2003). The global k-means clustering algorithm. Pattern recognition, 36(2), 451-461.

2. Installation and Basic Usage
===============================
A. Copy this file to the specific directory in your workspace. 

B. Start Spark and go to your Spark path

C. Submit the job
> ./bin/spark-submit YOUR PATH/GKmeans.py YOUR DATA NUM_CLUSTER

3. Functions in the package
===========================
	- main: we run Greedy K-means from 1 center to K centers.
	- parseVector: transforms the data into an array.
	- closestPoint: finds the nearest center.
	- CandidateCenter: adds one center.
	- BasicKmeans: runs the basic K-means. 

4. Contact
==========
For questions and comments, please feel free to contact Hongfu Liu(liu.hongf@husky.neu.edu).
