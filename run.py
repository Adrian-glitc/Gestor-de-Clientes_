import sys
from Gestor.menu import iniciar
from Gestor.ui import MainWindow

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        iniciar()  # Modo terminal
    else:
        app = MainWindow()
        app.mainloop()  # Modo gráfico