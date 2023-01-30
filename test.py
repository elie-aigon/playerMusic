import tkinter as tk
from tkinter import filedialog
import shutil
import os

def copy_files():
    src_files = filedialog.askopenfilenames(
        title="Sélectionnez les fichiers à copier",
        filetypes=(("Tous les fichiers", "*.*"),),
        initialdir=os.path.expanduser("~/Desktop")
    )
    
    dst_folder = filedialog.askdirectory(
        title="Sélectionnez le dossier de destination",
        initialdir=os.path.expanduser("~/Desktop")
    )

    for src_file in src_files:
        dst_file = os.path.join(dst_folder, os.path.basename(src_file))
        shutil.copy2(src_file, dst_file)
        
root = tk.Tk()
root.withdraw()
copy_files()
