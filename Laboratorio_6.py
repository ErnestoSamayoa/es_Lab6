import tkinter as tk
import serial
import threading

# Inicializar la comunicación serial con Arduino
arduino = serial.Serial('COM3', 9600, timeout=1)  # Reemplaza 'COM3' con el puerto correcto

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Dashboard")

# Título para la ventana
titulo = tk.Label(ventana, text="Estados de LED", font=("Helvetica", 16), pady=10)
titulo.pack(anchor='n')  # 'n' para alinear el título en la parte superior

# Función para enviar comandos a Arduino
def enviar_comando(comando):
    arduino.write(comando.encode())

# Función para manejar el dibujo de círculos y enviar comandos
def draw(event):
    x = event.x
    y = event.y
    color = ""

    if 100 <= x <= 200 and 100 <= y <= 200:
        enviar_comando('A')
        color = "yellow"
    elif 250 <= x <= 350 and 100 <= y <= 200:
        enviar_comando('B')
        color = "blue"
    elif 400 <= x <= 500 and 100 <= y <= 200:
        enviar_comando('C')
        color = "red"
    elif 550 <= x <= 650 and 100 <= y <= 200:
        enviar_comando('D')
        color = "green"
    elif 300 <= x <= 400 and 300 <= y <= 400:
        enviar_comando('E')
        color = "gray"

    if color:
        # Restablecer todos los círculos a blanco
        canvas.itemconfig("led", fill="white")
        # Cambiar color del LED clickeado
        canvas.itemconfig(tk.CURRENT, fill=color)

# Crear el canvas
canvas = tk.Canvas(ventana, width=750, height=500)
canvas.pack()

# Dibujar los círculos/LEDs en el canvas
canvas.create_oval(100, 100, 200, 200, fill="white", tags=("led",))  # LED amarillo
canvas.create_oval(250, 100, 350, 200, fill="white", tags=("led",))  # LED azul
canvas.create_oval(400, 100, 500, 200, fill="white", tags=("led",))  # LED rojo
canvas.create_oval(550, 100, 650, 200, fill="white", tags=("led",))  # LED verde
canvas.create_rectangle(300, 300, 400, 400, fill="light gray", tags=("led",))  # Botón de apagar

# Vincular la función draw al evento clic en el canvas
canvas.bind("<Button-1>", draw)

# Bucle principal para recibir y procesar datos de Arduino
def leer_datos_desde_arduino():
    while True:
        datos = arduino.readline().decode().strip()
        if datos:
            print(datos)  # Imprime los datos recibidos desde Arduino en la consola

# Crear un hilo para leer datos de Arduino en segundo plano
thread_arduino = threading.Thread(target=leer_datos_desde_arduino)
thread_arduino.start()

# Iniciar el bucle de la interfaz de usuario
ventana.mainloop()