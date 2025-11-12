import sqlite3
conn=sqlite3.connect('db.sqlite3')
cur=conn.cursor()
cur.execute("UPDATE core_course SET buy_url = '#' WHERE buy_url IS NULL")
conn.commit()
cur.execute("SELECT id,slug,buy_url FROM core_course WHERE slug='ui-ux-designing'")
print(cur.fetchone())
conn.close()