import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculette")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        self.current_input = ""
        self.total_expression = ""

        self.setup_ui()

    def setup_ui(self):
        # Entry widget to display input and results
        self.entry = tk.Entry(self.root, font=('Arial', 20), bd=10, insertwidth=2, width=14, borderwidth=4)
        self.entry.grid(row=0, column=0, columnspan=4)

        # Button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(self.root, text=text, font=('Arial', 14),
                           command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew", ipadx=10, ipady=10)

        # Configure grid weights
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == '=':
            self.calculate_result()
        elif char == 'C':
            self.clear()
        else:
            self.current_input += str(char)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.current_input)

    def calculate_result(self):
        try:
            self.total_expression = str(eval(self.current_input))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.total_expression)
            self.current_input = self.total_expression
        except Exception as e:
            messagebox.showerror("Error", "Invalid expression")
            self.clear()

    def clear(self):
        self.current_input = ""
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()