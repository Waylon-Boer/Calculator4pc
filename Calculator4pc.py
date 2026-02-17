import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from datetime import datetime, timedelta
import math, ast, re, calendar, random
import ctypes as ct

class MathParser(ast.NodeVisitor):
    def __init__(self, angle_mode = 1):
        self.angle_mode = angle_mode
        self.func = {"sin": math.sin, "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos, "atan": math.atan, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh, "asinh": math.asinh, "acosh": math.acosh, "atanh": math.atanh, "sqrt": math.sqrt, "log": math.log10, "ln": math.log, "abs": abs}
        self.const = {"pi": math.pi, "e": math.e}

    def visit_Expression(self, node):
        return self.visit(node.body)
    
    def visit_BinOp(self, node):
        l = self.visit(node.left); r = self.visit(node.right); o = node.op
        if isinstance(o, ast.Add): return l + r
        if isinstance(o, ast.Sub): return l - r
        if isinstance(o, ast.Mult): return l * r
        if isinstance(o, ast.Div): return l / r
        if isinstance(o, ast.FloorDiv): return l // r
        if isinstance(o, ast.Mod): return l % r
        if isinstance(o, ast.Pow): return l ** r
        raise ValueError
    
    def visit_UnaryOp(self, node):
        v = self.visit(node.operand)
        if isinstance(node.op, ast.UAdd): return +v
        if isinstance(node.op, ast.USub): return -v
        raise ValueError
    
    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError
        f = node.func.id
        if f not in self.func:
            raise ValueError
        if len(node.args) != 1:
            raise ValueError
        a = self.visit(node.args[0])
        if self.angle_mode == 0 and f in ("sin", "cos", "tan"):
            a = math.radians(a)
        if self.angle_mode == 0 and f in ("asin", "acos", "atan"):
            return math.degrees(self.func[f](a))
        return self.func[f](a)
    def visit_Name(self, node):
        if node.id in self.const:
            return self.const[node.id]
        raise ValueError
    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError
    def generic_visit(self, node):
        raise ValueError

def parse_expr(expr, angle_mode = 1):
    tree = ast.parse(expr, mode = "eval")
    return MathParser(angle_mode).visit(tree)

class Calculator4pc:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator4pc")
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        self.prefix = id(self.root)
        self.style = ttk.Style(self.root)

        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        self.toolbar_calculator = tk.Frame(self.root)
        self.toolbar_calculator.grid(row=0, column=0, sticky="nsew")
        self.toolbar_calculator.columnconfigure(1, weight=1)
        self.menubutton = ttk.Menubutton(self.toolbar_calculator, text="Standard", style=f"{self.prefix}.TMenubutton")
        self.menubutton.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=5)
        self.option = tk.IntVar(value=0)
        self.menu_options = tk.Menu(self.menubutton, tearoff=False, activeborderwidth=2.5)
        self.menu_options.add_radiobutton(label="Standard", variable=self.option, value=0, command=self.go_to)
        self.menu_options.add_radiobutton(label="Scientific", variable=self.option, value=1, command=self.go_to)
        self.menu_options.add_separator()
        self.menu_options.add_radiobutton(label="Base Conversion", variable=self.option, value=2, command=self.go_to)
        self.menu_options.add_radiobutton(label="Date Calculation", variable=self.option, value=3, command=self.go_to)
        self.menu_options.add_radiobutton(label="Probability", variable=self.option, value=4, command=self.go_to)
        self.menu_options.add_separator()
        self.menu_options.add_command(label="Help", command=self.help_window)
        self.menubutton.configure(menu=self.menu_options)
        self.button_new = tk.Button(self.toolbar_calculator, text="+", font=(font.nametofont("TkFixedFont").actual()["family"], 10), width=5, bd=0, relief=tk.FLAT, command=self.open_new_window)
        self.button_new.grid(row=0, column=1, sticky="nse")
        self.button_sidebar = tk.Button(self.toolbar_calculator, text=">>", font=(font.nametofont("TkFixedFont").actual()["family"], 10), width=5, bd=0, relief=tk.FLAT, command=self.toggle_notepad)
        self.button_sidebar.grid(row=0, column=2, sticky="nse")
        
        self.context_menu_edit = tk.Menu(self.root, tearoff=False, activeborderwidth=2.5)
        self.context_menu_edit.add_command(label="Cut", command=lambda: self.context_widget.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        self.context_menu_edit.add_command(label="Copy", command=lambda: self.context_widget.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        self.context_menu_edit.add_command(label="Paste", command=lambda: self.context_widget.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        self.context_menu_edit.add_separator()
        self.context_menu_edit.add_command(label="Select All", command=lambda: self.context_widget.event_generate("<<SelectAll>>"), accelerator="Ctrl+A")

        self.std_frame = tk.Frame(self.root)
        self.std_frame.grid(row=1, column=0, sticky="nsew")
        self.std_frame.rowconfigure(2, weight=1)
        self.std_frame.columnconfigure(0, weight=1)

        self.std_value = None
        self.std_memory = 0

        self.std_bar = tk.Entry(self.std_frame, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), border=5, justify="right")
        self.std_bar.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.std_bar.bind("<Button-3>", self.popup_context_menu_edit)

        self.std_memory_button_frame = tk.Frame(self.std_frame)
        self.std_memory_button_frame.grid(row=1, column=0, sticky="nsew")
        self.std_memory_button_frame.rowconfigure(0, weight=1)
        for i in range(0, 5):
            self.std_memory_button_frame.columnconfigure(i, weight=1)

        self.std_memory_buttons = {}

        self.std_memory_buttons[0] = tk.Button(self.std_memory_button_frame, text="M+", command=self.std_m_plus, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_memory_buttons[0].grid(row=0, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.std_memory_buttons[1] = tk.Button(self.std_memory_button_frame, text="M-", command=self.std_m_minus, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_memory_buttons[1].grid(row=0, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_memory_buttons[2] = tk.Button(self.std_memory_button_frame, text="MS", command=self.std_ms, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_memory_buttons[2].grid(row=0, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_memory_buttons[3] = tk.Button(self.std_memory_button_frame, text="MR", command=self.std_mr, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_memory_buttons[3].grid(row=0, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_memory_buttons[4] = tk.Button(self.std_memory_button_frame, text="MC", command=self.std_mc, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_memory_buttons[4].grid(row=0, column=4, sticky="nsew", padx=(0, 2), pady=(0, 2))

        self.std_button_frame = tk.Frame(self.std_frame, width=320)
        self.std_button_frame.grid(row=2, column=0, sticky="nsew")
        for i in range(0, 6):
            self.std_button_frame.rowconfigure(i, weight=1)
        for j in range(0, 4):
            self.std_button_frame.columnconfigure(j, weight=1)
            
        self.std_buttons = {}
        self.std_operator_buttons = {}
        self.std_operation = None

        self.std_buttons[(0, 0)] = tk.Button(self.std_button_frame, text="%", command=lambda: self.std_calculate("percent"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(0, 0)].grid(row=0, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.std_buttons[(0, 1)] = tk.Button(self.std_button_frame, text="CE", command=lambda: self.std_bar.delete(0, tk.END), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(0, 1)].grid(row=0, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_buttons[(0, 2)] = tk.Button(self.std_button_frame, text="C", command=self.std_clear, width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(0, 2)].grid(row=0, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_buttons[(0, 3)] = tk.Button(self.std_button_frame, text="⌫", command=lambda: self.std_bar.delete(self.std_bar.index(tk.INSERT) - 1), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(0, 3)].grid(row=0, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))

        self.std_buttons[(1, 0)] = tk.Button(self.std_button_frame, text="x²", command=lambda: self.std_calculate("sq"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(1, 0)].grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.std_buttons[(1, 1)] = tk.Button(self.std_button_frame, text="√", command=lambda: self.std_calculate("sqrt"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(1, 1)].grid(row=1, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_buttons[(1, 2)] = tk.Button(self.std_button_frame, text="1/x", command=lambda: self.std_calculate("invert"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(1, 2)].grid(row=1, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_operator_buttons["/"] = tk.Button(self.std_button_frame, text="÷", command=lambda: self.std_set_operation("/"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_operator_buttons["/"].grid(row=1, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))

        self.std_buttons[(2, 0)] = tk.Button(self.std_button_frame, text="7", command=lambda: self.std_bar.insert(tk.INSERT, "7"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(2, 0)].grid(row=2, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.std_buttons[(2, 1)] = tk.Button(self.std_button_frame, text="8", command=lambda: self.std_bar.insert(tk.INSERT, "8"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(2, 1)].grid(row=2, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_buttons[(2, 2)] = tk.Button(self.std_button_frame, text="9", command=lambda: self.std_bar.insert(tk.INSERT, "9"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(2, 2)].grid(row=2, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_operator_buttons["*"] = tk.Button(self.std_button_frame, text="×", command=lambda: self.std_set_operation("*"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_operator_buttons["*"].grid(row=2, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        
        self.std_buttons[(3, 0)] = tk.Button(self.std_button_frame, text="4", command=lambda: self.std_bar.insert(tk.INSERT, "4"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(3, 0)].grid(row=3, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.std_buttons[(3, 1)] = tk.Button(self.std_button_frame, text="5", command=lambda: self.std_bar.insert(tk.INSERT, "5"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(3, 1)].grid(row=3, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_buttons[(3, 2)] = tk.Button(self.std_button_frame, text="6", command=lambda: self.std_bar.insert(tk.INSERT, "6"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(3, 2)].grid(row=3, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_operator_buttons["-"] = tk.Button(self.std_button_frame, text="-", command=lambda: self.std_set_operation("-"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_operator_buttons["-"].grid(row=3, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        
        self.std_buttons[(4, 0)] = tk.Button(self.std_button_frame, text="1", command=lambda: self.std_bar.insert(tk.INSERT, "1"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(4, 0)].grid(row=4, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.std_buttons[(4, 1)] = tk.Button(self.std_button_frame, text="2", command=lambda: self.std_bar.insert(tk.INSERT, "2"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(4, 1)].grid(row=4, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_buttons[(4, 2)] = tk.Button(self.std_button_frame, text="3", command=lambda: self.std_bar.insert(tk.INSERT, "3"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(4, 2)].grid(row=4, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_operator_buttons["+"] = tk.Button(self.std_button_frame, text="+", command=lambda: self.std_set_operation("+"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_operator_buttons["+"].grid(row=4, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
                
        self.std_buttons[(5, 0)] = tk.Button(self.std_button_frame, text="+/-", command=lambda: self.std_calculate("negate"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(5, 0)].grid(row=5, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.std_buttons[(5, 1)] = tk.Button(self.std_button_frame, text="0", command=lambda: self.std_bar.insert(tk.INSERT, "0"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(5, 1)].grid(row=5, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_buttons[(5, 2)] = tk.Button(self.std_button_frame, text=".", command=lambda: self.std_bar.insert(tk.INSERT, "."), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(5, 2)].grid(row=5, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.std_buttons[(5, 3)] = tk.Button(self.std_button_frame, text="=", command=lambda: self.std_calculate("calculate"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.std_buttons[(5, 3)].grid(row=5, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))

        self.sci_frame = tk.Frame(self.root)
        self.sci_frame.rowconfigure(1, weight=1)
        self.sci_frame.columnconfigure(0, weight=1)

        self.sci_memory = 0

        self.sci_subframe = tk.Frame(self.sci_frame)
        self.sci_subframe.grid(row=0, column=0, sticky="nsew")
        self.sci_subframe.rowconfigure(0, weight=1)
        self.sci_subframe.columnconfigure(5, weight=1)
        
        self.sci_subframe_buttons = {}

        self.sci_subframe_buttons[0] = tk.Button(self.sci_subframe, text="M+", width=4, command=self.sci_m_plus, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_subframe_buttons[0].grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.sci_subframe_buttons[1] = tk.Button(self.sci_subframe, text="M-", width=4, command=self.sci_m_minus, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_subframe_buttons[1].grid(row=0, column=1, sticky="nsew", padx=(0, 2), pady=2)
        self.sci_subframe_buttons[2] = tk.Button(self.sci_subframe, text="MS", width=4, command=self.sci_ms, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_subframe_buttons[2].grid(row=0, column=2, sticky="nsew", padx=(0, 2), pady=2)
        self.sci_subframe_buttons[3] = tk.Button(self.sci_subframe, text="MR", width=4, command=self.sci_mr, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_subframe_buttons[3].grid(row=0, column=3, sticky="nsew", padx=(0, 2), pady=2)
        self.sci_subframe_buttons[4] = tk.Button(self.sci_subframe, text="MC", width=4, command=self.sci_mc, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_subframe_buttons[4].grid(row=0, column=4, sticky="nsew", padx=(0, 2), pady=2)

        self.sci_bar = tk.Entry(self.sci_subframe, width=5, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), border=5, justify="right")
        self.sci_bar.grid(row=0, column=5, sticky="nsew", padx=(0, 2), pady=2)
        self.sci_bar.bind("<Button-3>", self.popup_context_menu_edit)
        
        self.sci_subframe_buttons[5] = tk.Button(self.sci_subframe, text="⌫", command=lambda: self.sci_bar.delete(0, tk.END) if self.sci_bar.get() in ["Cannot divide by zero", "Invalid input", "Syntax error", "Error"] else self.sci_bar.delete(self.sci_bar.index(tk.INSERT) - 1), width=4, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_subframe_buttons[5].grid(row=0, column=6, sticky="nsew", padx=(0, 2), pady=2)
        self.sci_subframe_buttons[6] = tk.Button(self.sci_subframe, text="C", command=lambda: self.sci_bar.delete(0, tk.END), width=4, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_subframe_buttons[6].grid(row=0, column=7, sticky="nsew", padx=(0, 2), pady=2)

        self.sci_button_frame = tk.Frame(self.sci_frame, width=320)
        self.sci_button_frame.grid(row=1, column=0, sticky="nsew")
        for i in range(0, 6):
            self.sci_button_frame.rowconfigure(i, weight=1)
        for j in range(0, 7):
            self.sci_button_frame.columnconfigure(j, weight=1)
            
        self.sci_buttons = {}

        self.sci_buttons[(0, 0)] = tk.Button(self.sci_button_frame, text="sin", command=lambda: self.sci_bar.insert(tk.INSERT, "sin("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(0, 1)] = tk.Button(self.sci_button_frame, text="cos", command=lambda: self.sci_bar.insert(tk.INSERT, "cos("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(0, 2)] = tk.Button(self.sci_button_frame, text="tan", command=lambda: self.sci_bar.insert(tk.INSERT, "tan("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(0, 3)] = tk.Button(self.sci_button_frame, text="√", command=lambda: self.sci_bar.insert(tk.INSERT, "sqrt("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(0, 4)] = tk.Button(self.sci_button_frame, text="x²", command=lambda: self.sci_bar.insert(tk.INSERT, "^2"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(0, 5)] = tk.Button(self.sci_button_frame, text="x³", command=lambda: self.sci_bar.insert(tk.INSERT, "^3"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(0, 6)] = tk.Button(self.sci_button_frame, text="^", command=lambda: self.sci_bar.insert(tk.INSERT, "^"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))

        self.sci_buttons[(1, 0)] = tk.Button(self.sci_button_frame, text="sin⁻¹", command=lambda: self.sci_bar.insert(tk.INSERT, "asin("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(1, 1)] = tk.Button(self.sci_button_frame, text="cos⁻¹", command=lambda: self.sci_bar.insert(tk.INSERT, "acos("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(1, 2)] = tk.Button(self.sci_button_frame, text="tan⁻¹", command=lambda: self.sci_bar.insert(tk.INSERT, "atan("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(1, 3)] = tk.Button(self.sci_button_frame, text="(", command=lambda: self.sci_bar.insert(tk.INSERT, "("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(1, 4)] = tk.Button(self.sci_button_frame, text=")", command=lambda: self.sci_bar.insert(tk.INSERT, ")"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(1, 5)] = tk.Button(self.sci_button_frame, text="%", command=lambda: self.sci_bar.insert(tk.INSERT, "%"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(1, 6)] = tk.Button(self.sci_button_frame, text="÷", command=lambda: self.sci_bar.insert(tk.INSERT, "/"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))

        self.sci_buttons[(2, 0)] = tk.Button(self.sci_button_frame, text="sinh", command=lambda: self.sci_bar.insert(tk.INSERT, "sinh("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(2, 1)] = tk.Button(self.sci_button_frame, text="cosh", command=lambda: self.sci_bar.insert(tk.INSERT, "cosh("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(2, 2)] = tk.Button(self.sci_button_frame, text="tanh", command=lambda: self.sci_bar.insert(tk.INSERT, "tanh("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(2, 3)] = tk.Button(self.sci_button_frame, text="7", command=lambda: self.sci_bar.insert(tk.INSERT, "7"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(2, 4)] = tk.Button(self.sci_button_frame, text="8", command=lambda: self.sci_bar.insert(tk.INSERT, "8"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(2, 5)] = tk.Button(self.sci_button_frame, text="9", command=lambda: self.sci_bar.insert(tk.INSERT, "9"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(2, 6)] = tk.Button(self.sci_button_frame, text="×", command=lambda: self.sci_bar.insert(tk.INSERT, "*"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))

        self.sci_buttons[(3, 0)] = tk.Button(self.sci_button_frame, text="sinh⁻¹", command=lambda: self.sci_bar.insert(tk.INSERT, "asinh("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(3, 1)] = tk.Button(self.sci_button_frame, text="cosh⁻¹", command=lambda: self.sci_bar.insert(tk.INSERT, "acosh("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(3, 2)] = tk.Button(self.sci_button_frame, text="tanh⁻¹", command=lambda: self.sci_bar.insert(tk.INSERT, "atanh("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(3, 3)] = tk.Button(self.sci_button_frame, text="4", command=lambda: self.sci_bar.insert(tk.INSERT, "4"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(3, 4)] = tk.Button(self.sci_button_frame, text="5", command=lambda: self.sci_bar.insert(tk.INSERT, "5"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(3, 5)] = tk.Button(self.sci_button_frame, text="6", command=lambda: self.sci_bar.insert(tk.INSERT, "6"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(3, 6)] = tk.Button(self.sci_button_frame, text="-", command=lambda: self.sci_bar.insert(tk.INSERT, "-"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))

        self.sci_buttons[(4, 0)] = tk.Button(self.sci_button_frame, text="1/x", command=lambda: self.sci_bar.insert(tk.INSERT, "^(-1)"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(4, 1)] = tk.Button(self.sci_button_frame, text="log", command=lambda: self.sci_bar.insert(tk.INSERT, "log("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(4, 2)] = tk.Button(self.sci_button_frame, text="ln", command=lambda: self.sci_bar.insert(tk.INSERT, "ln("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(4, 3)] = tk.Button(self.sci_button_frame, text="1", command=lambda: self.sci_bar.insert(tk.INSERT, "1"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(4, 4)] = tk.Button(self.sci_button_frame, text="2", command=lambda: self.sci_bar.insert(tk.INSERT, "2"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(4, 5)] = tk.Button(self.sci_button_frame, text="3", command=lambda: self.sci_bar.insert(tk.INSERT, "3"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(4, 6)] = tk.Button(self.sci_button_frame, text="+", command=lambda: self.sci_bar.insert(tk.INSERT, "+"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))

        self.sci_buttons[(5, 0)] = tk.Button(self.sci_button_frame, text="|x|", command=lambda: self.sci_bar.insert(tk.INSERT, "abs("), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(5, 1)] = tk.Button(self.sci_button_frame, text="10ˣ", command=lambda: self.sci_bar.insert(tk.INSERT, "*10^()"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(5, 2)] = tk.Button(self.sci_button_frame, text="e", command=lambda: self.sci_bar.insert(tk.INSERT, "e"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(5, 3)] = tk.Button(self.sci_button_frame, text="π", command=lambda: self.sci_bar.insert(tk.INSERT, "π"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(5, 4)] = tk.Button(self.sci_button_frame, text="0", command=lambda: self.sci_bar.insert(tk.INSERT, "0"), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(5, 5)] = tk.Button(self.sci_button_frame, text=".", command=lambda: self.sci_bar.insert(tk.INSERT, "."), width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.sci_buttons[(5, 6)] = tk.Button(self.sci_button_frame, text="=", command=self.sci_calculate, width=6, bd=0, relief=tk.FLAT, font=(font.nametofont("TkDefaultFont").actual()["family"], 13))

        self.sci_buttons[(0, 0)].grid(row=0, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.sci_buttons[(0, 1)].grid(row=0, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(0, 2)].grid(row=0, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(0, 3)].grid(row=0, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(0, 4)].grid(row=0, column=4, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(0, 5)].grid(row=0, column=5, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(0, 6)].grid(row=0, column=6, sticky="nsew", padx=(0, 2), pady=(0, 2))

        self.sci_buttons[(1, 0)].grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.sci_buttons[(1, 1)].grid(row=1, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(1, 2)].grid(row=1, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(1, 3)].grid(row=1, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(1, 4)].grid(row=1, column=4, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(1, 5)].grid(row=1, column=5, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(1, 6)].grid(row=1, column=6, sticky="nsew", padx=(0, 2), pady=(0, 2))

        self.sci_buttons[(2, 0)].grid(row=2, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.sci_buttons[(2, 1)].grid(row=2, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(2, 2)].grid(row=2, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(2, 3)].grid(row=2, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(2, 4)].grid(row=2, column=4, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(2, 5)].grid(row=2, column=5, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(2, 6)].grid(row=2, column=6, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(3, 0)].grid(row=3, column=0, sticky="nsew", padx=2, pady=(0, 2))

        self.sci_buttons[(3, 1)].grid(row=3, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(3, 2)].grid(row=3, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(3, 3)].grid(row=3, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(3, 4)].grid(row=3, column=4, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(3, 5)].grid(row=3, column=5, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(3, 6)].grid(row=3, column=6, sticky="nsew", padx=(0, 2), pady=(0, 2))

        self.sci_buttons[(4, 0)].grid(row=4, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.sci_buttons[(4, 1)].grid(row=4, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(4, 2)].grid(row=4, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(4, 3)].grid(row=4, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(4, 4)].grid(row=4, column=4, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(4, 5)].grid(row=4, column=5, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(4, 6)].grid(row=4, column=6, sticky="nsew", padx=(0, 2), pady=(0, 2))

        self.sci_buttons[(5, 0)].grid(row=5, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.sci_buttons[(5, 1)].grid(row=5, column=1, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(5, 2)].grid(row=5, column=2, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(5, 3)].grid(row=5, column=3, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(5, 4)].grid(row=5, column=4, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(5, 5)].grid(row=5, column=5, sticky="nsew", padx=(0, 2), pady=(0, 2))
        self.sci_buttons[(5, 6)].grid(row=5, column=6, sticky="nsew", padx=(0, 2), pady=(0, 2))
        
        self.bc_frame = tk.Frame(self.root, bd=16)
        for i in range(0, 4):
            self.bc_frame.rowconfigure(i, weight=1)
        self.bc_frame.columnconfigure(1, weight=1)

        self.bc_bin_label = tk.Label(self.bc_frame, text="Binary", width=13, anchor="w", font=(font.nametofont("TkDefaultFont").actual()["family"], 11))
        self.bc_bin_label.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        self.bc_bin_entry = tk.Entry(self.bc_frame, bd=4, relief=tk.FLAT, font=(font.nametofont("TkFixedFont").actual()["family"], 12), justify="right")
        self.bc_bin_entry.grid(row=0, column=1, sticky="nsew", pady=(0, 4))
        self.bc_bin_entry.bind("<KeyRelease>", lambda event: self.bc_update(2) if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)

        self.bc_oct_label = tk.Label(self.bc_frame, text="Octal", width=13, anchor="w", font=(font.nametofont("TkDefaultFont").actual()["family"], 11))
        self.bc_oct_label.grid(row=1, column=0, sticky="nsew", pady=(0, 4))
        self.bc_oct_entry = tk.Entry(self.bc_frame, bd=4, relief=tk.FLAT, font=(font.nametofont("TkFixedFont").actual()["family"], 12), justify="right")
        self.bc_oct_entry.grid(row=1, column=1, sticky="nsew", pady=(0, 4))
        self.bc_oct_entry.bind("<KeyRelease>", lambda event: self.bc_update(8) if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)

        self.bc_dec_label = tk.Label(self.bc_frame, text="Decimal", width=13, anchor="w", font=(font.nametofont("TkDefaultFont").actual()["family"], 11))
        self.bc_dec_label.grid(row=2, column=0, sticky="nsew", pady=(0, 4))
        self.bc_dec_entry = tk.Entry(self.bc_frame, bd=4, relief=tk.FLAT, font=(font.nametofont("TkFixedFont").actual()["family"], 12), justify="right")
        self.bc_dec_entry.grid(row=2, column=1, sticky="nsew", pady=(0, 4))
        self.bc_dec_entry.bind("<KeyRelease>", lambda event: self.bc_update(10) if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)

        self.bc_hex_label = tk.Label(self.bc_frame, text="Hexadecimal", width=13, anchor="w", font=(font.nametofont("TkDefaultFont").actual()["family"], 11))
        self.bc_hex_label.grid(row=3, column=0, sticky="nsew")
        self.bc_hex_entry = tk.Entry(self.bc_frame, bd=4, relief=tk.FLAT, font=(font.nametofont("TkFixedFont").actual()["family"], 12), justify="right")
        self.bc_hex_entry.grid(row=3, column=1, sticky="nsew")
        self.bc_hex_entry.bind("<KeyRelease>", lambda event: self.bc_update(16) if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)

        self.dc_frame = tk.Frame(self.root, bd=16)
        self.dc_frame.rowconfigure(4, weight=1)
        self.dc_frame.columnconfigure(0, weight=1)

        self.dc_from_label = tk.Label(self.dc_frame, text="From", font=(font.nametofont("TkDefaultFont").actual()["family"], 13), anchor="w")
        self.dc_from_label.grid(row=0, column=0, sticky="nsew")
        self.dc_from_frame = tk.Frame(self.dc_frame)
        self.dc_from_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        for i in range(0, 3):
            self.dc_from_frame.columnconfigure(i, weight=1)
        self.dc_from_label_d = tk.Label(self.dc_from_frame, text="Day", anchor="w")
        self.dc_from_label_d.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        self.dc_from_label_m = tk.Label(self.dc_from_frame, text="Month", anchor="w")
        self.dc_from_label_m.grid(row=0, column=1, sticky="nsew", padx=(0, 2))
        self.dc_from_label_y = tk.Label(self.dc_from_frame, text="Year", anchor="w")
        self.dc_from_label_y.grid(row=0, column=2, sticky="nsew")
        self.dc_from_combobox_d = ttk.Combobox(self.dc_from_frame, values=list(range(1, 32)), state="readonly", style=f"{self.prefix}.TCombobox")
        self.dc_from_combobox_d.grid(row=1, column=0, sticky="nsew", padx=(0, 2))
        self.dc_from_combobox_m = ttk.Combobox(self.dc_from_frame, values=self.months, state="readonly", style=f"{self.prefix}.TCombobox")
        self.dc_from_combobox_m.grid(row=1, column=1, sticky="nsew", padx=(0, 2))
        self.dc_from_combobox_y = ttk.Combobox(self.dc_from_frame, values=list(range(0, 10000)), state="readonly", style=f"{self.prefix}.TCombobox")
        self.dc_from_combobox_y.grid(row=1, column=2, sticky="nsew")

        self.dc_to_label = tk.Label(self.dc_frame, text="To", font=(font.nametofont("TkDefaultFont").actual()["family"], 13), anchor="w")
        self.dc_to_label.grid(row=2, column=0, sticky="nsew")
        self.dc_to_frame = tk.Frame(self.dc_frame)
        self.dc_to_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
        for i in range(0, 3):
            self.dc_to_frame.columnconfigure(i, weight=1)
        self.dc_to_label_d = tk.Label(self.dc_to_frame, text="Day", anchor="w")
        self.dc_to_label_d.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        self.dc_to_label_m = tk.Label(self.dc_to_frame, text="Month", anchor="w")
        self.dc_to_label_m.grid(row=0, column=1, sticky="nsew", padx=(0, 2))
        self.dc_to_label_y = tk.Label(self.dc_to_frame, text="Year", anchor="w")
        self.dc_to_label_y.grid(row=0, column=2, sticky="nsew")
        self.dc_to_combobox_d = ttk.Combobox(self.dc_to_frame, values=list(range(1, 32)), state="readonly", style=f"{self.prefix}.TCombobox")
        self.dc_to_combobox_d.grid(row=1, column=0, sticky="nsew", padx=(0, 2))
        self.dc_to_combobox_m = ttk.Combobox(self.dc_to_frame, values=self.months, state="readonly", style=f"{self.prefix}.TCombobox")
        self.dc_to_combobox_m.grid(row=1, column=1, sticky="nsew", padx=(0, 2))
        self.dc_to_combobox_y = ttk.Combobox(self.dc_to_frame, values=list(range(0, 10000)), state="readonly", style=f"{self.prefix}.TCombobox")
        self.dc_to_combobox_y.grid(row=1, column=2, sticky="nsew")

        self.dc_label_difference = tk.Label(self.dc_frame, text="Difference", font=(font.nametofont("TkDefaultFont").actual()["family"], 13), anchor="w")
        self.dc_label_difference.grid(row=4, column=0, sticky="sew")
        self.dc_frame_difference = tk.Frame(self.dc_frame)
        self.dc_frame_difference.grid(row=5, column=0, sticky="nsew")
        self.dc_frame_difference.columnconfigure(3, weight=1)
        self.dc_button_days = tk.Button(self.dc_frame_difference, text="+", anchor="w", font=(font.nametofont("TkFixedFont").actual()["family"], 11), bd=0, relief=tk.FLAT, command=lambda: (self.dc_button_days.configure(text="-" if self.dc_button_days.cget("text") == "+" else "+"), self.dc_calculate_dmy()))
        self.dc_button_days.grid(row=0, column=0, sticky="w")
        self.dc_combobox_days = ttk.Combobox(self.dc_frame_difference, values=list(range(0, 1001)), width=10, state="readonly", style=f"{self.prefix}.TCombobox")
        self.dc_combobox_days.grid(row=0, column=1, sticky="w")
        self.dc_combobox_days.bind("<<ComboboxSelected>>", lambda event: self.dc_calculate_dmy())
        self.dc_label_days = tk.Label(self.dc_frame_difference, font=(font.nametofont("TkDefaultFont").actual()["family"], 11), anchor="w")
        self.dc_label_days.grid(row=0, column=2, sticky="w", padx=(2, 0))
        self.dc_button_today = tk.Button(self.dc_frame_difference, text="Today", font=(font.nametofont("TkDefaultFont").actual()["family"], 11), bd=0, relief=tk.FLAT, command=self.dc_go_to_today)
        self.dc_button_today.grid(row=0, column=3, sticky="e")

        for widget in [self.dc_from_combobox_d, self.dc_from_combobox_m, self.dc_from_combobox_y, self.dc_to_combobox_d, self.dc_to_combobox_m, self.dc_to_combobox_y]:
            widget.bind("<<ComboboxSelected>>", lambda event: (self.dc_calculate_difference(), self.dc_frame.focus_set()))

        self.dc_set_default()

        self.prb_frame = tk.Frame(self.root, bd=16)
        self.prb_frame.columnconfigure(0, weight=1)
        
        self.prb_cnr_label = tk.Label(self.prb_frame, text="Combinatorics", font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.prb_cnr_label.grid(row=0, column=0, sticky="nsw", pady=(0, 2))
        self.prb_cnr_frame = tk.Frame(self.prb_frame)
        self.prb_cnr_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        for i in range(0, 5, 2):
            self.prb_cnr_frame.columnconfigure(i, weight=1)
        self.prb_cnr_entry_n = tk.Entry(self.prb_cnr_frame, font=(font.nametofont("TkDefaultFont").actual()["family"], 11), bd=4, relief=tk.FLAT)
        self.prb_cnr_entry_n.grid(row=0, column=0, sticky="nsew")
        self.prb_cnr_entry_n.bind("<KeyRelease>", lambda event: self.prb_cnr_validate(self.prb_cnr_entry_n) if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)
        self.prb_cnr_button_operation = tk.Button(self.prb_cnr_frame, text="nCr", command=self.prb_switch_operation, width=5, bd=0, relief=tk.FLAT)
        self.prb_cnr_button_operation.grid(row=0, column=1, sticky="nsew")
        self.prb_cnr_entry_r = tk.Entry(self.prb_cnr_frame, font=(font.nametofont("TkDefaultFont").actual()["family"], 11), bd=4, relief=tk.FLAT)
        self.prb_cnr_entry_r.grid(row=0, column=2, sticky="nsew")
        self.prb_cnr_entry_r.bind("<KeyRelease>", lambda event: self.prb_cnr_validate(self.prb_cnr_entry_r) if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)
        self.prb_cnr_button_equal_sign = tk.Button(self.prb_cnr_frame, text="=", command=self.prb_cnr_calculate, width=5, bd=0, relief=tk.FLAT)
        self.prb_cnr_button_equal_sign.grid(row=0, column=3, sticky="nsew")
        self.prb_cnr_entry_ans = tk.Entry(self.prb_cnr_frame, font=(font.nametofont("TkDefaultFont").actual()["family"], 11), bd=4, relief=tk.FLAT)
        self.prb_cnr_entry_ans.grid(row=0, column=4, sticky="nsew")

        self.prb_rng_label = tk.Label(self.prb_frame, text="Random Number Generator", font=(font.nametofont("TkDefaultFont").actual()["family"], 13))
        self.prb_rng_label.grid(row=2, column=0, sticky="nw", pady=(0, 2))
        self.prb_rng_frame = tk.Frame(self.prb_frame)
        self.prb_rng_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
        self.prb_rng_frame.columnconfigure(0, weight=1)
        self.prb_rng_frame.columnconfigure(1, weight=1)
        self.prb_rng_label_min = tk.Label(self.prb_rng_frame, text="Min", justify="left")
        self.prb_rng_label_min.grid(row=0, column=0, sticky="nsw", padx=(0, 8))
        self.prb_rng_label_max = tk.Label(self.prb_rng_frame, text="Max", justify="left")
        self.prb_rng_label_max.grid(row=0, column=1, sticky="nsw", padx=(0, 8))
        self.prb_rng_label_count = tk.Label(self.prb_rng_frame, text="Count", justify="left")
        self.prb_rng_label_count.grid(row=0, column=2, sticky="nsw")
        self.prb_rng_entry_min = tk.Entry(self.prb_rng_frame, font=(font.nametofont("TkDefaultFont").actual()["family"], 11), bd=4, relief=tk.FLAT)
        self.prb_rng_entry_min.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        self.prb_rng_entry_min.bind("<KeyRelease>", lambda event: self.prb_rng_validate(self.prb_rng_entry_min) if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)
        self.prb_rng_entry_max = tk.Entry(self.prb_rng_frame, font=(font.nametofont("TkDefaultFont").actual()["family"], 11), bd=4, relief=tk.FLAT)
        self.prb_rng_entry_max.grid(row=1, column=1, sticky="nsew", padx=(0, 8))
        self.prb_rng_entry_max.bind("<KeyRelease>", lambda event: self.prb_rng_validate(self.prb_rng_entry_max) if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)
        self.prb_rng_frame_count = tk.Frame(self.prb_rng_frame)
        self.prb_rng_frame_count.grid(row=1, column=2, sticky="nsew")
        self.prb_rng_frame_count.rowconfigure(0, weight=1)
        self.prb_rng_frame_count.columnconfigure(0, weight=1)
        self.prb_rng_entry_count = tk.Entry(self.prb_rng_frame_count, font=(font.nametofont("TkDefaultFont").actual()["family"], 11), width=5, bd=4, relief=tk.FLAT)
        self.prb_rng_entry_count.grid(row=0, column=0, sticky="nsew")
        self.prb_rng_entry_count.bind("<KeyRelease>", lambda event: self.prb_rng_count_validate() if (event.char and event.char.isprintable()) or event.keysym in ("BackSpace", "Delete") else None)
        self.prb_rng_frame_count_buttons = tk.Frame(self.prb_rng_frame_count)
        self.prb_rng_frame_count_buttons.grid(row=0, column=1, sticky="nsew")
        self.prb_rng_frame_count_buttons.rowconfigure(0, weight=1)
        self.prb_rng_frame_count_buttons.rowconfigure(1, weight=1)
        self.prb_rng_button_count_plus = tk.Button(self.prb_rng_frame_count_buttons, text="+", font=(font.nametofont("TkFixedFont").actual()["family"], 8), command=lambda: self.prb_rng_count_adjust(1), bd=0, relief=tk.FLAT)
        self.prb_rng_button_count_plus.grid(row=0, column=0, sticky="nsew")
        self.prb_rng_button_count_minus = tk.Button(self.prb_rng_frame_count_buttons, text="-", font=(font.nametofont("TkFixedFont").actual()["family"], 8), command=lambda: self.prb_rng_count_adjust(-1), bd=0, relief=tk.FLAT)
        self.prb_rng_button_count_minus.grid(row=1, column=0, sticky="nsew")

        self.prb_ans_entry = tk.Entry(self.prb_frame, font=(font.nametofont("TkDefaultFont").actual()["family"], 11), bd=4, relief=tk.FLAT)
        self.prb_ans_entry.grid(row=4, column=0, sticky="nsew", pady=(0, 8))
        self.prb_ans_button_generate = tk.Button(self.prb_frame, text="Generate", width=8, command=self.prb_rng_generate, justify="left", font=(font.nametofont("TkDefaultFont").actual()["family"], 11), bd=0, relief=tk.FLAT)
        self.prb_ans_button_generate.grid(row=5, column=0, sticky="nsw")

        self.toolbar_notepad = tk.Frame(self.root)
        self.toolbar_notepad.rowconfigure(0, weight=1)
        self.toolbar_notepad.columnconfigure(3, weight=1)
        self.button_left = tk.Button(self.toolbar_notepad, text="L", width=5, bd=0, relief=tk.FLAT, command=lambda: (self.notepad.tag_configure("text", justify="left"), self.notepad.tag_add("text", 1.0, "end")))
        self.button_left.grid(row=0, column=0, sticky="nsw")
        self.button_center = tk.Button(self.toolbar_notepad, text="C", width=5, bd=0, relief=tk.FLAT, command=lambda: (self.notepad.tag_configure("text", justify="center"), self.notepad.tag_add("text", 1.0, "end")))
        self.button_center.grid(row=0, column=1, sticky="nsw")
        self.button_right = tk.Button(self.toolbar_notepad, text="R", width=5, bd=0, relief=tk.FLAT, command=lambda: (self.notepad.tag_configure("text", justify="right"), self.notepad.tag_add("text", 1.0, "end")))
        self.button_right.grid(row=0, column=2, sticky="nsw")
        self.button_undo = tk.Button(self.toolbar_notepad, text="Undo", width=8, bd=0, relief=tk.FLAT, command=lambda: self.notepad.edit_undo())
        self.button_undo.grid(row=0, column=3, sticky="nse")
        self.button_redo = tk.Button(self.toolbar_notepad, text="Redo", width=8, bd=0, relief=tk.FLAT, command=lambda: self.notepad.edit_redo())
        self.button_redo.grid(row=0, column=4, sticky="nse")

        self.notepad = tk.Text(self.root, width=30, bd=16, relief=tk.FLAT, wrap=tk.WORD, undo=True, font=(font.nametofont("TkDefaultFont").actual()["family"], 12))
        self.notepad.bind("<Button-3>", self.popup_context_menu_edit)

        self.angle_mode = tk.IntVar(value=1)

        self.context_menu = tk.Menu(self.menubutton, tearoff=False, activeborderwidth=2.5)
        self.context_menu.add_checkbutton(label="Pin Window", command=lambda: (self.root.attributes("-topmost", not self.root.attributes("-topmost")), self.root.overrideredirect(not self.root.overrideredirect()), self.restore_dark_mode()))
        self.context_menu.add_command(label="Switch Theme", command=self.switch_theme)
        self.context_menu.add_separator()
        self.context_menu.add_radiobutton(label="Degrees", variable=self.angle_mode, value=0)
        self.context_menu.add_radiobutton(label="Radians", variable=self.angle_mode, value=1)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Help", command=self.help_window)
        self.root.bind("<Button-3>", lambda event: self.context_menu.tk_popup(event.x_root, event.y_root))

        self.go_to()
        self.toolbar_calculator.configure(bg="#202020")
        self.switch_theme()
        self.toggle_notepad()
        self.toggle_notepad()
     
    def go_to(self):
        for widget in [self.std_frame, self.sci_frame, self.bc_frame, self.dc_frame, self.prb_frame, self.toolbar_notepad, self.notepad]:
            widget.grid_forget()
        self.button_sidebar.configure(text=">>")
        var = self.option.get()
        if var == 0:
            self.root.geometry("275x400")
            self.root.minsize(width=275, height=400)
            self.menubutton.configure(text="Standard")
            self.std_frame.grid(row=1, column=0, sticky="nsew")
            self.std_bar.focus_set()
        elif var == 1:
            self.root.geometry("545x400")
            self.root.minsize(width=545, height=400)
            self.menubutton.configure(text="Scientific")
            self.sci_frame.grid(row=1, column=0, sticky="nsew")
            self.sci_bar.focus_set()
        elif var == 2:
            self.root.geometry("352x189")
            self.root.minsize(width=325, height=189)
            self.menubutton.configure(text="Base Conversion")
            self.bc_frame.grid(row=1, column=0, sticky="nsew")
            self.bc_bin_entry.focus_set()
        elif var == 3:
            self.root.geometry("465x283")
            self.root.minsize(width=465, height=283)
            self.menubutton.configure(text="Date Calculation")
            self.dc_frame.grid(row=1, column=0, sticky="nsew")
            self.dc_from_label_d.focus_set()
        elif var == 4:
            self.root.geometry("320x480")
            self.root.minsize(width=320, height=480)
            self.menubutton.configure(text="Probability")
            self.prb_frame.grid(row=1, column=0, sticky="nsew")

    def popup_context_menu_edit(self, event):
        self.context_widget = event.widget
        self.context_menu_edit.tk_popup(event.x_root, event.y_root)
        return "break"

    def switch_theme(self):
        if self.toolbar_calculator.cget("bg") == "#202020":
            dark_mode = 1
        else:
            dark_mode = 0
        dark_mode = not dark_mode
        if dark_mode == 0:
            bg, bg2, bg3, bg4, bg5, bg6, fg, var = "#F0F0F0", "#E1E1E1", "#D2D2D2", "#FFFFFF", "#FFFFFF", "#C3C3C3", "#000000", 0
        elif dark_mode == 1:
            bg, bg2, bg3, bg4, bg5, bg6, fg, var = "#202020", "#111111", "#2F2F2F", "#000000", "#2F2F2F", "#3E3E3E", "#FFFFFF", 2
        try:
            ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(self.root.winfo_id()), 20, ct.byref(ct.c_int(var)), ct.sizeof(ct.c_int(var)))
        except:
            return
        self.menu_options.configure(bg=bg, fg=fg, activebackground=bg3, activeforeground=fg)
        self.context_menu.configure(bg=bg, fg=fg, activebackground=bg3, activeforeground=fg)
        self.context_menu_edit.configure(bg=bg, fg=fg, activebackground=bg3, activeforeground=fg)
        self.root["bg"] = bg
        self.toolbar_calculator.configure(bg=bg)
        self.toolbar_notepad.configure(bg=bg)
        self.style.configure(f"{self.prefix}.TMenubutton", background=bg, foreground=fg)
        self.style.configure(f"{self.prefix}.TCombobox", background=bg2)
        self.button_sidebar.configure(bg=bg, fg=fg)
        for widget in [self.std_frame, self.sci_frame, self.bc_frame, self.dc_frame, self.prb_frame, \
                       self.dc_from_frame, self.dc_to_frame, self.dc_frame_difference, \
                       self.prb_rng_frame, self.prb_cnr_frame]:
            widget.configure(bg=bg2)
        for widget in [self.std_memory_button_frame, self.std_button_frame, self.sci_subframe, self.sci_button_frame]:
            widget.configure(bg=bg2)
        for widget in [self.button_new, self.button_sidebar, self.prb_rng_button_count_plus, self.prb_rng_button_count_minus, \
                       self.button_left, self.button_center, self.button_right, self.button_undo, self.button_redo]:
            widget.configure(bg=bg, fg=fg, activebackground=bg6, activeforeground=fg)
            widget.unbind("<Enter>")
            widget.unbind("<Leave>")
            widget.bind("<Enter>", lambda event, button=widget: button.configure(bg=bg3, fg=fg))
            widget.bind("<Leave>", lambda event, button=widget: button.configure(bg=bg, fg=fg))
        for widget in [self.dc_button_today, self.prb_cnr_button_operation, self.prb_cnr_button_equal_sign, self.prb_ans_button_generate]:
            widget.configure(bg=bg2, fg=fg, activebackground=bg6, activeforeground=fg)
            widget.unbind("<Enter>")
            widget.unbind("<Leave>")
            widget.bind("<Enter>", lambda event, button=widget: button.configure(bg=bg3, fg=fg))
            widget.bind("<Leave>", lambda event, button=widget: button.configure(bg=bg2, fg=fg))
        for button_list in [self.std_buttons, self.std_operator_buttons, self.std_memory_buttons, self.sci_buttons, self.sci_subframe_buttons]:
            for widget in button_list:
                if button_list[widget].cget("bg") != "#0078D7":
                    button_list[widget].configure(bg=bg, fg=fg)
                    button_list[widget].configure(bg=bg, fg=fg, activebackground=bg6, activeforeground=fg)
                    button_list[widget].unbind("<Enter>")
                    button_list[widget].unbind("<Leave>")
                    button_list[widget].bind("<Enter>", lambda event, button=button_list[widget]: button.configure(bg=bg3, fg=fg))
                    button_list[widget].bind("<Leave>", lambda event, button=button_list[widget]: button.configure(bg=bg, fg=fg))
        for entry in [self.std_bar, self.sci_bar, \
                      self.bc_bin_entry, self.bc_oct_entry, self.bc_dec_entry, self.bc_hex_entry, \
                        self.prb_rng_entry_min, self.prb_rng_entry_max, self.prb_rng_entry_count, self.prb_ans_entry, \
                        self.prb_cnr_entry_n, self.prb_cnr_entry_r, self.prb_cnr_entry_ans]:
            entry.configure(bg=bg5, fg=fg, insertbackground=fg)
        for widget in [self.bc_bin_label, self.bc_oct_label, self.bc_dec_label, self.bc_hex_label, \
                        self.dc_from_label, self.dc_from_label_d, self.dc_from_label_m, self.dc_from_label_y, \
                        self.dc_to_label, self.dc_to_label_d, self.dc_to_label_m, self.dc_to_label_y, \
                        self.dc_label_difference, self.dc_button_days, self.dc_label_days, \
                        self.prb_rng_label, self.prb_rng_label_min, self.prb_rng_label_max, self.prb_rng_label_count, \
                        self.prb_cnr_label]:
            widget.configure(bg=bg2, fg=fg)
        self.notepad.configure(bg=bg4, fg=fg, insertbackground=fg)

    def restore_dark_mode(self):
        try:
            if self.toolbar_calculator.cget("bg") == "#202020":
                ct.windll.dwmapi.DwmSetWindowAttribute(ct.windll.user32.GetParent(self.root.winfo_id()), 20, ct.byref(ct.c_int(2)), ct.sizeof(ct.c_int(2)))
        except:
            return

    def std_update_operator_colors(self):
        for k, v in self.std_operator_buttons.items():
            v.unbind("<Enter>")
            v.unbind("<Leave>")
            if self.std_operation == k:
                v.configure(bg="#0078D7", fg="#FFFFFF", activebackground="#005AB9", activeforeground="#FFFFFF")
                v.bind("<Enter>", lambda event, button=v: button.configure(bg="#0069C8", fg="#FFFFFF"))
                v.bind("<Leave>", lambda event, button=v: button.configure(bg="#0078D7", fg="#FFFFFF"))
            else:
                if self.root.cget("bg") == "#F0F0F0":
                    bg, bg2, bg3, fg = "#F0F0F0", "#D2D2D2", "#C3C3C3", "#000000"
                else:
                    bg, bg2, bg3, fg = "#202020", "#2F2F2F", "#3E3E3E", "#FFFFFF"
                v.configure(bg=bg, fg=fg, activebackground=bg3, activeforeground=fg)
                v.bind("<Enter>", lambda event, button=v: button.configure(bg=bg2, fg=fg))
                v.bind("<Leave>", lambda event, button=v: button.configure(bg=bg, fg=fg))

    def std_set_operation(self, operation):
        text = self.std_bar.get()
        if self.std_operation is None:
            if isfloat(text):
                self.std_value = float(text)
                self.std_operation = operation
                self.std_bar.delete(0, tk.END)
                self.std_update_operator_colors()
            return
        if self.std_operation == operation:
            self.std_bar.delete(0, tk.END)
            self.std_bar.insert(0, str(self.std_value))
            self.std_value = None
            self.std_operation = None
            self.std_update_operator_colors()
            return
        self.std_operation = operation
        self.std_update_operator_colors()

    def std_m_plus(self):
        value = self.std_bar.get()
        if isfloat(value):
            value = self.std_memory + float(value)
            if value.is_integer():
                value = int(value)
            self.std_memory = value
    
    def std_m_minus(self):
        value = self.std_bar.get()
        if isfloat(value):
            value = self.std_memory - float(value)
            if value.is_integer():
                value = int(value)
            self.std_memory = value

    def std_ms(self):
        value = self.std_bar.get()
        if isfloat(value):
            value = float(value)
            if value.is_integer():
                value = int(value)
            self.std_memory = value
    
    def std_mr(self):
        self.std_bar.delete(0, tk.END)
        self.std_bar.insert(tk.END, self.std_memory)

    def std_mc(self):
        self.std_memory = 0

    def std_clear(self):
        self.std_bar.delete(0, tk.END)
        self.std_value = None
        self.std_operation = None
        self.std_update_operator_colors()

    def std_calculate(self, option):
        text = self.std_bar.get()
        try:
            if isfloat(text):
                value = float(text)
                if option == "sq":
                    value = value ** 2
                elif option == "sqrt":
                    value = math.sqrt(value)
                elif option == "invert":
                    value = 1 / value
                elif option == "negate":
                    value = -1 * value
                elif option == "percent":
                    value = 0.01 * value
                else:
                    value = eval(f"{self.std_value}{self.std_operation}{value}")
                    self.std_value = float(value)
                    self.std_operation = None
                    self.std_update_operator_colors()
                if isinstance(value, float) and abs(value - round(value)) < 1e-9:
                    answer = str(int(round(value)))
                else:
                    answer = str(value)
                self.std_bar.delete(0, tk.END)
                self.std_bar.insert(tk.END, answer)
        except:
            self.std_bar.delete(0, tk.END)
            self.std_bar.focus_set()
 
    def sci_m_plus(self):
        try:
            self.sci_calculate()
            value = self.sci_bar.get()
            value = self.sci_memory + float(value)
            if value.is_integer():
                value = int(value)
            self.sci_memory = value
        except:
            pass
    
    def sci_m_minus(self):
        try:
            self.sci_calculate()
            value = self.sci_bar.get()
            value = self.sci_memory - float(value)
            if value.is_integer():
                value = int(value)
            self.sci_memory = value
        except:
            pass

    def sci_ms(self):
        try:
            self.sci_calculate()
            value = self.sci_bar.get()
            value = self.sci_memory = float(value)
            if value.is_integer():
                value = int(value)
            self.sci_memory = value
        except:
            pass
    
    def sci_mr(self):
        self.sci_bar.delete(0, tk.END)
        self.sci_bar.insert(tk.END, self.sci_memory)

    def sci_mc(self):
        self.sci_memory = 0

    def sci_calculate(self):
        expr = self.sci_bar.get()
        if expr == "":
            return
        self.sci_bar.delete(0, tk.END)
        try:
            expr = expr.replace("^", "**")
            expr = re.sub(r"(\d|\))(?=\()", r"\1*", expr)
            expr = re.sub(r"(\d|\))(?=[a-zA-Zπe])", r"\1*", expr)
            expr = re.sub(r"\)(?=\d)", ")*", expr)
            expr = re.sub(r"(π|e)(?=\d|π|e|[a-zA-Z])", r"\1*", expr)
            expr = re.sub(r"(π|e)\(", r"\1*(", expr)
            expr = re.sub(r"(?<=\d)(π|e)", r"*\1", expr)
            expr = expr.replace("π", "pi")
            value = parse_expr(expr, self.angle_mode.get())
            if isinstance(value, float) and abs(value - round(value)) < 1e-9:
                value = str(int(round(value)))
            else:
                value = str(value)
            self.sci_bar.insert(0, value)
        except ZeroDivisionError:
            self.sci_bar.insert(0, "Cannot divide by zero")
        except ValueError:
            self.sci_bar.insert(0, "Invalid input")
        except SyntaxError:
            self.sci_bar.insert(0, "Syntax error")
        except Exception:
            self.sci_bar.insert(0, "Error")

    def bc_update(self, base):
        entries = {2: self.bc_bin_entry, 8: self.bc_oct_entry, 10: self.bc_dec_entry, 16: self.bc_hex_entry}
        text = entries[base].get()
        patterns = {2: r"[^01]", 8: r"[^0-7]", 10: r"[^0-9]", 16: r"[^0-9A-Fa-f]"}
        new_text = re.sub(patterns[base], "", text)
        self.bc_hex_entry.delete(0, tk.END)
        self.bc_bin_entry.delete(0, tk.END)
        self.bc_oct_entry.delete(0, tk.END)
        self.bc_dec_entry.delete(0, tk.END)
        if new_text == "":

            return
        value = int(new_text, base)
        bin_str = bin(value).replace("0b", "")
        oct_str = oct(value).replace("0o", "")
        dec_str = str(value)
        hex_str = hex(value).replace("0x", "").upper()
        self.bc_bin_entry.insert(tk.INSERT, bin_str)
        self.bc_oct_entry.insert(tk.INSERT, oct_str)
        self.bc_dec_entry.insert(tk.INSERT, dec_str)
        self.bc_hex_entry.insert(tk.INSERT, hex_str)

    def dc_go_to_today(self):
        today = datetime.now()
        self.dc_from_combobox_d.set(str(today.day))
        self.dc_from_combobox_m.set(self.months[today.month - 1])
        self.dc_from_combobox_y.set(str(today.year))
        try:
            self.dc_calculate_difference()
        except:
            pass

    def dc_set_default(self):
        self.dc_go_to_today()
        tomorrow = datetime.now() + timedelta(days=1)
        self.dc_to_combobox_d.set(str(tomorrow.day))
        self.dc_to_combobox_m.set(self.months[tomorrow.month - 1])
        self.dc_to_combobox_y.set(str(tomorrow.year))
        self.dc_calculate_difference()

    def dc_calculate_difference(self):
        from_d, from_m, from_y = (int(self.dc_from_combobox_d.get()), self.months.index(self.dc_from_combobox_m.get()) + 1, int(self.dc_from_combobox_y.get()))
        to_d, to_m, to_y = (int(self.dc_to_combobox_d.get()), self.months.index(self.dc_to_combobox_m.get()) + 1, int(self.dc_to_combobox_y.get()))
        try:
            from_dmy = datetime(from_y, from_m, from_d)
        except ValueError:
            from_d = calendar.monthrange(from_y, from_m)[1]
            from_dmy = datetime(from_y, from_m, from_d)
            self.dc_from_combobox_d.set(str(from_d))
        try:
            to_dmy = datetime(to_y, to_m, to_d)
        except ValueError:
            to_d = calendar.monthrange(to_y, to_m)[1]
            to_dmy = datetime(to_y, to_m, to_d)
            self.dc_to_combobox_d.set(str(to_d))
        difference = to_dmy - from_dmy
        days = difference.days
        self.dc_combobox_days.set(abs(days))
        self.dc_button_days.configure(text="-") if days < 0 else self.dc_button_days.configure(text="+")
        if abs(days) == 1:
            text = "day"
        else:
            text = "days"
        self.dc_label_days.configure(text=text)

    def dc_calculate_dmy(self):
        difference = timedelta(days=int(self.dc_combobox_days.get()))
        days = difference.days
        from_d, from_m, from_y = (int(self.dc_from_combobox_d.get()), self.months.index(self.dc_from_combobox_m.get()) + 1, int(self.dc_from_combobox_y.get()))
        try:
            from_dmy = datetime(from_y, from_m, from_d)
        except ValueError:
            from_d = calendar.monthrange(from_y, from_m)[1]
            from_dmy = datetime(from_y, from_m, from_d)
            self.dc_from_combobox_d.set(str(from_d))
        if days == 0:
            self.dc_button_days.configure(text="+")
        if self.dc_button_days.cget("text") == "-":
            to_dmy = from_dmy - difference
        else:
            to_dmy = from_dmy + difference
        self.dc_to_combobox_d.set(str(to_dmy.day))
        self.dc_to_combobox_m.set(self.months[to_dmy.month - 1])
        self.dc_to_combobox_y.set(str(to_dmy.year))
        if abs(days) == 1:
            text = "day"
        else:
            text = "days"
        self.dc_label_days.configure(text=text)

    def prb_rng_validate(self, entry):
        text = entry.get()
        new_text = re.sub(r"[^0-9-]", "", text)
        if new_text.startswith("-"):
            prefix = "-"
            new_text = new_text[1:]
        else:
            prefix = ""
        new_text = new_text.replace("-", "")
        if new_text == "":
            entry.delete(0, tk.END)
            entry.insert(tk.INSERT, prefix)
            return
        number = str(int(new_text))
        if prefix == "-" and number == "0":
            prefix = ""
        entry.delete(0, tk.END)
        entry.insert(tk.INSERT, f"{prefix}{number}")

    def prb_rng_count_validate(self):
        text = self.prb_rng_entry_count.get()
        new_text = re.sub(r"[^0-9]", "", text)
        if new_text != "":
            if int(new_text) not in list(range(1, 13)):
                new_text = "1"
        self.prb_rng_entry_count.delete(0, tk.END)
        self.prb_rng_entry_count.insert(tk.INSERT, new_text)

    def prb_rng_count_adjust(self, number):
        self.prb_rng_count_validate()
        text = self.prb_rng_entry_count.get()
        if text == "":
            text = "0"
        if int(text) >= 12 and number > 0:
            return
        new_text = str(int(text) + number)
        self.prb_rng_entry_count.delete(0, tk.END)
        self.prb_rng_entry_count.insert(tk.INSERT, new_text)
        self.prb_rng_count_validate()

    def prb_rng_generate(self):
        try:
            self.prb_rng_validate(self.prb_rng_entry_min)
            self.prb_rng_validate(self.prb_rng_entry_max)
            min_number = int(self.prb_rng_entry_min.get())
            max_number = int(self.prb_rng_entry_max.get())
            if min_number > max_number:
                self.prb_rng_entry_min.delete(0, tk.END)
                self.prb_rng_entry_max.delete(0, tk.END)
                self.prb_rng_entry_min.insert(tk.INSERT, str(max_number))
                self.prb_rng_entry_max.insert(tk.INSERT, str(min_number))
            min_number = int(self.prb_rng_entry_min.get())
            max_number = int(self.prb_rng_entry_max.get())
            count_number = int(self.prb_rng_entry_count.get())
            numbers = [random.randint(min_number, max_number) for n in range(count_number)]
            self.prb_ans_entry.delete(0, tk.END)
            if len(numbers) == 1:
                self.prb_ans_entry.insert(tk.INSERT, str(numbers[0]))
            else:
                self.prb_ans_entry.insert(tk.INSERT, str(numbers))
        except:
            pass

    def prb_switch_operation(self):
        option = self.prb_cnr_button_operation.cget("text")
        if option == "nCr":
            self.prb_cnr_frame.columnconfigure(2, weight=1)
            self.prb_cnr_entry_r.grid(row=0, column=2, sticky="nsew")
            self.prb_cnr_button_operation.configure(text="nPr")
        elif option == "nPr":
            self.prb_cnr_frame.columnconfigure(2, weight=0)
            self.prb_cnr_entry_r.grid_forget()
            self.prb_cnr_button_operation.configure(text="!")
        elif option == "!":
            self.prb_cnr_frame.columnconfigure(2, weight=1)
            self.prb_cnr_entry_r.grid(row=0, column=2, sticky="nsew")
            self.prb_cnr_button_operation.configure(text="nCr")
    
    def prb_cnr_validate(self, entry):
        text = entry.get()
        new_text = re.sub(r"[^0-9]", "", text)
        entry.delete(0, tk.END)
        entry.insert(tk.INSERT, new_text)

    def prb_cnr_calculate(self):
        try:
            self.prb_cnr_validate(self.prb_cnr_entry_n)
            self.prb_cnr_validate(self.prb_cnr_entry_r)
            n = int(self.prb_cnr_entry_n.get())
            r = int(self.prb_cnr_entry_r.get())
            if r > n:
                self.prb_cnr_entry_n.delete(0, tk.END)
                self.prb_cnr_entry_r.delete(0, tk.END)
                self.prb_cnr_entry_n.insert(tk.INSERT, str(r))
                self.prb_cnr_entry_r.insert(tk.INSERT, str(n))
            n = int(self.prb_cnr_entry_n.get())
            r = int(self.prb_cnr_entry_r.get())
            option = self.prb_cnr_button_operation.cget("text")
            if option == "nCr":
                answer = math.comb(n, r)
            elif option == "nPr":
                answer = math.perm(n, r)
            elif option == "!":
                answer = math.factorial(n)
            self.prb_cnr_entry_ans.delete(0, tk.END)
            self.prb_cnr_entry_ans.insert(tk.INSERT, str(answer))
        except:
            pass

    def toggle_notepad(self):
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        sidebar_width = self.notepad.winfo_width()
        if self.notepad.grid_info():
            self.toolbar_notepad.grid_forget()
            self.notepad.grid_forget()
            self.button_sidebar.configure(text=">>")
            var = self.option.get()
            if var == 0:
                self.root.geometry("275x400")
                self.root.minsize(width=275, height=400)
            elif var == 1:
                self.root.geometry("545x400")
                self.root.minsize(width=545, height=400)
            elif var == 2:
                self.root.geometry("352x189")
                self.root.minsize(width=325, height=189)
            elif var == 3:
                self.root.geometry("465x283")
                self.root.minsize(width=465, height=283)
            elif var == 4:
                self.root.geometry("320x480")
                self.root.minsize(width=320, height=480)
        else:
            self.toolbar_notepad.grid(row=0, column=1, sticky="nsew")
            self.notepad.grid(row=1, column=1, sticky="nsew")
            self.button_sidebar.configure(text="<<")
            self.root.geometry(f"{window_width+sidebar_width}x{window_height}")
            self.root.minsize(width=window_width+sidebar_width, height=window_height)

    def help_window(self):
        window = tk.Toplevel()
        try:
            window.iconbitmap("icon.ico")
        except:
            pass
        window.title("Help - Calculator4pc")
        window.geometry("700x510")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)
        help_tabs = ttk.Notebook(window)
        help_tabs.grid(row=0, column=0, sticky="nsew")
        about = tk.Text(help_tabs, relief=tk.FLAT, border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap="word", background="#E1E1E1")
        about.insert("insert", f"Calculator4pc\nCopyright (c) 2026-{str(datetime.now().year)}: Waylon Boer\n\nCalculator4pc is a multifunctional calculator app.")
        about.configure(state="disabled")
        help_tabs.add(about, text="About")
        mit_license = tk.Text(help_tabs, relief=tk.FLAT, border=16, font=(font.nametofont("TkDefaultFont").actual()["family"], 12), wrap="word", background="#E1E1E1")
        mit_license.insert("insert", """MIT License

Copyright (c) 2026 Waylon Boer

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
        mit_license.configure(state="disabled")
        help_tabs.add(mit_license, text="License")

    def open_new_window(self):
        new = tk.Toplevel(self.root)
        Calculator4pc(new)
        
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    root = tk.Tk()
    Calculator4pc(root)
    root.mainloop()