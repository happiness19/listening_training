
from tkinter import *
import tkinter.messagebox,tkinter.filedialog

# def initMainTextArea(root, bottomFrame):
#     #set up textbox
#     root.textinput = Canvas(root,width=700,background='gray13')
#     root.textinput.pack(in_=bottomFrame,side='left', fill='y')
#     #end of line number area

def exitMessage(root,event=None):
    if tkinter.messagebox.askokcancel("Are you sure you want to quit?",
            "Make sure to save the snippets or script before exit."):
        # root.text.after_cancel(root.callback)
        # root.text.after_cancel(root.lineCallback)
        root.destroy()

def initButtonBar(root, frame):
    inputbutton = Button(frame, text="Input", padx = 110)
    startbutton = Button(frame, text="Start", padx = 110)
    replaybutton = Button(frame, text="Replay",padx = 110)
    replay5sbutton = Button(frame, text="Replay5s", padx = 110)
    stopbutton = Button(frame, text="Pause", padx = 110)


    inputbutton.pack( side = LEFT)
    startbutton.pack( side = LEFT)
    replaybutton.pack(side = LEFT)
    replay5sbutton.pack( side = LEFT)
    stopbutton.pack( side = LEFT)
    # b = Button(master, text=longtext, anchor=W, justify=LEFT, padx=2)
    # b.pack()
    # aboutMenu.add_command(label='About',command = aboutMessage)
    # aboutMenu.add_command(label='Key Board Commands',command=keyShortcuts)
    # aboutMenu.add_command(label='Fragments on Github',underline = 7,
    #     command= lambda: openUrl("https://github.com/Troyanovsky/Fragments"))
    # menuBar.add_cascade(label='About', menu=aboutMenu)

def initMainTextArea(root,editorFrame):
    #set up main text area
    textFrame_left = Frame(borderwidth=1, width=700, relief="sunken")
    textFrame_right = Frame(borderwidth=1, width=700, relief="sunken")
    root.text = Text(background="gray13", width = 90, foreground = 'white', wrap = "none",
                        borderwidth=1, highlightthickness=0, undo = True,
                        insertbackground = "white")
    #setting up scrollbars for the main text area
    root.vsb = Scrollbar(orient="vertical", borderwidth=1,
                            command=lambda *args: yview(root,*args))
    root.hsb = Scrollbar(orient="horizontal", borderwidth=1,
                            command=root.text.xview)
    root.text.configure(yscrollcommand=root.vsb.set)
    root.text.configure(xscrollcommand=root.hsb.set)
    root.vsb.pack(in_=textFrame_right,side="right", fill="y", expand=False)
    root.hsb.pack(in_=textFrame_right,side="bottom", fill="x", expand=False)

    root.text.pack(in_=textFrame_right, side="right", fill="y", expand=False)

    textFrame_left.pack(in_=editorFrame,side="left", fill="both", expand=True)
    textFrame_right.pack(in_=editorFrame,side="right", fill="both", expand=True)

    
    #end of main text area

def initFrames(root):
    #set different areas, left for file browsing, right for editing
    upperFrame = Frame(root,borderwidth=1, relief="sunken", width = 1400)
    middleFrame = Frame(root,borderwidth=1, relief="sunken",height= 100, width = 1400)
    bottomFrame = Frame(root,borderwidth=1, relief="sunken",width = 1400)
    # initLineNumberArea(root,editorFrame)
    initMainTextArea(root,bottomFrame)
    initButtonBar(root, upperFrame)
    # initResult(root, resultFrame)
    # initDirectory(root, leftFrame)
    upperFrame.pack(side = "top", fill = "both", expand = True)
    middleFrame.pack(side = "top", fill = "both", expand = True)
    bottomFrame.pack(side = "top", fill = "both", expand = True)
    #end of area setting

def run():
    editorName = "Fragments"
    root = Tk()
    root.geometry('1400x600')
    root.title(editorName)

    initFrames(root)

    root.time = 0
    root.protocol('WM_DELETE_WINDOW', lambda: exitMessage(root))
    #redirect closing window to a confirmation message
    root.mainloop()

run()