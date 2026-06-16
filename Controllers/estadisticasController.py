from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
import os


class EstadisticasController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))            # Directorio Actual
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")  # Carpeta donde se guardan los archivos

        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
        try:
            #self.mainWindow.tableFileE.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)   # Para que la columna ocupe el espacio libre
            self.mainWindow.tableFileE.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.mainWindow.tableFileE.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Para que se selecciones la fila completa
            self.mainWindow.tableFileE.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Para que permita seleccionar una fila a la vez
            self.mainWindow.tableFileE.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Para que no permita editar las celdas
            self.mainWindow.tableFileE.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
            self.cargarTabla()          # Cargamos la tabla
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        
        
        
        
    def refrescarPanel(self):
        self.mainWindow.tableFileE.setRowCount(0)
        self.cargarTabla()
    
    def cargarTabla(self):
        if os.path.exists(self.carpetaArchivos):
            files = os.listdir(self.carpetaArchivos)
            for f in files:
                fileType = os.path.splitext(f)[1]
                file_path = os.path.join(self.carpetaArchivos, f)   # Ruta completa del archivo f
                if os.path.isfile(file_path):  # Pregunta si f es un archivo (y no una carpeta)
                    # Obtenemos el tamaño de f
                    tamaño = os.path.getsize(file_path)

                    # Convertir tamaño a formato B, KB o MB
                    if tamaño < 1024:
                        tamaño_str = f"{tamaño} B"
                    elif tamaño < 1024 * 1024:
                        tamaño_str = f"{tamaño / 1024:.2f} KB"
                    else:
                        tamaño_str = f"{tamaño / (1024 * 1024):.2f} MB"
                    
                    # Agregamos el archivo a la tabla
                    rowPosition = self.mainWindow.tableFileE.rowCount()
                    self.mainWindow.tableFileE.insertRow(rowPosition)
                    self.mainWindow.tableFileE.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                    self.mainWindow.tableFileE.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño