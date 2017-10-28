import os
import pygame
import difflib
from tkinter import *
import tkinter.messagebox,tkinter.filedialog
from tkinter.filedialog import askopenfilename
import speech_recognition as sr                       # speech to text; installed by pip install SpeechRecognition
from PyDictionary import PyDictionary  

def wavToText_Google(fileName):                       # takes in a file name and returns the recongnized text
    r = sr.Recognizer()
    with sr.WavFile(fileName) as source:              # use fileName as the audio source
        audio = r.record(source)                      # extract audio data from the file
    try:
        text = (r.recognize_google(audio))            # recognize speech using Google Speech Recognition
    except LookupError:                               # speech is unintelligible
        print("Could not understand audio")
    return text

paused = 0
started = 0
SOLUTION = None

def findfile(event):
  result = askopenfilename(filetypes=[("Audio", "*.wav")],)
  global SOLUTION 
  SOLUTION = wavToText_Google(result)
  pygame.mixer.music.load(result)

def startsong(event):
  global paused
  global started
  if started == 0:
    pygame.mixer.music.play()
    started = 1
    paused = 0
  elif paused == 1:
    pygame.mixer.music.unpause()
    paused = 0

def pausesong(event):
  global paused
  if paused == 0:
    pygame.mixer.music.pause()
    paused = 1

def stopsong(event):
  global started
  pygame.mixer.music.stop()
  started = 0

def replaysong(event):
  global started
  global paused
  pygame.mixer.music.play()
  started = 1
  paused = 0


def exitMessage(root,event=None):
    if tkinter.messagebox.askokcancel("Are you sure you want to quit?",
      "Okay Bye."):
    # root.text.after_cancel(root.callback)
    # root.text.after_cancel(root.lineCallback)
        root.destroy()

def removeBlank(l):
    result = []
    for i in range(len(l)):
        (a1,a2) = l[i]
        if (a1 != a2):
            result.append((a1,a2))
    return result

def textCom(a,b): # a is user input string  b is solution
    s = difflib.SequenceMatcher(lambda x: x in ",. \t", a.lower(),b.lower())
    l1,l2 = list(), list()
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if (tag != "equal"):
            l1.append((i1,i2))
            l2.append((j1,j2))
    l1n = removeBlank(l1)
    l2n = removeBlank(l2)
    return ((l1n,l2n), s.ratio()) # two lists of tuples

def initButtonBar(root, frame):
  inputbutton = Button(frame, text="Input", padx = 110)
  startbutton = Button(frame, text="Start", padx = 110)
  pausebutton = Button(frame, text="Pause", padx = 110)
  replaybutton = Button(frame, text="Replay",padx = 110)
  stopbutton = Button(frame, text="Stop", padx = 110)

  inputbutton.pack(side = LEFT)
  startbutton.pack(side = LEFT)
  pausebutton.pack(side = LEFT)
  replaybutton.pack(side = LEFT)
  stopbutton.pack(side = LEFT)

  startbutton.bind("<Button-1>",startsong)
  stopbutton.bind("<Button-1>",stopsong)
  inputbutton.bind("<Button-1>",findfile)
  replaybutton.bind("<Button-1>",replaysong)
  pausebutton.bind("<Button-1>",pausesong)


def initMainTextArea(root,editorFrame):
  #set up main text area
  textFrame = Frame(borderwidth=1, width=1400, relief="sunken")

  root.solution = Text(background="white", width = 80, foreground = 'black', wrap = WORD,
                      borderwidth=1, highlightthickness=0, undo = True,
                      insertbackground = "white", state='disabled')
  root.text = Text(background="gray13", width = 90, foreground = 'white', wrap = WORD,
                      borderwidth=1, highlightthickness=0, undo = True,
                      insertbackground = "white")
  #setting up scrollbars for the main text area
  root.vsb = Scrollbar(orient="vertical", borderwidth=1,
                          command=lambda *args: yview(root,*args))
  root.hsb = Scrollbar(orient="horizontal", borderwidth=1,
                            command=root.text.xview)
  root.text.configure(yscrollcommand=root.vsb.set)
  root.text.configure(xscrollcommand=root.hsb.set)

  root.vsb.pack(in_=textFrame,side="right", fill="y", expand=False)
  root.hsb.pack(in_=textFrame,side="bottom", fill="x", expand=False)


  root.text.pack(in_=textFrame, side="right", fill="y", expand=False)
  root.solution.pack(in_=textFrame, side = "left", fill="y", expand=False)

  textFrame.pack(in_=editorFrame,side="right", fill="both", expand=True)

    
  #end of main text area

def initCheck(root, frame):
    def retrieve_input():
        my_input = root.text.get("1.0",'end-1c')
        my_input = my_input.replace("\n", " ").strip()
        global SOLUTION
        diff, ratio = textCom(my_input,SOLUTION)
        root.solution.configure(state="normal")
        root.solution.delete("0.0","end")
        root.solution.insert("1.0",SOLUTION)
        ratio *= 100
        tkinter.messagebox.showinfo("Feedback", "Your score is %0.2f %%!" % ratio)
        root.text.tag_config('highlight',foreground = 'red')
        root.solution.tag_config('highlight', background = 'yellow')
        for i in diff[0]: 
            root.text.tag_add('highlight','1.{0}'.format(i[0]),'1.{0}'.format(i[1]))
        for i in diff[1]:
            root.solution.tag_add('highlight','1.{0}'.format(i[0]),'1.{0}'.format(i[1]))
        root.solution.configure(state="disabled")
        return
    checkbutton = Button(frame, text="CHECK", command= retrieve_input, padx = 700)
    checkbutton.pack(side = LEFT)


def initFrames(root):
  #set different areas, left for file browsing, right for editing
  upperFrame = Frame(root,borderwidth=1, relief="sunken", width = 1400)
  middleFrame = Frame(root,borderwidth=1, relief="sunken",height= 100, width = 1400)
  bottomFrame = Frame(root,borderwidth=1, relief="sunken",width = 1400)
  # initLineNumberArea(root,editorFrame)
  initMainTextArea(root,bottomFrame)
  initCheck(root, middleFrame)
  initButtonBar(root, upperFrame)
  
  # initDirectory(root, leftFrame)
  upperFrame.pack(side = "top", fill = "both", expand = True)
  middleFrame.pack(side = "top", fill = "both", expand = True)
  bottomFrame.pack(side = "top", fill = "both", expand = True)
  #end of area setting

def run():
  editorName = "Listening Practice"
  root = Tk()
  root.geometry('1400x600')
  root.title(editorName)
  pygame.mixer.init()

  initFrames(root)

  root.time = 0
  root.protocol('WM_DELETE_WINDOW', lambda: exitMessage(root))
  #redirect closing window to a confirmation message
  root.mainloop()

run()