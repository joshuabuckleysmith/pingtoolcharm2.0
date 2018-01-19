from datetime import datetime

#
# logfile = "log.txt"
# file = open(logfile, "a")
# file.write("**********************")
# file.write("Application Launched\n")
#

class Log:
    def __init__(self):
        self.log = "Log Start"
        self.logoutput = ""
        self.logline = ""

    def readlog(self):
        # a = self.logoutput
        self.logoutput = ""
        # return a

    def writelogline(self, logstr):
        logstr = str(logstr)
        # self.logoutput = self.logoutput + "\n" + (str(datetime.utcnow())) + "  |  "
        # self.logoutput = self.logoutput + logstr
        # self.log = self.log + self.logoutput
        # file.write(self.logoutput)

log=Log()


#junos cloud router version 12.4
#pyramid


