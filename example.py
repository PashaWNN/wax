#!/usr/bin/python3
from wax import *

def form_index(args):
  wf = WForm()                                                               # Создаём форму
  wf.set_title("WF 1")                                                       # Устанавливаем заголовок
  wf.add_object(WLabel('Hello, world'))                                      # Добавляем надпись
  wf.add_object(WTextEdit('Enter your name:','Name', name='name'))           # Текстовое поле
  edit = wf.add_object(WTextEdit('Disabled', 'test'))                        # Вы можете сохранять ссылки
  edit.set_enabled(False)                                                    # Чтобы взаимодействовать позже
  wf.add_object(WTextEdit('This is password:', password=True))               # И оно же со "звёздочками"
  wf.add_object(WButton('Invis', visible=False))                             # Невидимый элемент
  wf.add_object(WButton("foo", action="index"))                              # Добавляем кнопку
  wf.add_object(WButton("POST", action="post", html_method_post=True))       #
  wf.add_object(WLabel(args['variables'].get('name', 'No Name')))            #
  return wf


w = WaxServer(port=8080)                                                     # Запускаем сервер
w.bind_action('index', form_index)
w.start()
