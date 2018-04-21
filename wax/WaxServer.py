from .Core import WaxInterface, WForm
from http.server import *
from html import escape, unescape
import urllib
import re
from urllib.parse import parse_qs
import cgi

class WaxServer(WaxInterface):
  """Main class for Wax server
  You may specify port to start when creating WaxServer.
  After creation, you must bind some actions via bind_action() method.
  To fire it up, just call start()
  """
  def _decode_request(req):
    def d(s):
      return urllib.parse.unquote(s).replace("+", " ")#.decode('utf8') 
    result = {'mode': 'web', 'variables': {}}
    regexp = r'([^\/?\s&=]+)=([^\/?\s&=]+)'
    res = re.findall(regexp, req)
    regexp = r'(?:GET|POST)\s\/([\w]*)\??.+'
    act = re.findall(regexp, req)
    if act[0] == '':
      result['action'] = 'index'
    else:
      result['action'] = d(act[0])
    for i in res:
      result['variables'][d(i[0])] = d(i[1])
    return result
  def _HttpProcessor(self, w):
    class __HttpProcessor__(BaseHTTPRequestHandler):
      def resp(self, post=None):
        args = WaxServer._decode_request(self.requestline)
        if post:
          for k in post.keys():
            var = str(k)
            val = str(post.getvalue(var))
            args['variables'][var] = val
        print(args)
        try:
          form = w._actions[args['action']](args)
          r = 200
        except KeyError:
          f = lambda args: WForm('404 no action bind')
          r = 404
          form = f(args)
        self.send_response(r)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        string = form.html()
        self.wfile.write(bytes(string, 'utf-8'))
      def do_GET(self):
        self.resp()
      def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        self.resp(form)
    return __HttpProcessor__
  def __init__(self, port=80):
    """Constructor
    Kwargs:
      port:  Specify port to listen. Default is 80.
    """
    super().__init__()
    self._port = port
  def start(self):
    """Fire it up
    """
    self._handler = self._HttpProcessor(self)
    self.server = HTTPServer(("", self._port), self._handler)
    self.server.serve_forever()
