from subprocess import Popen
from time import sleep
from app import logger
from app import outputboxprinter
from datetime import datetime

wlog=logger.log.writelogline
outbox = outputboxprinter.outbox.set
outlog = outputboxprinter.outlog.set
wlog("imported pinger")


from app import printer, startasthread, pingcomponents

def pinger(store, pingnumber, primsec, buttondis, buttonen, prefix):
    '''Takes a store number, index as INT, primsec as STRING sets primary or secondary test'''
    wlog("pinger starting")
    wlog("resetting killed thread tracking to 0")
    pingcomponents.pingcomponents["threadkilled"] = 0
    lowmtu = pingcomponents.pingcomponents["lowmtu"]
    highmtu = pingcomponents.pingcomponents["highmtu"]
    displayconfirmationline = "Pinging {}{} {} times:".format(prefix, store, pingnumber)
    wlog("pinger is displaying confirmation line which is {}".format(displayconfirmationline))
    outlog("{}".format(datetime.now()))
    outbox(displayconfirmationline)
    outlog(displayconfirmationline)
    pingcomponents.pingcomponents["loggingwindow"] = pingcomponents.pingcomponents["loggingwindow"][0:-len(displayconfirmationline)]
    if primsec == "primary":
        lowmtu = "{}".format(lowmtu)
        pingthread = Popen("ping -n {} -l {} {}{} > 1\\temp{}.txt".format(pingnumber, lowmtu, prefix, store, pingcomponents.pingcomponents["UTCIdentity"]), shell=True)
        outputtolog = ("ping -n {} -l {} {}{}".format(pingnumber, lowmtu, prefix, store, pingcomponents.pingcomponents["UTCIdentity"]))
    if primsec == "secondary":
        highmtu = "{}".format(highmtu)
        pingthread = Popen("ping -n {} -l {} {}{} > 1\\temp{}.txt".format(pingnumber, highmtu, prefix, store, pingcomponents.pingcomponents["UTCIdentity"]), shell=True)
        outputtolog = ("ping -n {} -l {} {}{}".format(pingnumber, highmtu, prefix, store,
                                                                      pingcomponents.pingcomponents["UTCIdentity"]))
    outbox(outputtolog)
    pingcomponents.pingcomponents["process"] = pingthread.pid
    wlog("printer is started in its own thread here")
    #====================Output goes to printer from here. This thread goes down to the while loop below.
    outputthread = startasthread.T(target=printer.printer, args=[pingthread, store, prefix])
    outputthread.start()
    wlog("output thread started, this is started in printer, pinger now just wait for the thread to end.")
    while True:
        threadalive2 = bool(outputthread.is_alive())
        sleep(0.2)
        if threadalive2 == False:
            buttondis['state'] = 'normal'  # reenables buttons when ping completes.
            buttonen['state'] = 'disabled'
            break