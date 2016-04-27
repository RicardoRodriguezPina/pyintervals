# pyintervals
Small Python library to schedule works in intervals

Usage
-----

.. code-block:: python

from pyintervals import *

def tet(peyo=''):
    print peyo
 
w = Work()
w.every(2).minutes
w.do(tet, peyo='I`m Running every 2 minutes')
 
w2 = Work()
w2.every().time('10:00')
w2.do(tet, peyo='I`m running every day at 10:00')
 
w3 = Work()
w3.every('wednesday').at_time('10:00')
w3.do(tet, peyo='I`m running every wednesday at 10:00')
 
w4 = Work()
w4.every(1).hours
w4.do(tet, peyo='I`m running every hour')
 
w5 = Work()
w5.every(30).seconds
w5.do(tet, peyo='I`m running every 30 seconds')
 
mySdlMgr = ScheduleManager()
 
mySdlMgr.addWork(w)
mySdlMgr.addWork(w2)
mySdlMgr.addWork(w3)
mySdlMgr.addWork(w4)
mySdlMgr.addWork(w5)
mySdlMgr.runAll()
