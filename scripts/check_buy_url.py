import sqlite3
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
cur.execute("SELECT id, slug, buy_url FROM core_course WHERE slug=?", ('ui-ux-designing',))
row = cur.fetchone()
print(row)
conn.close()