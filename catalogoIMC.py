import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import imcDB
import csv

class CatalogoIMC:
    def __init__(self):
        self.__ventana = tk.Tk()
        self.__ventana.title("Catálogo de IMC registrados")
        self.__ventana.configure(bg="#F0F4FF")
        self.__ventana.geometry("800x400")
        self.__ventana.resizable(True, True)

        fuente = ("Segoe UI", 10)

        ttk.Label(self.__ventana, text="Listado de Registros de IMC", font=("Segoe UI", 12, "bold")).pack(pady=10)

        # Tabla Treeview
        columnas = ("Nombre", "Edad", "Estatura", "Peso", "IMC", "Clasificación")
        self.__tabla = ttk.Treeview(self.__ventana, columns=columnas, show="headings", height=15)

        for col in columnas:
            self.__tabla.heading(col, text=col)
            self.__tabla.column(col, anchor="center", width=120)

        self.__tabla.pack(padx=10, pady=5, fill="both", expand=True)

        # Cargar datos desde la BD
        self.__cargar_datos()

        # Botón Exportar CSV
        ttk.Button(self.__ventana, text="Exportar a CSV", command=self.__exportar_csv).pack(pady=10)

        self.__ventana.mainloop()

    def __cargar_datos(self):
        registros = imcDB.consultar()
        for fila in registros:
            self.__tabla.insert("", "end", values=fila)

    def __exportar_csv(self):
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivo CSV", "*.csv")],
                title="Guardar como",
                initialfile="imc_registros.csv"
            )
            if not archivo:
                return

            with open(archivo, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Nombre", "Edad", "Estatura", "Peso", "IMC", "Clasificación"])
                for item in self.__tabla.get_children():
                    fila = self.__tabla.item(item)["values"]
                    writer.writerow(fila)

            messagebox.showinfo("Éxito", "Archivo CSV exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")

# Ejecución directa
if __name__ == "__main__":
    app = CatalogoIMC()
