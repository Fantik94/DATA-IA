import tkinter as tk
from tkinter import ttk

def convert_temperature():
    try:
        temp = float(entry_temp.get())
        unit = unit_var.get()
        if unit == "Celsius":
            result = (temp * 9/5) + 32
            result_unit = "°F"
        else:
            result = (temp - 32) * 5/9
            result_unit = "°C"
        result_label.config(text=f"{result:.1f}{result_unit}")
    except ValueError:
        result_label.config(text="Entrée invalide")

# Interface utilisateur
root = tk.Tk()
root.title("Convertisseur de température")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_temp = ttk.Label(frame, text="Température:")
label_temp.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

entry_temp = ttk.Entry(frame)
entry_temp.grid(row=0, column=1, padx=5, pady=5)

unit_var = tk.StringVar(value="Celsius")
unit_menu = ttk.OptionMenu(frame, unit_var, "Celsius", "Fahrenheit")
unit_menu.grid(row=0, column=2, padx=5, pady=5)

convert_button = ttk.Button(frame, text="Convertir", command=convert_temperature)
convert_button.grid(row=1, column=0, columnspan=3, pady=10)

result_label = ttk.Label(frame, text="")
result_label.grid(row=2, column=0, columnspan=3)

root.mainloop()