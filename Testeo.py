import tkinter as tk
from tkinter import messagebox

def tomar_datos():
    messagebox.showinfo("Lectura", "Simulando toma de datos...")

# Crear ventana
root = tk.Tk()
root.title("Monitoreo de Planta - Test")
root.geometry("300x150")

# Etiqueta
label = tk.Label(root, text="Panel de Control - Planta", font=("Arial", 12, "bold"))
label.pack(pady=20)

# Botón
btn = tk.Button(root, text="Tomar datos", command=tomar_datos, width=15, height=2)
btn.pack()

# Iniciar interfaz
root.mainloop()
