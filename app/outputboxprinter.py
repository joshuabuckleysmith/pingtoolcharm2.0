from app import logger
wlog=logger.log.writelogline

wlog("imported pingprint")

class Outbox:
    def __init__(self):
        self.boxoutput = ""
        self.completeoutput = ""

    def get(self):
        a = self.boxoutput
        self.boxoutput = ""
        wlog("outbox returned a {}".format(a))
        return a

    def set(self, boxstr):
        boxstr = str(boxstr)
        self.boxoutput = self.boxoutput + boxstr + "\n"
        wlog("outbox is primed with = {}".format(self.boxoutput))

    def clear(self):
        wlog("outbox was cleared")
        self.boxoutput = ""

outbox=Outbox()




class Outlog:
    def __init__(self):
        self.logoutput = ""
        self.completeoutput = ""

    def get(self):
        a = self.logoutput
        self.logoutput = ""
        wlog("logoutput returned a {}".format(a))
        return a

    def set(self, logstr):
        logstr = str(logstr)
        self.logoutput = self.logoutput + logstr + "\n"
        wlog("outlog is primed with = {}".format(self.logoutput))

    def clear(self):
        wlog("outlog was cleared")
        self.logoutput = ""

outlog=Outlog()
