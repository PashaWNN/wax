from wax import *


def hello(args):
  wf = WForm("Hello, world!")
  wf.add_object(WTextEdit('Enter your name: ', name='name'))
  name = args['variables'].get('name', None)
  text = ('Hello, %s' % name) if name else 'Hello, world!'
  wf.add_object(WLabel(text))
  wf.add_object(WButton('Hello!', action='index'))
  return wf


w = WaxServer(port=8080)
w.bind_action('index', hello)
w.start()
