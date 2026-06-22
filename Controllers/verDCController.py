from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl, QTimer
from Clases.cargarArchivo import Cargar
import os


class VerDCController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")

        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
        try:
            self.mainWindow.tableFileVDC.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.mainWindow.tableFileVDC.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.mainWindow.tableFileVDC.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            self.mainWindow.tableFileVDC.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.mainWindow.tableFileVDC.setRowCount(0)
            self.cargarTabla()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.tableFileVDC.itemClicked.connect(self.mostrarArchivo)


    def cambiarPanel(self, indice):
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
                if fileType in [".txt",".pdf",".jpg",".png",".zip",".dhu"]:
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
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "No se ha seleccionado ningún archivo.")
            return
        extension = os.path.splitext(nombreArchivo)[1]
        nombre = os.path.splitext(nombreArchivo)[0]
        rutaCompleta = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(rutaCompleta):
            rutaRecuperado = os.path.join(self.carpetaArchivos, nombre + ".dhu")
            url_local1 = QUrl.fromLocalFile(rutaCompleta)       # Transformamos la ruta del archivo original a una URL que entienda el componente web        
            url_local2 = QUrl.fromLocalFile(rutaRecuperado)     # Transformamos la ruta del archivo recuperado a una URL que entienda el componente web
            self.mainWindow.viewVDC_O.setUrl(url_local1)        # Setteamos la vista web que lo dibuje en pantalla
            self.mainWindow.viewVDC_R.setUrl(url_local2)
        
