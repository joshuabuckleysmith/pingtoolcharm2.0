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

style = ttk.Style()
style.theme_use('clam')
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
startreleasedicon = tk.PhotoImage(file="startenabled.png")
startpressedicon = tk.PhotoImage(file="startdepressed.png")
cancelreleasedicon = tk.PhotoImage(file="cancel.png")
test = tk.StringVar()
pingnumber = tk.IntVar()
mtu = tk.StringVar()
hmtu = tk.StringVar()
store = tk.StringVar()
prefix = tk.StringVar()
mturadio = tk.StringVar()
prefix.set("Router(dg)")
logoutput = tk.StringVar()
storetxt = tk.Label(text="Store Number")
wlog("vars set")
arial = ("Arial", "10")
consolas = ("Consolas", 8)
arial = consolas
bgcolor = "#000000"
fgcolor = "#EEEEEE"
options = collections.OrderedDict(
    [
        ("Router(dg)", "dg"),
        ("Switch US(ussw010)", "ussw010"),
        ("Switch Canada(casw010)", "casw010"),
        ("Register US(usrg010)", "usrg010"),
        ("Register Canada(carg010)", "carg010"),
        ("Workstation(mws)", "mws"),
        ("FoH Switch(ussw030)", "ussw030"),
        ("IP Address", "")
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
    storetxt = ttk.Label(text="Store Number", font = arial, bg=bgcolor, fg=fgcolor)  # Ping test labels for text boxes.
    storetxt.place(x=10, y=10)
    pingtxt = tk.Label(text="Ping Number", font = arial, bg=bgcolor, fg=fgcolor)  # Ping test labels for text boxes.
    pingtxt.place(x=150, y=10)
    mtutxt = tk.Label(text="Default MTU", font = arial, bg=bgcolor, fg=fgcolor)  # Ping test labels for text boxes.
    mtutxt.place(x=30, y=94)
    hmtutxt = tk.Label(text="Alternate MTU", font = arial, bg=bgcolor, fg=fgcolor)  # Ping test labels for text boxes.
    hmtutxt.place(x=170, y=94)
    storeentry = tk.Entry(root, textvariable=store, font = consolas, bg=bgcolor, fg=fgcolor) # Entry box for store number for ip address
    storeentry.place(x=10, y=30)
    pingentry = tk.Entry(textvariable=pingnumber, font = consolas, bg=bgcolor, fg=fgcolor) # Entry box for ping number
    pingentry.place(x=150, y=30)
    mtuentry = tk.Entry(textvariable=mtu, font = consolas, bg=bgcolor, fg=fgcolor) # Entry box for mtu
    mtuentry.place(x=10, y=115)
    mtuentry.insert(tk.END, "1345")
    hmtuentry = tk.Entry(textvariable=hmtu, font = consolas, bg=bgcolor, fg=fgcolor) # Entry box for high mtu
    hmtuentry.place(x=150, y=115)
    hmtuentry.insert(tk.END, "4000")
    dropout = tk.OptionMenu(root, prefix, *options) # dropdown for ping choices
    dropout.config(font=arial, bg=bgcolor, fg=fgcolor)
    dropout.nametowidget(dropout.menuname).config(font=arial, bg=bgcolor, fg=fgcolor)
    dropout.place(x=7, y=50)
    mturadiobutton = tk.Radiobutton(text="", border=0, variable=mturadio, value="primary", bg=bgcolor, fg=fgcolor)
    mturadiobutton2 = tk.Radiobutton(text="", border=0, variable=mturadio, value="secondary", bg=bgcolor, fg=fgcolor)
    mturadiobutton.place(x=9, y=94)
    mturadiobutton2.place(x=149, y=94)
    mturadiobutton.select()
    #testbutton.place(x=80, y=150)


    #==============================================================# Runs sp command when start is clicked
    def spf(*args):
        wlog("spf run")
        outputbox.delete(index1=(1.0), index2=tk.END)
        statsoutputbox.delete(index1=(1.0), index2=tk.END)
        outboxclear()
        outlogclear()
        sp.sp(store.get(), mturadio.get(), pingnumber.get(), ping, cancelping, prefix.get(), options, storetxt, mtu.get(), hmtu.get())


    ping = tk.Button(image=startreleasedicon, relief = tk.SUNKEN, border="0", command=spf, bg=bgcolor, fg=fgcolor)  # Button runs SPF
    ping.place(x=0, y=130)

    def buttpress(*args):
        ping.config(image=startpressedicon)
    def buttrelease(*args):
        ping.config(image=startreleasedicon)

    ping.bind("<ButtonPress>", buttpress)
    ping.bind("<ButtonRelease>", buttrelease)


    # ==============================================================# Runs killthread when cancel is clicked
    def killthreadf():
        wlog("killthreadf run")
        killthread.killthread(cancelping, ping)
    cancelping = tk.Button(image = cancelreleasedicon, command=killthreadf, border ="2") #Cancel button
    cancelping['state'] = 'disabled'
    #cancelping.place(x=160, y=180)


    #===============================================================
    wlog("loggingwindow run")
    statsoutputbox = tk.Text(root, height=5, width=65, font="Consolas 8", bg=bgcolor)
    statsoutputbox.place(x=300, y=15)
    statsoutputbox.see("end")
    outputboxx = 300
    outputboxy = 100
    outputbox = tk.Text(root, height=10, width=65, font="Consolas 8", bg=bgcolor)
    outputbox.place(x=300, y=100)
    outputbox.see("end")
    scrol2 = tk.Scrollbar(root, command=outputbox.yview, bg=bgcolor)
    scrol2.place(x=outputboxx+378, y=outputboxy, height=134)


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
    scrollb = tk.Scrollbar(logout, command=loggingwindow.yview, bg=bgcolor)
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
    root.geometry('{}x{}'.format(710,260))
    root.configure(bg=bgcolor)
    root.mainloop()
