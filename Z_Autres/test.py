'''import sys
sys.path.append("/home/hermann/Desktop/Textilus/Textilus/Z_Autres/txt")
import txt as i

for j in i.data.columns:
    print(type(j))'''







'''import pandas as pd

# my_data = pd.read_csv("my_input_file.csv")
columns = ['a','b']
my_data = pd.DataFrame([[1, 2], [3, 4]], columns=columns)


## connect to database
import sqlite3

conn = sqlite3.connect('/home/hermann/Desktop/Textilus/Textilus/db.sqlite3')

##push the dataframe to sql 
my_data.to_sql("my_data", conn, if_exists="replace")

##create the table

conn.execute(
    """
    create table my_table as 
    select * from my_data
    """)'''

liste = []
for i in range(1550, 1910, 10):
    liste.append(str(i))

print(liste)