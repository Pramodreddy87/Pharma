#from tornado.wsgi import WSGIContainer
#from tornado.httpserver import HTTPServer
#from tornado.ioloop import IOLoop
#from tornado import autoreload
###from yourapplication import app
#
##app.run()
#http_server = HTTPServer(WSGIContainer(app))
#http_server.listen(5000)
##IOLoop.instance().start()
##ioloop = tornado.ioloop.IOLoop().instance()
#autoreload.start(IOLoop)
#IOLoop.start()

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado import autoreload
from blog import app
app.debug=True
app.secret_key='1234567ikmnbvfcdswerty'
app.url_map.strict_slashes = False
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
ioloop = IOLoop.instance()
autoreload.start(ioloop)
ioloop.start()