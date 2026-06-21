from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl, QTimer
from Clases.cargarArchivo import Cargar
import os


class VerDPController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")
        self.corregido = True

        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
        try:
            self.mainWindow.m8VDP_btn.setEnabled(False)
            self.mainWindow.m1024VDP_btn.setEnabled(False)
            self.mainWindow.m16384VDP_btn.setEnabled(False)
            self.mainWindow.tableFileVDP.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.mainWindow.tableFileVDP.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.mainWindow.tableFileVDP.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            self.mainWindow.tableFileVDP.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.mainWindow.tableFileVDP.setRowCount(0)
            self.cargarTabla()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.tableFileVDP.itemClicked.connect(self.mostrar)
        self.mainWindow.sinCorregirVDP_btn.clicked.connect(lambda: self.mostrarArchivo(False))
        self.mainWindow.corregidoVDP_btn.clicked.connect(lambda: self.mostrarArchivo(True))
        self.mainWindow.m8VDP_btn.clicked.connect(lambda: self.mostrarDesprotegido(1))
        self.mainWindow.m1024VDP_btn.clicked.connect(lambda: self.mostrarDesprotegido(2))
        self.mainWindow.m16384VDP_btn.clicked.connect(lambda: self.mostrarDesprotegido(3))


    def cambiarPanel(self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileVDP.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewVDP_O.setUrl(QUrl("about:blank"))
        self.mainWindow.viewVDP_R.setUrl(QUrl("about:blank"))
        self.mainWindow.m8VDP_btn.setEnabled(False)
        self.mainWindow.m1024VDP_btn.setEnabled(False)
        self.mainWindow.m16384VDP_btn.setEnabled(False)

    def cargarTabla(self):
        if os.path.exists(self.carpetaArchivos):
            files = os.listdir(self.carpetaArchivos)
            for f in files:
                fileType = os.path.splitext(f)[1]
                if True:
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
                        rowPosition = self.mainWindow.tableFileVDP.rowCount()
                        self.mainWindow.tableFileVDP.insertRow(rowPosition)
                        self.mainWindow.tableFileVDP.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                        self.mainWindow.tableFileVDP.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño

    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileVDP.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            nombreArchivo = self.mainWindow.tableFileVDP.item(row, 0).text()
            return nombreArchivo
        return None
    
    def mostrar(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "No se ha seleccionado ningún archivo.")
            return
        nombre = os.path.splitext(nombreArchivo)[0]
        rutaCompleta = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(rutaCompleta):
            url_local = QUrl.fromLocalFile(rutaCompleta)       # Transformamos la ruta del archivo original a una URL que entienda el componente web        
            self.mainWindow.viewVDP_O.setUrl(url_local)        # Setteamos la vista web que lo dibuje en pantalla
    
    def mostrarArchivo(self, corregir):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "No se ha seleccionado ningún archivo.")
            return
        nombre = os.path.splitext(nombreArchivo)[0]
        rutaCompleta = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(rutaCompleta):
            self.mainWindow.m8VDP_btn.setEnabled(True)
            self.mainWindow.m1024VDP_btn.setEnabled(True)
            self.mainWindow.m16384VDP_btn.setEnabled(True)
            if corregir:
                self.corregido = True
                for i in range(1,4):
                    rutaRecuperado = os.path.join(self.carpetaArchivos, nombre + f".DC{i}")
                    if os.path.exists(rutaRecuperado):
                        print(f"hola: {os.path.basename(rutaRecuperado)}")
                        url_local = QUrl.fromLocalFile(rutaRecuperado)     # Transformamos la ruta del archivo recuperado a una URL que entienda el componente web
                        self.mainWindow.viewVDP_R.setUrl(url_local)
                        break
            else:
                self.corregido = False
                for i in range(1,4):
                    rutaRecuperado = os.path.join(self.carpetaArchivos, nombre + f".DE{i}")
                    if os.path.exists(rutaRecuperado):
                        url_local = QUrl.fromLocalFile(rutaRecuperado)     # Transformamos la ruta del archivo recuperado a una URL que entienda el componente web
                        self.mainWindow.viewVDP_R.setUrl(url_local)
                        break
    
    def mostrarDesprotegido(self, modulo):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "No se ha seleccionado ningún archivo.")
            return
        nombre = os.path.splitext(nombreArchivo)[0]
        rutaCompleta = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(rutaCompleta):
            if self.corregido:
                rutaRecuperado = os.path.join(self.carpetaArchivos, nombre + f".DC{modulo}")
                url_local = QUrl.fromLocalFile(rutaRecuperado)
                self.mainWindow.viewVDP_R.setUrl(url_local)
            else:
                rutaRecuperado = os.path.join(self.carpetaArchivos, nombre + f".DE{modulo}")
                url_local = QUrl.fromLocalFile(rutaRecuperado)
                self.mainWindow.viewVDP_R.setUrl(url_local)