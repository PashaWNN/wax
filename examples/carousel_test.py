from wax.Core import WObject, WForm, bind, bindkey
from wax.Components import WLabel, WButton, WFormsCarousel, WTextEdit
from wax.WaxCurses import WaxCurses
from wax.WaxServer import WaxServer
KEY_ESCAPE = 27

w = WaxServer(port=9090)

tabs = [
    ('index', 'Index page'),
    ('first', 'first page'),
    ('second', 'SECOND PAGE'),
  ]

@bind(w, 'index')
def hello(args):
  wf = WForm()
  wf.add_object(WFormsCarousel(tabs, args['action']))
  wf.add_object(WLabel('Hello, world!'))
  wf.add_object(WButton('Hello!', action='terminate'))
  return wf

@bind(w, 'first')
def first(args):
  wf = WForm()
  wf.add_object(WFormsCarousel(tabs, args['action']))
  wf.add_object(WButton('exit', action='terminate'))
  wf.add_object(WTextEdit())
  return wf

@bind(w, 'second')
def first(args):
  wf = WForm()
  wf.add_object(WFormsCarousel(tabs, args['action']))
  wf.add_object(WButton('exit', action='terminate'))
  wf.add_object(WTextEdit())
  return wf

@bind(w, 'terminate')
@bindkey(w, KEY_ESCAPE)
def terminate(args=None):
  exit()

w.start()
