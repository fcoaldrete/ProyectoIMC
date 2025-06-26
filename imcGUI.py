import tkinter as tk
from tkinter import ttk, messagebox
import imc
import imcDB

class GUI:
    def __init__(self):
        self.__ventana = tk.Tk()
        self.__ventana.title("Calculadora de IMC")
        self.__ventana.configure(bg="#E8F0FE")
        self.__ventana.geometry("500x500")
        self.__ventana.resizable(False, False)

        fuente = ("Segoe UI", 10)

        # Variables
        self.__nombre = tk.StringVar()
        self.__edad = tk.IntVar(value=18)
        self.__estatura = tk.DoubleVar(value=1.70)
        self.__peso = tk.DoubleVar(value=70.0)
        self.__info = tk.StringVar()
        self.__mensaje_bienvenida = tk.StringVar()

        self.__nombre.trace_add("write", self.__activar_campos)

        # Fila 0: Nombre
        ttk.Label(self.__ventana, text="Nombre:", font=fuente).grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.__entrada_nombre = ttk.Entry(self.__ventana, textvariable=self.__nombre, font=fuente, width=25)
        self.__entrada_nombre.grid(row=0, column=1, padx=5)

        # Fila 1: Mensaje de bienvenida (centrado dentro del Label)
        self.__etiqueta_bienvenida = tk.Label(
            self.__ventana,
            textvariable=self.__mensaje_bienvenida,
            font=("Segoe UI", 10, "italic"),
            bg="#E8F0FE",
            fg="#003366",
            justify="center",
            anchor="center"
        )
        self.__etiqueta_bienvenida.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        # Fila 2: Edad
        ttk.Label(self.__ventana, text="Edad:", font=fuente).grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.__spin_edad = tk.Spinbox(self.__ventana, from_=1, to=120, textvariable=self.__edad, font=fuente, width=5, state="disabled")
        self.__spin_edad.grid(row=2, column=1, sticky="w", padx=5)

        # Fila 3: Estatura (con Scale)
        ttk.Label(self.__ventana, text="Estatura (m):", font=fuente).grid(row=3, column=0, sticky="ne", pady=5, padx=5)
        self.__scale_estatura = tk.Scale(
            self.__ventana, from_=0.30, to=2.50, resolution=0.01,
            orient="horizontal", variable=self.__estatura,
            length=250, state="disabled"
        )
        self.__scale_estatura.grid(row=3, column=1, sticky="w", pady=5)

        # Fila 4: Peso (con Scale)
        ttk.Label(self.__ventana, text="Peso (kg):", font=fuente).grid(row=4, column=0, sticky="ne", pady=5, padx=5)
        self.__scale_peso = tk.Scale(
            self.__ventana, from_=5, to=200, resolution=0.5,
            orient="horizontal", variable=self.__peso,
            length=250, state="disabled"
        )
        self.__scale_peso.grid(row=4, column=1, sticky="w", pady=5)

        # Fila 5: Botones
        ttk.Button(self.__ventana, text="Calcular IMC", command=self.__calcular).grid(row=5, column=0, pady=10, padx=5)
        ttk.Button(self.__ventana, text="Limpiar", command=self.__limpiar).grid(row=5, column=1, padx=5, sticky="w")

        # Fila 6: LabelFrame del resumen
        self.__resumen = tk.LabelFrame(self.__ventana, text="Resultado", font=("Segoe UI", 9, "bold"),
                                       bg="#F7FBFF", padx=10, pady=10)
        self.__resumen.grid(row=6, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        self.__resumen.grid_remove()

        tk.Label(self.__resumen, textvariable=self.__info, justify="left", bg="#F7FBFF", font=("Segoe UI", 9)).pack()

        self.__centrar_ventana()

    def mostrar(self):
        self.__ventana.mainloop()

    def __centrar_ventana(self):
        self.__ventana.update_idletasks()
        ancho = self.__ventana.winfo_width()
        alto = self.__ventana.winfo_height()
        pantalla_ancho = self.__ventana.winfo_screenwidth()
        pantalla_alto = self.__ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.__ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def __activar_campos(self, *args):
        nombre = self.__nombre.get().strip()
        if nombre:
            self.__mensaje_bienvenida.set(f"Hola {nombre}\n¡Bienvenido a la Calculadora del Índice de Masa Corporal!")
            self.__spin_edad.config(state="normal")
            self.__scale_estatura.config(state="normal")
            self.__scale_peso.config(state="normal")
        else:
            self.__mensaje_bienvenida.set("")
            self.__spin_edad.config(state="disabled")
            self.__scale_estatura.config(state="disabled")
            self.__scale_peso.config(state="disabled")

    def __calcular(self):
        try:
            est = self.__estatura.get()
            pes = self.__peso.get()
        except Exception:
            messagebox.showerror("Error", "Estatura y peso deben ser válidos.")
            return

        try:
            persona = imc.IMC(
                self.__nombre.get(),
                self.__edad.get(),
                est,
                pes
            )
            datos = persona.obtener_datos()
            imcDB.insertar(datos)
            resumen = (
                f"Nombre: {datos['nombre']}\n"
                f"Edad: {datos['edad']} años\n"
                f"Estatura: {datos['estatura']} m\n"
                f"Peso: {datos['peso']} kg\n"
                f"IMC: {datos['imc']}\n"
                f"Clasificación: {datos['clasificacion']}"
            )
            self.__info.set(resumen)
            self.__resumen.grid()
            self.__ventana.update_idletasks()
            self.__ventana.geometry("")
            self.__centrar_ventana()
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def __limpiar(self):
        self.__nombre.set("")
        self.__edad.set(18)
        self.__estatura.set(1.70)
        self.__peso.set(70.0)
        self.__mensaje_bienvenida.set("")
        self.__info.set("")
        self.__resumen.grid_remove()
        self.__ventana.geometry("")
        self.__centrar_ventana()
        self.__spin_edad.config(state="disabled")
        self.__scale_estatura.config(state="disabled")
        self.__scale_peso.config(state="disabled")

# Ejecución directa
if __name__ == "__main__":
    app = GUI()
    app.mostrar()
