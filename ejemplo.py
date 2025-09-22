import tkinter as tk
import threading
import time
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -------------------
MODO_PRUEBA = True
ESP32_IP = "192.168.1.45"

humedad_hist = []
temperatura_hist = []
tiempo_hist = []

# -------------------
def obtener_datos():
    if MODO_PRUEBA:
        return random.randint(30, 80), random.randint(20, 35)
    else:
        import requests
        try:
            r = requests.get(f"http://{ESP32_IP}/sensor", timeout=2)
            if r.status_code == 200:
                datos = r.json()
                return datos.get("humedad", "---"), datos.get("temperatura", "---")
        except:
            return "---", "---"

# -------------------
def actualizar():
    tiempo = 0
    while True:
        humedad, temperatura = obtener_datos()
        etiqueta_humedad_valor.config(text=f"{humedad} %")
        etiqueta_temp_valor.config(text=f"{temperatura} °C")

        tiempo_hist.append(tiempo)
        humedad_hist.append(humedad)
        temperatura_hist.append(temperatura)
        tiempo += 1

        if len(tiempo_hist) > 20:
            tiempo_hist.pop(0)
            humedad_hist.pop(0)
            temperatura_hist.pop(0)

        ax.clear()
        ax.plot(tiempo_hist, humedad_hist, color='green', label='Humedad %')
        ax.plot(tiempo_hist, temperatura_hist, color='blue', label='Temperatura °C')
        ax.set_ylim(0, 100)
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Valor")
        ax.legend()
        canvas.draw()
        time.sleep(2)

# -------------------
ventana = tk.Tk()
ventana.title("Monitoreo de Planta 🌱")
ventana.geometry("600x400")

# Frames para organizar diseño
frame_datos = tk.Frame(ventana, padx=10, pady=10)
frame_datos.pack(side=tk.TOP, fill=tk.X)

frame_grafica = tk.Frame(ventana)
frame_grafica.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# -------------------
# Datos (arriba)
etiqueta_titulo = tk.Label(frame_datos, text="Monitoreo de Planta", font=("Arial", 16, "bold"))
etiqueta_titulo.grid(row=0, column=0, columnspan=2, pady=5)

etiqueta_humedad = tk.Label(frame_datos, text="Humedad del suelo:", font=("Arial", 14))
etiqueta_humedad.grid(row=1, column=0, sticky="w")
etiqueta_humedad_valor = tk.Label(frame_datos, text="--- %", font=("Arial", 16), fg="green")
etiqueta_humedad_valor.grid(row=1, column=1, sticky="w")

etiqueta_temp = tk.Label(frame_datos, text="Temperatura:", font=("Arial", 14))
etiqueta_temp.grid(row=2, column=0, sticky="w")
etiqueta_temp_valor = tk.Label(frame_datos, text="--- °C", font=("Arial", 16), fg="blue")
etiqueta_temp_valor.grid(row=2, column=1, sticky="w")

# -------------------
# Gráfica (abajo)
fig = Figure(figsize=(6,3), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# -------------------
hilo = threading.Thread(target=actualizar, daemon=True)
hilo.start()

ventana.mainloop()