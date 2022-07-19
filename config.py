from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'FsSDjF6u65'
app.config['MYSQL_DATABASE_PASSWORD'] = 'oQsWSvJroz'
app.config['MYSQL_DATABASE_DB'] = 'FsSDjF6u65'
app.config['MYSQL_DATABASE_HOST'] = 'remotemysql.com'
mysql.init_app(app)