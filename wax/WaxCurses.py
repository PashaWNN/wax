from .Core import WaxInterface, WObject, WForm
import curses

class WaxCurses(WaxInterface):
  """Main class for Wax CLI controller
  After creation, you must bind some actions via bind_action() method
  To start controlling terminal, just call start()
  """
  def __init__(self):
    super().__init__()
    self._selected_object = WObject() # Empty object
    self._current_form = None
  def start(s):
    s._f_scroll = 0
    s._f_sel = 0
    curses.wrapper(s._main)

  def _act(s, action):
    _vars = {}
    if s._current_form:
      for o in s._current_form._objects:
        v = o._get_value()
        if v:
          _vars[v[0]] = v[1]
    args = {'action': action, 'variables': _vars, 'mode': 'terminal'}  
    s._current_form = s._actions[action](args)

  def _main(s, stdscr):
    s._scr = stdscr
    s._act('index')
    ex = False
    while True:
      s._scr.clear()      
      s._render_form()
      s._handle_key(s._scr.getch())
      
  def _handle_key(s, c):
    for k in s._keys:
      if c == k:
        s._keys[k]()
    s._current_form._objects[s._f_sel]._handle_key(s, c)
    if c == curses.KEY_DOWN:
      s._f_sel += 1
    elif (c == curses.KEY_UP) and s._f_sel>0:
      s._f_sel -= 1
    elif c == curses.KEY_HOME:
      s._f_sel = 0
    #if s._selectedType == WTextEdit:

  def _render_form(s):
    form = s._current_form
    ### Window
    width  = curses.COLS  -1
    height = curses.LINES -1
    upper  = '╔'+'═'*(width-2)+'╗'
    medium = '║'+' '*(width-2)+'║'
    bottom = '╚'+'═'*(width-2)+'╝'
    title = ' %s ' % form._title
    s._scr.addstr(0, 0, upper)
    s._scr.addstr(0, width//2-len(title)//2, title)
    s._scr.addstr(height, 0, bottom)
    for i in range(1, height):
      s._scr.addstr(i, 0, medium)
    ### Window contents
    ## Scrollbar
    if s._f_sel > len(s._current_form._objects)-1:
      s._f_sel = len(s._current_form._objects)-1
    sel = s._f_sel        # Selected element number
    count = (height-2)//2 # Count of objects per page
    scroll = (sel//count)*count   # Scrollbar position
    position = round((scroll / len(s._current_form._objects)) * height)+1
    for i in range(1, height):
      s._scr.addstr(i, width-2, ('▓' if i==position else '░'))
    s._win = curses.newwin(height-2, width-3, 1, 1)
    width -= 3    #Now it's width and height of _win
    height -= 2
    for i, y in enumerate(range(1, height, 2)):
      try:
        selected = (i+scroll == sel)
        for line in s._current_form._objects[i+scroll].render_curses(selected):
          _y, _x, _text, _fmt = line
          s._win.addstr(_y+y, _x+2, _text, _fmt)
      except IndexError:
        break
    s._scr.leaveok(True)
    s._scr.refresh()
    s._win.refresh()
