from wax.Core import WObject, WForm, bind, bindkey
from wax.Components import *
from wax.WaxCurses import WaxCurses
KEY_ESCAPE = 27


w = WaxCurses()


tabs = [
    ('index', 'Hello, world!'),
    ('test', 'Test page #1'),
    ('test2', 'Test2'),
]

@bind(w, 'index')
def hello(args):
  wf = WForm("Hello, world!")
  wf.add_object(WFormsCarousel(tabs, 'index', width=60))
  wf.add_object(WTextEdit('Enter your name: ', name='name'))
  name = args['variables'].get('name', None)
  text = ('Hello, %s' % name) if name else 'Hello, world!'
  wf.add_object(WLabel(text))
  wf.add_object(WButton('Hello!', action='index', html_method_post=True))
  return wf

@bind(w, 'test')
def test(args):
  wf = WForm('Test1')
  wf.add_object(WFormsCarousel(tabs, 'test', width=60))
  wf.add_object(WLabel('This is test1'))
  return wf


@bind(w, 'test2')
def test(args):
  wf = WForm('Test2')
  wf.add_object(WFormsCarousel(tabs, 'test2', width=60))
  wf.add_object(WLabel('This is test2'))
  return wf

@bindkey(w, KEY_ESCAPE)
def terminate():
  exit()

w.start()
