import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from fonctions import text_to_pandas
from fonctions import stack_data
from fonctions import stack_transpose
from fonctions import plot_mesure
from fonctions import num
from fonctions import les_infos
from fonctions import list_plage
from fonctions import list_mesure
from fonctions import list_mesure1
from fonctions import plot_list
from fonctions import numeric_X
from fonctions import split_data





#IMPORTATION DE LA DATA

cot = '/home/hermann/Desktop/Textilus/Textilus/Z_Autres/data/coton.txt'
lai = '/home/hermann/Desktop/Textilus/Textilus/Z_Autres/data/laine.txt'
polya = '/home/hermann/Desktop/Textilus/Textilus/Z_Autres/data/polyamide.txt'
poly = '/home/hermann/Desktop/Textilus/Textilus/Z_Autres/data/polyster.txt'

coton = text_to_pandas(cot, 'Coton')
laine = text_to_pandas(lai, 'Laine')
polyamide = text_to_pandas(polya, 'Polyamide')
polyster = text_to_pandas(poly, 'Polyster')

listedata = [laine, polyamide, polyster]
textile = coton
for i in range(3):
  textile = stack_data(textile, listedata[i])

coll = [i for i in range(1550, 1960, 10)]
coll.append('type_tissu')
textile.columns = coll
textileT, textile_csv = stack_transpose(textile, 20)


#
plot_mesure(textile, 50)
varr = plt.gcf()
print(varr)








