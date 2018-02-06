from subprocess import Popen
import math
from time import sleep
from app import logger
from app import outputboxprinter
from datetime import datetime

wlog=logger.log.writelogline
outbox = outputboxprinter.outbox.set
outlog = outputboxprinter.outlog.set
wlog("imported pinger")


from app import printer, startasthread, pingcomponents

def pinger(store, pingnumber, primsec, buttondis, buttonen, prefix, rate):
    actualpingnumber = pingnumber
    pingnumber = 1
    '''Takes a store number, index as INT, primsec as STRING sets primary or secondary test'''
    wlog("pinger starting")
    wlog("resetting killed thread tracking to 0")
    pingcomponents.pingcomponents["threadskilled"] = 0
    lowmtu = pingcomponents.pingcomponents["lowmtu"]
    highmtu = pingcomponents.pingcomponents["highmtu"]
    displayconfirmationline = "Pinging {}{} {} times:".format(prefix, store, pingnumber)
    wlog("pinger is displaying confirmation line which is {}".format(displayconfirmationline))
    if pingcomponents.pingcomponents["startupsuccessful"] == 0:
        outlog("============Log=============")
    outlog("{}".format(datetime.now()))
    if pingcomponents.pingcomponents["startupsuccessful"] == 0:
        outlog("============================")
    if pingcomponents.pingcomponents["startupsuccessful"] == 1:
        outbox(displayconfirmationline)
        outlog(displayconfirmationline)
    pingcomponents.pingcomponents["loggingwindow"] = pingcomponents.pingcomponents["loggingwindow"][0:-len(displayconfirmationline)]


    if primsec == "primary":
        mtu = "{}".format(lowmtu)
    if primsec == "secondary":
        mtu = "{}".format(highmtu)

    pingthreads={}
    outputtolog = (
    "ping -n {} -l {} {}{}".format(pingnumber, mtu, prefix, store, pingcomponents.pingcomponents["UTCIdentity"]))
    outbox(outputtolog)
    print("actual number {}".format(actualpingnumber))
    if actualpingnumber/rate < 1:
        rate = actualpingnumber
    pingperthread = actualpingnumber/rate
    a, b = math.modf(pingperthread)
    print("a = {}, b = {}".format(a, b))
    remainingpings = round(a*rate)
    print("remaining pings = {}".format(remainingpings))
    pingperthreaddict = {}
    for i in range(1, rate+1):
        pingperthreaddict["{}".format(i)] = b
        if remainingpings > 0:
            pingperthreaddict["{}".format(i)] += 1
            remainingpings -= 1
    print("pingperthread number {}".format(pingperthread))
    print(pingperthreaddict["{}".format(1)])
    pingcomponents.pingcomponents["threadcount"] = rate

    for i in range(1, rate+1):
        print("creating thread {}".format(i))
        print('ping per thread in thread {} is {}'.format(pingperthreaddict[str(i)],pingperthreaddict[str(i)]))
        pingthreads[str(i)] = Popen("ping -n {} -l {} {}{} > 1\\temp{}.txt".format(pingperthreaddict[str(i)], mtu, prefix, store, pingcomponents.pingcomponents["UTCIdentity"]+str(i)), shell=True)
        pingcomponents.pingcomponents["process{}".format(i)] = pingthreads[str(i)].pid
        pingcomponents.pingcomponents["generatestats{}".format(i)] = 1
        outputthread = startasthread.T(target=printer.printer, args=[pingthreads[str(i)], store, prefix, i, rate])
        outputthread.start()
        sleep(1/rate)

    pingcomponents.pingcomponents["pingbutton"].config(state="active")
    if pingcomponents.pingcomponents["startupsuccessful"] == 0:
        pingcomponents.pingcomponents["pingbutton"].config(state="disabled")
        pingcomponents.pingcomponents["cancelbutton"].config(state="disabled")

    wlog("printer is started in its own thread here")
    #====================Output goes to printer from here. This thread goes down to the while loop below.

