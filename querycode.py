import psycopg2
hostname ='localhost'
database='DBMS Project'
username='postgres'
pwd='0328'
port_id= 5432
conn=None
cur=None

try:
    conn=psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
    cur=conn.cursor()

    cur.execute("SELECT * FROM Teachers")
    for record in cur.fetchall():
        print(record[1], record[3])
    print(cur.fetchall())


    conn.commit()
except Exception as error:
    print(error)
finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()