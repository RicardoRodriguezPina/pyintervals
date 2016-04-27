"""
Python activities scheduled in intervals.
The time for running is not fixed, if the work takes long time
the next run will be the finish time plus the interval.
PyIntervals lets you run Python functions (or any other
callable)  at pre-determined intervals using a simple syntax.
Features:
    - Works with Python 2.7 and I guess 3.3
Usage:
    >>> from pyintervals import *
    >>> 
    >>> def tet(peyo=''):
    >>>     print peyo
    >>> 
    >>> w = Work()
    >>> w.every(2).minutes
    >>> w.do(tet, peyo='I`m Running every 2 minutes')
    >>> 
    >>> w2 = Work()
    >>> w2.every().time('10:00')
    >>> w2.do(tet, peyo='I`m running every day at 10:00')
    >>> 
    >>> w3 = Work()
    >>> w3.every('wednesday').at_time('10:00')
    >>> w3.do(tet, peyo='I`m running every wednesday at 10:00')
    >>> 
    >>> w4 = Work()
    >>> w4.every(1).hours
    >>> w4.do(tet, peyo='I`m running every hour')
    >>> 
    >>> w5 = Work()
    >>> w5.every(30).seconds
    >>> w5.do(tet, peyo='I`m running every 30 seconds')
    >>> 
    >>> 
    >>> mySdlMgr = ScheduleManager()
    >>> 
    >>> mySdlMgr.addWork(w)
    >>> mySdlMgr.addWork(w2)
    >>> mySdlMgr.addWork(w3)
    >>> mySdlMgr.addWork(w4)
    >>> mySdlMgr.addWork(w5)
    >>> mySdlMgr.runAll()
"""
from datetime import datetime
import time
import functools
import re
import threading


INT_RE = re.compile(r"^[-]?\d+$")

class Interval(object):
    """An interval used by `PyInterval`."""
    
    def ItisInt(self, s):
        return INT_RE.match(str(s)) is not None

    def __init__(self):
        self.unit = None
        self.period = None
        self.at_time_sdl = {}
        self.times = None
        self.last_time_run = None
        self.isWeek = False

    def every(self, times=None):
        self.last_time_run = None
        self.isWeek = False == self.ItisInt(times)
        if self.isWeek:
            self.unit = times
            if self.unit == 'monday':
                self.period = 0
            if self.unit ==  'tuesday':
                self.period = 1
            if self.unit ==  'wednesday':
                self.period = 2
            if self.unit ==  'thursday':
                self.period = 3
            if self.unit ==  'friday':
                self.period = 4
            if self.unit ==  'saturday':
                self.period = 5
            if self.unit ==  'sunday':
                self.period = 6
            return self
        else:
            self.times = times
        return self

    @property
    def seconds(self):
        if not  self.isWeek:
            self.last_time_run = int(time.time())
            self.unit = 'seconds'
            self.period = self.times * 1

    @property
    def minutes(self):
        if not  self.isWeek:
            self.last_time_run = int(time.time())
            self.unit = 'minutes'
            self.period = self.times * 60

    @property
    def hours(self):
        if not  self.isWeek:
            self.last_time_run = int(time.time())
            self.unit = 'hours'
            self.period = self.times * 60 * 60

    @property
    def days(self):
        if not  self.isWeek:
            self.last_time_run = int(time.time())
            self.unit = 'days'
            self.period = self.times * 60 * 60 * 24

    
    def time(self, ats='00:00'):
        self.unit = 'time'
        self.period = None
        self.last_time_run = None
        hour, minute = ats.split(':')
        hour = int(hour)
        assert 0 <= hour <= 23
        minute = int(minute)
        assert 0 <= hour <= 23
        self.at_time_sdl['minute'] = minute
        self.at_time_sdl['hour'] = hour

    def at_time(self, ats='00:00'):
        self.last_time_run = None
        hour, minute = ats.split(':')
        hour = int(hour)
        assert 0 <= hour <= 23
        minute = int(minute)
        assert 0 <= minute <= 59
        self.at_time_sdl['minute'] = minute
        self.at_time_sdl['hour'] = hour


class Work(object):
    def __init__(self):
        self.interval = Interval()
        self._func = None
        self.ImBusy = False


    def every(self, inter=None):
        return self.interval.every(inter)

    def do(self, work_func, *args, **kwargs):
        self._func = functools.partial(work_func, *args, **kwargs)
        try:
            functools.update_wrapper(self._func, work_func)
        except AttributeError:
            pass

    def run(self):
        self.ImBusy = True
        if self.interval.unit in ['seconds', 'minutes', 'hours', 'days']:
            if self.interval.last_time_run == None:
                self._func()
                self.interval.last_time_run = int(time.time())
            elif (int(time.time()) - self.interval.last_time_run) > self.interval.period:
                self._func()
                self.interval.last_time_run = int(time.time())
        elif self.interval.unit == 'time':
            currentMinute= datetime.now().minute
            currentHour = datetime.now().hour
            currentDay = datetime.now().day
            if currentMinute >= self.interval.at_time_sdl['minute'] and self.interval.at_time_sdl['hour']==currentHour and self.interval.last_time_run != currentDay:
                self._func()
                self.interval.last_time_run = currentDay
        elif self.interval.unit in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            currentMinute= datetime.now().minute
            currentHour = datetime.now().hour
            currentDay = datetime.now().day
            currentWeekDay = datetime.now().weekday()
            if currentMinute >= self.interval.at_time_sdl['minute'] and self.interval.at_time_sdl['hour']==currentHour and self.interval.period == currentWeekDay and self.interval.last_time_run != currentDay:
                self._func()
                self.interval.last_time_run = currentDay
        self.ImBusy = False


class ScheduleManager(object):
    def __init__(self):
        self.works = []

    def addWork(self, wrk):
        self.works.append(wrk)

    def runAll(self):
        while True:
            for i in self.works:
                t = threading.Thread(target=i.run())
                t.start()
            time.sleep(1)
     

        




