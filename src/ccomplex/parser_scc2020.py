def bdf_from_scc2020(path):
    """Read a file written with scc2020 format and convert it to bdf
    :param path: path to scc2020 file
    :type path: path
    :rtype: list (bdf)
    """ 
    # Read file and delete the non-essential features (comments...)
    f = open(path)
    lines = f.readlines()
    f.close()
    striped_output = [line for line in lines if line[0] != '#' and line != "\n" ]

    #Convert to proper types
    dim = [int(x) for x in striped_output[2].split()]
    blocs = []
    start = 3
    for d in dim[:-1]:
        prebloc = [s.split(";") for s in striped_output[start:start+d]] 
        bloc = [[[float(x) for x in tile.split()] for tile in line] for line in prebloc]
        blocs.append(bloc)
        start = start + d

    zero_grades = []
    for grade in [s.split(";") for s in striped_output[start:]]:
        zero_grades.append([float(grade[0].split()[0]), float(grade[0].split()[1])])


    #Format to bdf
    dim.reverse()
    bd = [[0, tuple(g), []] for g in zero_grades]
    for i in range(1,len(blocs)+1) :
        bd += [[-i, tuple(line[0]), [int(x + sum(dim[:i-1])) for x in line[1]]] for line in blocs[-i]] 
    
    return bd

def scc2020_from_bdf(boundary, path):
    """Write a file in scc2020 format from a bdf input (2 parameter only)
    :param boundary: boundary matrix in bdf
    :type boundary: list
    :param path: path of the file to write
    :type path: path
    """ 
    lbloc = []
    mbloc = []
    rbloc = []

    for l in boundary:
        if l[0] == 0 :
            rbloc.append(str(l[1][0]) + " " + str(l[1][1]))

        if l[0] == -1:
            cln = ""
            for x in l[2]: cln = cln + str(x) + " "
            mbloc.append(str(l[1][0]) + " " + str(l[1][1]) + " ; " + cln)
    
    for l in boundary:
        if l[0] == -2:
            cln = ""
            for x in l[2]: cln = cln + str(x - len(rbloc)) + " "
            lbloc.append(str(l[1][0]) + " " + str(l[1][1]) + " ; " + cln)

    f = open(path, 'w')
    f.write("scc2020\n2\n" + str(len(lbloc)) + " " + str(len(mbloc)) + " " + str(len(rbloc)) + "\n\n")
    for x in lbloc : f.write(x + "\n")
    f.write("\n")
    for x in mbloc : f.write(x + "\n")
    f.write("\n")
    for x in rbloc : f.write(x + "\n")
    f.close()

