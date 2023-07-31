import tkinter as tk
# colors
light_blue = '#0099FF' # hef value for the color light blue
label_color = '#FBBF77'    # hef value for the color light orange
white_color = '#FFFFFF'
offwhite_color = '#F8FAFF'


small_label_font_style = ("Arial", 16)
large_label_font_style = ("Arial", 40, 'bold')
digit_font_style = ("Arial", 24, 'bold')

default_font_style = ("Arial", 20)

class CalculatorApp:
    def __init__(self):
        # calculator details / body
        self.window = tk.Tk()
        self.window.geometry('375x667')  # calculator size
        self.window.resizable(0,0)      # calculator app size can't be changed
        self.window.title('Calculus Calculator') # calculator title

        # display display labels
        self.current_expression = ""  # current expression
        self.total_expression = ""  # total expression

        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        # buttons
        self.digits = {
            7: (1,1), 8: (1,2), 9: (1,3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4,1)
        }

        self.operations = {'/':'\u00F7', '*':'\u00D7', '-':'-', '+':'+'}
        self.buttons_frame = self.create_buttons_frame()

        # expands buttons to the entire screen
        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1,5):
            self.buttons_frame.rowconfigure(x, weight= 1)
            self.buttons_frame.columnconfigure(x, weight= 1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind('<Return>', lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))


    def create_special_buttons(self):
        self.create_clear_buttons()
        self.create_equal_buttons()
        self.create_square_buttons()
        self.create_sqrt_buttons()

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=light_blue)
        frame.pack(expand=True, fill='both')
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
    # buttons buttons
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')
        return frame

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=light_blue,
                                   fg=label_color, padx=24, font=small_label_font_style)
        total_label.pack(expand=True, fill='both')

        # current labels
        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=light_blue,
                             fg=label_color, padx=24, font=large_label_font_style)
        label.pack(expand=True, fill='both')
        return total_label, label

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=offwhite_color,
                               fg=label_color, font=default_font_style, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i+=1

    # clear button
    def clear(self):
        self.current_expression = ''
        self.total_expression = ''
        self.update_label()
        self.update_total_label()

    def create_clear_buttons(self):
        button = tk.Button(self.buttons_frame, text='C', bg=offwhite_color,
                           fg=label_color, font=default_font_style, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    # square button
    def square(self):
            self.current_expression = str(eval(f'{self.current_expression} ** 2'))
            self.update_label()

    def create_square_buttons(self):
        button = tk.Button(self.buttons_frame, text='x\u00b2', bg=offwhite_color,
                           fg=label_color, font=default_font_style, borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    # square button
    def sqrt(self):
            self.current_expression = str(eval(f'{self.current_expression}** 0.5'))
            self.update_label()

    def create_sqrt_buttons(self):
        button = tk.Button(self.buttons_frame, text='\u221ax', bg=offwhite_color,
                           fg=label_color, font=default_font_style, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def create_equal_buttons(self):
        button = tk.Button(self.buttons_frame, text='=', bg=offwhite_color,
                           fg=label_color, font=default_font_style, borderwidth=0, command= self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ''

        except Exception as e:
            self.current_expression = 'Error'

        finally:
            self.update_label()


    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.total_label.config(text=expression)

    def update_label(self):

        self.label.config(text=self.current_expression[:11])


    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ''
        self.update_total_label()
        self.update_label()


    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=white_color, fg=label_color,
                               font=digit_font_style,borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)


    def run(self):
        self.window.mainloop()