import ccomplex.parser_scc2020 as pscc
import ccomplex.display as dp

#========================================================
# Testfile for display with "./tests/" samples
#========================================================

SHAPE = "torus"                  #[circle, octogone, torus]
HOMOLOGY_DEGREE = 1

#========================================================

path = f"tests/{SHAPE}/{SHAPE}_H{HOMOLOGY_DEGREE}.scc2020"
bd = pscc.bdf_from_scc2020(path) 

dp.display(bd, pbt_enabled= True, infinite_bar= False, verbose= True)