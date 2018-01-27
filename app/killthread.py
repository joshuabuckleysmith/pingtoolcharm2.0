import os
from app import pingcomponents
from app import logger
from app import outputboxprinter
from app import pingstatsgen

stats = pingstatsgen.getstats
outlog = outputboxprinter.outlog.set
wlog=logger.log.writelogline

wlog("imported killthread")

def killthread(button):

    pingcomponents.pingcomponents["threadkilled"] = 1
    wlog("in killthread, threadkilled = {}".format(pingcomponents.pingcomponents["threadkilled"]))
    #should disable cancel and enable ping
    #buttondis['state'] = 'disabled'
    #buttonen['state'] = 'normal'
    button.config(command=killthread)
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
    pingcomponents.pingcomponents["pingbutton"].config(state="active")
    wlog("in killthread after taskkill threadkilled = {}".format(pingcomponents.pingcomponents["threadkilled"]))
    pingcomponents.pingcomponents["generatestats"] = 0
    pingcomponents.pingcomponents["pingrunningforicons"] = False
    pingcomponents.pingcomponents["pingbutton"].config(command=pingcomponents.pingcomponents["pingfunction"])

    os.system("del 1\\temp{}.txt > nul".format(pingcomponents.pingcomponents["UTCIdentity"]))
