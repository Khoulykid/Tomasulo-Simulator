from Classes import ReservationStation, CommonDataBus, InstructionQueue, RegisterFile, Memory, FunctionalUnit
from Simulate import simulate

import tkinter as tk

def create_window():
    window = tk.Tk()
    window.title("MA")
    window.geometry("800x400")
    window.mainloop()
create_window()
# simulate()