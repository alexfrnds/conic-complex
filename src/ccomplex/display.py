import numpy as np
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import ccomplex.projbar as pb

#========================================================
# Display API for the projected barcode
#========================================================

def display(bd, pbt_enabled = False, infinite_bar = False, verbose = False):
    """
    Display the persistence diagram with a slider allowing the choice of a projection.
    :rtype: None
    """
    
    # Computes persistence pairs
    if pbt_enabled: 
        pbt = pb.compute_pbt(bd, infinite_bar= infinite_bar, verbose = verbose)
        pb_0, pb_1 = pb.pb_pp(bd, [0.5, 0.5], pbt= pbt)
    else : 
        pb_0, pb_1 = pb.pb_pp(bd, [0.5, 0.5], infinite_bar = infinite_bar)

    pb0_noinf = np.array([x for x in pb_0 if x[1] != np.inf])
    pb1_noinf = np.array([x for x in pb_1 if x[1] != np.inf])

    if len(pb0_noinf) != 0 : d0 =[pb_0.transpose()[0], pb0_noinf.transpose()[1]]
    else : d0 = [pb_0.transpose()[0], [1]]
    
    if len(pb1_noinf) != 0 : d1 =[pb_1.transpose()[0], pb1_noinf.transpose()[1]]
    elif len(pb_1) == 0 : d1 = []
    else : d1 = [pb_1.transpose()[0], [1]]

    fig, ax = plt.subplots()

    # Handle xlim/ylim
    if len(d1) != 0 :
        xm = np.min(np.concatenate((d0[0],d1[0]))) - max(0.2 * abs(np.min(np.concatenate((d0[0],d1[0]))) - np.max(np.concatenate((d0[0],d1[0])))), 0.1)
        xM = np.max(np.concatenate((d0[0],d1[0]))) + max(0.2 * abs(np.min(np.concatenate((d0[0],d1[0]))) - np.max(np.concatenate((d0[0],d1[0])))), 0.1)
        ym = np.min(np.concatenate((d0[1],d1[1]))) - max(0.2 * abs(np.min(np.concatenate((d0[1],d1[1]))) - np.max(np.concatenate((d0[1],d1[1])))), 0.1)
        yM = np.max(np.concatenate((d0[1],d1[1]))) + max(0.2 * abs(np.min(np.concatenate((d0[1],d1[1]))) - np.max(np.concatenate((d0[1],d1[1])))), 0.1)
    else :
        xm = np.min(d0[0]) - max(0.2 * abs(np.min(d0[0]) - np.max(d0[0])), 0.1)
        xM = np.max(d0[0]) + max(0.2 * abs(np.min(d0[0]) - np.max(d0[0])), 0.1)
        ym = np.min(d0[1]) - max(0.2 * abs(np.min(d0[1]) - np.max(d0[1])), 0.1)
        yM = np.max(d0[1]) + max(0.2 * abs(np.min(d0[1]) - np.max(d0[1])), 0.1)
    m = min(xm,ym)
    M = max(xM,yM)
    old_M = M
    M = M + 0.08 * abs(M - m)
    ax.set_xlim(m,M)
    ax.set_ylim(m,M)

    #Handle infinite bars
    if len(pb_0) != len(pb0_noinf):
        pb0_inf = np.array([[x[0], old_M] for x in pb_0 if x[1] == np.inf])
        if len(pb0_noinf) != 0 : d0 = np.concatenate((pb0_noinf.transpose(), pb0_inf.transpose()), axis = 1)
        else : d0 = pb0_inf.transpose()

    if len(pb_1) != len(pb1_noinf): 
        pb1_inf = np.array([[x[0], old_M] for x in pb_1 if x[1] == np.inf])
        if len(pb1_noinf) != 0 : d1 = np.concatenate((pb1_noinf.transpose(), pb1_inf.transpose()), axis = 1)
        else : d1 = pb1_inf.transpose()

    poly = plt.Polygon([[m,m],[M,m], [M, M]], color = ".4")
    tr = ax.add_patch(poly)

    #Infinite bars display
    if infinite_bar :
        ticks = np.linspace(m, M, 7, endpoint = False)
        ticksv = [round(x,1) for x in ticks if m < round(x,1) < M * 0.9]
        ticksl = [str(x) for x in ticksv] + [r'$ \infty $']
        ticksv = ticksv + [old_M]
        ax.set_yticks(ticksv, labels = ticksl)

    line_0 = ax.scatter(d0[0],d0[1], c = 'royalblue', label = 'H0', marker = 'D', s = 15)
    if len(d1) != 0 : line_1 = ax.scatter(d1[0],d1[1], c = 'firebrick', label = 'H1', marker = 'D', s = 15)

    plt.legend(loc = 'lower right')
    fig.subplots_adjust(bottom=0.25)
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.03])
    slider = Slider(ax = axes, label= "", valmin = 0, valmax= 1)

    def update(val):
        L = slider.val
        direction = [L,1-L] 

        # Computes persistence pairs
        if pbt_enabled: pb_0, pb_1 = pb.pb_pp(bd, direction, pbt)
        else : pb_0, pb_1 = pb.pb_pp(bd, direction, infinite_bar = infinite_bar)

        pb0_noinf = np.array([x for x in pb_0 if x[1] != np.inf])
        pb1_noinf = np.array([x for x in pb_1 if x[1] != np.inf])

        if len(pb0_noinf) != 0 : d0 =[pb_0.transpose()[0], pb0_noinf.transpose()[1]]
        else : d0 = [pb_0.transpose()[0], [1]]
        if len(pb1_noinf) != 0 : d1 =[pb_1.transpose()[0], pb1_noinf.transpose()[1]]
        elif len(pb_1) == 0 : d1 = []
        else : d1 = [pb_1.transpose()[0], [1]]

        
        # Handle xlim/ylim
        if len(d1) != 0 :
            xm = np.min(np.concatenate((d0[0],d1[0]))) - max(0.2 * abs(np.min(np.concatenate((d0[0],d1[0]))) - np.max(np.concatenate((d0[0],d1[0])))), 0.1)
            xM = np.max(np.concatenate((d0[0],d1[0]))) + max(0.2 * abs(np.min(np.concatenate((d0[0],d1[0]))) - np.max(np.concatenate((d0[0],d1[0])))), 0.1)
            ym = np.min(np.concatenate((d0[1],d1[1]))) - max(0.2 * abs(np.min(np.concatenate((d0[1],d1[1]))) - np.max(np.concatenate((d0[1],d1[1])))), 0.1)
            yM = np.max(np.concatenate((d0[1],d1[1]))) + max(0.2 * abs(np.min(np.concatenate((d0[1],d1[1]))) - np.max(np.concatenate((d0[1],d1[1])))), 0.1)
        else :
            xm = np.min(d0[0]) - max(0.2 * abs(np.min(d0[0])-np.max(d0[0])), 0.1)
            xM = np.max(d0[0]) + max(0.2 * abs(np.min(d0[0])-np.max(d0[0])), 0.1)
            ym = np.min(d0[1]) - max(0.2 * abs(np.min(d0[1])-np.max(d0[1])), 0.1)
            yM = np.max(d0[1]) + max(0.2 * abs(np.min(d0[1])-np.max(d0[1])), 0.1)

        m = min(xm,ym)
        M = max(xM,yM)
        old_M = M
        M = M + 0.08 * abs(M - m) 
        ax.set_xlim(m,M)
        ax.set_ylim(m,M)

        #Handle infinite bars
        if len(pb_0) != len(pb0_noinf):
            pb0_inf = np.array([[x[0], old_M] for x in pb_0 if x[1] == np.inf])
            if len(pb0_noinf) != 0 : 
                d0 = np.concatenate((pb0_noinf.transpose(), pb0_inf.transpose()), axis = 1)
            else : 
                d0 = pb0_inf.transpose()
        
        if len(pb_1) != len(pb1_noinf):
            pb1_inf = np.array([[x[0], old_M] for x in pb_1 if x[1] == np.inf])
            if len(pb1_noinf) != 0: 
                d1 = np.concatenate((pb1_noinf.transpose(), pb1_inf.transpose()), axis = 1)
            else :
                d1 = pb1_inf.transpose()

        tr.set_xy([[m,m],[M,m], [M, M]])
        line_0.set_offsets(np.column_stack((d0[0], d0[1])))
        if len(d1) != 0 : line_1.set_offsets(np.column_stack((d1[0], d1[1])))

        fig.canvas.draw_idle()

        #Infinite bars display
        if infinite_bar : 
            ticks = np.linspace(m, M, 7, endpoint = False)
            ticksv = list(np.unique([round(x,1) for x in ticks if m < round(x,1) < old_M * 0.9]))
            ticksl = [str(x) for x in ticksv] + [r'$ \infty $']
            ticksv = ticksv + [old_M]
            ax.set_yticks(ticksv, labels = ticksl)

    slider.on_changed(update)
    plt.show()