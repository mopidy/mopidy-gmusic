from threading import Event, Thread


class RepeatingTimer(Thread):
    def __init__(self, method, interval=0, start_after=0):
        Thread.__init__(self)
        self._stop_event = Event()
        self._interval = interval
        self._start_after = start_after
        self._method = method

    def run(self):
        if self._start_after > 0 and self._stop_event.wait(self._start_after):
            # stopped during start_after
            return
        # call method the first time
        self._method()
        while self._interval > 0 and not self._stop_event.wait(self._interval):
            # wait for interval
            # call method over and over again
            self._method()

    def cancel(self):
        self._stop_event.set()
