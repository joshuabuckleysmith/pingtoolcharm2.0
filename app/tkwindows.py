import collections
import os
import tkinter as tk
from tkinter import ttk
from time import sleep
from app import pingcomponents
from app import killthread
from app import sp
from app import startasthread
from app import logger
from app import outputboxprinter
from app import pingstatsgen


root = tk.Tk()
style = ttk.Style()
style.theme_use('clam')
style.configure('Gray.TRadiobutton',    # First argument is the name of style. Needs to end with: .TRadiobutton
        background='#EFEFEF',         # Setting background to our specified color above
        foreground='#FFFFFF')


outstats = pingstatsgen.getstats
wlog=logger.log.writelogline
rlog=logger.log.readlog
outboxget = outputboxprinter.outbox.get
outboxset = outputboxprinter.outbox.set
outlogget = outputboxprinter.outlog.get
outlogset = outputboxprinter.outlog.set
outboxclear = outputboxprinter.outbox.clear
outlogclear = outputboxprinter.outlog.clear

startreleasedicon = tk.PhotoImage(file="SE.png")
startrollovericon = tk.PhotoImage(file="SE.png")
startpressedicon = tk.PhotoImage(file="SR.png")
cancelreleasedicon = tk.PhotoImage(file="CE.png")
cancelrollovericon = tk.PhotoImage(file="CE.png")
cancelpressedicon = tk.PhotoImage(file="CR.png")

pingcomponents.pingcomponents["startreleasedicon"] = startreleasedicon


test = tk.StringVar()
pingnumber = tk.IntVar()
pingnumber.set(200)
mtu = tk.StringVar()
hmtu = tk.StringVar()
store = tk.StringVar()
prefix = tk.StringVar()
mturadio = tk.StringVar()
rate = tk.IntVar()
rate.set(1)
prefix.set("")
logoutput = tk.StringVar()
storetxt = tk.Label(text="Store Number")
wlog("vars set")
arial = ("Arial", "10")
consolas = ("Fira Code", 8)
consolas = ("Sans", 8)
arial = consolas
bgcolor = "#FFFFFF"
fgcolor = "#000000"

options = collections.OrderedDict(
    [
        ("Select Device...", ""),("IP or Name", ""),
        ("Routger(dg)", "dg"),
        ("Switch US(ussw010)", "ussw010"),
        ("Switch Canada(casw010)", "casw010"),
        ("Register US(usrg010)", "usrg010"),
        ("Register Canada(carg010)", "carg010"),
        ("Workstation(mws)", "mws"),
        ("Workstation(bo)", "bo"),
        ("FoH Switch(ussw030)", "ussw030")
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
    storetxt.place(x=8, y=10)
    pingtxt = tk.Label(text="Ping Number")  # Ping test labels for text boxes.
    pingtxt.place(x=106, y=10)
    mtutxt = tk.Label(text="MTU")  # Ping test labels for text boxes.
    hmtutxt = tk.Label(text="MTU")  # Ping test labels for text boxes.

    storeentry = ttk.Entry(root, textvariable=store) # Entry box for store number for ip address
    storeentry.insert(tk.END, "::1")
    storeentry.config(width=12)
    storeentry.place(x=10, y=30)
    pingentry = ttk.Entry(textvariable=pingnumber) # Entry box for ping number
    pingentry.config(width=11)
    pingentry.place(x=109, y=30)

    mtuentry = ttk.Entry(textvariable=mtu) # Entry box for mtu
    mtuentry.config(width=6)
    mtuentry.insert(tk.END, "1345")
    hmtuentry = ttk.Entry(textvariable=hmtu) # Entry box for high mtu
    hmtuentry.config(width=6)
    hmtuentry.insert(tk.END, "4000")
    mturadiobutton = ttk.Radiobutton(text="", variable=mturadio, value="primary", style="Gray.TRadiobutton")
    highmtubutton = ttk.Radiobutton(text="", variable=mturadio, value="secondary", style="Gray.TRadiobutton")

    mtuentry.place(x=10, y=108)  # right high
    hmtuentry.place(x=10, y=128) #right low
    mtutxt.place(x=8, y=88)
    #hmtutxt.place(x=9, y=145)
    mturadiobutton.place(x=52, y=108) #left high
    highmtubutton.place(x=52, y=128) #left low
    mturadio.set("primary")

    dropout = ttk.OptionMenu(root, prefix, *options) # dropdown for ping choices
    dropout.config(width=23)
    #dropout.nametowidget(dropout.menuname).config(font=arial)
    dropout.place(x=10, y=52)

    #testbutton.place(x=80, y=150)


    #==============================================================# Runs sp command when start is clicked
    def spf(*args):
        wlog("spf run")
        pingcomponents.pingcomponents["pingrunningforicons"] = True
        ping.config(state="disabled")

        ping.config(image=cancelreleasedicon)
        outputbox.delete(index1=(1.0), index2=tk.END)
        statsoutputbox.delete(index1=(1.0), index2=tk.END)
        outboxclear()
        outlogclear()
        ping.config(command=killthreadf)
        ratesent = rate.get()
        if ratesent == 3:
            ratesent = 5
        if ratesent == 4:
            ratesent = 30
        sp.sp(store.get(), mturadio.get(), pingnumber.get(), ping, cancelping, prefix.get(), options, storetxt, mtu.get(), hmtu.get(), ratesent)

    pingcomponents.pingcomponents["pingfunction"]=spf


    ping = tk.Button(image=startreleasedicon, command=spf, relief='sunken', border=0)  # Button runs SPF
    ping.place(x=108, y=96)
    pingcomponents.pingcomponents["pingbutton"] = ping

    def buttenter(*args):
        if pingcomponents.pingcomponents["pingrunningforicons"] == False:
            ping.config(image=startrollovericon)
        if pingcomponents.pingcomponents["pingrunningforicons"] == True:
            ping.config(image=cancelrollovericon)
    def buttleave(*args):
        if pingcomponents.pingcomponents["pingrunningforicons"] == False:
            ping.config(image=startreleasedicon)
        if pingcomponents.pingcomponents["pingrunningforicons"] == True:
            ping.config(image=cancelreleasedicon)
    def buttpress(*args):
        if pingcomponents.pingcomponents["pingrunningforicons"] == False:
            ping.config(image=startpressedicon)
        if pingcomponents.pingcomponents["pingrunningforicons"] == True:
            state = str(ping['state'])
            if state == 'active':
                ping.config(image=cancelpressedicon)
    def buttrelease(*args):
        if pingcomponents.pingcomponents["pingrunningforicons"] == False:
            ping.config(image=startreleasedicon)
        if pingcomponents.pingcomponents["pingrunningforicons"] == True:
            ping.config(image=cancelreleasedicon)


    ping.bind("<ButtonPress>", buttpress)
    ping.bind("<ButtonRelease>", buttrelease)
    ping.bind("<Enter>", buttenter)
    ping.bind("<Leave>", buttleave)


    # ==============================================================# Runs killthread when cancel is clicked
    def killthreadf():
        ping.config(image=cancelpressedicon)
        pingcomponents.pingcomponents["pingbutton"].config(state="disabled")
        ping.config(command=spf)
        wlog("killthreadf run")
        killthread.killthread(ping, pingcomponents.pingcomponents["rate"])
    cancelping = ttk.Button(image = cancelreleasedicon, command=killthreadf) #Cancel button
    cancelping['state'] = 'disabled'
    pingcomponents.pingcomponents["killfunction"] = killthreadf
    pingcomponents.pingcomponents["cancelbutton"] = cancelping
    #cancelping.place(x=160, y=180)


    #===============================================================
    wlog("loggingwindow run")
    statsoutputbox = tk.Text(root, height=5, width=65, font="Consolas 8", bg=bgcolor)
    statsoutputbox.place(x=200, y=15)
    statsoutputbox.see("end")
    outputboxx = 300
    outputboxy = 100
    outputbox = tk.Text(root, height=7, width=65, font="Consolas 8", bg=bgcolor)
    outputbox.place(x=200, y=100)
    outputbox.see("end")
    scrol2 = ttk.Scrollbar(root, command=outputbox.yview)
    scrol2.place(x=outputboxx+378, y=outputboxy, height=104)


    #================================================================== rate slider
    ratetext=tk.StringVar()
    ratetext.set("1")
    rateslider = tk.Scale(root, from_=1, to=4, variable=rate, showvalue = 0, orient=tk.HORIZONTAL)
    def rateupdate():
        while True:
            if rate.get()==1:
                ratetext.set("Slow")
            if rate.get()==2:
                ratetext.set("Medium")
            if rate.get()==3:
                ratetext.set("Fast")
            if rate.get()==4:
                ratetext.set("Very Fast")
            sleep(0.1)
    ratelabel = tk.Label(root, textvariable=ratetext)
    ratelabel.place(x=10, y=160)
    rateslider.place(x=10, y=180)
    startasthread.startasthread(rateupdate)


    #========================================outputs realtime ping data
    def outputboxf(outputbox):
        while True:
            a = outboxget()
            if a != "":
                outputbox.insert(tk.END, a)
                outputbox.see(tk.END)
            sleep(0.1)

    def statsoutputboxf2(outputbox2): # outputs realtime ping statistics
        b = ""
        while True:
            a = outstats()
            if a != b:
                if a != "":
                    outputbox2.delete(index1=(1.0), index2=tk.END)
                    outputbox2.insert(tk.END, a)
                    b = a
            sleep(0.1)

    pingcomponents.pingcomponents["statsoutputbox"] = statsoutputbox
    pingcomponents.pingcomponents["outputbox"] = outputbox
    outputboxthread = startasthread.T(target=outputboxf, args=[outputbox])
    outputboxthread.start()
    outputboxthread2 = startasthread.T(target=statsoutputboxf2, args=[statsoutputbox])
    outputboxthread2.start()
    #====================================runs a quick self test
    outboxset("Testing...")


    sp.sp("::1", "primary", "1", ping, cancelping, "IP or Name", options, storetxt, "1345",
          "4000", 1)



    #================================================================================== Logging window
    logout=tk.Toplevel()
    logout.title("Starbucks Ping Log Window")
    loggingwindow = tk.Text(logout, height=40, width=80, font="Consolas 10")
    loggingwindow.grid(row=0, column=0)
    loggingwindow.see("end")
    scrollb = ttk.Scrollbar(logout, command=loggingwindow.yview)
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
    root.geometry('{}x{}'.format(610,210))
    #root.configure(bg=bgcolor)
    root.mainloop()
