from wax.Core import WObject, WForm, bind, bindkey
from wax.Components import WLabel, WButton
from wax.WaxCurses import WaxCurses
from wax.WaxServer import WaxServer
KEY_ESCAPE = 27

w = WaxCurses()

@bind(w, 'index')
def hello(args):
  wf = WForm()
  wf.add_object(WLabel('Hello, world!'))
  wf.add_object(WButton('Hello!', action='terminate'))
  return wf

@bind(w, 'terminate')
@bindkey(w, KEY_ESCAPE)
def terminate(args=None):
  exit()

w.start()
