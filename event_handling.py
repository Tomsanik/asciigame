from global_vars import gv

class Event:
    def __init__(self, obj, run):
        # run je [] s vypsanymy cas. Pri dovrseni casu se prepne (muzu delat blikani)
        self.obj = obj
        n = 0
        self.run = []
        for i in run:
            n += i
            self.run.append(n)
        self.used = False
        self.running = False

    def start(self):
        self.running = True
        for i in range(len(self.run)):
            self.run[i] += gv.timer
        self.use()

    def use(self):
        self.used = True

    def unuse(self):
        self.used = False


class EventChangeColor(Event):
    def __init__(self, obj, color, run):
        super().__init__(obj,run)
        self.color = color

    def use(self):
        self.used = True
        self.obj.color = self.color

    def unuse(self):
        self.used = False
        self.obj.color = self.obj.def_color


class EventChangeChar(Event):
    def __init__(self, obj, char, run):
        super().__init__(obj, run)
        self.char = char

    def use(self):
        self.used = True
        self.obj.char = self.char

    def unuse(self):
        self.used = False
        self.obj.char = self.obj.def_char


def handle_events(events, timer):
    for e in events:
        if (not e.running) or (e.run == []): continue
        if timer > min(e.run):
            if e.used: e.unuse()
            else: e.use()
            e.run.remove(min(e.run))
            print(e.run)
            if e.run == []:
                events.remove(e)
                del e
