import pygame
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter.ttk import *
from tkinter import *
import random
import time
import shutil
import os

window = Tk()
window.config( bg="grey")
window.resizable(False, False)
window.title("Player tahh 2002")
window.geometry("300x400")

pygame.mixer.init()
is_paused = False
is_repeat = False
is_random = False
current_pos = 0
max_time = StringVar()
current_time = StringVar()
value  = 50

def load_and_play():
    global current_max
    reset_progressbar()
    selected_song = listbox_songs.get(ACTIVE)
    index_song = listbox_songs.curselection()
    path =  selected_song
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    current_max = pygame.mixer.Sound(listbox_songs.get(ACTIVE)).get_length() 
    progressbar['maximum'] = current_max
    max_time.set(str(convert(current_max)))
    
def random_song():
    global is_random
    if not is_random:
        random_button.config(bg='black', fg='white')
        index_song = random.randint(0, listbox_songs.size())
        listbox_songs.selection_clear(0, END)
        listbox_songs.activate(index_song)
        listbox_songs.selection_set(index_song, last= index_song)   
        load_and_play()
        is_random = True
    else:
        random_button.config(bg='white', fg='black')
        is_random = False
    
def pause():
    global is_paused
    if not is_paused:
        pygame.mixer.music.pause()
        pause_button.config(text= "Resume")
        is_paused = True
    
    else:
        pygame.mixer.music.unpause()
        pause_button.config(text= "Pause")
        is_paused = False

def next():
    reset_progressbar()
    current_index = listbox_songs.curselection()
    if not current_index:
        next_index = 0
    else:
        next_index = current_index[0] + 1 
        if next_index >= listbox_songs.size():
            next_index -= listbox_songs.size()
            
    listbox_songs.selection_clear(0, END)
    listbox_songs.activate(next_index)
    listbox_songs.selection_set(next_index, last= next_index)   
    load_and_play()

def previous():

    reset_progressbar()
    current_index = listbox_songs.curselection()
    if not current_index:
        prev_index = 0
    else:
        prev_index = current_index[0] - 1
        if prev_index >= listbox_songs.size():
            prev_index += listbox_songs.size() 
    listbox_songs.selection_clear(0, END)
    listbox_songs.activate(prev_index)
    listbox_songs.selection_set(prev_index, last= prev_index)   
    load_and_play()

def repeat():
    global is_repeat
    if not is_repeat:
        repeat_button.config(bg="black", fg="white")
        is_repeat = True
    else:
        repeat_button.config(bg="white", fg="black")
        is_repeat = False
        
def change_volume(value):
    pygame.mixer.music.set_volume(int(value)/100)

def end():
    if is_repeat:
        load_and_play()
    elif is_random:
        random_song()
    else:
        next()
 
def update():
    global current_pos, current_max
    if not is_paused and pygame.mixer.music.get_busy():
        progressbar['value'] = current_pos
        current_time.set(str(convert(current_pos)))
        current_pos += 1
        if current_pos >= int(current_max):
            current_pos = 0
            end()
        window.after(1000, update)
    else:
        window.after(1000, update)

def convert(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%02d:%02d" % (minutes, seconds)    

def on_progressbar_click(event):
    global current_pos
    new_pos = int(((event.x / progressbar.winfo_width()) * progressbar["maximum"]))
    current_pos = new_pos
    pygame.mixer.music.rewind()
    pygame.mixer.music.set_pos(new_pos)
    progressbar.config(value=new_pos)

def add_file():
    destination = filedialog.askdirectory(
        title= "Selectionnez l'endroit ou vous voulez copiez les fichiers"
        
    )   
    src_files = filedialog.askopenfilenames(
        title="Sélectionnez les fichiers à copier",
        filetypes=(("Tous les fichiers", "*.*"),),
        initialdir=os.path.expanduser("~/Desktop")
    )
    for src_file in src_files:
        shutil.copy2(src_file, destination)

    listbox_songs.delete(0, END)

    for fichier in os.listdir():
        listbox_songs.insert(END, fichier)

def stop():
    pygame.mixer.music.stop()
    reset_progressbar()


def reset_progressbar():
    global current_pos
    progressbar.config(value= 0)
    current_pos = 0
    current_time.set(str(convert(0)))
    max_time.set(str(convert(0)))

# UI ----------------------

os.chdir(askdirectory())

listbox_songs = Listbox(window, bg="grey", width=47)
listbox_songs.place(x=8, y=10)
for fichier in os.listdir():
    listbox_songs.insert(END, fichier)

current_time_aff = Label(window,width=5, textvariable=current_time)
current_time_aff.place(x=40, y=222)

max_time_aff = Label(window,width=5, textvariable=max_time)
max_time_aff.place(x=218, y=222)

progressbar = Progressbar(window, orient= HORIZONTAL, length=220)
progressbar.place(x=40, y=200)
progressbar.bind("<Button-1>", on_progressbar_click)



play_button = Button(window, text = 'Play', bg="white", fg="black", command = load_and_play)
play_button.place(x= 117, y=240)

stop_button = Button(window, text= 'Stop', bg= "white", fg="black", command = stop)
stop_button.place(x= 155, y= 240)

random_button = Button(window, text="Random Song", bg="white", fg="black", command = random_song)
random_button.place(x=110, y=275)

pause_button = Button(window, text = 'Pause', bg="white", fg="black", command = pause)
pause_button.place(x= 130, y=310)

next_button = Button(window, text = 'Next', bg="white", fg="black", command = next)
next_button.place(x= 178, y=310)

previous_button = Button(window, text = 'Prev', bg="white", fg="black", command = previous)
previous_button.place(x= 90, y=310)

repeat_button = Button(window, text = 'Repeat', bg="white", fg="black", command = repeat)
repeat_button.place(x= 127, y=360)

volume_bar = Scale(window, from_=100, to=0, orient="vertical", bg="white", fg="black", command=change_volume)
volume_bar.set(50)
volume_bar.place(x= 250, y=290)

add_file_button = Button(window, text="ADD File", bg="white", fg="black", command=add_file)
add_file_button.place(x=20, y=360 )

update()
window.mainloop()

