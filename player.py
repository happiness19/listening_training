import os
import pygame
from mutagen.id3 import ID3
from tkinter import *
from tkinter.filedialog import askopenfilename
 
root = Tk()
root.minsize(300,300)
pygame.mixer.init()

result = askopenfilename(
    filetypes=[("Foos", "*.wav")],
)

pygame.mixer.music.load(result)

paused = 0

def startsong(event):
  global paused
  pygame.mixer.music.play()
  if paused == 1:
    paused = 0

def pausesong(event):
  global paused
  if paused:
    pygame.mixer.music.unpause()
  else:
    pygame.mixer.music.pause()
  paused = 1 - paused

def stopsong(event):
  pygame.mixer.music.stop()
  pygame.quit()
  root.destroy()

startbutton = Button(root,text='Start Music')
startbutton.pack()

pausebutton = Button(root,text='Pause Music')
pausebutton.pack()

stopbutton = Button(root,text='Stop Music')
stopbutton.pack()
 
 
startbutton.bind("<Button-1>",startsong)
pausebutton.bind("<Button-1>",pausesong)
stopbutton.bind("<Button-1>",stopsong)

root.mainloop()