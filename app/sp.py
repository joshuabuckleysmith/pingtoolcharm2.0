from datetime import datetime
from app import startasthread
from app import startping
from app import pingcomponents
from app import logger
wlog=logger.log.writelogline

def sp(a, b, c, d, e, f, g, h, i, j):
    wlog("sp defined")
    '''a store.get(), b test.get(), c pingnumber.get(), d ping, e cancelping, f prefix.get(), g options, h storetxt'''
    c=int(c)
    pingcomponents.pingcomponents["store"] = a
    pingcomponents.pingcomponents["test"] = b
    pingcomponents.pingcomponents["pingnumber"] = c
    pingcomponents.pingcomponents["prefix"] = f
    pingcomponents.pingcomponents["UTCIdentity"] = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    pingcomponents.pingcomponents["lowmtu"] = i
    pingcomponents.pingcomponents["highmtu"] = j
    pingcomponents.pingcomponents["generatestats"] = 1
    wlog("startping runs this point")
    startasthread.startasthread(startping.startping(a, b, c, d, e, f, g, h))