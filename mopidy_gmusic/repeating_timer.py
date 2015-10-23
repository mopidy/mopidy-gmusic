from threading import Event, Thread


class RepeatingTimer(Thread):
    def __init__(self, method, interval=0):
        Thread.__init__(self)
        self._stop_event = Event()
        self._interval = interval
        self._method = method

    def run(self):
        self._method()
        while self._interval > 0 and not self._stop_event.wait(self._interval):
            # wait for interval
            # call method over and over again
            self._method()

    def cancel(self):
        self._stop_event.set()
