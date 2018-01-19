import re
from app import pingcomponents
from app import logger

wlog=logger.log.writelogline
wlog = print
wlog("imported pingstatsgen")

def getstats():
    if pingcomponents.pingcomponents["generatestats"] == 1:
        try:
            openfile = open("1\\temp{}.txt".format(pingcomponents.pingcomponents["UTCIdentity"]), 'r')
        except:
            return ""
        store = pingcomponents.pingcomponents["store"]
        #wlog("store for stats was {}".format(store))
        #wlog("pingstatsgen starting, open file was opened OK")
        openstring = openfile.read()
        #wlog("pingstatsgenopenstring = {}".format(openstring))
        openfile.close()
        #wlog("pingstatsgenclosed openfile")
        #wlog("pingstatsgen reading openfile yields {}".format(openstring))
        sent_total = 0
        received_total = 0
        lost_total = 0
        #wlog("when pingstatsgen starts, the open string was {}".format(openstring))
        try:
            received = re.compile('(?<=Reply from )')
            received = ((received.findall(openstring)))
            received = len(received)
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
            #wlog("times is {}".format(times))
            try:
                for time in times:
                    timesints.append(int(time))
            except:
                raise
            #wlog("len times is {}".format(len(times)))
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
        #wlog("pingstatsgen is nearly done")
        sent_total += int(sent)
        received_total += int(received)
        lost_total += int(lost)
        try:
            loss_total = int(round(lost_total / sent_total * 100))
        except:
            loss_total = "0"
        stats = (
            'Ping statistics for {}:\nPackets: Sent = {}, Received = {}, Lost = {} ({}% loss),\nApproximate round trip times in milli-seconds:\nMinimum = {}ms, Maximum = {}ms, Average = {}ms'.format(
                store, sent_total, received_total, lost_total, loss_total, mintime, maxtime, avetime))
        return stats
    return ""