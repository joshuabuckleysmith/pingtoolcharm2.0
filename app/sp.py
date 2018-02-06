from datetime import datetime
from app import startasthread
from app import startping
from app import pingcomponents
from app import logger
wlog=logger.log.writelogline

def sp(a, b, c, d, e, f, g, h, i, j, k):
    wlog("sp defined")
    '''a store.get(), b test.get(), c pingnumber.get(), d ping, e cancelping, f prefix.get(), g options, h storetxt, k rate'''
    c=int(c)
    pingcomponents.pingcomponents["store"] = a
    pingcomponents.pingcomponents["test"] = b
    pingcomponents.pingcomponents["pingnumber"] = c
    pingcomponents.pingcomponents["prefix"] = f
    pingcomponents.pingcomponents["UTCIdentity"] = str((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())
    pingcomponents.pingcomponents["lowmtu"] = i
    pingcomponents.pingcomponents["highmtu"] = j
    pingcomponents.pingcomponents["rate"] = k
    pingcomponents.pingcomponents["threadscomplete"] = 0
    pingcomponents.pingcomponents["threadskilled"] == 0
    pingcomponents.pingcomponents["pingrunningforicons"] = True
    wlog("startping runs this point")
    startasthread.startasthread(startping.startping(a, b, c, d, e, f, g, h ,k))