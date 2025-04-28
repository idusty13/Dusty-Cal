import tkinter as tk
from tkinter import ttk
import math

class DustysCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Dusty's Calculator")
        self.root.geometry("350x450")
        self.root.resizable(False, False)
        
        # Set pink theme
        self.pink_color = "#FF69B4"  # Hot Pink
        self.light_pink = "#FFB6C1"  # Light Pink
        self.dark_pink = "#C71585"   # Medium Violet Red
        self.white = "#FFFFFF"
        self.black = "#000000"
        
        self.root.configure(bg=self.pink_color)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("Pink.TButton", 
                            background=self.pink_color, 
                            foreground=self.black,
                            font=("Arial", 14, "bold"))
        
        # Calculator display
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        # Frame for the display
        display_frame = tk.Frame(self.root, bg=self.dark_pink, padx=10, pady=10)
        display_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.display = tk.Entry(display_frame, 
                              textvariable=self.result_var,
                              font=("Arial", 24, "bold"),
                              bd=10,
                              insertwidth=4,
                              justify='right',
                              bg=self.white)
        self.display.pack(fill=tk.BOTH)
        
        # Calculator buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.pink_color)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure the grid
        for i in range(6):
            buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
        
        # Button layout
        button_layout = [
            ("C", 0, 0), ("±", 0, 1), ("%", 0, 2), ("/", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("*", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0, 2), (".", 4, 2), ("=", 4, 3),
            ("√", 5, 0), ("x²", 5, 1), ("1/x", 5, 2), ("π", 5, 3),
        ]
        
        # Create buttons
        for button_info in button_layout:
            if len(button_info) == 4:  # Button that spans multiple columns
                text, row, col, colspan = button_info
                self.create_button(buttons_frame, text, row, col, colspan=colspan)
            else:
                text, row, col = button_info
                self.create_button(buttons_frame, text, row, col)
        
        # Variables for calculations
        self.current_input = "0"
        self.operator = None
        self.first_number = None
        self.prepare_for_next_input = False
        
    def create_button(self, parent, text, row, col, colspan=1):
        button = tk.Button(parent, 
                         text=text,
                         font=("Arial", 16, "bold"),
                         bd=5,
                         relief=tk.RAISED,
                         bg=self.light_pink if text.isdigit() or text == "." else self.dark_pink,
                         fg=self.black if text.isdigit() or text == "." else self.white,
                         activebackground=self.pink_color,
                         activeforeground=self.white,
                         height=1,
                         width=3 if colspan == 1 else 8,
                         command=lambda t=text: self.button_click(t))
        button.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="nsew")
    
    def button_click(self, value):
        if self.prepare_for_next_input:
            self.current_input = "0"
            self.prepare_for_next_input = False
        
        current_display = self.result_var.get()
        
        if value == "C":
            self.result_var.set("0")
            self.current_input = "0"
            self.first_number = None
            self.operator = None
        
        elif value == "=":
            if self.operator and self.first_number is not None:
                second_number = float(current_display)
                result = self.perform_calculation(self.first_number, second_number, self.operator)
                self.result_var.set(self.format_result(result))
                self.first_number = result
                self.prepare_for_next_input = True
        
        elif value in ["+", "-", "*", "/"]:
            if self.first_number is not None and not self.prepare_for_next_input:
                # Chain operations
                second_number = float(current_display)
                result = self.perform_calculation(self.first_number, second_number, self.operator)
                self.result_var.set(self.format_result(result))
                self.first_number = result
            else:
                self.first_number = float(current_display)
            self.operator = value
            self.prepare_for_next_input = True
        
        elif value == "±":
            if current_display != "0":
                if current_display.startswith("-"):
                    self.result_var.set(current_display[1:])
                else:
                    self.result_var.set("-" + current_display)
        
        elif value == "%":
            current_value = float(current_display)
            result = current_value / a100
            self.result_var.set(self.format_result(result))
            self.prepare_for_next_input = True
        
        elif value == "√":
            current_value = float(current_display)
            if current_value >= 0:
                result = math.sqrt(current_value)
                self.result_var.set(self.format_result(result))
                self.prepare_for_next_input = True
            else:
                self.result_var.set("Error")
                self.prepare_for_next_input = True
        
        elif value == "x²":
            current_value = float(current_display)
            result = current_value ** 2
            self.result_var.set(self.format_result(result))
            self.prepare_for_next_input = True
        
        elif value == "1/x":
            current_value = float(current_display)
            if current_value != 0:
                result = 1 / current_value
                self.result_var.set(self.format_result(result))
            else:
                self.result_var.set("Error")
            self.prepare_for_next_input = True
        
        elif value == "π":
            self.result_var.set(str(math.pi))
            self.prepare_for_next_input = True
        
        elif value == ".":
            if "." not in current_display:
                self.result_var.set(current_display + ".")
        
        else:  # Numbers
            if current_display == "0" or self.prepare_for_next_input:
                self.result_var.set(value)
                self.prepare_for_next_input = False
            else:
                self.result_var.set(current_display + value)
    
    def perform_calculation(self, first, second, operator):
        if operator == "+":
            return first + second
        elif operator == "-":
            return first - second
        elif operator == "*":
            return first * second
        elif operator == "/":
            if second == 0:
                return "Error"
            return first / second
    
    def format_result(self, result):
        if isinstance(result, str):
            return result
        
        # Check if result is essentially an integer
        if result == int(result):
            return str(int(result))
        else:
            # Limit decimal places for floating point numbers
            return f"{result:.8f}".rstrip('0').rstrip('.') if '.' in f"{result:.8f}" else f"{result:.8f}"

def main():
    root = tk.Tk()
    app = DustysCalculator(root)
    
    # Add an attribution footer
    footer = tk.Label(root, 
                    text="Dusty's Calculator - A LinkedIn Project",
                    font=("Arial", 8),
                    bg="#FF69B4",
                    fg="#FFFFFF")
    footer.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
