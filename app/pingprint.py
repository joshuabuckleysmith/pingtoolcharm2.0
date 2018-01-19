import re
import os
from app import pingcomponents
from app import logger
from app import pingstatsgen
from time import sleep
import subprocess

wlog=logger.log.writelogline
outstats = pingstatsgen.getstats



wlog("imported pingprint")

def pingprint(store):
    openfile = open("1\\temp{}.txt".format(pingcomponents.pingcomponents["UTCIdentity"]), 'r')
    wlog("pingprint starts here")
    wlog("pingprint received store which were {}".format(store))
    openstring = openfile.read()
    openfile.close()
    wlog("closed openfile")
    wlog("reading openfile yields {}".format(openstring))
    sent_total = 0
    received_total = 0
    lost_total = 0
    wlog("when pingprint starts, the open string was {}".format(openstring))
    try:
        received = re.compile('(?<=Reply from )')
        received = ((received.findall(openstring)))
        received2 = re.compile('(?<=PING:)')
        received2 = ((received2.findall(openstring)))
        received3 = re.compile('(?<=Request timed out)')
        received3 = ((received3.findall(openstring)))
        received = len(received)+len(received2)+len(received3)
    except:
        received = "0"
    try:
        sent = re.compile('(?<=Reply from )')
        sent = ((sent.findall(openstring)))
        sent2 = re.compile('(?<=PING:)')
        sent2 = ((sent2.findall(openstring)))
        sent3 = re.compile('(?<=Request timed out)')
        sent3 = ((sent3.findall(openstring)))
        sent = len(sent)+len(sent2)+len(sent3)
    except:
        sent = "0"
    try:
        lost = sent - received
    except:
        lost = "0"
    try:
        times = re.compile('(?<=time.)[0-9]*(?=ms)')
        times = ((times.findall(openstring)))
        timesints = []
        wlog("times is {}".format(times))
        try:
            for time in times:
                timesints.append(int(time))
        except:
            raise
        wlog("len times is {}".format(len(times)))
        if len(times) < 1:
            timesints.append(0)
            timesints.append(0)
            timesints.append(0)
        maxtime = max(timesints)
        mintime = min(timesints)
        sumtime = sum(timesints)
        lentime = len(timesints)
        avetime = int(sumtime / lentime)
    except:
        raise
    sent_total += int(sent)
    received_total += int(received)
    lost_total += int(lost)
    try:
        loss_total = int(round(lost_total / sent_total * 100))
    except:
        loss_total = "0"
    #print(
        '\nPing statistics for {}:\nPackets: Sent = {}, Received = {}, Lost = {} ({}% loss),\nApproximate round trip times in milli-seconds:\nMinimum = {}ms, Maximum = {}ms, Average = {}ms'.format(
            store, sent_total, received_total, lost_total, loss_total, mintime, maxtime, avetime))
    #print('\n')
    # a = outstats()
    # outputbox2.delete(index1=(1.0), index2=tk.END)
    # outputbox2.insert(tk.END, a)
    # outputbox2.insert(tk.END, "\n")
    #
    # os.system("del 1\\temp{}.txt > nul".format(pingcomponents.pingcomponents["UTCIdentity"]))

    wlog("deleted openfile")