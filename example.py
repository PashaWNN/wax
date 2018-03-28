#!/usr/bin/python3
from wax import *


wf = WForm()                       # Создаём форму
wf.setTitle("WF 1")                # Устанавливаем заголовок
wf.label1 = WLabel('Hello, world') # Добавляем надпись
wf.lbl = WButton("foo")            # Добавляем кнопку
w = WaxServer(wf)                  # Запускаем сервер
