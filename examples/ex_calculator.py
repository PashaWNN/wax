#!/usr/bin/python3
from wax import *

def form_calc(args):
  wf = WForm('Calculator')
  wf.add_object(WTextEdit('A:', '2', name='a'))
  wf.add_object(WTextEdit('B:', '4', name='b'))
  wf.add_object(WButton("Add", action="add"))
  wf.add_object(WButton("Subtract", action="subtract"))
  return wf

def form_show_result(args):
  wf = WForm('Result')
  a = int(args['variables']['a'])
  b = int(args['variables']['b'])
  if args['action'] == 'add':
    result = 'Result is ' + str(a+b)
  elif args['action'] == 'subtract':
    result = 'Result is ' + str(a-b)
  wf.add_object(WLabel(text=result))
  wf.add_object(WButton("Return", action="index"))
  return wf

w = WaxServer(port=8080)
w.bind_action("index", form_calc)
w.bind_action("add", form_show_result)
w.bind_action("subtract", form_show_result)
w.start()

