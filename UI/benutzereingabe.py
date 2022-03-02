from tkinter import *
import tkinter.font as tkFont
from UI import Reviewanalyser
import time


def main():
    window = Tk()
    window.title("Review Analyser")
    window.geometry('600x300')

    fontStyleTitle = tkFont.Font(family="Lucida Grande", size=20)
    fontStyle = tkFont.Font(family="Lucida Grande", size=15)




    lbl = Label(window, text="Welcome to the review analyzer", font = fontStyleTitle)
    lbl.pack()


    lbl2 = Label(window, text="Please insert a valid Amazon review product ID", font = fontStyle)
    lbl2.pack()

    txt = Entry(window,width=10)
    txt.pack()

    def clicked():
        lbl3.pack()
        time.sleep(1)
        result = txt.get()
        do_analysing(result)

    def do_analysing(result):
        Reviewanalyser.main(result)


    btn = Button(window, text="Submit", command=clicked)
    btn.pack()

    lbl3 = Label(window, text="Thank you, please wait a moment :)", font = fontStyle)

    def center(win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    center(window)

    window.mainloop()
