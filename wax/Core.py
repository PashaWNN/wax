def bind(target, action):
  def decorator(fn):
    target.bind_action(action, fn)
    def wrapped(args):
      return fn(args)
    return wrapped
  return decorator

def bindkey(target, key):
  def decorator(fn):
    target.bind_key(key, fn)
    def wrapped(args):
      return fn(args)
    return wrapped
  return decorator


class WObject:
  """Parent class for all GUI elements, such as Label, TextEdit or Button
  """
  def __init__(self, enabled=True):
    """Constructor.
    Kwargs:
      visible:  Is element must be shown on the form
      enabled:  Is element able to change it's value or grayed
    """
    self._enabled = enabled
    self._value = None
    self._name = None

  def set_value(self, value):
    self._value = value

  def _get_value(self):
    if self._name:
      return (self._name, self._value)
    else:
      return None

  def _get_html(self):
    return '<p>%s</p>\n' % self.html()

  def _handle_key(self, iface, key):
    pass

  def html(self):
    """Function for rendering HTML code of this element
    Returns:
      A string with HTML-code of element
    """
    return 'Undefined object.<br>\n'

  def render_curses(self, sel=False):
    """Render this object to a curses screen
    Args:
      y: Y-coord on the screen
      x: X-coord on the screen
      scr: curses screen to render
    Kwargs:
      sel: component must be rendered as selected
    """
    return [(0, 0, '%sUndefined object.' % ('>' if sel else ' '), 0)]


  def set_enabled(self, state):
    """Setting active state of element. If element is inactive, it grayed and unable to change value.
    Args:
      state:  Enabled state of element. Must be value of True or False. True for active and False for inactive
    """
    self._enabled = state


class WForm:
  """Form class
  Form is a basic class to render form on the Web-page or in the terminal. It must be returned from action functions.
  """
  def __init__(self, title="Wax Form"):
    """Constructor
    Kwargs:
      title: Title of form.
    """
    self.set_title(title)
    self._objects = []

  def set_title(self, title):
    """Change title
      title: New title
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
    self._keys = {}
  def bind_action(self, name, func):
    """Bind actions
    Args:
      name:  Name of action to trigger it.
      func:  A function, that will be called, when action is triggered. That function **must accept one parameter**, that is a dictionary with action name and passes variables and it **must return WForm object** to render it.
    """
    self._actions[name] = func
  def bind_key(self, key, func):
    self._keys[key] = func

