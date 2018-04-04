from html import escape, unescape
import urllib
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
    Kwargs:
      visible:  Is element must be shown on the form
      enabled:  Is element able to change it's value or grayed
    """
    self._visible = visible
    self._enabled = enabled
  def _get_html(self):
    if self._visible:
      return '<p>%s</p>\n' % self.html()
    else:
      return ''
  def html(self):
    """Function for rendering HTML code of this element
    Returns:
      A string with HTML-code of element
    """
    return 'Undefined object.<br>\n'
  def render_curses(self, y, x, scr, sel=False):
    """Render this object to a curses screen
    Args:
      y: Y-coord on the screen
      x: X-coord on the screen
      scr: curses screen to render
    Kwargs:
      sel: component must be rendered as selected
    """
    scr.addstr(y, x, '%sUndefined object.' % ('>' if sel else ' '))
  def set_visible(self, state):
    """Setting hidden state of element
    Args:
      state:  State of element. Must be value of True or False. True for visible and False for invisible
    """
    self._visible = state
  def set_enabled(self, state):
    """Setting active state of element. If element is inactive, it grayed and unable to change value.
    Args:
      state:  Enabled state of element. Must be value of True or False. True for active and False for inactive
    """
    self._enabled = state


class WLabel(WObject):
  """Label element.
  """
  def __init__(self, text="Label", visible=True):
    """
    Creating label

    Kwargs:
      text:  Text to be shown in element
      visible: Is label visible on the form
    """
    super().__init__(visible=visible)
    self._text = text
    self._bold = False
    self._italic = False
  def set_style(self, bold=False, italic=False):
    """Setting font style

    Kwargs:
      bold:  Bold font
      italic:  Italic font
    """
    self._bold = bold
    self._italic = italic
  def html(self):
    """Function for rendering HTML code of this element
    Returns:
      A string with HTML-code of element
    """
    bop = ('<b>' if self._bold else '')
    iop = ('<i>' if self._italic else '')
    icl = ('</i>' if self._italic else '')
    bcl = ('</b>' if self._bold else '')
    txt = escape(self._text)
    s = '%s%s%s%s%s' % (bop, iop, txt, icl, bcl)
    return '%s' % s
  def render_curses(self, y, x, scr, sel=False):
    text = '%s%s' % (('>' if sel else ' '), self._text)
    if not self._bold:
      scr.addstr(y, x, text)
    else:
      scr.addstr(y, x, text, 2097152)

class WButton(WObject):
  """Button element
  """
  def __init__(self, text="Button", action='', enabled=True, visible=True, html_method_post=False):
    """Constructor.
    Kwargs:
      text:  Text on the button
      enabled:  Is it active to click
      visible:  Is it visible on the form
      action:  What action it will trigger
    """
    super().__init__(visible=visible, enabled=enabled)
    self._text = text
    self._action = action
    self._html_post = html_method_post
  def html(self):
    """Function for rendering HTML code of this element
    Returns:
      A string with HTML-code of element
    """
    dis = ('disabled' if not self._enabled else '')
    met = ('post' if self._html_post else 'get')
    act = escape(self._action)
    txt = escape(self._text)
    return '<button %s formaction="%s" formmethod="%s">%s</button>' % (dis, act, met, txt)
  def render_curses(self, y, x, scr, sel=False):
    text = '%s[ %s ]' % (('>' if sel else ' '), self._text)
    scr.addstr(y, x, text, (65536 if sel else 0))


class WTextEdit(WObject):
  """TextEdit element
  """
  def __init__(self, label="Edit", value="", size=40, password=False, enabled=True, visible=True, name="edit"):
    """Constructor.
    Kwargs:
      label: Text before edit bot
      value: Initial value entered in the box
      size: Size of box
      password: Is value hidden above asterisks
      name: Name of field in variables dict to store its value
      enabled: Is it active to change its value
      visible: Is it shown on the form
    """
    super().__init__(enabled=enabled, visible=visible)
    self._label = label
    self._value = value
    self._size = size
    self._name = name
    self._password = password
  def html(self):
    """Function for rendering HTML code of this element
    Returns:
      A string with HTML-code of element
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
    Kwargs:
      title Title of form.
    """
    self.set_title(title)
    self._objects = []
  def set_title(self, title):
    """Change title
      title New title
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
    Args:
      obj: WObject to add
    Returns:
      Pointer to this component
    Raises:
      TypeError if obj isn't WObject
    """
    if isinstance(obj, WObject):
      self._objects.append(obj)
      return obj # Return it's id
    else:
      raise TypeError    

class WaxInterface:
  """Parent class for WaxCurses and WaxServer
  Provides common methods
  """
  def __init__(self):
    self._actions = {
      'index': lambda args: WForm('Hello, world!')
    }
  def bind_action(self, name, func):
    """Bind actions
    Args:
      name:  Name of action to trigger it.
      func:  A function, that will be called, when action is triggered. That function **must accept one parameter**, that is a dictionary with action name and passes variables and it **must return WForm object** to render it.
    """
    self._actions[name] = func


class WaxCurses(WaxInterface):
  """Main class for Wax CLI controller
  After creation, you must bind some actions via bind_action() method
  To start controlling terminal, just call start()
  """
  def __init__(self):
    super().__init__()
    self._curses = __import__('curses')
  def start(s):
    s._f_scroll = 0
    s._f_sel = 0
    s._curses.wrapper(s._main)
  def _main(s, stdscr):
    s._scr = stdscr
    args = {'action': 'index', 'variables': {}}    
    ex = False
    while not ex:
      s._scr.clear()
      s._render_form(s._actions['index'](args))
      c = s._scr.getch()
      if c == s._curses.KEY_DOWN:
        s._f_sel += 1
      elif (c == s._curses.KEY_UP) and s._f_sel>0:
        s._f_sel -= 1
      elif c == ord('q'):
        ex = True
  def _render_form(s, form):
    ### Window
    width  = s._curses.COLS  -1
    height = s._curses.LINES -1
    upper  = '╔'+'═'*(width-2)+'╗'
    medium = '║'+' '*(width-2)+'║'
    bottom = '╚'+'═'*(width-2)+'╝'
    title = ' %s ' % form._title
    objects = form._objects
    s._scr.addstr(0, 0, upper)
    s._scr.addstr(0, width//2-len(title)//2, title)
    s._scr.addstr(height, 0, bottom)
    for i in range(1, height):
      s._scr.addstr(i, 0, medium)
    ### Window contents
    ## Scrollbar
    if s._f_sel > len(objects)-1:
      s._f_sel = len(objects)-1
    sel = s._f_sel        # Selected element number
    count = (height-2)//2 # Count of objects per page
    scroll = (sel//count)*count   # Scrollbar position
    position = round((scroll / len(objects)) * height)+1
    for i in range(1, height):
      s._scr.addstr(i, width-2, ('▓' if i==position else '░'))
    s._win = s._curses.newwin(height-2, width-3, 1, 1)
    width -= 3    #Now it's width and height of _win
    height -= 2
    for i, y in enumerate(range(1, height, 2)):
      try:
        selected = (i+scroll == sel)
        objects[i+scroll].render_curses(y, 3, s._win, selected)
      except IndexError:
        break
    s._scr.refresh()
    s._win.refresh()


class WaxServer(WaxInterface):
  """Main class for Wax server
  You may specify port to start when creating WaxServer.
  After creation, you must bind some actions via bind_action() method.
  To fire it up, just call start()
  """
  def _decode_request(req):
    def d(s):
      return urllib.parse.unquote(s).replace("+", " ")#.decode('utf8') 
    result = {}
    result['variables'] = {}
    regexp = r'([^\/?\s&=]+)=([^\/?\s&=]+)'
    res = re.findall(regexp, req)
    regexp = r'\/([^?]*)(?:\?.*){0,1}\s'
    act = re.findall(regexp, req)
    if act[0] == '':
      result['action'] = 'index'
    else:
      result['action'] = d(act[0])
    for i in res:
      result['variables'][d(i[0])] = d(i[1])
    return result
  def _HttpProcessor(self, w):
    class __HttpProcessor__(self._http.server.BaseHTTPRequestHandler):
      def resp(self, post=None):
        args = WaxServer._decode_request(self.requestline)
        args['post'] = post
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
    self._http = __import__('http.server')
  def start(self):
    """Fire it up
    """
    self._handler = self._HttpProcessor(self)
    self.server = self._http.server.HTTPServer(("", self._port), self._handler)
    self.server.serve_forever()
