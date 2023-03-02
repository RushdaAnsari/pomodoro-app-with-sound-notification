import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
from pygame import mixer

# ---------------------------- UI SETUP ------------------------------- #
class PomodoroTimer:        
    def __init__(self):
        # window settings
        self.root = tk.Tk()
        self.root.geometry("600x350")
        self.root.title("Pomodoro Timer")
        self.root.tk.call("wm", "iconphoto", self.root._w, PhotoImage(file="img/tomato.png")) 
        mixer.init()
        mixer.music.load('audio/clock-alarm.mp3') 

        # window style settings
        self.s = ttk.Style()
        self.s.theme_use('classic')
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 13), background="Tomato2")
        self.s.configure("Tbutton.Tab", font=("Ubuntu", 16))

        # tabs settings
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)

        # creating labels
        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", font=("Ubuntu", 48))
        self.pomodoro_timer_label.pack(pady=50)
        
        self.shortbreak_timer_label = ttk.Label(self.tab2, text="05:00", font=("Ubuntu", 48))
        self.shortbreak_timer_label.pack(pady=50)

        self.longbreak_timer_label = ttk.Label(self.tab3, text="15:00", font=("Ubuntu", 48))
        self.longbreak_timer_label.pack(pady=50)

        # naming tabs
        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        # grid layout
        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=20)

        # adding buttons
        self.start_button = tk.Button(self.grid_layout, text="Start", command=self.start_timer_thread, bg="Tomato2", padx=10, pady=5)
        self.start_button.grid(row=0, column=0)
        
        self.skip_button = tk.Button(self.grid_layout, text="Skip", command=self.skip_clock, bg="Tomato2", padx=10, pady=5)
        self.skip_button.grid(row=0, column=1)

        self.reset_button = tk.Button(self.grid_layout, text="Reset", command=self.reset_clock, bg="Tomato2", padx=10, pady=5)
        self.reset_button.grid(row=0, column=2)

        # counting pomodoro sessions
        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros: 0", font=("Ubuntu", 10))
        self.pomodoro_counter_label.grid(row=1, columnspan=3, column=0)
        
        # adding default values to variables
        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False
        
        self.root.mainloop()    

    def start_timer_thread(self):
        #  check if the timer is running 
        if not self.running:
            # start the timer 
            t = threading.Thread(target=self.start_timer)
            t.start()
            # timer is now running
            self.running = True

    # timer function
    def start_timer(self):
        self.skipped = False
        self.stopped = False
        # adding number to each tab
        timer_id = self.tabs.index(self.tabs.select()) + 1

        if timer_id == 1:
            # setting 25 mins to clock
            full_seconds = 60 * 25
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
                if full_seconds == 0:
                    self.pomodoro_timer_label.config(text="00:00")
                    mixer.music.play()
                    time.sleep(5)
                    mixer.music.stop()
                    
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f"Pomodoro: {self.pomodoros}")
                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer()

        # short break setting
        elif timer_id == 2:
            full_seconds = 60 * 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.shortbreak_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
                if full_seconds == 0:
                    self.shortbreak_timer_label.config(text="00:00")
                    mixer.music.play()
                    time.sleep(5)
                    mixer.music.stop()

            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()

        # long break setting
        elif timer_id == 3:          
            full_seconds = 60 * 15
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.longbreak_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
                if full_seconds == 0:
                    self.longbreak_timer_label.config(text="00:00")
                    mixer.music.play()
                    time.sleep(5)
                    mixer.music.stop()

            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        else:
            print("Invalid timer id")         

    # resetting the clock
    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoros = 0
        self.pomodoro_timer_label.config(text="25:00")
        self.shortbreak_timer_label.config(text="05:00")
        self.longbreak_timer_label.config(text="15:00")
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        mixer.music.stop()

        self.running = False
    
    # skip button
    def skip_clock(self):
        current_tab = self.tabs.index(self.tabs.select())
        # label resets
        if current_tab == 0:
            self.pomodoro_timer_label.config(text="25:00")
        elif current_tab == 1:
            self.shortbreak_timer_label.config(text="05:00")
        elif current_tab == 2:
            self.longbreak_timer_label.config(text="15:00")


        self.stopped = True
        self.skipped = True
        mixer.music.stop()



PomodoroTimer()
