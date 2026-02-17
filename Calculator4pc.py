from tkinter import *
from tkinter.ttk import Notebook
from tkinter import font
import math, re, datetime

def calculate(option):
    text = bar.get()
    if text != "":
        text = text.replace("%", " * 0.01").replace("mod", "%").replace("÷", "/").replace("e", str(math.e)).replace("π", str(math.pi))
        bar.delete(0, END)
        try:
            if re.match(r"^[\d\s.+\-*/%box\(\)]+$", text):
                if option == "bin":
                    answer = str(bin(int(round(eval(text), 0))))
                elif option == "oct":
                    answer = str(oct(int(round(eval(text), 0))))
                elif option == "hex":
                    answer = str(hex(int(round(eval(text), 0))))
                elif option == "s":
                    answer = str(eval(text) ** 2)
                elif option == "r":
                    answer = str(math.sqrt(eval(text)))
                elif option == "i":
                    answer = str(1/float(eval(text)))
                elif option == "f":
                    answer = math.factorial(eval(text))
                elif option == "abs":
                    answer = abs(eval(text))
                elif option == "ln":
                    answer = math.log(eval(text))
                elif option == "log":
                    answer = math.log10(eval(text))
                else:
                    answer = eval(text)
                bar.insert(INSERT, answer)
            else:
                bar.insert(INSERT, "Error!")
        except:
            bar.insert(INSERT, "Error!")

def memory_p():
    global memory
    text = bar.get()
    text = text.replace("%", " * 0.01").replace("mod", "%").replace("÷", "/").replace("e", str(math.e)).replace("π", str(math.pi))
    try:
        if re.match(r"^[\d\s.+\-*/%box\(\)]+$", text):
            answer = float(eval(text))
        else:
            answer = 0
    except:
        answer = 0
    memory = memory + answer

def memory_m():
    global memory
    text = bar.get()
    text = text.replace("%", " * 0.01").replace("mod", "%").replace("÷", "/").replace("e", str(math.e)).replace("π", str(math.pi))
    try:
        if re.match(r"^[\d\s.+\-*/%box\(\)]+$", text):
            answer = float(eval(text))
        else:
            answer = 0
    except:
        answer = 0
    memory = memory - answer

def memory_s():
    global memory
    text = bar.get()
    text = text.replace("%", " * 0.01").replace("mod", "%").replace("÷", "/").replace("e", str(math.e)).replace("π", str(math.pi))
    try:
        if re.match(r"^[\d\s.+\-*/%box\(\)]+$", text):
            answer = float(eval(text))
        else:
            answer = 0
    except:
        answer = 0
    memory = answer

def memory_c():
    global memory
    memory = 0

def memory_r():
    bar.insert(INSERT, f"({memory})")

def standard_mode():
    for i in buttons:
        buttons[i].grid_forget()
    frameCalculator.rowconfigure(6, weight=0)
    frameCalculator.rowconfigure(7, weight=0)
    frameCalculator.columnconfigure(4, weight=0)
    buttons["memory_p"].grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=(0, 2))
    buttons["memory_m"].grid(row=0, column=1, sticky="nsew", padx=2, pady=(0, 2))
    buttons["memory_c"].grid(row=0, column=2, sticky="nsew", padx=2, pady=(0, 2))
    buttons["memory_r"].grid(row=0, column=3, sticky="nsew", padx=(2, 0), pady=(0, 2))
    buttons["root"].grid(row=1, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["open_parenthesis"].grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
    buttons["close_parenthesis"].grid(row=1, column=2, sticky="nsew", padx=2, pady=2)
    buttons["divide"].grid(row=1, column=3, sticky="nsew", padx=(2, 0), pady=2)
    buttons["7"].grid(row=2, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["8"].grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
    buttons["9"].grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
    buttons["multiply"].grid(row=2, column=3, sticky="nsew", padx=(2, 0), pady=2)
    buttons["4"].grid(row=3, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["5"].grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
    buttons["6"].grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
    buttons["minus"].grid(row=3, column=3, sticky="nsew", padx=(2, 0), pady=2)
    buttons["1"].grid(row=4, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["2"].grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
    buttons["3"].grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
    buttons["plus"].grid(row=4, column=3, sticky="nsew", padx=(2, 0), pady=2)
    buttons["clear"].grid(row=5, column=0, sticky="nsew", padx=(0, 2), pady=(2, 0))
    buttons["0"].grid(row=5, column=1, sticky="nsew", padx=2, pady=(2, 0))
    buttons["dot"].grid(row=5, column=2, sticky="nsew", padx=2, pady=(2, 0))
    buttons["equals"].grid(row=5, column=3, sticky="nsew", padx=(2, 0), pady=(2, 0))

def advanced_mode():
    for i in buttons:
        buttons[i].grid_forget()
    frameCalculator.rowconfigure(6, weight=1)
    frameCalculator.rowconfigure(7, weight=1)
    frameCalculator.columnconfigure(4, weight=1)
    buttons["memory_p"].grid(row=0, column=0, sticky="nsew", padx=(0, 2), pady=(0, 2))
    buttons["memory_m"].grid(row=0, column=1, sticky="nsew", padx=2, pady=(0, 2))
    buttons["memory_s"].grid(row=0, column=2, sticky="nsew", padx=2, pady=(0, 2))
    buttons["memory_c"].grid(row=0, column=3, sticky="nsew", padx=2, pady=(0, 2))
    buttons["memory_r"].grid(row=0, column=4, sticky="nsew", padx=(2, 0), pady=(0, 2))
    buttons["bin"].grid(row=1, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["oct"].grid(row=1, column=1, sticky="nsew", padx=2, pady=2)
    buttons["hex"].grid(row=1, column=2, sticky="nsew", padx=2, pady=2)
    buttons["e"].grid(row=1, column=3, sticky="nsew", padx=2, pady=2)
    buttons["10_power_x"].grid(row=1, column=4, sticky="nsew", padx=(2, 0), pady=2)
    buttons["square"].grid(row=2, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["root"].grid(row=2, column=1, sticky="nsew", padx=2, pady=2)
    buttons["power"].grid(row=2, column=2, sticky="nsew", padx=2, pady=2)
    buttons["ln"].grid(row=2, column=3, sticky="nsew", padx=2, pady=2)
    buttons["log"].grid(row=2, column=4, sticky="nsew", padx=(2, 0), pady=2)
    buttons["1/x"].grid(row=3, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["factorial"].grid(row=3, column=1, sticky="nsew", padx=2, pady=2)
    buttons["open_parenthesis"].grid(row=3, column=2, sticky="nsew", padx=2, pady=2)
    buttons["close_parenthesis"].grid(row=3, column=3, sticky="nsew", padx=2, pady=2)
    buttons["divide"].grid(row=3, column=4, sticky="nsew", padx=(2, 0), pady=2)
    buttons["percent"].grid(row=4, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["7"].grid(row=4, column=1, sticky="nsew", padx=2, pady=2)
    buttons["8"].grid(row=4, column=2, sticky="nsew", padx=2, pady=2)
    buttons["9"].grid(row=4, column=3, sticky="nsew", padx=2, pady=2)
    buttons["multiply"].grid(row=4, column=4, sticky="nsew", padx=(2, 0), pady=2)
    buttons["mod"].grid(row=5, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["4"].grid(row=5, column=1, sticky="nsew", padx=2, pady=2)
    buttons["5"].grid(row=5, column=2, sticky="nsew", padx=2, pady=2)
    buttons["6"].grid(row=5, column=3, sticky="nsew", padx=2, pady=2)
    buttons["minus"].grid(row=5, column=4, sticky="nsew", padx=(2, 0), pady=2)
    buttons["abs"].grid(row=6, column=0, sticky="nsew", padx=(0, 2), pady=2)
    buttons["1"].grid(row=6, column=1, sticky="nsew", padx=2, pady=2)
    buttons["2"].grid(row=6, column=2, sticky="nsew", padx=2, pady=2)
    buttons["3"].grid(row=6, column=3, sticky="nsew", padx=2, pady=2)
    buttons["plus"].grid(row=6, column=4, sticky="nsew", padx=(2, 0), pady=2)
    buttons["clear"].grid(row=7, column=0, sticky="nsew", padx=(0, 2), pady=(2, 0))
    buttons["pi"].grid(row=7, column=1, sticky="nsew", padx=2, pady=(2, 0))
    buttons["0"].grid(row=7, column=2, sticky="nsew", padx=2, pady=(2, 0))
    buttons["dot"].grid(row=7, column=3, sticky="nsew", padx=2, pady=(2, 0))
    buttons["equals"].grid(row=7, column=4, sticky="nsew", padx=(2, 0), pady=(2, 0))

def switch_mode():
    if buttons["memory_s"].grid_info() == {}:
        advanced_mode()
        root.minsize(width=400, height=500)
    else:
        standard_mode()
        root.minsize(width=275, height=400)

def light_mode():
    root["bg"] = "#d1d1d1"
    frameCalculator["bg"] = "#d1d1d1"
    bar.configure(bg="#ffffff", fg="#000000", insertbackground="#000000", selectbackground="#bbbbbb", selectforeground="#000000")
    menu_B3.configure(background="#f0f0f0", foreground="#000000", activebackground="#d1d1d1", activeforeground="#000000")
    for i in buttons:
        buttons[i].configure(bg="#ffffff", fg="#000000", activebackground="#bbbbbb", activeforeground="#000000")
        buttons[i].bind("<Enter>", lambda event, button=buttons[i]: button.configure(bg="#f0f0f0", fg="#000000"))
        buttons[i].bind("<Leave>", lambda event, button=buttons[i]: button.configure(bg="#ffffff", fg="#000000"))

def dark_mode():
    root["bg"] = "#000000"
    frameCalculator["bg"] = "#000000"
    bar.configure(bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff", selectbackground="#777777", selectforeground="#ffffff")
    menu_B3.configure(background="#000000", foreground="#ffffff", activebackground="#3d3d3d", activeforeground="#ffffff")
    for i in buttons:
        buttons[i].configure(bg="#2e2e2e", fg="#ffffff", activebackground="#444444", activeforeground="#ffffff")
        buttons[i].bind("<Enter>", lambda event, button=buttons[i]: button.configure(bg="#3d3d3d", fg="#ffffff"))
        buttons[i].bind("<Leave>", lambda event, button=buttons[i]: button.configure(bg="#2e2e2e", fg="#ffffff"))

def switch_theme():
    if root["bg"] == "#d1d1d1":
        dark_mode()
    else:
        light_mode()

def help_window():
    window = Toplevel()
    window.title("Help - Calculator4pc")
    window.geometry("700x510")
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    help_tabs = Notebook(window)
    help_tabs.grid(row=0, column=0, sticky="nsew")
    about = Text(help_tabs, relief=FLAT, border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap=WORD, background="#dcb")
    about.insert(INSERT, f"Calculator4pc\nCopyright (c) 2025-{str(datetime.datetime.now().year)}: Waylon Boer\n\nCalculator4pc is a calculator app.")
    about.configure(state=DISABLED)
    help_tabs.add(about, text="About")
    mit_license = Text(help_tabs, relief=FLAT, border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap=WORD, background="#dcb")
    mit_license.insert(INSERT, """MIT License

Copyright (c) 2025 Waylon Boer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")
    mit_license.configure(state=DISABLED)
    help_tabs.add(mit_license, text="License")
    window.mainloop()

if __name__ == "__main__":
    root = Tk()
    root.title("Calculator4pc")
    root.minsize(width=275, height=400)
    memory = 0
    root["bd"] = 16
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    bar = Entry(root, font=("", 15), relief=FLAT)
    bar.grid(row=0, column=0, sticky="nsew", ipady=4, pady=(0, 4))
    bar.bind("<Return>", lambda event: buttons["equals"].invoke())
    frameCalculator = Frame(root, bg="#e1e1e1")
    frameCalculator.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
    for i in range(0, 6):
        frameCalculator.rowconfigure(i, weight=1)
    for j in range(0, 4):
        frameCalculator.columnconfigure(j, weight=1)
    buttons = {}
    buttons["0"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="0", command=lambda: bar.insert(INSERT, "0"))
    buttons["1"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="1", command=lambda: bar.insert(INSERT, "1"))
    buttons["2"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="2", command=lambda: bar.insert(INSERT, "2"))
    buttons["3"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="3", command=lambda: bar.insert(INSERT, "3"))
    buttons["4"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="4", command=lambda: bar.insert(INSERT, "4"))
    buttons["5"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="5", command=lambda: bar.insert(INSERT, "5"))
    buttons["6"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="6", command=lambda: bar.insert(INSERT, "6"))
    buttons["7"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="7", command=lambda: bar.insert(INSERT, "7"))
    buttons["8"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="8", command=lambda: bar.insert(INSERT, "8"))
    buttons["9"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="9", command=lambda: bar.insert(INSERT, "9"))
    buttons["dot"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text=".", command=lambda: bar.insert(INSERT, "."))
    buttons["plus"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="+", command=lambda: bar.insert(INSERT, " + "))
    buttons["minus"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="-", command=lambda: bar.insert(INSERT, " - "))
    buttons["multiply"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="x", command=lambda: bar.insert(INSERT, " * "))
    buttons["divide"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="÷", command=lambda: bar.insert(INSERT, " ÷ "))
    buttons["power"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="xⁿ", command=lambda: bar.insert(INSERT, " ** "))
    buttons["square"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="x²", command=lambda: calculate("s"))
    buttons["root"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="√", command=lambda: calculate("r"))
    buttons["1/x"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="1/x", command=lambda: calculate("i"))
    buttons["equals"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="=", command=lambda: calculate("e"))
    buttons["bin"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="bin", command=lambda: calculate("bin"))
    buttons["oct"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="oct", command=lambda: calculate("oct"))
    buttons["hex"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="hex", command=lambda: calculate("hex"))
    buttons["clear"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="C", command=lambda: bar.delete(0, END))
    buttons["memory_p"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="M+", command=memory_p)
    buttons["memory_m"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="M-", command=memory_m)
    buttons["memory_s"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="MS", command=memory_s)
    buttons["memory_c"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="MC", command=memory_c)
    buttons["memory_r"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="MR", command=memory_r)
    buttons["e"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="e", command=lambda: bar.insert(INSERT, "e"))
    buttons["10_power_x"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="10^x", command=lambda: bar.insert(INSERT, "10 ** "))
    buttons["ln"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="ln", command=lambda: calculate("ln"))
    buttons["log"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="log", command=lambda: calculate("log"))
    buttons["factorial"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="!", command=lambda: calculate("f"))
    buttons["percent"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="%", command=lambda: bar.insert(INSERT, "%"))
    buttons["mod"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="mod", command=lambda: bar.insert(INSERT, "mod"))
    buttons["abs"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="|x|", command=lambda: calculate("abs"))
    buttons["pi"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="π", command=lambda: bar.insert(INSERT, "π"))
    buttons["open_parenthesis"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text="(", command=lambda: bar.insert(INSERT, "("))
    buttons["close_parenthesis"] = Button(frameCalculator, width=1, font=("tkDefaultFont", 15), relief=FLAT, bd=0, text=")", command=lambda: bar.insert(INSERT, ")"))
    menu_B3 = Menu(root, tearoff=False, activeborderwidth=2.5)
    menu_B3.add_command(label="Switch Mode", command=switch_mode)
    menu_B3.add_command(label="Switch Theme", command=switch_theme)
    menu_B3.add_separator()
    always_on_top = IntVar()
    menu_B3.add_checkbutton(label="Always on top", command=lambda: root.attributes("-topmost", not root.attributes("-topmost")), variable=always_on_top)
    menu_B3.add_command(label="Help", command=help_window)
    standard_mode()
    light_mode()
    root.bind("<F1>", lambda event: help_window())
    root.bind("<Button-3>", lambda event: menu_B3.tk_popup(event.x_root, event.y_root))
    root.mainloop()
