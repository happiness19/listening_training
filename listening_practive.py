import os
import pygame
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

# def initMainTextArea(root, bottomFrame):
#     #set up textbox
#     root.textinput = Canvas(root,width=700,background='gray13')
#     root.textinput.pack(in_=bottomFrame,side='left', fill='y')
#     #end of line number area

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
  pygame.mixer.music.play()
  started = 1

def exitMessage(root,event=None):
    if tkinter.messagebox.askokcancel("Are you sure you want to quit?",
      "Make sure to save the snippets or script before exit."):
    # root.text.after_cancel(root.callback)
    # root.text.after_cancel(root.lineCallback)
        root.destroy()

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

def initCheck(root, frame):
    def retrieve_input():
        my_input = root.text.get("1.0",'end-1c')
        print(my_input)
        global SOLUTION
        print("Solutuon is")
        print(SOLUTION)
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