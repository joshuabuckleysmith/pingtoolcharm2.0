import os
from app import pingcomponents
from app import logger
from app import outputboxprinter
from app import pingstatsgen
from app import startasthread
from subprocess import Popen

stats = pingstatsgen.getstats
outlog = outputboxprinter.outlog.set
wlog=logger.log.writelogline

wlog("imported killthread")

def killthread(button, rate):
    pingcomponents.pingcomponents["pingbutton"].config(state="disabled")
    button.config(command=killthread)
    outlog(stats())
    UTC = pingcomponents.pingcomponents["UTCIdentity"]
    def endprocesses():
        for i in range(1, rate+1):
            pingcomponents.pingcomponents["generatestats{}".format(i)] = 0
            Popen("TASKKILL /F /PID {} /T".format(pingcomponents.pingcomponents["process{}".format(i)]))
   #     for i in range(1, rate + 1):
            Popen("del 1\\temp{}{}.txt".format(UTC, str(i)))

    outlog("===================")
    startasthread.startasthread(endprocesses)
    pingcomponents.pingcomponents["threadskilled"] = 1

    pingcomponents.pingcomponents["pingbutton"].config(state="active")
    wlog("in killthread after taskkill threadskilled = {}".format(pingcomponents.pingcomponents["threadskilled"]))
    pingcomponents.pingcomponents["pingrunningforicons"] = False
    pingcomponents.pingcomponents["pingbutton"].config(command=pingcomponents.pingcomponents["pingfunction"])

