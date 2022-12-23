from src.constants import *
import src.log

_keysheld = []

def keypress_wrapper(func):
    def inner(evt):
        if evt.keycode not in _keysheld:
            _keysheld.append(evt.keycode)
            func(evt)
        else:
            return
    return inner

def keyrelease_wrapper(func):
    def inner(evt):
        _keysheld.remove(evt.keycode)
        func(evt)
    return inner

def tkinter_event_wrapper(func):
    def inner(evt):
        evt.controller = evt.widget.controller
        evt.controller.core.logger.write("TKinter event: <{}>\n".format(str(evt)))
        func(evt)
    return inner

def task_event_wrapper(func):
    def inner(evt):
        evt.controller = evt.root.entity.controller
        evt.controller.core.logger.write("Task complete event: <{}>\n".format(str(evt)))
        func(evt)
    return inner

# Arrowkeys

@keypress_wrapper
@tkinter_event_wrapper
def onUpArrowPress(e):
    e.controller.pc.vel[1] = 1
    return

@keyrelease_wrapper
@tkinter_event_wrapper
def onUpArrowRelease(e):
    e.controller.pc.vel[1] = 0
    return

@keypress_wrapper
@tkinter_event_wrapper
def onDownArrowPress(e):
    e.controller.pc.vel[1] = -1
    return

@keyrelease_wrapper
@tkinter_event_wrapper
def onDownArrowRelease(e):
    e.controller.pc.vel[1] = 0
    return

@keypress_wrapper
@tkinter_event_wrapper
def onLeftArrowPress(e):
    e.controller.pc.vel[0] = -1
    return

@keyrelease_wrapper
@tkinter_event_wrapper
def onLeftArrowRelease(e):
    e.controller.pc.vel[0] = 0
    return

@keypress_wrapper
@tkinter_event_wrapper
def onRightArrowPress(e):
    e.controller.pc.vel[0] = 1
    return

@keyrelease_wrapper
@tkinter_event_wrapper
def onRightArrowRelease(e):
    e.controller.pc.vel[0] = 0
    return

@task_event_wrapper
def onTaskComplete(e):
    pass