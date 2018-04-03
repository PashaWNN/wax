from html import escape
import re
from urllib.parse import parse_qs
import cgi
"""@package wax
Wax is a microframework to build WEB- and curses- interfaces for servers, IoT and other "control panels" GUIs.
"""

class WObject:
  """Parent class for all GUI elements, such as Label, TextEdit or Button
  """
  def __init__(self, visible=True, enabled=True):
    """Constructor.
    @param visible Is element must be shown on the form
    @param enabled Is element able to change it's value or grayed
    """
    self._visible = visible
    self._enabled = enabled
  def _get_html(self):
    if self._visible:
      return '<p>%s</p>\n' % self.html()
    else:
      return ''
  def html(self):
    """This function returns html-formatted element if it isn't hidden
    """
    return 'Undefined object.<br>\n'
  def set_visible(self, state):
    """Setting hidden state of element
    @param state state of element. Must be value of True or False. True for visible and False for invisible
    """
    self._visible = state
  def set_enabled(self, state):
    """Setting active state of element. If element is inactive, it grayed and unable to change value.
    @param state enabled state of element. Must be value of True or False. True for active and False for inactive
    """
    self._enabled = state


class WLabel(WObject):
  """Label element.
  """
  def __init__(self, text="Label", visible=True):
    """Creating label
    @param text Text to be shown in element
    """
    super().__init__(visible=visible)
    self._text = text
    self._bold = False
    self._italic = False
  def set_style(self, bold=False, italic=False):
    """Setting font style
    @param bold Bold font
    @param italic Italic font
    """
    self._bold = bold
    self._italic = italic
  def html(self):
    """This function returns html-formatted element if it isn't hidden
    """
    bop = ('<b>' if self._bold else '')
    iop = ('<i>' if self._italic else '')
    icl = ('</i>' if self._italic else '')
    bcl = ('</b>' if self._bold else '')
    txt = escape(self._text)
    s = '%s%s%s%s%s' % (bop, iop, txt, icl, bcl)
    return '%s' % s


class WButton(WObject):
  """Button element
  """
  def __init__(self, text="Button", action='', enabled=True, visible=True, html_method_post=False):
    """Constructor
    @param text Text on the button
    @param enabled Is it active to click
    @param visible Is it visible on the form
    @param action What action it will trigger
    """
    super().__init__(visible=visible, enabled=enabled)
    self._text = text
    self._action = action
    self._html_post = html_method_post
  def html(self):
    """This function returns html-formatted element if it isn't hidden
    """
    dis = ('disabled' if not self._enabled else '')
    met = ('post' if self._html_post else 'get')
    act = escape(self._action)
    txt = escape(self._text)
    return '<button %s formaction="%s" formmethod="%s">%s</button>' % (dis, act, met, txt)


class WTextEdit(WObject):
  """TextEdit element
  """
  def __init__(self, label="Edit", value="", size=40, password=False, enabled=True, visible=True, name="edit"):
    """Constructor.
    @param label Text before edit bot
    @param value Initial value entered in the box
    @param size Size of box
    @param password Is value hidden above asterisks
    @param name Name of field in variables dict to store its value
    @param enabled Is it active to change its value
    @param visible Is it shown on the form
    """
    super().__init__(enabled=enabled, visible=visible)
    self._label = label
    self._value = value
    self._size = size
    self._name = name
    self._password = password
  def html(self):
    """This function returns html-formatted element if it isn't hidden
    """
    lbl = escape(self._label)
    dis = ('disabled' if not self._enabled else '')
    typ = ('password' if self._password else 'text')
    nam = escape(self._name)
    val = escape(self._value)
    return '%s <input name="%s" %s type="%s" value="%s" size="%i">' % (lbl, nam, dis, typ, val, self._size)


class WForm:
  """Form class
  Form is a basic class to render form on the Web-page or in the terminal. It must be returned from action functions.
  """
  def __init__(self, title="Wax Form"):
    """Constructor
    @param title Title of form.
    """
    self.set_title(title)
    self._objects = []
  def set_title(self, title):
    """Change title
    @param title New title
    """
    self._title = str(title)
  def _get_html(self):
    html = '<html>\n'
    html+= '  <head>\n'
    html+= '  <meta charset="utf-8">\n'
    html+= '    <title>%s</title>\n' % self._title
    html+= '  </head>\n'
    html+= '  <body>\n  <form>'
    for o in self._objects:
      html += o._get_html()
    html+= '  </form>\n  </body>\n'
    html+= '</html>\n'
    return html
  def html(self):
    """This function returns html-formatted form
    """
    return self._get_html()
  def add_object(self, obj):
    """Add a component to this form
    @param obj A component to add
    @return Pointer to this component
    """
    if isinstance(obj, WObject):
      self._objects.append(obj)
      return obj # Return it's id
    else:
      raise TypeError    

class WaxCursesInterface:
  pass


class WaxServer:
"""Main class to server Wax server
You may specify port to start when creating WaxServer.
After creation, you must bind some actions via bind_action() method.
To fire it up, just call start()
"""
  def _decode_request(req):
    result = {}
    result['variables'] = {}
    regexp = r'([^\/?\s&=]+)=([^\/?\s&=]+)'
    res = re.findall(regexp, req)
    regexp = r'\/([^?]*)(?:\?.*){0,1}\s'
    act = re.findall(regexp, req)
    if act[0] == '':
      result['action'] = 'index'
    else:
      result['action'] = act[0]
    for i in res:
      result['variables'][i[0]] = i[1]
    return result
  def _HttpProcessor(self, w):
    class __HttpProcessor__(self._http.server.BaseHTTPRequestHandler):
      def resp(self):
        args = WaxServer._decode_request(self.requestline)
        print(args)
        try:
          form = w._actions[args['action']](args)
        except KeyError:
          f = lambda args: WForm('404 no action bind')
          form = f(args)
        self.send_response(200)
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
        print(form.getvalue('name'))
        self.resp()
    return __HttpProcessor__
  def __init__(self, port=80):
    """Constructor
    @param port Specify port to listen. Default is 80.
    """
    self._port = port
    self._http = __import__('http.server')
    self._actions = {
      'index': lambda args: WForm('Hello, world!')
    }
  def start(self):
    """Fire it up
    """
    self._handler = self._HttpProcessor(self)
    self.server = self._http.server.HTTPServer(("", self._port), self._handler)
    self.server.serve_forever()
  def bind_action(self, name, func):
    """Bind actions
    @param name Name of action to trigger it.
    @param func A function, that will be called, when action is triggered. That function **must accept one parameter**, that is a dictionary with action name and passes variables and it **must return WForm object** to render it.
    """
    self._actions[name] = func
