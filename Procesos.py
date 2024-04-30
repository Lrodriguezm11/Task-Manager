import tkinter as tk
from tkinter import ttk
from collections import deque

class Proceso:
    def __init__(self, nombre, tiempo):
        self.nombre = nombre
        self.tiempo = tiempo
        self.tiempo_restante = tiempo

class ProgramaScheduling:
    def __init__(self, root):
        self.root = root
        self.procesos_lifo = deque()
        self.procesos_fifo = deque()
        self.en_ejecucion = None
        self.algoritmo_actual = tk.StringVar()

        self.menu_frame = tk.Frame(root, bg="#f0f0f0")  
        self.menu_frame.pack()

        self.lifo_button = tk.Button(self.menu_frame, text="LIFO", command=self.mostrar_ventana_proceso_lifo, bg="#4caf50", fg="white", padx=10)
        self.lifo_button.pack(side="left")

        self.fifo_button = tk.Button(self.menu_frame, text="FIFO", command=self.mostrar_ventana_proceso_fifo, bg="#2196f3", fg="white", padx=10)
        self.fifo_button.pack(side="left")

        self.borrar_button = tk.Button(self.menu_frame, text="Borrar", command=self.borrar_procesos, bg="#f44336", fg="white", padx=10)
        self.borrar_button.pack(side="left")

        self.algoritmo_label = tk.Label(self.menu_frame, textvariable=self.algoritmo_actual, font=("Arial", 12))
        self.algoritmo_label.pack(side="left")

        self.procesos_frame = tk.Frame(root, bg="#ffffff")  
        self.procesos_frame.pack(fill=tk.BOTH, expand=True)

        self.root.after(1000, self.actualizar_procesos)
    
    def borrar_procesos(self):
        for widget in self.procesos_frame.winfo_children():
            widget.destroy()
        self.procesos_lifo.clear()
        self.procesos_fifo.clear()
        self.en_ejecucion = None
        self.algoritmo_actual.set("")

    def mostrar_ventana_proceso_lifo(self):
        ventana_proceso = tk.Toplevel(self.root)
        ventana_proceso.title("Agregar Proceso LIFO")
        ventana_proceso.geometry("300x200")

        self.nombre_label = tk.Label(ventana_proceso, text="Nombre del proceso:", font=("Arial", 12))
        self.nombre_label.pack()

        self.nombre_entry = tk.Entry(ventana_proceso, font=("Arial", 12))
        self.nombre_entry.pack()

        self.tiempo_label = tk.Label(ventana_proceso, text="Tiempo del proceso:", font=("Arial", 12))
        self.tiempo_label.pack()

        self.tiempo_entry = tk.Entry(ventana_proceso, font=("Arial", 12))
        self.tiempo_entry.pack()

        self.agregar_button = tk.Button(ventana_proceso, text="Agregar Proceso", command=self.agregar_proceso_lifo, bg="#4caf50", fg="white", padx=10)
        self.agregar_button.pack()

    def mostrar_ventana_proceso_fifo(self):
        ventana_proceso = tk.Toplevel(self.root)
        ventana_proceso.title("Agregar Proceso FIFO")
        ventana_proceso.geometry("300x200")

        self.nombre_label = tk.Label(ventana_proceso, text="Nombre del proceso:", font=("Arial", 12))
        self.nombre_label.pack()

        self.nombre_entry = tk.Entry(ventana_proceso, font=("Arial", 12))
        self.nombre_entry.pack()

        self.tiempo_label = tk.Label(ventana_proceso, text="Tiempo del proceso:", font=("Arial", 12))
        self.tiempo_label.pack()

        self.tiempo_entry = tk.Entry(ventana_proceso, font=("Arial", 12))
        self.tiempo_entry.pack()

        self.agregar_button = tk.Button(ventana_proceso, text="Agregar Proceso", command=self.agregar_proceso_fifo, bg="#2196f3", fg="white", padx=10)
        self.agregar_button.pack()

    def agregar_proceso_lifo(self):
        nombre = self.nombre_entry.get()
        tiempo = int(self.tiempo_entry.get())
        proceso = Proceso(nombre, tiempo)
        self.procesos_lifo.append(proceso)

        proceso_frame = tk.Frame(self.procesos_frame, bg="#ffffff", padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
        proceso_frame.pack(fill=tk.X)

        proceso_nombre_label = tk.Label(proceso_frame, text="Proceso: " + proceso.nombre, font=("Arial", 10))
        proceso_nombre_label.pack(side="left")

        proceso_tiempo_label = tk.Label(proceso_frame, text="Tiempo restante: " + str(proceso.tiempo), font=("Arial", 10))
        proceso_tiempo_label.pack(side="left")

        proceso.barra_progreso = ttk.Progressbar(proceso_frame, length=150, mode='determinate', maximum=tiempo)
        proceso.barra_progreso.pack(side="left")
        proceso.barra_progreso['value'] = tiempo

        proceso.tiempo_label = proceso_tiempo_label

        self.nombre_entry.delete(0, tk.END)
        self.tiempo_entry.delete(0, tk.END)

    def agregar_proceso_fifo(self):
        nombre = self.nombre_entry.get()
        tiempo = int(self.tiempo_entry.get())
        proceso = Proceso(nombre, tiempo)
        self.procesos_fifo.append(proceso)

        proceso_frame = tk.Frame(self.procesos_frame, bg="#ffffff", padx=10, pady=5, relief=tk.RAISED, borderwidth=1)
        proceso_frame.pack(fill=tk.X)

        proceso_nombre_label = tk.Label(proceso_frame, text="Proceso: " + proceso.nombre, font=("Arial", 10))
        proceso_nombre_label.pack(side="left")

        proceso_tiempo_label = tk.Label(proceso_frame, text="Tiempo restante: " + str(proceso.tiempo), font=("Arial", 10))
        proceso_tiempo_label.pack(side="left")

        proceso.barra_progreso = ttk.Progressbar(proceso_frame, length=150, mode='determinate', maximum=tiempo)
        proceso.barra_progreso.pack(side="left")
        proceso.barra_progreso['value'] = tiempo

        proceso.tiempo_label = proceso_tiempo_label

        self.nombre_entry.delete(0, tk.END)
        self.tiempo_entry.delete(0, tk.END)


    def actualizar_procesos(self):
        if self.en_ejecucion is None or self.en_ejecucion.tiempo_restante <= 0:
            if len(self.procesos_lifo) > 0:
                self.en_ejecucion = self.procesos_lifo.pop()  # Obtener el último proceso de la cola LIFO
            elif len(self.procesos_fifo) > 0:
                self.en_ejecucion = self.procesos_fifo.popleft()  # Obtener el primer proceso de la cola FIFO

        if self.en_ejecucion is not None:
            self.en_ejecucion.tiempo_restante -= 1
            if self.en_ejecucion.tiempo_restante >= 0:
                self.en_ejecucion.barra_progreso['value'] = self.en_ejecucion.tiempo_restante  # Actualizar la barra de progreso
                self.en_ejecucion.tiempo_label.config(text="Tiempo restante: " + str(self.en_ejecucion.tiempo_restante))

        self.root.after(1000, self.actualizar_procesos)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Administrador de Procesos")
    root.geometry("400x300")
    programa = ProgramaScheduling(root)
    root.mainloop()
