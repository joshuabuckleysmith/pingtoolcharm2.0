import threading
from app import testpingnumber
from app import pingcomponents
from app import pinger
from app import logger
from app import outputboxprinter
outbox = outputboxprinter.outbox.set
wlog=logger.log.writelogline

import IPy

T=threading.Thread

def startping(store, test, pingnumber, buttondis, buttonen, prefix, options, storetxt, rate):
    pingcomponents.pingcomponents["count"] = 0
    wlog("startping run")
    store = pingcomponents.pingcomponents["store"]
    pingnumber = pingcomponents.pingcomponents["pingnumber"]
    prefix = options[pingcomponents.pingcomponents["prefix"]]
    wlog("testing ping no")
    if testpingnumber.testpingnumber(pingnumber) == True:
        wlog("ping no tested true")
        if prefix != "":
            wlog("prefix is blank")
            wlog(store)
            store = (str(store).zfill(5))
            store = store[-5:]
            wlog(store)
        if prefix == "":
            try:
                IPy.IP(store)
            except:
                outbox("IP Address was invalid")
                return
        if pingnumber != 0:
            wlog("ping number was {}".format(pingnumber))
            buttonen['state'] = 'normal'
            buttondis['state'] = 'disabled'
            pingthread = T(target=pinger.pinger, args=[store, pingnumber, test, buttondis, buttonen, prefix, rate])
            pingthread.start()
            wlog("pingthread started")
        if pingnumber == 0:
            outbox("Can't ping zero times")
            #print("Can't ping zero times")
    else:
        #print('Number of pings was not a number.')
        outbox('Number of pings was not a number.')
        return