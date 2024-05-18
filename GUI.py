from Simulate import simulate
from Classes import ReservationStation, CommonDataBus, InstructionQueue, RegisterFile, Memory, FunctionalUnit

import tkinter as tk

def create_window():
    window = tk.Tk()
    window.title("MA")
    window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
    window.configure(bg = "#1f2228")
    window.update()
    x = int(window.winfo_width() * 0.1)
    y = int(window.winfo_height() * 0.1)

    inst_field = tk.Text(window, width= x//3, height = y//8, bg="#1f2a35", fg="white", font=("Arial", 12))
    inst_field.place(x= x//5, y= y*1.2)


    play_button_img = tk.PhotoImage(file="play.png")
    play_button = tk.Button(window, image=play_button_img, bg="#1f2a35", command=simulate)
    play_button.image = play_button_img
    play_button.place(x= x//5, y= y//1.3)


    output_field = tk.Text(window, width= x//3, height = y//8, bg="#1f2a35", fg="white", font=("Arial", 12))
    output_field.place(x= x//5, y= y*4)
    output_field.configure(state="disabled")


    mem_field = tk.Text(window, width= x//3, height = y//8, bg="#1f2a35", fg="white", font=("Arial", 12))
    mem_field.place(x= x*5, y= y*1.2)

    label1 = tk.Label(window, text="Instruction Queue", bg="#1f2228", fg="white", font=("Arial", 18))
    label1.place(x= x//2, y= y//1.3)

    label2 = tk.Label(window, text="Memory\nInput in this format: \"Address, Number\"", bg="#1f2228", fg="white", font=("Arial", 16))
    label2.place(x= x*5.4, y= y//1.7)

    label3 = tk.Label(window, text="Output", bg="#1f2228", fg="white", font=("Arial", 20))
    label3.place(x= x//5, y= y*3.6)

    mem_button = tk.Button(window, image=play_button_img, bg="#1f2a35", fg="white", font=("Arial", 12))
    mem_button.image = play_button_img
    mem_button.place(x= x*5, y= y//1.3)
    window.mainloop()
