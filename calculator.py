import tkinter as tk
import math
import re
import sympy as sp

# prepare symbols for differentiation/integration
x, y, z = sp.symbols('x y z')

# colors
light_blue     = '#0099FF'
label_color    = '#FBBF77'
white_color    = '#FFFFFF'
offwhite_color = '#F8FAFF'

# fonts
small_label_font_style = ("Arial", 16)
large_label_font_style = ("Arial", 40, "bold")
default_font_style     = ("Arial", 20)

class CalculatorApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('450x900')  # enough height for 10 rows
        self.window.resizable(0, 0)
        self.window.title('Calculus Calculator')

        # expressions & memory
        self.current_expression = ""
        self.total_expression   = ""
        self.last_answer        = None
        self.operations         = {'*':'×', '/':'÷', '**':'^'}

        # UI setup
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.buttons_frame = self.create_buttons_frame()

        # grid config: rows 0–9, cols 1–6
        for r in range(10):
            self.buttons_frame.rowconfigure(r, weight=1)
        for c in range(1, 7):
            self.buttons_frame.columnconfigure(c, weight=1)

        self.create_all_buttons()
        self.bind_keys()

    # --- Key bindings ---
    def bind_keys(self):
        self.window.bind('<Return>',    lambda e: self.evaluate())
        self.window.bind('<BackSpace>', lambda e: self.backspace())
        self.window.bind('<KeyPress>',  self.handle_keypress)

    def handle_keypress(self, event):
        c = event.char
        if c.isdigit() or c == '.':
            self.add_to_expression(c)
        elif c in '+-*/^()':
            self.add_to_expression(c)
        elif c == 'π':
            self.add_to_expression('π')
        elif c == '!':
            self.add_to_expression('!')

    # --- Display frames & labels ---
    def create_display_frame(self):
        f = tk.Frame(self.window, height=300, bg=light_blue)
        f.pack(expand=True, fill='both')
        return f

    def create_display_labels(self):
        total = tk.Label(self.display_frame, text='', anchor=tk.E,
                         bg=light_blue, fg=label_color, padx=24, font=small_label_font_style)
        total.pack(expand=True, fill='both')
        curr  = tk.Label(self.display_frame, text='', anchor=tk.E,
                         bg=light_blue, fg=label_color, padx=24, font=large_label_font_style)
        curr.pack(expand=True, fill='both')
        return total, curr

    def create_buttons_frame(self):
        f = tk.Frame(self.window)
        f.pack(expand=True, fill='both')
        return f

    # --- Helpers ---
    def add_to_expression(self, val):
        self.current_expression += str(val)
        self.update_label()

    def clear(self):
        self.current_expression = ""
        self.total_expression   = ""
        self.update_label()
        self.update_total_label()

    def ce(self):
        self.current_expression = ""
        self.update_label()

    def ans(self):
        if self.last_answer is not None:
            self.current_expression += str(self.last_answer)
            self.update_label()

    def percent(self):
        self.current_expression += '/100'
        self.update_label()

    def floor(self):
        self.current_expression += 'floor('
        self.update_label()

    def ceil(self):
        self.current_expression += 'ceil('
        self.update_label()

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def square(self):
        try:
            v = float(self.current_expression)
            self.current_expression = str(v * v)
        except:
            self.current_expression = 'Error'
        self.update_label()

    def sqrt(self):
        try:
            self.current_expression = str(eval(self.current_expression + '**0.5'))
        except:
            self.current_expression = 'Error'
        self.update_label()

    # --- Button grid ---
    def create_all_buttons(self):
        buttons = [
            (0,1,'C','C'),     (0,2,'x²','x²'),    (0,3,'√x','√x'),
            (0,4,'÷','/'),     (0,5,'×','*'),      (0,6,'-','-'),
            (1,1,'7','7'),     (1,2,'8','8'),      (1,3,'9','9'),
            (1,4,'+','+'),     (1,5,'x','x'),      (1,6,'y','y'),
            (2,1,'4','4'),     (2,2,'5','5'),      (2,3,'6','6'),
            (2,4,'=','='),     (2,5,'z','z'),      (2,6,'d/dx','d/dx('),
            (3,1,'1','1'),     (3,2,'2','2'),      (3,3,'3','3'),
            (3,4,'^','^'),     (3,5,'sin','sin('), (3,6,'cos','cos('),
            (4,1,'.','.'),     (4,2,'0','0'),      (4,3,'!','!'),
            (4,4,'tan','tan('),(4,5,'cot','cot('),(4,6,'csc','csc('),
            (5,1,'∂/∂x','d/dx('),(5,2,'∂/∂y','d/dy('),(5,3,'∂/∂z','d/dz('),
            (5,4,'exp','exp('),(5,5,'log₁₀','log('),(5,6,'ln','ln('),
            (6,1,'abs','abs('),(6,2,'π','π'),   (6,3,'sinh','sinh('),
            (6,4,'cosh','cosh('),(6,5,'tanh','tanh('),(6,6,'log₂','log2('),
            (7,1,'(', '('),   (7,2,')',')'),     (7,3,'d/dy','d/dy('),
            (7,4,'d/dz','d/dz('),(7,5,'eⁿ','exp('),(7,6,'√-1','sqrt(-1)'),
            (8,1,'∫dx','intdx('),(8,2,'∫dy','intdy('),(8,3,'∫dz','intdz('),
            (8,4,'asin','asin('),(8,5,'acos','acos('),(8,6,'atan','atan('),
            (9,1,'CE','CE'),  (9,2,'ANS','ANS'), (9,3,'%','%'),
            (9,4,'floor','floor('),(9,5,'ceil','ceil('),(9,6,'⌫','BACK')
        ]
        digits = set(str(i) for i in range(10)) | {'.'}
        for r, c, label, key in buttons:
            if   label == 'C':     cmd = self.clear
            elif label == 'x²':    cmd = self.square
            elif label == '√x':    cmd = self.sqrt
            elif label == '=':     cmd = self.evaluate
            elif label == 'CE':    cmd = self.ce
            elif label == 'ANS':   cmd = self.ans
            elif label == '%':     cmd = self.percent
            elif label == 'floor': cmd = self.floor
            elif label == 'ceil':  cmd = self.ceil
            elif label == '⌫':     cmd = self.backspace
            else:                  cmd = lambda v=key: self.add_to_expression(v)

            bg = white_color if label in digits else offwhite_color
            tk.Button(self.buttons_frame, text=label, bg=bg, fg=label_color,
                      font=default_font_style, borderwidth=0,
                      command=cmd).grid(row=r, column=c, sticky=tk.NSEW)

    # --- Evaluation logic ---
    def evaluate(self):
        full = self.total_expression + self.current_expression
        self.total_expression = full

        # sympy locals
        locals_map = {
            'x': x, 'y': y, 'z': z,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'cot': sp.cot, 'csc': sp.csc,
            'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
            'exp': sp.exp, 'log': sp.log, 'ln': sp.log,
            'log2': lambda a: sp.log(a, 2),
            'sqrt': sp.sqrt,
            'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
            'floor': sp.floor, 'ceil': sp.ceiling
        }

        # derivatives & partials
        derivs = [
            ('d/dx(', x), ('∂/∂x(', x),
            ('d/dy(', y), ('∂/∂y(', y),
            ('d/dz(', z), ('∂/∂z(', z),
        ]
        for prefix, symb in derivs:
            if full.startswith(prefix) and full.endswith(')'):
                inner = full[len(prefix):-1]
                # ensure multiplication where implicit
                inner = re.sub(r'(?<=[0-9])(?=[xyz])', '*', inner)
                inner = re.sub(r'(?<=[xyz])(?=[0-9])', '*', inner)
                inner = re.sub(r'(?<=[xyz])(?=[xyz])', '*', inner)
                try:
                    expr = sp.sympify(inner, locals=locals_map)
                    self.current_expression = str(sp.diff(expr, symb))
                    self.last_answer = self.current_expression
                except:
                    self.current_expression = 'Error'
                return self.update_labels()

        # integrals
        integrals = [
            ('intdx(', x), ('intdy(', y), ('intdz(', z)
        ]
        for prefix, symb in integrals:
            if full.startswith(prefix) and full.endswith(')'):
                inner = full[len(prefix):-1]
                inner = re.sub(r'(?<=[0-9])(?=[xyz])', '*', inner)
                inner = re.sub(r'(?<=[xyz])(?=[0-9])', '*', inner)
                inner = re.sub(r'(?<=[xyz])(?=[xyz])', '*', inner)
                try:
                    expr = sp.sympify(inner, locals=locals_map)
                    self.current_expression = str(sp.integrate(expr, symb))
                    self.last_answer = self.current_expression
                except:
                    self.current_expression = 'Error'
                return self.update_labels()

        # numeric, trig, inverse-trig, factorial, etc.
        expr = (full.replace('^', '**')
                    .replace('π', str(math.pi)))
        # replace constant e without touching words like 'exp' or scientific notation
        expr = re.sub(r'(?<![\w])e(?![\w])', str(math.e), expr)
        expr = re.sub(r'(\d+)!', r'math.factorial(\1)', expr)
        expr = expr.replace('sqrt(-1)', '(0+1j)')

        patterns = [
            (r'log\(([^)]+)\)',   r'math.log10(\1)'),
            (r'ln\(([^)]+)\)',    r'math.log(\1)'),
            (r'sin\(([^)]+)\)',   r'math.sin(math.radians(\1))'),
            (r'cos\(([^)]+)\)',   r'math.cos(math.radians(\1))'),
            (r'tan\(([^)]+)\)',   r'math.tan(math.radians(\1))'),
            (r'cot\(([^)]+)\)',   r'1/math.tan(math.radians(\1))'),
            (r'csc\(([^)]+)\)',   r'1/math.sin(math.radians(\1))'),
            (r'asin\(([^)]+)\)',  r'math.degrees(math.asin(\1))'),
            (r'acos\(([^)]+)\)',  r'math.degrees(math.acos(\1))'),
            (r'atan\(([^)]+)\)',  r'math.degrees(math.atan(\1))'),
            (r'exp\(([^)]+)\)',   r'math.exp(\1)'),
            (r'sinh\(([^)]+)\)',  r'math.sinh(\1)'),
            (r'cosh\(([^)]+)\)',  r'math.cosh(\1)'),
            (r'tanh\(([^)]+)\)',  r'math.tanh(\1)'),
            (r'log2\(([^)]+)\)',  r'math.log2(\1)'),
            (r'floor\(([^)]+)\)', r'math.floor(\1)'),
            (r'ceil\(([^)]+)\)',  r'math.ceil(\1)'),
        ]
        for pat, rep in patterns:
            expr = re.sub(pat, rep, expr)

        try:
            val = eval(expr)
            self.current_expression = str(val)
            self.last_answer        = self.current_expression
        except:
            self.current_expression = 'Error'

        self.update_labels()

    # --- Update labels ---
    def update_labels(self):
        self.update_total_label()
        self.update_label()

    def update_total_label(self):
        disp = self.total_expression
        for k, v in self.operations.items():
            disp = disp.replace(k, v)
        size = small_label_font_style[1]
        if len(disp) > 12:
            size = max(10, size - (len(disp) - 12))
        self.total_label.config(font=("Arial", size), text=disp)

    def update_label(self):
        txt = self.current_expression
        size = large_label_font_style[1]
        if len(txt) > 10:
            size = max(14, size - (len(txt) - 10) * 2)
        self.label.config(font=("Arial", size, "bold"), text=txt)

    # --- Run ---
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    CalculatorApp().run()
