import datetime
from src.constants import *

if LOGEVENTS:
    with open(EVTLOGFILE, "w") as file:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write("Event log started on: {}\n".format(now))
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

def event_wrapper(func):
    def inner(evt):
        evt.controller = evt.widget.controller
        if LOGEVENTS:
            with open(EVTLOGFILE,"a") as file:
                file.write("[{:06.3f}] <{}>\n".format(evt.controller.t_ns/(1*10**9),str(evt)))
        func(evt)
    return inner

# Arrowkeys

@keypress_wrapper
@event_wrapper
def onUpArrowPress(e):
    e.controller.pc.vel[1] = 0.5
    return

@keyrelease_wrapper
@event_wrapper
def onUpArrowRelease(e):
    e.controller.pc.vel[1] = 0
    return

@keypress_wrapper
@event_wrapper
def onDownArrowPress(e):
    e.controller.pc.vel[1] = -0.5
    return

@keyrelease_wrapper
@event_wrapper
def onDownArrowRelease(e):
    e.controller.pc.vel[1] = 0
    return

@keypress_wrapper
@event_wrapper
def onLeftArrowPress(e):
    e.controller.pc.vel[0] = -0.5
    return

@keyrelease_wrapper
@event_wrapper
def onLeftArrowRelease(e):
    e.controller.pc.vel[0] = 0
    return

@keypress_wrapper
@event_wrapper
def onRightArrowPress(e):
    e.controller.pc.vel[0] = 0.5
    return

@keyrelease_wrapper
@event_wrapper
def onRightArrowRelease(e):
    e.controller.pc.vel[0] = 0
    return