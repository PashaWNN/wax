#!/usr/bin/python3
from wax import *


def index(args):
  wf = WForm('Hello, world!')
  wf.add_object(WLabel('You\'re great!'))
  wf.add_object(WTextEdit('Enter text: ', name='txt'))
  wf.add_object(WCheckBox('Toggle greeting', name='greet'))
  wf.add_object(WButton('Hello', action='test'))
  return wf


def test(args):
  wf = WForm('Form 2')
  text = 'Hello, ' if args['variables'].get('greet', '') else ''
  text+= args['variables'].get('txt', '')
  wf.add_object(WLabel(text))
  wf.add_object(WButton('Return', action='index'))
  return wf


#w = WaxServer(8080)
w = WaxCurses()
w.bind_action('test', test)
w.bind_action('index', index)
w.start()
