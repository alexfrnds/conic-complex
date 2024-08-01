import numpy as np
import struct
import ccomplex.free_twopac as ftp

#========================================================
# This script generates the binary files for the tests
#========================================================

# === Generating functions ===

def circle(sample_size, ambient_dimension = 2, vertical_noise=0):
    '''Generates a circle with a chisquare vertical noise'''
    points = np.zeros((0, ambient_dimension))
    while points.shape[0] < sample_size:
        new_sample_size = sample_size-points.shape[0]
        new_points = np.random.random_sample(size=(new_sample_size, ambient_dimension)) * 2 - 1
        norms      = np.linalg.norm(new_points, axis=1)
        selection  = norms > 0.1
        points     = np.vstack((points, new_points[selection,:] / norms[selection, None]))
    noise = np.sqrt(np.random.chisquare(4, sample_size)) * vertical_noise
    points = points + noise[:, None] *points
    return points

def half_circle(sample_size, ambient_dimension, vertical_noise=0):
    '''Generates a circle with a chisquare vertical noise'''
    points = np.zeros((0, ambient_dimension))
    while points.shape[0] < sample_size:
        new_sample_size = sample_size-points.shape[0]
        new_points = np.random.random_sample(size=(new_sample_size, ambient_dimension)) * 2 - 1
        norms      = np.linalg.norm(new_points, axis=1)
        selection  = norms > 0.1
        points     = np.vstack((points, new_points[selection,:] / norms[selection, None]))
        points     = np.vstack([np.array([abs(pt[0]), pt[1]]) for pt in points])
    noise = np.sqrt(np.random.chisquare(4, sample_size)) * vertical_noise
    points = points + noise[:, None] *points
    return points

def torus(num_points, major_radius, minor_radius, vertical_noise=0):
    '''Generates a circle with a chisquare vertical noise'''
    theta = 2 * np.pi * np.random.rand(num_points)
    phi = 2 * np.pi * np.random.rand(num_points)

    x = (major_radius + minor_radius * np.cos(phi)) * np.cos(theta)
    y = (major_radius + minor_radius * np.cos(phi)) * np.sin(theta)
    z = minor_radius * np.sin(phi)

    points = np.array([x,y,z]).transpose()
    noise = np.sqrt(np.random.chisquare(4, num_points)) * vertical_noise
    points = points + noise[:, None] *points
    return points

# === Density ===

def ball_density(pts, r):
    distance_matrix  = np.linalg.norm(pts[:,None,:] - pts[None,:,:], axis=-1)
    return np.count_nonzero(distance_matrix <= r, axis=1)

# === Binary matric ===

def binary_matrix(distance_matrix, grades, filename):
    '''Writes a binary file with the distance matrix and grades''' 
    with open(filename, 'wb') as file:
        n = distance_matrix.shape[0]
        b = file.write(
            struct.pack(
                f'II{n + n*(n+1)//2}d',
                0, n, *(grades), *distance_matrix[np.triu_indices(n)]
            )
        )
        print(b, "bytes written to", filename)

# === Generations ===
# ====== Circle ======

print("Circle")

np.random.seed(3)

p = circle(100, vertical_noise= 0.2)
ftp.print_points(p, ball_density(p,0.5), "./tests/circle/circle.png")
binary_matrix(np.linalg.norm(p[:,None,:] - p[None,:,:], axis=-1), ball_density(p,0.5), f'./tests/circle/circle.bin')

# ====== Torus ======

print("Torus")

np.random.seed(3)
p = torus(500, major_radius= 0.7, minor_radius= 0.3, vertical_noise= 0.2)
ftp.print_points(p, ball_density(p,0.15), "./tests/torus/torus.png")
binary_matrix(np.linalg.norm(p[:,None,:] - p[None,:,:], axis=-1), ball_density(p,0.15), f'./tests/torus/torus.bin')

# ====== Dragon ======

print("Dragon")

np.random.seed(3)
p = np.loadtxt("./tests/dragon/dragon.txt")
ftp.print_points(p, ball_density(p,0.02), "./tests/dragon/dragon.png")
binary_matrix(np.linalg.norm(p[:,None,:] - p[None,:,:], axis=-1), ball_density(p,0.02), f'./tests/dragon/dragon.bin')
