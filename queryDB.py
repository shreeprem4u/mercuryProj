import psycopg2

conn = psycopg2.connect("dbname='smartbuilding' port='5432' user='amudalab3' host='172.17.137.160' password='amudalab'")
cur = conn.cursor()		
cur.execute("SELECT * FROM main_asset where epc='0028029C1301230000E6CBD9' ORDER BY time DESC limit 1;")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.commit()
cur.close()

