from http.server import BaseHTTPRequestHandler, HTTPServer

class WObject:
  def __init__(self):
    self._visible = True
    self._enabled = True


class WLabel(WObject):
  def __init__(self, text="Label"):
    super().__init__()
    self._text = text


class WButton(WObject):
  def __init__(self, text="Button", action=None):
    super().__init__()
    self._text = text
    self._action = action


class WForm:
  _title = 'Wax Form'
  def setTitle(self, title):
    self._title = str(title)


class WaxServer:
  def _HttpProcessor(self, form):
    class __HttpProcessor__(BaseHTTPRequestHandler):
      def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        string = form._title
        for o in form.__dict__:
          if isinstance(form.__dict__[o], WLabel):
            string += '<br>' + form.__dict__[o]._text
          elif isinstance(form.__dict__[o], WButton):
            string += '<br><a href="#">[ %s ]</a>' % form.__dict__[o]._text
        self.wfile.write(bytes(string, 'utf-8'))
    return __HttpProcessor__
  def __init__(self, form):
    self.attachForm(form)
    self.server = HTTPServer(("", 80), self._handler)
    self.server.serve_forever()
  def attachForm(self, form):
    self._form = form
    self._handler = self._HttpProcessor(form)

