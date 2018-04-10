from .Core import WObject
from html import escape, unescape

class WCheckBox(WObject):
  def __init__(self, text='Checkbox', name='checkbox', value=False, enabled=True):
    self._text = text
    self._enabled = enabled
    self._value = value
    self._name = name

  def set_value(self, value):
    self._value = bool(value)

  def _get_value(self):
    if self._value:
      return (self._name, 'on')
    else:
      return (self._name, '')

  def html(self):
    checked = ('checked' if self._value else '')
    disabled = ('disabled' if not self._enabled else '')
    text = escape(self._text)
    name = escape(self._name)
    code = '<input type="checkbox" %s name="%s" %s>%s' % (disabled, name, checked, text)
    return code

  def render_curses(self, sel=False):  
    _x = 'X' if self._value else ' '
    s = ('>' if sel else ' ')
    text = '%s[%s] %s' % (s, _x, self._text)
    formatting = (0 if self._enabled else 1048576) + (65536 if sel else 0)
    #scr.addstr(y, x, text, formatting)
    return [(0, 0, text, formatting)]
  
  def _handle_key(self, iface, key):
    if self._enabled and key == ord(' '):
      self._value = not self._value
    

class WLabel(WObject):
  """Label element.
  """
  def __init__(self, text="Label"):
    """
    Creating label

    Kwargs:
      text:  Text to be shown in element
      visible: Is label visible on the form
    """
    super().__init__()
    self._text = text
    self._bold = False
    self._italic = False
  
  def set_value(self, value):
    self._value = str(value)

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

  def render_curses(self, sel=False):
    text = '%s%s' % (('>' if sel else ' '), self._text)
    if not self._bold:
      return [(0,0,text, 0)]
    else:
      return [(0,0,text, 2097152)]


class WButton(WObject):
  """Button element
  """
  def __init__(self, text="Button", action='', enabled=True, html_method_post=False):
    """Constructor.
    Kwargs:
      text:  Text on the button
      enabled:  Is it active to click
      visible:  Is it visible on the form
      action:  What action it will trigger
    """
    super().__init__(enabled=enabled)
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

  def _handle_key(self, iface, key):
    if self._enabled and key == ord(' ') and self._action:
      iface._act(self._action)

  def render_curses(self, sel=False):
    formatting = (0 if self._enabled else 1048576) + (65536 if sel else 0)
    text = '%s[ %s ]' % (('>' if sel else ' '), self._text)
    return [(0,0,text, formatting)]


class WFormsCarousel(WObject):
  def __init__(self, tabs=[], current_action=None, enabled=True, width=50):
    super().__init__(enabled=enabled)
    self._tabs = tabs
    self._enabled = enabled
    self._index = 0
    self._width = width
    if current_action:
      for i, t in enumerate(tabs):
        if t[0] == current_action:
          self._index = i
  
  def html(self):
    pass

  def render_curses(self, sel=False):    
    w = self._width - 13
    lbl = self._tabs[self._index][1]
    if len(lbl)<w:
      spc = ' ' * ((w - len(lbl)) // 2)
    else:
      spc = ''
    fmt = (0 if self._enabled else 1048576) + (65536 if sel else 0)
    sel = '>' if sel else ' '
    txt = '%s{ << |%s%s%s| >> }' % (sel, spc, lbl, spc)
    return [(0, 0, txt, fmt)]

  def _handle_key(self, iface, key):
    if self._enabled and self._tabs:
      if key == ord(' '):
        iface._act(self._tabs[self._index][0])
      elif (key == 261): #KEY_RIGHT
        if (self._index < len(self._tabs)-1):
          self._index += 1
        else:
          self._index = 0
      elif (key == 260): #KEY_LEFT
        if (self._index > 0):
          self._index -= 1
        else:
          self._index = len(self._tabs)-1


class WTextEdit(WObject):
  """TextEdit element
  """
  def __init__(self, label="Edit", value="", size=40, password=False, enabled=True, name="edit"):
    """Constructor.
    Kwargs:
      label: Text before edit bot
      value: Initial value entered in the box
      size: Size of box
      password: Is value hidden above asterisks
      name: Name of field in variables dict to store its value
      enabled: Is it active to change its value
    """
    super().__init__(enabled=enabled)
    self._label = label
    self._enabled = enabled
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

  def render_curses(self, sel=False):
    text = '%s%s(' + (' '*self._size) + ')'
    text = text % (('>' if sel else ' '), self._label)
    return [(0, 0, text, (65536 if sel else 0)),
            (0, 2+len(self._label), self._value, 131072+(65536 if sel else 0)),
           ]

  def _handle_key(self, iface, key):
    LETTERS = 'qwertyuiop[]asdfghjkl;\'/":zxcvbnm,.?!|1234567890!@#$%^&*()=-+{}[]!"№;%:?*(_'
    LETTERS+= LETTERS.upper()
    if self._enabled:
      if key == 263 and len(self._value)>0: #KEY_BACKSPACE
        self._value = self._value[:-1]
      elif chr(key) in LETTERS and len(self._value)<self._size:
        self._value+=chr(key)
