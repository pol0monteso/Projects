import tkinter as tk
import sys


class LogWindow:
    """Crea una ventana para mostrar logs en modo de solo lectura."""

    def __init__(self, master=None):
        # Crear la ventana de logs
        self.window = tk.Toplevel(master)
        self.window.title("Log Output")
        self.window.geometry("900x400")
        self.window.resizable(True, True)

        # Configurar el área de texto de solo lectura
        self.text_widget = tk.Text(
            self.window, wrap="word", state=tk.DISABLED, font=("Arial", 10), cursor="xterm"  # Cursor tipo "I"
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Añadir una barra de desplazamiento
        self.scrollbar = tk.Scrollbar(
            self.text_widget, command=self._on_scroll, cursor="arrow"  # Cursor tipo flecha
        )
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Redirigir sys.stdout a esta ventana
        sys.stdout = self

        # Estado para controlar si el desplazamiento es automático
        self.auto_scroll = True

        # Vincular evento de cierre de ventana
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def _on_scroll(self, *args):
        """Maneja el desplazamiento manual de la barra."""
        self.text_widget.yview(*args)
        # Verificar si el usuario está en el final del texto
        current_scroll_position = self.text_widget.yview()
        if current_scroll_position[1] == 1.0:  # Si la barra está al final
            self.auto_scroll = True
        else:
            self.auto_scroll = False

    def write(self, message):
        """Agrega un mensaje al log."""
        try:
            if self.window.winfo_exists():  # Comprobar si la ventana aún existe
                self.text_widget.config(state=tk.NORMAL)  # Habilitar edición temporalmente
                self.text_widget.insert(tk.END, message)
                self.text_widget.config(state=tk.DISABLED)  # Volver a modo de solo lectura

                # Realizar desplazamiento automático solo si está habilitado
                if self.auto_scroll:
                    self.text_widget.see(tk.END)
        except Exception as e:
            print(f"Error al escribir en log: {e}", file=sys.__stdout__)

    def flush(self):
        """Necesario para implementar sys.stdout."""
        pass

    def on_close(self):
        """Oculta la ventana en lugar de cerrarla."""
        self.window.withdraw()  # Ocultar la ventana

    def show(self):
        """Vuelve a mostrar la ventana si está oculta."""
        self.window.deiconify()  # Mostrar la ventana

