import tornado.ioloop
import tornado.web

class ApplicationHandler(tornado.web.RequestHandler):
  ''' serves as the handler for a request and returns a response using the "write()" method'''
  def get(self):
    self.message = message = """<html>
<head>
    <title>Tornado Framework</title>
</head>
<body>
    <h2>Welcome to the Tornado Framework</h2>
</body>
</html>"""

    self.write(message)

if __name__ == '__main__':  # 'main' method is the entry for the program
  application = tornado.web.Application([    # creates a base for the web application and takes a collection of handlers
      (r'/', ApplicationHandler),
  ])
  application.listen(5000)
  tornado.ioloop.IOLoop.instance().start()  # creates a nonblocking thread for an application  (what does it mean ??)
