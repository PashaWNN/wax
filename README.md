WAX Project
===========
**WAX** is framework for creating settings user interfaces(such as home router settings on 192.168.0.1) to be showed as web-interface and/or CLI.

Simple example
--------------
The code below will create a single window with label and button.

```python
from wax import *

def form_index(args):
  wf = WForm("Foobar")                                                       # Creating a form with title "Foobar"
  wf.add_object(WLabel('Hello, world'))                                      # Adding label to it
  wf.add_object(WButton("foo", action="index"))                              # Adding button
  return wf #Action function always must return WForm()


w = WaxServer(port=8080)                                                     # Creating server class object
w.bind_action('index', form_index)                                           # Binding default action to our form
w.start()                                                                    # Firing it up
```

But it's too simple and boring and have no functionality. Let's go to more advanced example!
Advanced example
----------------
```python
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
  a = int(args['variables']['a'])     #When 'Add' and 'Subtract' button pressed, TextEdit's values passed
  b = int(args['variables']['b'])     #To args['variables'] dictionary
  if args['action'] == 'add':         #If action were 'add'
    result = 'Result is ' + str(a+b)  #Add our integers
  elif args['action'] == 'subtract':  #Else subtract it.
    result = 'Result is ' + str(a-b)
  wf.add_object(WLabel(text=result))  #Let's create label with result
  wf.add_object(WButton("Return", action="index"))
  return wf

w = WaxServer(port=8080)
w.bind_action("index", form_calc)           #Binding form_calc to index page
w.bind_action("add", form_show_result)      #Binding form_show_result to actions, triggered by buttons on index page
w.bind_action("subtract", form_show_result)
w.start()
```


TODO
----
At this moment the project is at very beginning. A lot of work in future:
* Basic ncurses functionality
* UI Layouts
* Dynamic page updating
* More UI components, such as ProgressBars etc.
* Tabs, accordions...
And a lot of different things...
