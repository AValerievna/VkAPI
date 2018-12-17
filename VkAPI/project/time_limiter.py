from datetime import datetime


class TimeLimiter:
    def __init__(self, time_limit):
        self._start = datetime.now()
        self._time_limit = time_limit

    def check_time(self):
        if self._time_limit <= (datetime.now() - self._start).total_seconds():
            raise Exception("Run out of time!")
