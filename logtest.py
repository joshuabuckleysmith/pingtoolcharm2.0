import tkinter as tk

root = tk.Tk()


photo = tk.PhotoImage(file="exit.png")
b = tk.Button(root, image=photo)
b.grid(row=10, column=10)

tk.mainloop()