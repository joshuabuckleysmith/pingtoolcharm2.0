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


def printer(monitoredthread, store, prefix, threadnumber, rate):
    if pingcomponents.pingcomponents["threadscomplete"] == 1:
        return
    wlog("printer running")
    outputstring = ""
    pingcount = 1
    threadrunning = 1
    while threadrunning < 3:
        sleep(0.1)
        if pingcomponents.pingcomponents["threadskilled"] == 0:
            wlog("printer is attempting to open the temp file")
            x=0
            while x <=30:
                try:
                    #print(x)
                    openfile = open("1\\temp{}.txt".format(pingcomponents.pingcomponents["UTCIdentity"]+str(threadnumber)), 'r')
                    break
                except:
                    pass
                sleep(1)
                x=x+1
            if x == 30:
                outboxset("parser failure, abandoning operation. Output is \n{}".format(outstats()))
                pingcomponents.pingcomponents["threadscomplete"] == 1
                return
        if pingcomponents.pingcomponents["threadskilled"] == 1:
            #bails out of this if the thread was killed by killthread
            pingcomponents.pingcomponents["generatestats{}".format(threadnumber)] = 0
            return
        openstring = str(openfile.read())
        openfile.close()
        if openstring == "Ping request could not find host {}{}. " \
                         "Please check the name and try again.\n".format(prefix, store):
            outboxset(
                "Ping request could not find host {}{}.\nIs your prefix correct? This is usually caused by entering "
                "an IP address when a store number is expected. When entering a store number, make sure to select "
                "a store device from the dropdown menu. If entering an IP address, select 'IP Address or Name'"
                "\nPlease start ping again when ready.\n".format(
                    prefix, store))
            outlogset(
                "Ping request could not find host {}{}.\nIs your prefix correct? This is usually caused by entering "
                "an IP address when a store number is expected. When entering a store number, make sure to select "
                "a store device from the dropdown menu. If entering an IP address, select 'IP Address or Name'"
                "\nPlease start ping again when ready.\n".format(
                    prefix, store))
            openfile.close()
            pingcomponents.pingcomponents["generatestats"] = 0
            return
        openstring = openstring.splitlines()[1+pingcount:2+pingcount]
        #print("openstring is {}".format(openstring))
        openstring = "".join(openstring)
        if openstring != "":
            pingcount = pingcount + 1
            pingcomponents.pingcomponents["count"] = pingcomponents.pingcomponents["count"] + 1
            if pingcomponents.pingcomponents["startupsuccessful"]==1:
                openstring = "{} {}".format(pingcomponents.pingcomponents["count"], openstring)
                outboxset(openstring)
                outlogset(openstring)
        th1 = monitoredthread.poll()
        wlog("polled monitored thread, it is {}".format(th1))
        #print(threadrunning)
        if threadrunning == 1:
            if th1 == 0:
                threadrunning = 2
                continue
        if threadrunning == 2:
            #print("th1 was 2")
            #print("printer is running, pinger thread ended just now".format(store))
            a = outstats(threadnumber)
            wlog("a is set to {}".format(a))
            pingcomponents.pingcomponents["statsoutputbox"].delete(index1=(1.0), index2=tk.END)
            pingcomponents.pingcomponents["statsoutputbox"].insert(tk.END, a)
            #pingcomponents.pingcomponents["loggingwindow"] += a+"\n"
            pingcomponents.pingcomponents["statsoutputbox"].insert(tk.END, "\n")

            if pingcomponents.pingcomponents["startupsuccessful"] == 0:
                #print("startupsuccessful was 0, setting to 1 and cleaning up")
                pingcomponents.pingcomponents["startupsuccessful"] = 1
                clearoutbox()
                wlog("get outbox returned ({})".format(getoutbox()))
                pingcomponents.pingcomponents["statsoutputbox"].delete(index1=(1.0), index2=tk.END)
                pingcomponents.pingcomponents["statsoutputbox"].insert(tk.END, "Ready")
                pingcomponents.pingcomponents["statsoutputbox"].insert(tk.END, "\n")
                pingcomponents.pingcomponents["outputbox"].delete(index1=(1.0), index2=tk.END)
                pingcomponents.pingcomponents["outputbox"].insert(tk.END, "Ready")
                pingcomponents.pingcomponents["outputbox"].insert(tk.END, "\n")
                pingcomponents.pingcomponents["pingrunningforicons"] = False
                pingcomponents.pingcomponents["pingbutton"].config(state="active")
                pingcomponents.pingcomponents["pingbutton"].config(
                    image=pingcomponents.pingcomponents["startreleasedicon"])
                pingcomponents.pingcomponents["pingbutton"].config(
                    command=pingcomponents.pingcomponents["pingfunction"])
                return


            pingcomponents.pingcomponents["generatestats{}".format(threadnumber)] = 0
            wlog("output thread has ended, no action after here?")


            completedthreads = 0
            for i in range (1, rate+1):
                if pingcomponents.pingcomponents["generatestats{}".format(i)] == 0:
                    completedthreads += 1
                    #print("completedthreads = {}, range was = {}".format(completedthreads, rate))
                    if completedthreads == rate:
                        pingcomponents.pingcomponents["threadscomplete"] = 1
                        #print("comp threads = range")
                        pingcomponents.pingcomponents["pingrunningforicons"] = False
                        pingcomponents.pingcomponents["pingbutton"].config(state="active")
                        pingcomponents.pingcomponents["pingbutton"].config(
                            image=pingcomponents.pingcomponents["startreleasedicon"])
                        pingcomponents.pingcomponents["pingbutton"].config(
                            command=pingcomponents.pingcomponents["pingfunction"])
                        outlogset("\nPing Complete\n")
                        outlogset("===================")
                        outboxset("Ping Complete\n")
                        outlogset(a)
                        break

            break
