
import pandas as  pd
from my_second_assignment.app.helper import create_and_load_table , load_from, remove_apostrophe
from dotenv import load_dotenv
import os
import psycopg2
import sqlite3

load_dotenv()


# Creating the postgresql connection
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# first will get the data of the csv of the titanic

# getting the path for the titanic
TITANIC_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "titanic.csv")
# getting the titanic df
df = pd.read_csv(TITANIC_PATH)

# changing the column name to add apostrophes
# where needed
df["Name"] = df["Name"].apply(remove_apostrophe)

# creating the sqlite3 conncetion
# saving the database but just in memory
connection = sqlite3.connect("titanic.sqlite3")
# will change the titancic df to sql
df.to_sql("titanic", con=connection, if_exists='replace' )

# Will put the sql in to the new table that will be created for it
quer_get_sql_titanic = """
        SELECT *
        FROM titanic
"""
# Creating the cursor with the connection for the sqlite3 
# and then getting the table as a list of tuples
s_cursor = connection.cursor()
s_cursor.execute(quer_get_sql_titanic)
titanic_Table = s_cursor.fetchall()


# Will now work on the loading of the titaninc set

# This is the query that will create the titanic table
quer_titanic_create = """
        CREATE TYPE gender AS ENUM ('male', 'female');
        CREATE TABLE IF NOT EXISTS titanic (
                        id_num        SERIAL PRIMARY KEY,
                        survived INT,	
                        pclass	INT,
                        name VARCHAR(120),
                        sex  gender,
                        age INT,	
                        siblings_spouses_aboard INT,
                        parents_children_aboard	INT,
                        fare float(4) 
                
                );

"""


quer_insert = """
        INSERT INTO titanic 
        (survived, pclass, name,sex, age, siblings_spouses_aboard, parents_children_aboard, fare)
        VALUES 
        
        """




#creating the connection
p_connection = psycopg2.connect(dbname=DB_NAME , password=DB_PASSWORD , user=DB_USER , host=DB_HOST )

# Using the create and the load function 
# to make the table on the postgresql if needed
create_and_load_table(p_connection, titanic_Table, quer_titanic_create, quer_insert, "titanic")


# Checking the see the number of rows that are now in the 
# dataBase
cursor = p_connection.cursor()
cursor.execute("SELECT count(*) FROM titanic;")
result = cursor.fetchall()
print("The number of rows that are in the titanic table is:", result)


# This returning the First 34 names

cursor.execute("SELECT titanic.name FROM titanic LIMIT 34")
result = cursor.fetchall()
print("\n")
print("These are the 34 first names in the table titanic", result)
