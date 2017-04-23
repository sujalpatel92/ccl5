import sqlite3
db = sqlite3.connect('id_pass.db')
db.execute("CREATE TABLE pass (id CHAR(100) PRIMARY KEY, password CHAR(100) NOT NULL)")
db.execute("INSERT INTO pass (id,password) VALUES ('coolsujal3392@gmail.com', 'Sgnss1964')")
#db.execute("INSERT INTO picnic (item,quant) VALUES ('cheese', 2)")
#db.execute("INSERT INTO picnic (item,quant) VALUES ('grapes', 30)")
#db.execute("INSERT INTO picnic (item,quant) VALUES ('cake', 1)")
#db.execute("INSERT INTO picnic (item,quant) VALUES ('soda', 4)")
#db.execute("INSERT INTO picnic (item,quant) VALUES ('plates', 5)")
#db.execute("INSERT INTO devices (id,email,location) VALUES ('asdewc345tgb6781','parth@gmail.com','blah')")
#db.execute("INSERT INTO devices (id,email,location) VALUES ('asdewc344tgb6781','parth@gmail.com','blah')")
#db.execute("INSERT INTO devices (id,email,location) VALUES ('asdewc347tgb6781','parth@gmail.com','blah')")
db.commit()

