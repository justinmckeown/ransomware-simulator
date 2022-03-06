import logging
import tkinter as tk
from tkinter import ttk
from tkinter import  Tk, Label, LabelFrame, Button, Entry, W, N, E, S, X,Y, Frame, LEFT, RIGHT, CENTER, Text, messagebox, Scrollbar, StringVar, OptionMenu, PhotoImage
from tkinter import ttk
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
import threading
from interface.malwarescreen import MalwareScreenView
from interface.styling import BG_COLOR

logger = logging.getLogger()

class RootViewController(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('GOMPI | RaaS Removal Service ')
        self.minsize(750, 500)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.file_count_display: int = 0
        self.configure(bg=BG_COLOR)     


        self.malware_display_frame = MalwareScreenView(self)
        self.malware_display_frame.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)