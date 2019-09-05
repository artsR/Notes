# "Database code" for the DB Forum.

# Prevent SQL Injection: https://bobby-tables.com/python


import datetime
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]
#DBNAME = 'forum'

def get_posts():
  """Return all posts from the 'database', most recent first."""
  return reversed(POSTS)
  #db = connect(dbname=forum)
  #c = db.cursor()
  #c.execute(
"""SELECT * FROM post ORDER BY time DESC"""
  #)
  #posts = c.fetchall()
  #db.close()
  #return posts
  

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  POSTS.append(content, datetime.datetime.now()))
  #db = connect(dbname=DBNAME)
  #c = db.cursor()
  #c.execute("INSERT INTO posts VALEUS('%s')" % ((bleach.clean(content),))
  # SQL Injection Attack:
  # w/o tuple'(,)' SQL injection attack is possible.
  #User is able remove all posts in db by putting:
  # "'); delete from posts; --" in the post's field.
  """Warning:
  Never, never, NEVER use Python string concatenation (+) or string parameters
  interpolation (%) to pass variable to a SQL quety string. Not even at gunpoint.
  The PROPER way is using the second argument of the 'execute()':
  *************************************************************
  SQL = "INSERT INTO authors (name) VALUES (%s);"
  data = ("O'Reilly",)
  cur.execute(SQL, data) # no % operator."""
  # Script Injection Attack:
  # https://bleach.readthedocs.io/en/latest/
  #db.commit()
  #db.close()
