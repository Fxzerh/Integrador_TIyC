from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
import os


class VerDCController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))            # Directorio Actual
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")  # Carpeta donde se guardan los archivos

        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
        try:
            self.mainWindow.tableFileVDC.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)   # Para que la columna ocupe el espacio libre
            self.mainWindow.tableFileVDC.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Para que se selecciones la fila completa
            self.mainWindow.tableFileVDC.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Para que permita seleccionar una fila a la vez
            self.mainWindow.tableFileVDC.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Para que no permita editar las celdas
            self.mainWindow.tableFileVDC.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
            self.cargarTabla()          # Cargamos la tabla
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.tableFileVDC.itemClicked.connect(self.mostrarArchivo)



    
    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileVDC.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewVDC_O.setUrl(QUrl("about:blank"))
        self.mainWindow.viewVDC_R.setUrl(QUrl("about:blank"))

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
                    rowPosition = self.mainWindow.tableFileVDC.rowCount()
                    self.mainWindow.tableFileVDC.insertRow(rowPosition)
                    self.mainWindow.tableFileVDC.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                    self.mainWindow.tableFileVDC.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño

    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileVDC.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            nombreArchivo = self.mainWindow.tableFileVDC.item(row, 0).text()
            return nombreArchivo
        return None

    def mostrarArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        ruta_completa = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(ruta_completa):
            url_local = QUrl.fromLocalFile(ruta_completa)   # Transformamos la ruta de Windows a una URL que entienda el componente web        
            self.mainWindow.viewVDC_O.setUrl(url_local)         # Setteamos la vista web que lo dibuje en pantalla
