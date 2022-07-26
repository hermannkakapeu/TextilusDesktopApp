def text_to_pandas(path, etiquette):
  import pandas as pd
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
  df = df.drop([0, 1], 0)
  df = num(df)
  df = df.assign(type_tissu=et)
  #col = df.columns[0]
  #df.drop(df.loc[df[col] == 'NaN'])
  return df



def num(df):
  a = df.apply(lambda x: x.str.replace(',','.'))
  return a.astype(float)



def stack_data(data1, data2):
  import pandas as pd
  """
  cette fonction prend en entrée deux DataFrames Pandas et renvoie une seule Table
  qui est la superposition verticale de ces deux dernières.
  """
  data = pd.concat([data1, data2], join = 'inner', ignore_index = True)
  return data


def les_infos(data):
  """
  Cette fonction prend en entrée un DataFrame pandas et renvoie
  des informations specifiques et utiles à notre études sur le datset. 
  """
  a1 = data.columns[1]
  b1 = a1.replace(',', '.')
  c1 = float(b1)
  a2 = data.columns[2]
  b2 = a2.replace(',', '.')
  c2 = float(b2)
  pas = c2 - c1

  first = float(data.columns[0].replace(',', '.'))
  last = float(data.columns[-2].replace(',', '.'))

  numMesure = data.shape[0]
  numWL = data.shape[1]-1



  print('************INFOS SUR CE DATA**************')
  print('')
  print('')
  print(f"plage de longueur d'onde : [{first} - {last}]\nPas d'incrementation : {pas}\nNombre de Mesures : {numMesure}\nNombre de longueurs d'onde : {numWL}")
  


def list_plage(data):
  """
  Cette fonction prend en entree un DataFrame pandas contenant les donnees
  et renvoie la liste des longueurs d'onde dans une liste en format float
  ca peut etre utile si on veut trcaer des courbes
  """
  liste1 = []
  liste2 = []
  col = []
  for i in data.columns[:-1]:
    col.append(i)
  for i in col:
    if (type(i)==str):
      x = float(i.replace(',', '.'))
      liste1.append(x)
      return liste1
    else:

      return col



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



def list_mesure1(data, numLigne):
  """
  Cette fonction prend en entrée un dataFrame pandas et le numéro d'une ligne 
  qu'elle renvoie sous forme de liste.
  c'est comme si on renvoie une mésure parmi les autres mesures. Elle sera utile pour des traces de courbes
  mais aussi pour faciliter les predictions. 
  """
  liste = []
  liste1 = []
  iter = data.loc[numLigne]
  for i in iter :
    liste.append(i)
  L = liste
  #for i in L :
      #x = float(i.replace(',', '.'))
      #liste1.append(x)
  return L


def plot_mesure(data, numLigne):
  """
  Cette fonction prend en entree le DataFrame avec le numéro de ligne de la mésure et renvoie en sortie
  le tracé de la mesure en fonction de la plage de longueur d'onde définie.
  """
  import matplotlib.pyplot as plt
  import numpy as np
  plage = list_plage(data)
  mesure = list_mesure(data, numLigne)

  plt.axes()
  plot = plt.plot(plage, mesure)
  #plt.plot(plage, mesure)
  plt.xlim([1550, 1900])
  plt.ylim([min(mesure), max(mesure)])
  plt.yticks(np.arange(min(mesure), max(mesure), 0.01))
  plt.xticks(np.arange(1550, 1900, 10))
  plt.savefig(f'./{numLigne}.png')
  #return plot

#plage = list_plage(montel)
#mesure7 = list_mesure(carton2, 5)

#plt.plot(plage, mesure7)

def plot_list(data, listMesure):
  """
  Cette fonction prend en entree le DataFrame avec le numéro de ligne de la mésure et renvoie en sortie
  le tracé de la mesure en fonction de la plage de longueur d'onde définie.
  """
  import matplotlib.pyplot as plt

  
  plage = list_plage(data)
  #mesure = list_mesure(data, numLigne)

  plt.axes()
  #plot = plt.plot(plage, mesure)
  for i in listMesure :
    plt.subplot()
    mesure = list_mesure(data, i)
    plt.plot(plage, mesure)
    plt.xlim([1550, 1900])
    plt.ylim([min(mesure), max(mesure)])
    plt.yticks(np.arange(min(mesure), max(mesure), 0.01))
    plt.xticks(np.arange(1550, 1900, 30))
    plt.grid(True)
    plt.show()
  #return plot


def numeric_X(X):
  """
  le but de cette fonction est de prendre en entrée les variables X et de retourner
  les valeurs de ce dataframe en numerique. car ils sont en format str au depart.
  """
  liste4 = X.columns
  liste2 = []
  for i in range(X.shape[0]) :
    liste2.append(list_mesure1(X, i))
  X_num = pd.DataFrame(liste2, columns=liste4)

  return X_num




def split_data(stack, pourcentage) :
  """
  cette fonction prend en entree toute notre data et la portion pour le test et
  le divise en deux parties pour ensuite renvoyer le X_train, X_test, y_train et y_test
  """
  X = stack.iloc[:,:-1]
  Y = stack.iloc[:,-1:]
  if pourcentage>=0 or pourcentage<=1 :
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=pourcentage)
  else:
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

  #X_train = num(X_train)
  #X_test = num(X_test)

  return X_train, X_test, y_train, y_test


def stack_transpose(stack, num_samples=20):
  stack_transposed = stack.drop(columns=["type_tissu"])
  stack_transposed = stack_transposed.T
  new_columns = []
  categories = ['coton', 'laine', 'polyamide', 'polyster']
  for type_tissu in categories:
    for j in range(num_samples):
      new_columns.append(f"{type_tissu}{str(j + 1)}")

  stack_transposed.columns = new_columns
  stack_transposed.index = [i for i in range(1550, 1960, 10)]
  stack_csv = stack_transposed.to_csv()

  return stack_transposed, stack_csv
