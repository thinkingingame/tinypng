
from threading import Timer
import traceback
from datetime import datetime

class Listener():
    def __init__(self, name, callback):
        self.name = name
        self.callback = callback

class Emiter():
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

class Event():

    id = 0

    def __init__(self):
        self.observers = {}
        self.listeners = {}
        self.emiters = []
        self._timer = None
        self.schedule()

    def schedule(self):
        self.trigger()
        self._timer = Timer(0.1, self.schedule)
        self._timer.start()

    def on(self, name, callback):
        Event.id = Event.id + 1
        if not name in self.observers.keys():
            self.observers[name] = []
        callbacks = self.observers.get(name)
        callbacks.append(callback)
        self.listeners[Event.id] = Listener(name, callback)
        return Event.id

    def emit(self, name, *args, **kwargs):
        self.emiters.append(Emiter(name, *args, **kwargs))

    def trigger(self):
        emiters = self.emiters
        self.emiters = []
        for index in range(len(emiters)):
            emiter = emiters[index]
            if emiter.name in self.observers.keys():
                callbacks = self.observers.get(emiter.name)
                for listener in callbacks:
                    try:
                        listener(*emiter.args, **emiter.kwargs)
                    except Exception as e:
                        print(traceback.format_exc())

    def off(self, id):
        if id in self.listeners.keys():
            event = self.listeners[Event.id]
            self.listeners[Event.id] = None
            self.observers[event.name].remove(event.callback)

    def stop(self):
        if self._timer != None:
            self._timer.cancel()

event = Event()

if __name__ == "__main__":
    print("hello")
    event = Event()

    def func1(*args, **kwargs):
        print("func1")
        print(args)
        print(kwargs)

    def func2(*args, **kwargs):
        print("func2")
        print(args)
        print(kwargs)

    def func3(*args, **kwargs):
        print("func3")
        print(args)
        # print(kwargs)

    id = event.on("event1", func1)
    print("id====" + str(id))
    event.emit("event1", 1, 10, 100)
    id = event.on("event1", func2)
    print("id====" + str(id))
    event.emit("event1", 2, a = 20, b = 100)
    id = event.on("event3", func3)
    print("id====" + str(id))
    event.emit("event3", 3, D = 1)

    def func5(*args, **kwargs):
        print("func5")
        print(args)
        print(kwargs)

    def func4():
        id = event.on("event4", func5)
        print("id====" + str(id))
        event.emit("event4")

    t = Timer(1, func4)
    t.start()