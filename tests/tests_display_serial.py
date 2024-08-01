import ccomplex.parser_scc2020 as pscc
import ccomplex.display as dp

#========================================================
# Testfile for display with "./tests/" samples
#========================================================


SHAPE = "circle"
for hom_deg in [0,1]:
    path = f"tests/{SHAPE}/{SHAPE}_H{hom_deg}.scc2020"
    bd = pscc.bdf_from_scc2020(path)
    for ib in [False, True]:
        print(SHAPE, hom_deg, ib) 
        dp.display(bd, pbt_enabled= True, infinite_bar= ib, verbose= True)
        dp.display(bd, pbt_enabled= False, infinite_bar= ib, verbose= True)

SHAPE = "octogone"
for hom_deg in [0,1]:
    path = f"tests/{SHAPE}/{SHAPE}_H{hom_deg}.scc2020"
    bd = pscc.bdf_from_scc2020(path)
    for ib in [False, True]:
        print(SHAPE, hom_deg, ib) 
        dp.display(bd, pbt_enabled= True, infinite_bar= ib, verbose= True)
        dp.display(bd, pbt_enabled= False, infinite_bar= ib, verbose= True)

SHAPE = "torus"
for hom_deg in [0,1,2]:
    path = f"tests/{SHAPE}/{SHAPE}_H{hom_deg}.scc2020"
    bd = pscc.bdf_from_scc2020(path)
    for ib in [False, True]:
        print(SHAPE, hom_deg, ib)
        dp.display(bd, pbt_enabled= True, infinite_bar= ib, verbose= True)
        dp.display(bd, pbt_enabled= False, infinite_bar= ib, verbose= True)