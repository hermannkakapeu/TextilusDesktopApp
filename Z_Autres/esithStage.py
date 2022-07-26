import pandas as pd
import numpy as np

#from .fonctions import text_to_pandas
def text_to_pandas(path, etiquette):
  """
  Ctette fonction prend en entrée le chemin du fichier 
  texte contenant les donnee recueillies par SensorControl
  et les retourne sous forme de table Pandas en ajoutant une colonne 
  specifiant le type de tissu. 
  """
  path_text = path
  et = etiquette
  df = pd.read_csv(path_text, sep='\t', header=1)
  del(df['Time'])
  del(df['Date'])
  df = df.drop([0,1], 0)
  df = num(df)
  df = df.assign(type_tissu=et)
  #col = df.columns[0]
  #df.drop(df.loc[df[col] == 'NaN'])
  return df


def num(df):
  a = df.apply(lambda x: x.str.replace(',','.'))
  return a.astype(float)

cot = '/home/hermann/Desktop/Textilus/Textilus/Z_Autres/data/coton.txt'
lai = '/home/hermann/Desktop/Textilus/Textilus/Z_Autres/data/laine.txt'
polya = '/home/hermann/Desktop/Textilus/Textilus/Z_Autres/data/polyamide.txt'
poly = '/home/hermann/Desktop/Textilus/Textilus/Z_Autres/data/polyster.txt'

coton = text_to_pandas(cot, 'Coton')
laine = text_to_pandas(lai, 'Laine')
polyamide = text_to_pandas(polya, 'Polyamide')
polyster = text_to_pandas(poly, 'Polyster')


def stack_data(data1, data2):
  """
  cette fonction prend en entrée deux DataFrames Pandas et renvoie une seule Table
  qui est la superposition verticale de ces deux dernières.
  """
  data = pd.concat([data1, data2], join='inner', ignore_index=True)
  return data



def stack_transpose(stack, num_samples=20):
  stack_transposed = stack.drop(columns=["type_tissu"])
  stack_transposed = stack_transposed.T
  new_columns = []
  categories = ['coton', 'laine', 'polyamide', 'polyster']
  for type_tissu in categories :
    for j in range(num_samples) :
      new_columns.append(f"{type_tissu}{str(j+1)}")
  
  stack_transposed.columns = new_columns
  stack_transposed.index = [i for i in range(1550, 1960, 10)]
  stack_csv = stack_transposed.to_csv()

  return stack_transposed, stack_csv



listedata = [laine, polyamide, polyster]
textile = coton
for i in range(3):
  textile = stack_data(textile, listedata[i])

coll = ['1550', '1560', '1570', '1580', '1590', '1600', '1610', '1620', '1630', '1640', '1650', '1660', '1670', '1680', '1690', '1700', '1710', '1720', '1730', '1740', '1750', '1760', '1770', '1780', '1790', '1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900', '1910', '1920', '1930', '1940', '1950', 'type_tissu']
textile.columns = coll
textileT, textile_csv = stack_transpose(textile, 20)

print(textileT)
import matplotlib.pyplot as plt

def list_plage(data):
  """
  Cette fonction prend en entree un DataFrame pandas contenant les donnees
  et renvoie la liste des longueurs d'onde dans une liste en format float
  ca peut etre utile si on veut trcaer des courbes
  """
  liste = []
  col = []
  for i in data.columns:
    col.append(i)
  for i in col :
    if (col.index(i) != len(col)-1) :
      x = float(i)
      liste.append(x)

  return liste



def list_mesure(data, numLigne):
  """
  Cette fonction prend en entrée un dataFrame pandas et le numéro d'une ligne
  qu'elle renvoie sous forme de liste.
  c'est comme si on renvoie une mésure parmi les autres mesures. Elle sera utile pour des traces de courbes
  mais aussi pour faciliter les predictions.
  """
  liste = []
  liste1 = []
  #iter = data.iloc[numLigne:numLigne+1,:-1].loc[0]
  iter = data.loc[numLigne]
  for i in iter :
    liste.append(i)
  L = liste[:-1]

  return L

#plt.plot(list_plage(textile), list_mesure(textile, 21))
x = list_plage(textile)
print(x)
y = list_mesure(textile, 21)
print(y)

def plot_mesure(data, numLigne):
  """
  Cette fonction prend en entree le DataFrame avec le numéro de ligne de la mésure et renvoie en sortie
  le tracé de la mesure en fonction de la plage de longueur d'onde définie.
  """
  import matplotlib.pyplot as plt

  plage = list_plage(data)
  mesure = list_mesure(data, numLigne)

  plt.axes()
  plot = plt.plot(plage, mesure)
  #plt.plot(plage, mesure)
  plt.xlim([1550, 1900])
  plt.ylim([min(mesure), max(mesure)])
  plt.yticks(np.arange(min(mesure), max(mesure), 0.01))
  plt.xticks(np.arange(1550, 1900, 10))
  plt.show()
  return plot


plot_mesure(textile, 21)
