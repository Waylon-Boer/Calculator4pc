from tkinter import *
import math, re

def calculate(option):
        text = bar.get()
        bar.delete(0, END)
        try:
            if re.match(r'^[\d\s.+\-*/%]+$', text):
                if option == "b":
                    answer = str(bin(int(eval(text))))
                elif option == "o":
                    answer = str(oct(int(eval(text))))
                elif option == "h":
                    answer = str(hex(int(eval(text))))
                elif option == "s":
                    answer = str(eval(text) ** 2)
                elif option == "r":
                    answer = str(math.sqrt(eval(text)))
                elif option == "i":
                    answer = str(1/float(eval(text)))                
                else:
                    answer = eval(text)
                bar.insert(INSERT, answer)
            else:
                bar.insert(INSERT, "Error!")
        except:
           bar.insert(INSERT, "Error!")

if __name__ == "__main__":
    root = Tk()
    root["bd"] = 16
    root["bg"] = "#e1e1e1"
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1, minsize=320)
    bar = Entry(root, font=("", 12), relief=FLAT)
    bar.grid(row=0, column=0, sticky="nsew", ipady=8, pady=(0, 4))
    frameCalculator = Frame(root)
    frameCalculator.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
    frameCalculator["bg"] = "#e1e1e1"
    for i in range(0, 6):
        frameCalculator.rowconfigure(i, weight=1)
    for j in range(0, 4):
        frameCalculator.columnconfigure(j, weight=1)
    Button(frameCalculator, relief=FLAT, text="bin", command=lambda: calculate("b")).grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=(0, 2))
    Button(frameCalculator, relief=FLAT, text="oct", command=lambda: calculate("o")).grid(row=0, column=1, sticky="nsew", padx=2, pady=(0, 2))
    Button(frameCalculator, relief=FLAT, text="hex", command=lambda: calculate("h")).grid(row=0, column=2, sticky="nsew", padx=2, pady=(0, 2))
    Button(frameCalculator, relief=FLAT, text="^", command=lambda: bar.insert(INSERT, " ** ")).grid(row=0, column=3, sticky="nsew", padx=(2, 0), pady=(0, 2))
    Button(frameCalculator, relief=FLAT, text="x²", command=lambda: calculate("s")).grid(row=1, column=0, sticky="nsew", padx=(0, 2), pady=2)
    Button(frameCalculator, relief=FLAT, text="√", command=lambda: calculate("r")).grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
    Button(frameCalculator, relief=FLAT, text="1/x", command=lambda: calculate("i")).grid(row=1, column=2, sticky="nsew", padx=2, pady=2)
    Button(frameCalculator, relief=FLAT, text="+", command=lambda: bar.insert(INSERT, " + ")).grid(row=1, column=3, sticky="nsew", padx=(2, 0), pady=2)
    Button(frameCalculator, relief=FLAT, text="7", command=lambda: bar.insert(INSERT, "7")).grid(row=2, column=0, sticky="nsew", padx=(0, 2), pady=2)
    Button(frameCalculator, relief=FLAT, text="8", command=lambda: bar.insert(INSERT, "8")).grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
    Button(frameCalculator, relief=FLAT, text="9", command=lambda: bar.insert(INSERT, "9")).grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
    Button(frameCalculator, relief=FLAT, text="-", command=lambda: bar.insert(INSERT, " - ")).grid(row=2, column=3, sticky="nsew", padx=(2, 0), pady=2)
    Button(frameCalculator, relief=FLAT, text="2", command=lambda: bar.insert(INSERT, "2")).grid(row=3, column=0, sticky="nsew", padx=(0, 2), pady=2)
    Button(frameCalculator, relief=FLAT, text="5", command=lambda: bar.insert(INSERT, "5")).grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
    Button(frameCalculator, relief=FLAT, text="6", command=lambda: bar.insert(INSERT, "6")).grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
    Button(frameCalculator, relief=FLAT, text="x", command=lambda: bar.insert(INSERT, " * ")).grid(row=3, column=3, sticky="nsew", padx=(2, 0), pady=2)
    Button(frameCalculator, relief=FLAT, text="1", command=lambda: bar.insert(INSERT, "1")).grid(row=4, column=0, sticky="nsew", padx=(0, 2), pady=2)
    Button(frameCalculator, relief=FLAT, text="2", command=lambda: bar.insert(INSERT, "2")).grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
    Button(frameCalculator, relief=FLAT, text="3", command=lambda: bar.insert(INSERT, "3")).grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
    Button(frameCalculator, relief=FLAT, text="÷", command=lambda: bar.insert(INSERT, " / ")).grid(row=4, column=3, sticky="nsew", padx=(2, 0), pady=2)
    Button(frameCalculator, relief=FLAT, text="C", command=lambda: bar.delete(0, END)).grid(row=5, column=0, sticky="nsew", padx=(0, 2), pady=(2, 0))
    Button(frameCalculator, relief=FLAT, text="0", command=lambda: bar.insert(INSERT, "0")).grid(row=5, column=1, sticky="nsew", padx=2, pady=(2, 0))
    Button(frameCalculator, relief=FLAT, text=".", command=lambda: bar.insert(INSERT, ".")).grid(row=5, column=2, sticky="nsew", padx=2, pady=(2, 0))
    Button(frameCalculator, relief=FLAT, text="=", command=lambda: calculate("e")).grid(row=5, column=3, sticky="nsew", padx=(2, 0), pady=(2, 0))
    root.mainloop()