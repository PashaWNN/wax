#!/usr/bin/python3
from wax import *


def index(args):
  wf = WForm('Hello, world!')
  wf.add_object(WLabel('You\'re great!'))
  wf.add_object(WButton('Button1', action='test'))
  lbl = wf.add_object(WLabel('You\'re great!'))
  lbl.set_style(bold=True)
  wf.add_object(WTextEdit('Enter text: ', 'placeholder', name='txt'))
  for i in range(1,28):
    wf.add_object(WLabel('Надпись номер %i' % i))
  return wf


w = WaxCurses()
w.bind_action('index', index)
w.start()
