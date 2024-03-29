import logging
import tkinter as tk
import typing
from datetime import datetime
from tkinter import BOTH, E, N, S, StringVar, W, X, Y, filedialog, font, messagebox
from tkinter.messagebox import showinfo
from tkinter.ttk import *
from xmlrpc.client import TRANSPORT_ERROR
from interface.styling import (BG_BUTTON_COLOUR, BG_COLOR, BG_COLOR_2,
                               BG_COLOR_2_IR, BG_COLOR_IR, BOLD_FONT,
                               BOLD_FONT_IR, FG_COLOR, FG_COLOR_2, FG_COLOR_IR,
                               GLOBAL_FONT, IR_FONT, IR_FONT_B, GLOBAL_SMALL_HEADING, HEADING_FONT)
import json

logger = logging.getLogger()

class IncidentReportingView(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        #self.configure(bg='grey')
        
        #self.pack(FILL=BOTH, expand=True)
        
        self.frame0 = tk.Frame(self)
        self.frame0.pack(fill=X)
        self.img0 = tk.PhotoImage(file='images/genericlogo.png')
        #TODO: Inser image here in label form
        self.lbl0 = tk.Label(self.frame0, image=self.img0)
        self.lbl0.pack(side=tk.TOP, padx=5, pady=5)
        
        
        self.frame1 = tk.Frame(self)
        self.frame1.pack(fill=X)
        self.lbl1 = tk.Label(self.frame1, text="Event ID", width=7, font=IR_FONT_B)
        self.lbl1.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry1 = tk.Entry(self.frame1, font=IR_FONT, width=100)
        self.entry1.pack(fill=X, padx=5, expand=True)
        
        self.frame2 = tk.Frame(self)
        self.frame2.pack(fill=X)
        self.lbl2 = tk.Label(self.frame2, text="Owner", width=7, font=IR_FONT_B)
        self.lbl2.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry2 = tk.Entry(self.frame2, font=IR_FONT, width=100)
        self.entry2.pack(fill=X, padx=5, expand=True)
        
        self.frame3 = tk.Frame(self)
        self.frame3.pack(fill=X)
        self.lbl3 = tk.Label(self.frame3, text="Summary", width=7, font=IR_FONT_B)
        self.lbl3.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry3 = tk.Entry(self.frame3, font=IR_FONT, width=100)
        self.entry3.pack(fill=X, padx=5, expand=True)
        
        self.frame4 = tk.Frame(self)
        self.frame4.pack(fill=BOTH, expand=True)
        self.lbl4 = tk.Label(self.frame4, text="Response", width=7, font=IR_FONT_B)
        self.lbl4.pack(side=tk.LEFT, anchor=N, padx=5, pady=5)
        self.txt = tk.Text(self.frame4, font=IR_FONT, width=100)
        self.txt.pack(fill=BOTH, pady=5, padx=5, expand=True)
        self.frame5= tk.Frame(self)
        self.frame5.pack(fill=X)
        
        self.btn = tk.Button(self.frame5, font=IR_FONT_B, text='Log Event', command=self.write_log)
        self.btn.pack(side=tk.RIGHT, anchor=N ,padx=5, pady=5)
    
    
    def write_log(self):
        print(f'Button pressed')
        data: typing.Dict[str : str] = {}
        data['event_id'] = self.entry1.get()
        data['owner'] = self.entry2.get()
        data['summary'] = self.entry3.get()
        data['response'] = self.txt.get('1.0', 'end')
        data['timestamp'] = datetime.now().strftime("%Y-%H-%M-%S")
        
        file_name = f'{data.get("timestamp")}-response.json' 
        
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        
        self.entry1.delete(0, 'end')
        self.entry2.delete(0, 'end')
        self.entry3.delete(0, 'end')
        self.txt.delete('1.0', 'end')