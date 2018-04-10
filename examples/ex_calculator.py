from wax.Core import WObject, WForm, bind, bindkey
from wax.Components import *
from wax.WaxCurses import WaxCurses
from wax.WaxServer import WaxServer
import argparse as ap
KEY_ESCAPE = 27

p = ap.ArgumentParser()                                                  #Parsing command line arguments
p.add_argument("-w", "--web-server", dest='web', action='store_true',
               help='Start a web-server')
p.add_argument('-p', '--port', type=int, default=80)
a = p.parse_args()

if a.web:                                                    #If '-w' specified
  w = WaxServer(port=a.port)                                 #Run server on -p port
else:                                                        #Else
  w = WaxCurses()                                            #Run in terminal

@bind(w, 'index')                                            #Form to show by default
def form_calc(args):
  wf = WForm('Calculator')                                   #Title
  wf.add_object(WTextEdit('A:', '2', name='a'))              #TextEdit's
  wf.add_object(WTextEdit('B:', '4', name='b'))              #Values will be stored in args['variables'] as a dict
  wf.add_object(WButton("Add", action="add"))                #A button for first action
  wf.add_object(WButton("Subtract", action="subtract"))      #And for second
  return wf

@bind(w, 'add')
@bind(w, 'subtract')
def form_show_result(args):                                  #Form to show if action == 'add' or 'subtract'
  wf = WForm('Result')
  try:
    a = int(args['variables']['a'])                          #Restoring vars from dictionary
    b = int(args['variables']['b'])
    if args['action'] == 'add':                              #Calculating
      result = 'Result is ' + str(a+b)
    elif args['action'] == 'subtract':
      result = 'Result is ' + str(a-b)
    wf.add_object(WLabel(text=result))                       #Output result
  except ValueError:                                         #Or, if input is not integers, show error
    wf.add_object(WLabel('Invalid input provided!'))
  wf.add_object(WButton("Return", action="index"))           #Add a button to return
  return wf

@bindkey(w, KEY_ESCAPE)                                      #Affect only if "w" is WaxCurses
def terminate():
  exit()

w.start()
