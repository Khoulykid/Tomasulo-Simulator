from Simulate import Simulation
from Classes import ReservationStation, CommonDataBus, InstructionQueue, RegisterFile, Memory, FunctionalUnit, Instruction

import tkinter as tk

class GUI:
    def __init__(self):
        self.flag = False
        self.InstructionQueue = InstructionQueue()
        self.simulation = Simulation(self.InstructionQueue)

    def divide_instruction(self, text):
        self.flag = True
        text = text.strip()
        lines = text.split("\n")
        for i in range(len(lines)):
            inst = lines[i].split(",")[0].split(" ")[0]
            R = lines[i].replace(inst, "").replace(" ", "").split(",")
            
            if len(R) == 3:
                instruction = Instruction(inst, R[0], R[1], R[2])
            elif len(R) == 2:
                instruction = Instruction(inst, R[0], R[1])
            elif len(R) == 1:
                instruction = Instruction(inst, R[0])
            else:
                instruction = Instruction(inst)
            self.InstructionQueue.enqueue(instruction)
        self.simulation.set_instruction_queue(self.InstructionQueue)
        
        
    
    def play_pressed(self):
        if not self.flag:
            self.divide_instruction(self.inst_field.get("1.0", "end-1c"))
        string = self.simulation.simulate(self.flag)
        self.output_field.configure(state="normal")
        self.output_field.delete("1.0", tk.END)
        self.output_field.insert(tk.END, string)
        self.output_field.configure(state="disabled")


    def stop_pressed(self):
        self.flag = False
        self.simulation.simulate(self.flag)
        self.output_field.configure(state="normal")
        self.output_field.delete("1.0", tk.END)
        self.output_field.configure(state="disabled")
        inter = InstructionQueue()
        self.simulation = Simulation(inter)

    def mem_pressed(self):
        text = self.mem_field.get("1.0", "end-1c")
        lines = text.split("\n")
        for i in range(len(lines)):
            address, value = lines[i].replace(" ", "").split(",")
            self.simulation.memory.store(int(address), int(value))
            print(address, value)
            print(self.simulation.memory.data[int(address)])
            

    def create_window(self):
        window = tk.Tk()
        window.title("MA")
        window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
        window.configure(bg = "#1f2228")
        window.update()
        x = int(window.winfo_width() * 0.1)
        y = int(window.winfo_height() * 0.1)

        self.inst_field = tk.Text(window, width= x//3, height = y//8, bg="#1f2a35", fg="white", font=("Arial", 12))
        self.inst_field.place(x= x//5, y= y*1.2)

        stop_button_img = tk.PhotoImage(file="stop.png")
        self.stop_button = tk.Button(window, image=stop_button_img, bg="#1f2a35", command=self.stop_pressed, fg="white", font=("Arial", 12))
        self.stop_button.image = stop_button_img
        self.stop_button.place(x= x//2.3, y= y//1.3)


        play_button_img = tk.PhotoImage(file="play.png")
        self.play_button = tk.Button(window, image=play_button_img, bg="#1f2a35", command=self.play_pressed, fg="#1f2a35", font=("Arial", 12)) #command= lambda:
        self.play_button.image = play_button_img
        self.play_button.place(x= x//5, y= y//1.3)


        self.output_field = tk.Text(window, width= x//3, height = y//8, bg="#1f2a35", fg="white", font=("Arial", 12))
        self.output_field.place(x= x//5, y= y*4)
        self.output_field.configure(state="disabled")


        self.mem_field = tk.Text(window, width= x//3, height = y//8, bg="#1f2a35", fg="white", font=("Arial", 12))
        self.mem_field.place(x= x*5, y= y*1.2)

        label1 = tk.Label(window, text="Instruction Queue", bg="#1f2228", fg="white", font=("Arial", 18))
        label1.place(x= x//1.1, y= y//1.3)

        label2 = tk.Label(window, text="Memory\nInput in this format: \"Address, Number\"", bg="#1f2228", fg="white", font=("Arial", 16))
        label2.place(x= x*5.4, y= y//1.7)

        label3 = tk.Label(window, text="Output", bg="#1f2228", fg="white", font=("Arial", 20))
        label3.place(x= x//5, y= y*3.6)

        self.mem_button = tk.Button(window, image=play_button_img, bg="#1f2a35", command= self.mem_pressed, fg="white", font=("Arial", 12))
        self.mem_button.image = play_button_img
        self.mem_button.place(x= x*5, y= y//1.3)
        window.mainloop()
