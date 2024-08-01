from twopac import FunctionRipsComplex
import numpy as np
import matplotlib.pyplot as plt

def fr_Hres(pts,grds, dghom):
    dists  = np.linalg.norm(pts[:,None,:] - pts[None,:,:], axis=-1)
    cpx = FunctionRipsComplex(grds, dists)
    homology = cpx.sfd().Chunk(dghom+1).Homology(dghom)

    # Hacky fix, to allow the use of twopac for all chips
    it_hom = iter(homology)
    n = [0]*(dghom+1)
    for i in range(len(n)):
        n[i] = next(it_hom) 

    m0_rgrd = n[dghom][0].row_grades
    m0_cgrd = n[dghom][0].column_grades
    m0_clm = n[dghom][0].columns

    m1_cgrd = n[dghom][1].column_grades
    m1_clm = n[dghom][1].columns

    bd = []
    for x in m0_rgrd:
        bd.append([0,x,[]])
    for i in range(len(m0_cgrd)):
        bd.append([-1,m0_cgrd[i],m0_clm[i]])
    for i in range(len(m1_cgrd)):
        bd.append([-2,m1_cgrd[i],[x + len(m0_rgrd) for x in m1_clm[i]]])
    
    return bd

def print_points(pts,grds, path = None):
    if len(pts[0]) == 2 : 
        fig, ax = plt.subplots()
        ax.scatter(pts[:, 0],pts[:,1], c = grds)
    if len(pts[0]) == 3 : 
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        plt.scatter(pts[:, 0],pts[:,1], pts[:,2], c = grds)
    if path != None : plt.savefig(path, dpi = 500)
    return None

