import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from testCase import start_emulation
import threading

def main():
    root = tk.Tk()
    root.title("Yokogawa Translation to IIS")
    root.geometry("1000x500")
    root.iconbitmap(r"C:\Emulation\inp_logo.ico")

    # Estilo de ttk
    style = ttk.Style()
    style.theme_use("clam")

    def add_placeholder(entry, placeholder_text):
        placeholder_font = ("Arial", 10, "italic")

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(foreground="gray", font=placeholder_font)

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(foreground="black", font=("Arial", 10))

        entry.insert(0, placeholder_text)
        entry.config(foreground="gray", font=placeholder_font)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def select_hierarchy_file():
        file = filedialog.askopenfilename(
            title="Select Hierarchy CSV File",
            filetypes=(("CSV Files", "*.csv"),)
        )
        if file:
            hierarchy_file_entry.delete(0, tk.END)
            hierarchy_file_entry.insert(0, file)

    def check_files_and_generate():
        alarms_file = alarms_file_entry.get()
        tuning_params = tuning_file_entry.get()
        windows_directory = windows_folder_entry.get()
        database_path = database_folder_entry.get()
        filter_value = starts_entry.get()

        # Si el filtro está vacío, asignar un valor que indique que no se debe filtrar
        if not filter_value:  # Si está vacío
            filter_value = None

        if not alarms_file or not tuning_params or not windows_directory or not database_path:
            messagebox.showerror("Error", "Please select all required files and folders.")
            return

        # Crear un hilo separado para ejecutar la emulación
        emulation_thread = threading.Thread(target=start_emulation, args=(alarms_file, windows_directory, tuning_params, database_path, filter_value))
        emulation_thread.start()

    def select_alarms_file():
        file = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=(("CSV Files", "*.csv"),)
        )
        if file:
            alarms_file_entry.delete(0, tk.END)
            alarms_file_entry.insert(0, file)

    def select_tuning_parameters_folder():
        folder = filedialog.askdirectory(
            title="Select Folder with Tuning Parameters CSV Files"
        )
        if folder:
            tuning_file_entry.delete(0, tk.END)
            tuning_file_entry.insert(0, folder)

    def select_screens_folder():
        folder = filedialog.askdirectory(
            title="Select Folder with Screens"
        )
        if folder:
            windows_folder_entry.delete(0, tk.END)
            windows_folder_entry.insert(0, folder)

    def select_database_folder():
        folder = filedialog.askdirectory(
            title="Select Folder with FCS SCS Database"
        )
        if folder:
            database_folder_entry.delete(0, tk.END)
            database_folder_entry.insert(0, folder)

    button_help = ttk.Button(root, text="Help", width=5)
    button_help.grid(row=0, column=3, padx=10, pady=10, sticky="w")

    ttk.Label(root, text="Alarm Information (CSV):", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5)
    global alarms_file_entry
    alarms_file_entry = ttk.Entry(root, width=30)
    alarms_file_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(root, text="Select File", command=select_alarms_file).grid(row=1, column=2, padx=5, pady=5)

    # TUNING PARAMETERS INFORMATION
    ttk.Label(root, text="Tuning Parameters Folder:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5)
    global tuning_file_entry
    tuning_file_entry = ttk.Entry(root, width=30)
    tuning_file_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(root, text="Select Folder", command=select_tuning_parameters_folder).grid(row=2, column=2, padx=5, pady=5)

    # WINDOWS FOLDER
    ttk.Label(root, text="WINDOWS Folder:", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=5, pady=5)
    global windows_folder_entry
    windows_folder_entry = ttk.Entry(root, width=30)
    windows_folder_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(root, text="Select Folder", command=select_screens_folder).grid(row=3, column=2, padx=5, pady=5)

    tk.Label(root, text="XAML files Starting With:", font=("Arial", 8, "bold")).grid(row=4, column=0, padx=5, pady=5, sticky="e")
    starts_entry = ttk.Entry(root, width=20)
    starts_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    add_placeholder(starts_entry, "Ex: PRO-01")

    # FCS&SCS INFORMATION
    ttk.Label(root, text="FCS & SCS Folder:", font=("Arial", 10, "bold")).grid(row=5, column=0, padx=5, pady=5)
    global database_folder_entry
    database_folder_entry = ttk.Entry(root, width=30)
    database_folder_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(root, text="Select Folder", command=select_database_folder).grid(row=5, column=2, padx=5, pady=5)

    # HIERARCHY INFORMATION
    ttk.Label(root, text="Hierarchy Information (CSV):", font=("Arial", 10, "bold")).grid(row=6, column=0, padx=5, pady=5)
    global hierarchy_file_entry
    hierarchy_file_entry = ttk.Entry(root, width=30)
    hierarchy_file_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(root, text="Select File", command=select_hierarchy_file).grid(row=6, column=2, padx=5, pady=5)

    # Generate Button
    generate_button = ttk.Button(root, text="Generate .iis Project", width=30, command=check_files_and_generate)
    generate_button.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

    # version Label
    tk.Label(root, text="DEMO ---- testing version", font=("Arial", 8, "bold", "italic")).grid(row=7, column=0, padx=5, pady=5, sticky="ws")

    # Al cerrar la ventana, detener el hilo de emulación si está en ejecución
    def on_close():
        # Si el hilo de emulación está en ejecución, puedes hacer un "join" para esperar que termine
        if threading.active_count() > 1:  # Si hay más de un hilo activo (el hilo principal y el de emulación)
            messagebox.showinfo("Closing", "Process is running. Please wait until it completes.")
        else:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)
    root.grid_rowconfigure(7, weight=3)

    # Ejecutar la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
