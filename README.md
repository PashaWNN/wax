WAX Project pre-release 0.0.1
=============================
**WAX** is framework for creating user interfaces(such as home router settings on 192.168.0.1) as web-interface and/or CLI.

Simple example
--------------
The code below will create a single window with label.

```python
from wax.Core import WObject, WForm, bind, bindkey
from wax.Components import *
from wax.WaxCurses import WaxCurses
from wax.WaxServer import WaxServer

w = WaxCurses()                                            #Creating WAX instance for terminal
#w = WaxServer()                                           #Creating WAX instance for web

@bind(w, 'index')
def hello(args):                                           #Defining form to be showed by default('index')
  wf = WForm()                                             #Form object
  wf.add_object(WLabel('Hello, WAX world!'))               #A label
  if args['mode'] == 'terminal':
    wf.add_object(WButton('Hello!', action='terminate'))   #And a button if app running in terminal mode(we can't exit from browser)
  return wf

@bind(w, 'terminate')                                      #We'll call this function when button with action 'terminate' is triggered
@bindkey(w, 27)                                            #And when key with code 27(Escape) is pressed, but it's only in terminal mode
def terminate(args=None):                                  #Defining exit function
  exit()

w.start()                                                  # Firing it up
```

But it's too simple and boring and have no functionality. You can see more useful examples in `/examples`

TODO
----
* `WFormsCarousel` rendering in WEB mode
* Authorization
* Multiline components support for terminal mode
* Docs
* Unit tests
* More components
* Passing arguments through actions
* WTimer or/and just self-updating WForm
And a lot of different things...
