import os
from time import sleep
from app import pingcomponents
from app import logger
from app import pingstatsgen
from app import outputboxprinter

import tkinter as tk
wlog=logger.log.writelogline
outboxset = outputboxprinter.outbox.set
outlogset = outputboxprinter.outlog.set
clearoutbox = outputboxprinter.outbox.clear
clearoutlog = outputboxprinter.outlog.clear
getoutbox = outputboxprinter.outbox.get
getoutlog = outputboxprinter.outlog.get
outstats = pingstatsgen.getstats


def printer(monitoredthread, store, prefix):

    wlog("printer running")
    outputstring = ""
    pingcount = 1
    threadrunning = 1
    while threadrunning < 3:
        wlog("at the start of printer, threadrunning = {}".format(threadrunning))
        wlog("in printer, threadkilled = {}".format(pingcomponents.pingcomponents["threadkilled"]))
        wlog("pingcount is {}".format(pingcount))
        sleep(1)
        wlog("running printer, slept for 1 seconds")
        wlog("in printer after sleep, threadkilled = {}".format(pingcomponents.pingcomponents["threadkilled"]))
        if pingcomponents.pingcomponents["threadkilled"] == 0:
            wlog("printer is attempting to open the temp file")
            x=0
            while x <=2:
                try:
                    openfile = open("1\\temp{}.txt".format(pingcomponents.pingcomponents["UTCIdentity"]), 'r')
                except:
                    sleep(1)
                x=x+1
        if pingcomponents.pingcomponents["threadkilled"] == 1:
            pingcomponents.pingcomponents["threadkilled"] == 0
            #bails out of this if the thread was killed by killthread
            pingcomponents.pingcomponents["generatestats"] = 0
            return
        wlog("opened file is {}".format(openfile))
        openstring = str(openfile.read())
        wlog("PRINTER 47: Openstring created")
        openfile.close()
        wlog("PRINTER 48: opened string is {}".format(openstring))
        if openstring == "Ping request could not find host {}{}. " \
                         "Please check the name and try again.\n".format(prefix, store):
            outboxset(
                "Ping request could not find host {}{}.\nIs your prefix correct? "
                "\nPlease start ping again when ready.\n".format(
                    prefix, store))
            outlogset(
                "Ping request could not find host {}{}.\nIs your prefix correct? "
                "\nPlease start ping again when ready.\n".format(
                    prefix, store))
            openfile.close()
            pingcomponents.pingcomponents["generatestats"] = 0
            return
        openstring = openstring.splitlines()[1+pingcount:2+pingcount]
        wlog("openstring is {}".format(openstring))
        openstring = "".join(openstring)
        if openstring != "":
            openstring = "{} {}".format(pingcount, openstring)
            outboxset(openstring)
            outlogset(openstring)
            pingcount = pingcount + 1
        th1 = monitoredthread.poll()
        wlog("polled monitored thread, it is {}".format(th1))
        #print(threadrunning)
        if threadrunning == 1:
            if th1 == 0:
                #print("th1 was 1")
                threadrunning = 2
                continue
        if threadrunning == 2:
            #print("th1 was 2")
            wlog("printer is running, pinger thread ended just now".format(store))
            a = outstats()
            wlog("a is set to {}".format(a))
            pingcomponents.pingcomponents["statsoutputbox"].delete(index1=(1.0), index2=tk.END)
            pingcomponents.pingcomponents["statsoutputbox"].insert(tk.END, a)
            #pingcomponents.pingcomponents["loggingwindow"] += a+"\n"
            pingcomponents.pingcomponents["statsoutputbox"].insert(tk.END, "\n")
            outboxset("Ping Complete\n")
            outlogset("Ping Complete\n")
            outlogset(a)
            outlogset("===================")
            if pingcomponents.pingcomponents["startupsuccessful"] == 0:
                wlog("startupsuccessful was 0, setting to 1 and cleaning up")
                pingcomponents.pingcomponents["startupsuccessful"] = 1
                clearoutbox()

                wlog("get outbox returned ({})".format(getoutbox()))
                pingcomponents.pingcomponents["statsoutputbox"].delete(index1=(1.0), index2=tk.END)
                pingcomponents.pingcomponents["statsoutputbox"].insert(tk.END, "Ready")
                pingcomponents.pingcomponents["statsoutputbox"].insert(tk.END, "\n")
                pingcomponents.pingcomponents["outputbox"].delete(index1=(1.0), index2=tk.END)
                pingcomponents.pingcomponents["outputbox"].insert(tk.END, "Ready")
                pingcomponents.pingcomponents["outputbox"].insert(tk.END, "\n")
            os.system("del 1\\temp{}.txt > nul".format(pingcomponents.pingcomponents["UTCIdentity"]))
            pingcomponents.pingcomponents["pingrunningforicons"] = False
            pingcomponents.pingcomponents["pingbutton"].config(state="active")
            pingcomponents.pingcomponents["pingbutton"].config(image=pingcomponents.pingcomponents["startreleasedicon"])
            pingcomponents.pingcomponents["pingbutton"].config(command=pingcomponents.pingcomponents["pingfunction"])
            pingcomponents.pingcomponents["generatestats"] = 0
            wlog("output thread has ended, no action after here?")
            break
