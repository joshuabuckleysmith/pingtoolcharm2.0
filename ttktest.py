import tkinter as tk
from tkinter import ttk

root = tk.Tk()
store = tk.StringVar()
store.set("4444")
#store = "4444"
style = ttk.Style()
style.theme_use('clam')
scrol2 = ttk.Scrollbar(root)
scrol2.place(x=1, y=2, height=134)
storeentry = tk.Entry(root, textvariable=store) # Entry box for store number for ip address
storeentry.place(x=10, y=30)
texte=tk.Label(root, text="LEL")
texte.place(x=10, y=10)

root.mainloop()