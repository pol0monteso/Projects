"""import tkinter as tk
from tkinter import filedialog, messagebox
from testCase import start_emulation


def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=(("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx"))
    )
    if archivo:
        lista_izquierda.insert(tk.END, archivo)  # Añade el archivo a la lista izquierda


def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(
        title="Selecciona una carpeta"
    )
    if carpeta:
        lista_izquierda.insert(tk.END, carpeta)  # Añade la carpeta a la lista izquierda


def ejecutar_start_emulation():
    archivo_xml = start_emulation()  # Llama a la función para generar el archivo XML
    if archivo_xml:
        lista_derecha.insert(tk.END, archivo_xml)  # Añade el XML generado a la lista derecha


def main():
    # Crear la ventana principal
    global lista_izquierda, lista_derecha
    root = tk.Tk()
    root.title("")
    root.geometry("600x400")

    # Establecer el ícono de la ventana
    root.iconbitmap("C:\Emulation\Images/yeti_.ico")  # Reemplaza "ruta/del/icono.ico" con la ubicación de tu archivo .ico

    # Configura las filas y columnas para que se expandan
    root.grid_rowconfigure(0, weight=0)  # Primera fila (títulos)
    root.grid_rowconfigure(1, weight=0)  # Segunda fila (botones)
    root.grid_rowconfigure(2, weight=0)  # Tercera fila (listas)
    root.grid_rowconfigure(3, weight=1, minsize=200)  # Caja central que se expandirá
    root.grid_columnconfigure(0, weight=1)  # Columna de la izquierda (Archivos)
    root.grid_columnconfigure(1, weight=0)  # Columna central (Botón)
    root.grid_columnconfigure(2, weight=1)  # Columna de la derecha (XML generado)

    # Etiqueta "Alarm Inform" y botón de selección de archivo
    tk.Label(root, text="Alarm Inform:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    boton_archivo = tk.Button(root, text="Seleccionar archivo CSV o XLSX", command=seleccionar_archivo)
    boton_archivo.grid(row=0, column=1, padx=10, pady=10)

    # Etiqueta "Windows" y botón de selección de carpeta
    tk.Label(root, text="Windows:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    boton_carpeta = tk.Button(root, text="Seleccionar carpeta", command=seleccionar_carpeta)
    boton_carpeta.grid(row=1, column=1, padx=10, pady=10)

    # Lista izquierda (archivos y carpetas seleccionados por el usuario)
    tk.Label(root, text="Archivos seleccionados:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    lista_izquierda = tk.Listbox(root, width=30, height=10)
    lista_izquierda.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    # Botón para ejecutar la emulación
    boton_emulacion = tk.Button(root, text="Generar XML", command=ejecutar_start_emulation)
    boton_emulacion.grid(row=3, column=1, padx=10, pady=10)

    # Lista derecha (XML generado por el código)
    tk.Label(root, text="XML generado:").grid(row=2, column=2, padx=10, pady=10, sticky="w")
    lista_derecha = tk.Listbox(root, width=30, height=10)
    lista_derecha.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

    # Ejecutar el bucle de la interfaz
    root.mainloop()


if __name__ == "__main__":
    main()
"""
"""import tkinter as tk
from tkinter import filedialog, messagebox
from testCase import start_emulation  # Asegúrate de que esta función acepte parámetros


def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=(("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx"))
    )
    if archivo:
        lista_izquierda.insert(tk.END, archivo)  # Añade el archivo a la lista izquierda


def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(
        title="Selecciona una carpeta"
    )
    if carpeta:
        lista_izquierda.insert(tk.END, carpeta)  # Añade la carpeta a la lista izquierda


def ejecutar_start_emulation():
    # Obtiene las rutas seleccionadas
    alarmas_ruta = lista_izquierda.get(0)  # Suponiendo que la ruta de alarmas está en el primer elemento
    ventanas_ruta = lista_izquierda.get(1)  # Suponiendo que la ruta de ventanas está en el segundo elemento

    if alarmas_ruta and ventanas_ruta:
        archivo_xml = start_emulation(alarmas_ruta, ventanas_ruta)  # Llama a la función para generar el archivo XML
        if archivo_xml:
            lista_derecha.insert(tk.END, archivo_xml)  # Añade el XML generado a la lista derecha
    else:
        messagebox.showerror("Error", "Debes seleccionar tanto un archivo de alarmas como una carpeta de ventanas.")


def main():
    # Crear la ventana principal
    global lista_izquierda, lista_derecha

    root = tk.Tk()
    root.title("Interfaz de Alarmas")
    root.geometry("600x400")

    # Establecer el ícono de la ventana
    root.iconbitmap("C:\Emulation\Images/yeti_.ico")  # Reemplaza "ruta/del/icono.ico" con la ubicación de tu archivo .ico

    # Configura las filas y columnas para que se expandan
    root.grid_rowconfigure(0, weight=0)  # Primera fila (títulos)
    root.grid_rowconfigure(1, weight=0)  # Segunda fila (botones)
    root.grid_rowconfigure(2, weight=0)  # Tercera fila (listas)
    root.grid_rowconfigure(3, weight=1, minsize=200)  # Caja central que se expandirá
    root.grid_columnconfigure(0, weight=1)  # Columna de la izquierda (Archivos)
    root.grid_columnconfigure(1, weight=0)  # Columna central (Botón)
    root.grid_columnconfigure(2, weight=1)  # Columna de la derecha (XML generado)

    # Etiqueta "Alarm Inform" y botón de selección de archivo
    tk.Label(root, text="Alarm Inform:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    boton_archivo = tk.Button(root, text="Seleccionar archivo CSV o XLSX", command=seleccionar_archivo)
    boton_archivo.grid(row=0, column=1, padx=10, pady=10)

    # Etiqueta "Windows" y botón de selección de carpeta
    tk.Label(root, text="Windows:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    boton_carpeta = tk.Button(root, text="Seleccionar carpeta", command=seleccionar_carpeta)
    boton_carpeta.grid(row=1, column=1, padx=10, pady=10)

    # Lista izquierda (archivos y carpetas seleccionados por el usuario)
    tk.Label(root, text="Archivos seleccionados:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    lista_izquierda = tk.Listbox(root, width=30, height=10)
    lista_izquierda.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    # Botón para ejecutar la emulación
    boton_emulacion = tk.Button(root, text="Generar XML", command=ejecutar_start_emulation)
    boton_emulacion.grid(row=3, column=1, padx=10, pady=10)

    # Lista derecha (XML generado por el código)
    tk.Label(root, text="XML generado:").grid(row=2, column=2, padx=10, pady=10, sticky="w")
    lista_derecha = tk.Listbox(root, width=30, height=10)
    lista_derecha.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

    # Ejecutar el bucle de la interfaz
    root.mainloop()


if __name__ == "__main__":
    main()"""

import tkinter as tk
from tkinter import filedialog, messagebox
from testCase import start_emulation  # Asegúrate de que esta función acepte parámetros
import threading
from PIL import Image, ImageTk
from tkinter import PhotoImage


def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=(("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx"))
    )
    if archivo:
        lista_izquierda.insert(tk.END, archivo)  # Añade el archivo a la lista izquierda


def seleccionar_carpeta():
    carpeta = filedialog.askdirectory(
        title="Selecciona una carpeta"
    )
    if carpeta:
        lista_izquierda.insert(tk.END, carpeta)  # Añade la carpeta a la lista izquierda


def ejecutar_start_emulation():
    # Obtiene las rutas seleccionadas
    alarmas_ruta = lista_izquierda.get(0)  # Suponiendo que la ruta de alarmas está en el primer elemento
    ventanas_ruta = lista_izquierda.get(1)  # Suponiendo que la ruta de ventanas está en el segundo elemento

    if alarmas_ruta and ventanas_ruta:
        # Crear un hilo separado para ejecutar la función y evitar que la GUI se congele
        hilo_emulacion = threading.Thread(target=procesar_emulacion, args=(alarmas_ruta, ventanas_ruta))
        hilo_emulacion.start()
    else:
        messagebox.showerror("Error", "Debes seleccionar tanto un archivo de alarmas como una carpeta de ventanas.")


def procesar_emulacion(alarmas_ruta, ventanas_ruta):
    try:
        archivo_xml = start_emulation(alarmas_ruta, ventanas_ruta)  # Llama a la función para generar el archivo XML
        if archivo_xml:
            # Utiliza el método after para actualizar la interfaz en el hilo principal
            root.after(0, actualizar_lista_xml, archivo_xml)
        else:
            root.after(0, mostrar_error, "Error al generar el XML")
    except Exception as e:
        root.after(0, mostrar_error, f"Error: {str(e)}")


def actualizar_lista_xml(archivo_xml):
    lista_derecha.insert(tk.END, archivo_xml)  # Añade el XML generado a la lista derecha


def mostrar_error(mensaje):
    messagebox.showerror("Error", mensaje)


def main():
    # Crear la ventana principal
    global root
    root = tk.Tk()
    root.title("YETI")
    root.geometry("600x400")
    """img = Image.open(r'C:\Emulation\Images\yeti_.jpg')
    img = img.resize((16, 16))  # Redimensiona el ícono si es necesario
    icon = ImageTk.PhotoImage(img)
    root.iconphoto(False, icon)"""
    # Establecer el ícono de la ventana
    root.iconbitmap("C:\Emulation\Images/yeti_.ico")  # Reemplaza "ruta/del/icono.ico" con la ubicación de tu archivo .ico

    # Configura las filas y columnas para que se expandan
    root.grid_rowconfigure(0, weight=0)  # Primera fila (títulos)
    root.grid_rowconfigure(1, weight=0)  # Segunda fila (botones)
    root.grid_rowconfigure(2, weight=0)  # Tercera fila (listas)
    root.grid_rowconfigure(3, weight=1, minsize=200)  # Caja central que se expandirá
    root.grid_columnconfigure(0, weight=1)  # Columna de la izquierda (Archivos)
    root.grid_columnconfigure(1, weight=0)  # Columna central (Botón)
    root.grid_columnconfigure(2, weight=1)  # Columna de la derecha (XML generado)

    # Etiqueta "Alarm Inform" y botón de selección de archivo
    tk.Label(root, text="Alarm Information:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
    boton_archivo = tk.Button(root, text="Select XSLX or CSV file", command=seleccionar_archivo)
    boton_archivo.grid(row=0, column=1, padx=10, pady=10)

    # Etiqueta "Windows" y botón de selección de carpeta
    tk.Label(root, text="Windows Folder:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    boton_carpeta = tk.Button(root, text="Select Folder With XAML", command=seleccionar_carpeta)
    boton_carpeta.grid(row=1, column=1, padx=10, pady=10)

    # Lista izquierda (archivos y carpetas seleccionados por el usuario)
    tk.Label(root, text="Emulation Sources:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    global lista_izquierda
    lista_izquierda = tk.Listbox(root, width=30, height=10)
    lista_izquierda.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    # Botón para ejecutar la emulación
    boton_emulacion = tk.Button(root, text="Generate XML", command=ejecutar_start_emulation)
    boton_emulacion.grid(row=3, column=1, padx=10, pady=10)

    # Lista derecha (XML generado por el código)
    tk.Label(root, text="new XML:").grid(row=2, column=2, padx=10, pady=10, sticky="w")
    global lista_derecha
    lista_derecha = tk.Listbox(root, width=30, height=10)
    lista_derecha.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

    # Ejecutar el bucle de la interfaz
    root.mainloop()


if __name__ == "__main__":
    main()
