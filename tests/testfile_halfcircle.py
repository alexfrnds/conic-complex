import numpy as np
import ccomplex.free_twopac as ftp
from ccomplex.display import display
import matplotlib.pyplot as plt
import ccomplex.parser_scc2020 as pscc

#========================================================
# Generates the half circle test
#========================================================
# Generating functions

np.random.seed(2)

def ball_density(pts, r):
    distance_matrix  = np.linalg.norm(pts[:,None,:] - pts[None,:,:], axis=-1)
    return np.count_nonzero(distance_matrix <= r, axis=1)

def half_sphere(sample_size, ambient_dimension, vertical_noise=0):
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
   

#========================================================
# Points generation
NUMPOINTS_HALF_CIRCLE = 30
NUMPOINTS_CIRCLE = 40

pts_circle = circle(NUMPOINTS_CIRCLE,2,0)
dec = np.array([2,0])
pts_circle = np.array([x + dec for x in pts_circle])

pts = half_sphere(NUMPOINTS_HALF_CIRCLE, 2, 0)

pts_out = np.array([[-0.7,0]])

pts = np.concatenate([pts, pts_out, pts_circle])

dists  = np.linalg.norm(pts[:,None,:] - pts[None,:,:], axis=-1)
grades = ball_density(dists, 1.5)

fig, ax = plt.subplots()
ax.set_xlim(-1.2, 3.5)
ax.set_ylim(-2.25, 2.25)
ax.scatter(pts[:, 0],pts[:,1], c = grades)
plt.savefig("tests/half_circle/halfcircle.png", dpi = 500)

# Analyse

 #if twopac python bindings are not installed comment the following two lines
bd = ftp.fr_Hres(pts,grades, 1)
pscc.scc2020_from_bdf(bd, "tests/half_circle/halfcircle.scc2020")
bd = pscc.bdf_from_scc2020("tests/half_circle/halfcircle.scc2020")
display(bd, pbt_enabled = False)

