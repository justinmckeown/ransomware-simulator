import logging
import typing
import threading
from threading import Thread
import tkinter as tk
from tkinter import (CENTER, LEFT, RIGHT, Button, E, Entry, Frame, Label,
                     LabelFrame, N, OptionMenu, PhotoImage, S, Scrollbar,
                     StringVar, Text, Tk, W, X, Y, messagebox, ttk)
from tkinter.filedialog import askdirectory
from tkinter.ttk import *

from structlog import configure

from interface.incidentreporting import IncidentReportingView
from interface.malwarescreen import MalwareScreenView
from interface.styling import BG_COLOR
from datetime import datetime, timedelta
from time import sleep


logger = logging.getLogger()

class RootViewController(tk.Tk):
    def __init__(self) -> None:

        #Configure screen initial setup
        super().__init__()
        self.minsize(750, 500)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.file_count_display: int = 0
        self.geometry(f'{self.width-100}x{self.height-100}')
       

        #Set up first view        
        self.title('Overwatch | Response Input system')
        self.incident_reporting_frame = IncidentReportingView(self)
        self.incident_reporting_frame.grid(row=0, column=0)

        self.malware_frame = MalwareScreenView(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        timer_object = InputScreenTimer()
        timer_object = threading.Thread(target=timer_object.check_time, args=(self.incident_reporting_frame,self.malware_frame, self.configure, self.title, self.attributes))
        timer_object.start()


class InputScreenTimer(Thread):
    def __init__(self) -> None:
        super().__init__()
        self.termination_time = datetime.strptime('17:12', '%H:%M')
        self.not_time_yet = True

    def check_time(self, incident_frame: IncidentReportingView, malware_frame: MalwareScreenView, conf: configure, window_title, screen_size) -> None:
        while self.not_time_yet:
            time_now = datetime.now()
            todays_date = datetime.today()
            remaining = time_now.combine(todays_date, self.termination_time.time()) - time_now.combine(todays_date, time_now.time())
            sleep(1)
            if remaining <= timedelta(microseconds=10):
                incident_frame.destroy()
                self.not_time_yet = False
        conf(bg=BG_COLOR)
        window_title('GOMPI | RaaS Removal Service')
        malware_frame.grid(row=0, column=0)
        screen_size("-fullscreen", True)
        malware_frame.begin_countdown()
