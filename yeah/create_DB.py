import sqlite3
import pandas as pd

df = pd.read_csv("RECORD.csv")

dbname = 'data.db'

conn = sqlite3.connect(dbname)
cur = conn.cursor()

df.to_sql('record', conn, if_exists = 'replace')

select_sql = 'SELECT * FROM record'

for row in cur.execute(select_sql):
    print(row)

cur.close()
conn.close()