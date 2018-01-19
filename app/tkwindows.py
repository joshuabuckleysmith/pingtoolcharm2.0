import collections
import os
import tkinter as tk
from time import sleep
from app import pingcomponents
from app import killthread
from app import sp
from app import startasthread
from app import logger
from app import outputboxprinter
from app import pingstatsgen


outstats = pingstatsgen.getstats
wlog=logger.log.writelogline
rlog=logger.log.readlog
outboxget = outputboxprinter.outbox.get
outboxset = outputboxprinter.outbox.set
outlogget = outputboxprinter.outlog.get
outlogset = outputboxprinter.outlog.set
outboxclear = outputboxprinter.outbox.clear
outlogclear = outputboxprinter.outlog.clear
root = tk.Tk()
starticon = tk.PhotoImage(file="start.png")
cancelicon = tk.PhotoImage(file="cancel.png")
test = tk.StringVar()
pingnumber = tk.IntVar()
mtu = tk.IntVar()
hmtu = tk.IntVar()
store = tk.StringVar()
prefix = tk.StringVar()
prefix.set("IP Address")
logoutput = tk.StringVar()
storetxt = tk.Label(text="Store Number")
wlog("vars set")
options = collections.OrderedDict(
    [
        ("IP Address", ""), ("Router(dg)", "dg"),
        ("Switch US(ussw010)", "ussw010"),
        ("Switch Canada(casw010)", "casw010"),
        ("Workstation(mws)", "mws"), ("FoH Switch(ussw030)", "ussw030")
    ]
)


#=======================================
def updatetext(button2): #for ipaddress
    wlog("updatetext")
    button2['text'] = "Store Number"


#=======================================
def downdatetext(button2):  # for store number
    wlog("downdatetext")
    button2['text'] = "IP Address"


#=======================================
def destroyapp():
    wlog("downdatetext")
    os.system("del 1\* /s /q")
    root.destroy()


#=======================================creates TK window
def buttons():
    wlog("buttons from tkwindows")
    '''creates tk window'''
    storetxt = tk.Label(text="Store Number")  # Ping test labels for text boxes.
    storetxt.place(x=10, y=5)
    pingtxt = tk.Label(text="Ping Number")  # Ping test labels for text boxes.
    pingtxt.place(x=150, y=5)
    mtutxt = tk.Label(text="Default MTU")  # Ping test labels for text boxes.
    mtutxt.place(x=10, y=100)
    hmtutxt = tk.Label(text="Alternate MTU")  # Ping test labels for text boxes.
    hmtutxt.place(x=150, y=100)
    storeentry = tk.Entry(root, textvariable=store) # Entry box for store number for ip address
    storeentry.place(x=10, y=30)
    pingentry = tk.Entry(textvariable=pingnumber) # Entry box for ping number
    pingentry.place(x=150, y=30)
    mtuentry = tk.Entry(textvariable=mtu) # Entry box for mtu
    mtuentry.place(x=10, y=120)
    hmtuentry = tk.Entry(textvariable=hmtu) # Entry box for high mtu
    hmtuentry.place(x=150, y=120)
    dropout = tk.OptionMenu(root, prefix, *options) # dropdown for ping choices
    dropout.place(x=7, y=50)
    testbutton = tk.Checkbutton\
        (text="Use Alternate Mtu", variable=test, onvalue="secondary",
        offvalue="primary", )                           # dropdown for mtu choices
    testbutton.deselect()
    testbutton.place(x=80, y=150)


    #==============================================================# Runs sp command when start is clicked
    def spf(*args):
        wlog("spf run")
        outputbox.delete(index1=(1.0), index2=tk.END)
        statsoutputbox.delete(index1=(1.0), index2=tk.END)
        outboxclear()
        outlogclear()
        sp.sp(store.get(), test.get(), pingnumber.get(), ping, cancelping, prefix.get(), options, storetxt, mtu.get(), hmtu.get())

    ping = tk.Button(image = starticon,  command=spf, bg="white", border = "0", relief="flat") # Button runs SPF
    ping.place(x=20, y=200)


    # ==============================================================# Runs killthread when cancel is clicked
    def killthreadf():
        wlog("killthreadf run")
        killthread.killthread(cancelping, ping)


    cancelping = tk.Button(image = cancelicon, command=killthreadf, bg = "white", border = "0") #Cancel button
    cancelping['state'] = 'disabled'
    cancelping.place(x=160, y=200)
    wlog("loggingwindow run")
    statsoutputbox = tk.Text(root, height=5, width=65, font="Consolas 8")
    statsoutputbox.place(x=300, y=15)
    statsoutputbox.see("end")
    outputboxx = 300
    outputboxy = 100
    outputbox = tk.Text(root, height=16, width=65, font="Consolas 8")
    outputbox.place(x=300, y=100)
    outputbox.see("end")
    scrol2 = tk.Scrollbar(root, command=outputbox.yview, )
    scrol2.place(x=outputboxx+378, y=outputboxy, height=212)


    #========================================outputs realtime ping data
    def outputboxf(outputbox):
        while True:
            a = outboxget()
            if a != "":
                outputbox.insert(tk.END, a)
                outputbox.see(tk.END)
            sleep(0.5)

    def statsoutputboxf2(outputbox2): # outputs realtime ping statistics
        b = ""
        while True:
            a = outstats()
            if a != b:
                if a != "":
                    outputbox2.delete(index1=(1.0), index2=tk.END)
                    outputbox2.insert(tk.END, a)
                    b = a
            sleep(0.5)

    pingcomponents.pingcomponents["statsoutputbox"] = statsoutputbox
    pingcomponents.pingcomponents["outputbox"] = outputbox
    outputboxthread = startasthread.T(target=outputboxf, args=[outputbox])
    outputboxthread.start()
    outputboxthread2 = startasthread.T(target=statsoutputboxf2, args=[statsoutputbox])
    outputboxthread2.start()

    outboxset("Testing...")
    sp.sp("::1", "primary", "1", ping, cancelping, "IP Address", options, storetxt, "1345",
          "4000")


    #================================================================================== Logging window
    logout=tk.Toplevel()
    logout.title("Starbucks Ping Log Window")
    loggingwindow = tk.Text(logout, height=40, width=80, font="Consolas 10")
    loggingwindow.grid(row=0, column=0)
    loggingwindow.see("end")
    scrollb = tk.Scrollbar(logout, command=loggingwindow.yview)
    loggingwindow['yscrollcommand'] = scrollb.set
    scrollb.grid(row=0, column=1, sticky='nsew')


    # ================================================= logging function, updates logging window.
    def loggingwindowf(loggingwindow):
        while True:
            a = outlogget()
            if a != "":
                loggingwindow.insert(tk.END, a)
            sleep(0.5)

    loggingwindowdaemon = startasthread.T(target=loggingwindowf, args=[loggingwindow])
    loggingwindowdaemon.setDaemon(True)
    loggingwindowdaemon.start()


    #================================================================================== Verbose Logging window
    # verboselog=tk.Toplevel()
    # verboselog.title("Verbose Log Window")
    # verboseloggingwindow = tk.Text(verboselog, height=50, width=140, font="Consolas 10")
    # verboseloggingwindow.grid(row=0, column=0)
    # verboseloggingwindow.see("end")
    # verbosescrollb = tk.Scrollbar(verboselog, command=verboseloggingwindow.yview)
    # verboseloggingwindow['yscrollcommand'] = verbosescrollb.set
    # verbosescrollb.grid(row=0, column=1, sticky='nsew')
    #
    #
    # # ================================================= Verbose logging function, updates logging window.
    # def verboseloggingwindowf(verboseloggingwindow):
    #     while True:
    #         a = rlog()
    #         if a != "":
    #             verboseloggingwindow.insert(tk.END, a+"\n")
    #         sleep(2)
    #
    # verboseloggingwindowdaemon = startasthread.T(target=verboseloggingwindowf, args=[verboseloggingwindow])
    # verboseloggingwindowdaemon.setDaemon(True)
    # verboseloggingwindowdaemon.start()

    # ================================================== binds return to run pinger
    root.bind('<Return>', spf)
    root.title("Starbucks Ping")


    #=============================================== updates labels
    def textdaemonf(prefix, storetxt):
        wlog("textdaemonf run")
        while True:
            if prefix.get() == "IP Address":
                storetxt['text'] = "IP Address"
            if prefix.get() != "IP Address":
                storetxt['text'] = "Store Number"
            sleep(0.1)

    textdaemon = startasthread.T(target=textdaemonf, args=[prefix, storetxt])
    textdaemon.setDaemon(True)
    textdaemon.start()
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(710,330))
    root.mainloop()
