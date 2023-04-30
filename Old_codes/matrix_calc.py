import numpy as np

# given points
points = np.array([(482, 192), (1477, 255), (437, 880), (1438, 922)])

# desired points
desired_points = np.array([(350, 350), (350, 50), (550, 350), (550, 50)])

# center of mass of given points
centroid = np.mean(points, axis=0)

# center of mass of desired points
desired_centroid = np.mean(desired_points, axis=0)

# translation to move centroid of given points to centroid of desired points
translation = desired_centroid - centroid

# compute the covariance matrix of given points
cov_matrix = np.cov(points.T)

# singular value decomposition of covariance matrix
U, S, V = np.linalg.svd(cov_matrix)

# rotation matrix
R = np.dot(U, V)

# scaling matrix
scaling = np.diag(np.sqrt(S))

# final transformation matrix
T = np.dot(np.dot(R, scaling), R.T)

# apply transformation to points
transformed_points = np.dot(points - centroid, T) + desired_centroid + translation

print(transformed_points)
