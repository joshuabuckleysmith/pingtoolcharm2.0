import os
from app import pingcomponents
from app import logger
from app import outputboxprinter
from app import pingstatsgen

stats = pingstatsgen.getstats
outlog = outputboxprinter.outlog.set
wlog=logger.log.writelogline

wlog("imported killthread")

def killthread(buttondis, buttonen):
    pingcomponents.pingcomponents["threadkilled"] = 1
    wlog("in killthread, threadkilled = {}".format(pingcomponents.pingcomponents["threadkilled"]))
    #should disable cancel and enable ping
    buttondis['state'] = 'disabled'
    buttonen['state'] = 'normal'
    outlog(stats())
    outlog("===================")
    try:
        process = pingcomponents.pingcomponents["process"]
    except:
        pass
    try:
        os.system("TASKKILL /F /PID {} /T > nul".format(process))
    except:
        pass

    wlog("in killthread after taskkill threadkilled = {}".format(pingcomponents.pingcomponents["threadkilled"]))
    pingcomponents.pingcomponents["generatestats"] = 0
    os.system("del 1\\temp{}.txt > nul".format(pingcomponents.pingcomponents["UTCIdentity"]))
