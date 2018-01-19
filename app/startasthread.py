import threading
T = threading.Thread
def startasthread(funct):
    thread = T(target=funct)
    thread.start()
