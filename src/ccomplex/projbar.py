import numpy as np
import phat
from tqdm import tqdm

def proj_sorted(boundary,direction):
    """Computes the (gamma-linear) projected barcode along the provided direction
        from a boundary matrix in bdf format
    :param boundary: boundary matrix in bdf
    :type boundary: list (bdf)
    :param direction: direction along which the projected barcode is computed
    :type direction: array
    :returns: projected barcode in bdf format, convertion table new -> old
    :rtype: list bdf, dict, dict
    """    
    projected_bd = [ [boundary[i][0], np.dot(boundary[i][1],direction) , boundary[i][2], i] 
                    for i in range(len(boundary)) ]
    sorted_bd = sorted(projected_bd, key=lambda item: (item[1], -item[0]))
    convertion_table = {i : sorted_bd[i][-1] for i in range(len(sorted_bd))}

    # Update boundaries index
    temp_reverse_table = {sorted_bd[i][-1] : i for i in range(len(sorted_bd))}
    sorted_bd = [line[:-2] + [[temp_reverse_table[y] for y in line[2]]] for line in sorted_bd]
    
    return sorted_bd, convertion_table

def phat_from_bdf(boundary):
    """Format a bdf boundary matrix and apply phat
    :param boundary: boundary matrix in bdf
    :type boundary: list
    :returns: array of persistence pairs
    :rtype: array
    """    
    phat_bd = phat.boundary_matrix(representation = phat.representations.vector_vector)
    phat_bd.columns = [(-x[0], sorted(x[2])) for x in boundary]
    phat_pairs = phat_bd.compute_persistence_pairs()
    return phat_pairs

def pb_perspairs(boundary, direction, infinite_bar = False, reverse_convert = False):
    """Computes the projected barcode persistence pairs along the provided direction
        from a boundary matrix in bdf format
    :param boundary: boundary matrix in bdf
    :type boundary: list
    :param direction: direction along which the projected barcode is computed
    :type direction: array
    :param infinite_bar: add infinite bars to persistence pairs 
    :type infinite_bar: boolean
    :param infinite_bar: yield the projected barcode with original boundary index 
    :type infinite_bar: boolean
    :returns: array of projected barcode
    :rtype: array
    """
    proj_bd, conversion_table = proj_sorted(boundary, direction)
    phat_pairs = phat_from_bdf(proj_bd)

    bar_unproj_0 = np.array([np.array(pair) for pair in phat_pairs 
                             if proj_bd[pair[1]][0] == -1])
    bar_unproj_1 = np.array([np.array(pair) for pair in phat_pairs 
                             if proj_bd[pair[1]][0] == -2])
    
    # Add infinite bar
    if infinite_bar :
        inf_ind_0 = [i for i in range(len(boundary)) 
                     if (boundary[i][0] == 0) 
                     and ((len(bar_unproj_0) == 0) or (i not in bar_unproj_0[:,0]))]
        inf_ind_1 = [i for i in range(len(boundary)) 
                     if (boundary[i][0] == -1) 
                     and ((len(bar_unproj_1) == 0) or (i not in bar_unproj_1[:,0])) 
                     and ((len(bar_unproj_0) == 0) or (i not in bar_unproj_0[:,1]))]

        # index -1 correspond to +infty 
        if len(inf_ind_0) == 0 : bar0 = bar_unproj_0
        elif len(bar_unproj_0) == 0: bar0 = np.array([np.array([i, -1]) for i in inf_ind_0])
        else : bar0 = np.concatenate([bar_unproj_0 , np.array([np.array([i, -1]) for i in inf_ind_0])])

        if len(inf_ind_1) == 0 : bar1 = bar_unproj_1
        elif len(bar_unproj_1) == 0: bar1 = np.array([np.array([i, -1]) for i in inf_ind_1])
        else : bar1 = np.concatenate([bar_unproj_1 , np.array([np.array([i, -1]) for i in inf_ind_1])])
    else :
        bar0, bar1 = bar_unproj_0, bar_unproj_1
   
    # Reverse convert it with the original bd index
    if reverse_convert :
        def convert(pair):
            if pair[1] == -1:
                return np.array([conversion_table[pair[0]],-1])
            else :
                return np.array([conversion_table[pair[0]],conversion_table[pair[1]]])

        bar0 = np.apply_along_axis(convert, 1, bar0)
        if len(bar1) != 0 : bar1 = np.apply_along_axis(convert, 1, bar1)
    #Use the projected generators
    else :
        def convert(pair):
            if pair[1] == -1:
                return np.array([proj_bd[int(pair[0])][1], np.inf])
            else :
                return np.array([proj_bd[int(pair[0])][1], proj_bd[int(pair[1])][1]])

        bar0 = np.apply_along_axis(convert, 1, bar0)
        if len(bar1) != 0 : bar1 = np.apply_along_axis(convert, 1, bar1)

    return bar0, bar1

def stratification(boundary):
    """Computes the (projected) stratification along the y-axis as a sorted list of boundary points
    :param boundary: boundary matrix in bdf
    :type boundary: list (bdf)
    :returns: sorted list of boundary points
    :rtype: list (sorted)
    """ 
    gen = np.array([np.array(x[1]) for x in boundary])
    stratif = set()
    for i in range(len(gen)):
        for j in range(i+1,len(gen)):
            g = gen[i] - gen[j]
            if g[0]*g[1] < 0:
                if g[0] > 0: h = np.array([-g[1],g[0]])
                if g[0] < 0: h = np.array([g[1],-g[0]])
                ph = h[1]/(h[0]+h[1]) 
                stratif.add(ph)
    
    return sorted(list(stratif))

def compute_pbt(boundary, strat = None, infinite_bar = False, verbose = False):
    """Computes the projected barcode template
    :param boundary: boundary matrix in bdf
    :type boundary: list (bdf)
    :param strat: stratification 
    :type strat: list
    :returns: projected barcode template (stratif, bars)
    :rtype: tuple of (list, list)
    """     
    
    # Extremal stratification sizes
    if strat == None : strat = stratification(boundary)
    if len(strat) == 0:
        return pb_perspairs(boundary,[.5,.5],infinite_bar= infinite_bar, reverse_convert= True)

    # Compute PBT per stratification
    pairs = []
    pairs.append(pb_perspairs(boundary,[1 - np.mean([0,strat[0]]), np.mean([0,strat[0]])],
                              infinite_bar= infinite_bar, reverse_convert= True))
    
    if len(strat) > 1:
        if verbose :
            print("Computing PBT")
            for i in tqdm(range(len(strat)-1)):
                pairs.append(pb_perspairs(boundary,[1 - np.mean([strat[i],strat[i+1]]), np.mean([strat[i],strat[i+1]])],
                              infinite_bar= infinite_bar, reverse_convert= True)) 
        else :
            for i in range(len(strat)-1):
                pairs.append(pb_perspairs(boundary,[1 - np.mean([strat[i],strat[i+1]]), np.mean([strat[i],strat[i+1]])],
                              infinite_bar= infinite_bar, reverse_convert= True))

    pairs.append(pb_perspairs(boundary,[1 - np.mean([1,strat[-1]]), np.mean([1,strat[-1]])],
                              infinite_bar= infinite_bar, reverse_convert= True))

    return (strat, pairs)

def pb_pp(boundary, direction, pbt = None, infinite_bar = False):
    """Computes the projected barcode persistence pairs along [direction]
    :param boundary: boundary matrix in bdf
    :type boundary: list (bdf)
    :param direction: projection direction
    :type direction: list
    :param pbt: projected barcode template
    :type pbt: list
    :returns: projected barcode persistence pairs
    :rtype: list
    """ 

    if pbt == None : 
        return pb_perspairs(boundary, direction, infinite_bar= infinite_bar)
        
    stratification = pbt[0]

    # One point localisation
    if len(stratification) != 0:    
        def bsi(arr, q):
            low, high = 0, len(arr) - 1
            result_index = -1
            while low <= high:
                mid = (low + high) // 2
                if arr[mid] <= q:
                    result_index = mid
                    low = mid + 1
                else:
                    high = mid - 1
            return result_index

        index = bsi(stratification, direction[1]) + 1
    else : index = 0

    # Projection from PBT
    pairs_0 = pbt[1][index][0]
    pairs_1 = pbt[1][index][1]
    def convert(pair):
            if pair[1] == -1:
                return np.array([np.dot(boundary[int(pair[0])][1], direction), np.inf])
            else :
                return np.array([np.dot(boundary[int(pair[0])][1], direction), 
                                 np.dot(boundary[int(pair[1])][1], direction)])

    if len(pairs_0) != 0 : bars_0 = np.apply_along_axis(convert, 1, pairs_0)
    else : bars_0 = []
    if len(pairs_1) != 0 : bars_1 = np.apply_along_axis(convert, 1, pairs_1)
    else : bars_1 = []

    return np.array(bars_0), np.array(bars_1)
    
def pb_bdf(boundary, direction):
    """Computes the (gamma-linear) projected barcode along the provided direction 
    :param boundary: boundary matrix in bdf
    :type boundary: list (bdf)
    :param direction: direction along which the projected barcode is computed
    :type direction: array
    :returns: projected barcode 
    :rtype: list bdf
    """ 
    return proj_sorted(boundary, direction)[0]