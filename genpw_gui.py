from tkinter import Tk, Label, Button, StringVar, Entry, BooleanVar, \
    Checkbutton, E, W, END, TclError, messagebox

import genpw

genpw.TEXFRIENDLY = False
genpw.RECURSIVE = True

fenstarr = []


def fkt(event=None):
    global t1, myfont, mycolor, v1, v2, v3, v4
    try:
        if v1.get() == v2.get() == v3.get() == v4.get() is False or int(
                t1.get()) <= 0 or int(t1.get()) > 200:
            raise ValueError
        fenst = Tk()
        fenstarr.append(fenst)
        pw = genpw.main(int(t1.get()), v1.get(), v2.get(), v3.get(), v4.get())
        labe = Label(fenst, text=pw, font=myfont)

        def butto_com():
            fenst.clipboard_clear()
            fenst.clipboard_append(pw)

        butto = Button(
            fenst,
            text=" In Zwischenablage kopieren ",
            command=butto_com,
            font=myfont,
            highlightbackground=mycolor)
        labe.grid(row=0, columnspan=2, padx=25, pady=25)
        butto.grid(row=1, columnspan=2, padx=15, pady=(0, 20))
        fenst.wm_title("Generiertes Passwort")
        fenst.mainloop()
    except ValueError:
        messagebox.showerror("Fehler",
                             """Bitte mindestens einen Zeichenvorrat auswählen.
Die Länge muss zwischen 1 und 200 liegen.""")


myfont = ("Helvetica Neue Light", 15, "")
myfontItalic = ("Helvetica Neue Italic", 15, "")
mycolor = '#E0E0E0'
top = Tk()
msg = Label(
    top, text="""Wählen Sie den gewünschten Zeichenvorrat:""", font=myfont)
but = Button(
    top,
    text=" Generieren ",
    command=fkt,
    font=myfont,
    highlightbackground=mycolor)

l1 = Label(top, text="Zeichenvorrat", font=myfont)
l2 = Label(top, text="Länge", font=myfont)
# e1 = Entry(top,font=myfont)
t1 = StringVar()
e1 = Entry(top, font=myfont, width=4, textvariable=t1)


def cXfkt(event=None):
    if all([v1.get(), v2.get(), v3.get(), v4.get()]):
        c5.select()
    else:
        c5.deselect()


def c5fkt(event=None):
    if v5.get():
        c1.select()
        c2.select()
        c3.select()
        c4.select()
    else:
        c1.deselect()
        c2.deselect()
        c3.deselect()
        c4.deselect()


v1 = BooleanVar()
v2 = BooleanVar()
v3 = BooleanVar()
v4 = BooleanVar()
v5 = BooleanVar()
cl1 = Label(top, text="Kleinbuchstaben", font=myfont)
cl2 = Label(top, text="Großbuchstaben", font=myfont)
cl3 = Label(top, text="Zahlen", font=myfont)
cl4 = Label(top, text="Sonderzeichen", font=myfont)
cl5 = Label(top, text="alle wählen", font=myfontItalic)
c1 = Checkbutton(top, variable=v1, onvalue=True, offvalue=False, command=cXfkt)
c2 = Checkbutton(top, variable=v2, onvalue=True, offvalue=False, command=cXfkt)
c3 = Checkbutton(top, variable=v3, onvalue=True, offvalue=False, command=cXfkt)
c4 = Checkbutton(top, variable=v4, onvalue=True, offvalue=False, command=cXfkt)
c5 = Checkbutton(top, variable=v5, onvalue=True, offvalue=False, command=c5fkt)

msg.grid(row=0, column=0, columnspan=3, padx=10, pady=(0, 5))
cl1.grid(row=1, column=0, padx=(30, 0), pady=(0, 5), sticky=E)
cl2.grid(row=2, column=0, padx=0, pady=(0, 5), sticky=E)
cl3.grid(row=3, column=0, padx=0, pady=(0, 5), sticky=E)
cl4.grid(row=4, column=0, padx=0, pady=(0, 5), sticky=E)
cl5.grid(row=5, column=0, padx=0, pady=(10, 5), sticky=E)

c1.grid(row=1, column=1, padx=(0, 5), pady=(0, 5), sticky=W)
c2.grid(row=2, column=1, padx=(0, 5), pady=(0, 5), sticky=W)
c3.grid(row=3, column=1, padx=0, pady=(0, 5), sticky=W)
c4.grid(row=4, column=1, padx=0, pady=(0, 5), sticky=W)
c5.grid(row=5, column=1, padx=(0, 5), pady=(10, 5), sticky=W)

l2.grid(row=6, column=0, padx=(10, 0), pady=(10, 10), sticky=E)
e1.grid(row=6, column=1, padx=(0, 5), pady=(10, 10), sticky=W)
but.grid(row=7, column=0, columnspan=3, pady=(0, 10))
top.wm_title("Passwort-Generator")

e1.bind("<Return>", fkt)
# e2.bind("<Return>",fkt)
c5.select()
c5fkt()
t1.set('12')
e1.focus()
e1.selection_range(0, END)
e1.icursor(END)

ws = top.winfo_screenwidth()
hs = top.winfo_screenheight()
w = 310
h = 270
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)


# set the dimensions of the screen
# and where it is placed
def onclose():
    top.destroy()
    for fenst in fenstarr:
        try:
            fenst.destroy()
        except TclError:  # falls fenst bereits geschlossen wurde
            pass


top.geometry('%dx%d+%d+%d' % (w, h, x, y))
top.protocol("WM_DELETE_WINDOW", onclose)
top.mainloop()
