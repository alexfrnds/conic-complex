import ccomplex.projbar as pb
import ccomplex.parser_scc2020 as pscc

import pandas as pd
from time import time

#========================================================
# Experiment
#========================================================

# === Scenarios === 

Name = []
Homology_degree = []
Nb_generators = []
Nb_cells = []
Time_wPBT = []
Time_woPBT = []
Time_PBT = []

# ====== Circle ======
print("Circle")

# Loading SCC2020
bd_H0 = pscc.bdf_from_scc2020("./tests/circle/circle_H0.scc2020")
bd_H1 = pscc.bdf_from_scc2020("./tests/circle/circle_H1.scc2020")

## H0 
begin_pp_nopbt = time()
pb.pb_pp(bd_H0, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H0 = pb.compute_pbt(bd_H0)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H0, [0.9,0.1], pbt_H0)
end_pp_pbt = time()

Name.append("Circle")
Homology_degree.append("0")
Nb_generators.append(len(bd_H0))
Nb_cells.append(len(pbt_H0[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

## H1
begin_pp_nopbt = time()
pb.pb_pp(bd_H1, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H1 = pb.compute_pbt(bd_H1)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H1, [0.9,0.1], pbt_H1)
end_pp_pbt = time()

Name.append("Circle")
Homology_degree.append("1")
Nb_generators.append(len(bd_H1))
Nb_cells.append(len(pbt_H1[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)


# ====== Torus ======

print("Torus")

# Loading SCC2020
bd_H0 = pscc.bdf_from_scc2020("./tests/torus/torus_H0.scc2020")
bd_H1 = pscc.bdf_from_scc2020("./tests/torus/torus_H1.scc2020")
bd_H2 = pscc.bdf_from_scc2020("./tests/torus/torus_H2.scc2020")

## H0 
begin_pp_nopbt = time()
pb.pb_pp(bd_H0, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H0 = pb.compute_pbt(bd_H0)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H0, [0.9,0.1], pbt_H0)
end_pp_pbt = time()

Name.append("Torus")
Homology_degree.append("0")
Nb_generators.append(len(bd_H0))
Nb_cells.append(len(pbt_H0[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

## H1
begin_pp_nopbt = time()
pb.pb_pp(bd_H1, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H1 = pb.compute_pbt(bd_H1)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H1, [0.9,0.1], pbt_H1)
end_pp_pbt = time()

Name.append("Torus")
Homology_degree.append("1")
Nb_generators.append(len(bd_H1))
Nb_cells.append(len(pbt_H1[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

## H2
begin_pp_nopbt = time()
pb.pb_pp(bd_H2, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H2 = pb.compute_pbt(bd_H2)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H2, [0.9,0.1], pbt_H2)
end_pp_pbt = time()

Name.append("Torus")
Homology_degree.append("2")
Nb_generators.append(len(bd_H2))
Nb_cells.append(len(pbt_H2[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

# ====== Octogone ======
print("Octogone")

# Free resolutions
bd_H0 = pscc.bdf_from_scc2020("./tests/octogone/octogone_H0.scc2020")
bd_H1 = pscc.bdf_from_scc2020("./tests/octogone/octogone_H1.scc2020")

## H0 
begin_pp_nopbt = time()
pb.pb_pp(bd_H0, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H0 = pb.compute_pbt(bd_H0)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H0, [0.9,0.1], pbt_H0)
end_pp_pbt = time()

Name.append("Octogone")
Homology_degree.append("0")
Nb_generators.append(len(bd_H0))
Nb_cells.append(len(pbt_H0[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

## H1
begin_pp_nopbt = time()
pb.pb_pp(bd_H1, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H1 = pb.compute_pbt(bd_H1)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H1, [0.9,0.1], pbt_H1)
end_pp_pbt = time()

Name.append("Octogone")
Homology_degree.append("1")
Nb_generators.append(len(bd_H1))
Nb_cells.append(len(pbt_H1[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

# ====== Dragon ======
print("Dragon")

# Loading SCC2020
bd_H0 = pscc.bdf_from_scc2020("./tests/dragon/dragon_H0.scc2020")
bd_H1 = pscc.bdf_from_scc2020("./tests/dragon/dragon_H1.scc2020")
bd_H2 = pscc.bdf_from_scc2020("./tests/dragon/dragon_H2.scc2020")

## H0 
begin_pp_nopbt = time()
pb.pb_pp(bd_H0, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H0 = pb.compute_pbt(bd_H0)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H0, [0.9,0.1], pbt_H0)
end_pp_pbt = time()

Name.append("Dragon")
Homology_degree.append("0")
Nb_generators.append(len(bd_H0))
Nb_cells.append(len(pbt_H0[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

## H1
begin_pp_nopbt = time()
pb.pb_pp(bd_H1, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H1 = pb.compute_pbt(bd_H1)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H1, [0.9,0.1], pbt_H1)
end_pp_pbt = time()

Name.append("Dragon")
Homology_degree.append("1")
Nb_generators.append(len(bd_H1))
Nb_cells.append(len(pbt_H1[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

## H1
begin_pp_nopbt = time()
pb.pb_pp(bd_H2, [0.9,0.1])
end_pp_nopbt = time()

begin_pbt = time()
pbt_H2 = pb.compute_pbt(bd_H2)
end_pbt = time()

begin_pp_pbt = time()
pb.pb_pp(bd_H2, [0.9,0.1], pbt_H2)
end_pp_pbt = time()

Name.append("Dragon")
Homology_degree.append("2")
Nb_generators.append(len(bd_H2))
Nb_cells.append(len(pbt_H2[0]))
Time_wPBT.append(end_pp_pbt - begin_pp_pbt)
Time_woPBT.append(end_pp_nopbt - begin_pp_nopbt)
Time_PBT.append(end_pbt - begin_pbt)

results = pd.DataFrame({"Name" : Name, "Homology degree" : Homology_degree,
                         "Nb Generators": Nb_generators, "Nb Cells": Nb_cells, 
                         "Time (wPBT)" : Time_wPBT, "Time (woPBT)" : Time_woPBT,
                         "Time PBT" : Time_PBT})

results.to_csv("./tests/results.csv", index = False)