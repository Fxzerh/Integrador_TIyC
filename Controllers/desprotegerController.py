from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
import os


class DesprotegerController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))            # Directorio Actual
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")  # Carpeta donde se guardan los archivos

        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
        try:
            self.mainWindow.tableFileDP.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)   # Para que la columna ocupe el espacio libre
            self.mainWindow.tableFileDP.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Para que se selecciones la fila completa
            self.mainWindow.tableFileDP.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Para que permita seleccionar una fila a la vez
            self.mainWindow.tableFileDP.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Para que no permita editar las celdas
            self.mainWindow.tableFileDP.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
            self.cargarTabla()          # Cargamos la tabla
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.subirArchivoDP_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.tableFileDP.itemClicked.connect(self.mostrar)


    
    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileDP.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewDP.setUrl(QUrl("about:blank"))
    
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
                    rowPosition = self.mainWindow.tableFileDP.rowCount()
                    self.mainWindow.tableFileDP.insertRow(rowPosition)
                    self.mainWindow.tableFileDP.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                    self.mainWindow.tableFileDP.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño

    def mostrarArchivo(self, nombre_archivo):
        ruta_completa = os.path.join(self.carpetaArchivos, nombre_archivo)
        if os.path.exists(ruta_completa):
            url_local = QUrl.fromLocalFile(ruta_completa)   # Transformamos la ruta de Windows a una URL que entienda el componente web        
            self.mainWindow.viewDP.setUrl(url_local)         # Setteamos la vista web que lo dibuje en pantalla

    def mostrar(self, item):
        fila = item.row()      # Obtenemos el número de la fila que el usuario tocó
        nombre = self.mainWindow.tableFileDP.item(fila, 0)    # Extraemos el objeto celda de la columna 0 (Nombre) en esa fila
        nombreArchivo = nombre.text()    # Sacamos el texto plano (el nombre real del archivo)
        self.mostrarArchivo(nombreArchivo)     # Le pasamos el nombre a la función que lo carga en el visor web