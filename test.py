
from cs50 import SQL
import psycopg2

db = SQL("postgres://pwjdyffldbnkyw:88c8437d27352dfc5e4128c60929cdab961f02fed030886dd1cf13ccbd6b5a0a@ec2-54-88-130-244.compute-1.amazonaws.com:5432/d9eg0n6e5s9srl")
username="ishan"

rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
