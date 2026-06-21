from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
import random
import os


class InsertarErrorController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))            # Directorio Actual
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")  # Carpeta donde se guardan los archivos

        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
        try:
            self.mainWindow.tableFileIE.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)   # Para que la columna ocupe el espacio libre
            self.mainWindow.tableFileIE.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Para que se selecciones la fila completa
            self.mainWindow.tableFileIE.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Para que permita seleccionar una fila a la vez
            self.mainWindow.tableFileIE.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Para que no permita editar las celdas
            self.mainWindow.tableFileIE.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
            self.cargarTabla()          # Cargamos la tabla
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.subirArchivoIE_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.insertar1Error_btn.clicked.connect(self.insertar1Error)
        self.mainWindow.insertar2Errores_btn.clicked.connect(self.insertar2Errores)
        self.mainWindow.tableFileIE.itemClicked.connect(self.mostrarArchivo)
        

    
    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileIE.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewIE.setUrl(QUrl("about:blank"))

    def cargarTabla(self):
        if os.path.exists(self.carpetaArchivos):
            files = os.listdir(self.carpetaArchivos)
            for f in files:
                fileType = os.path.splitext(f)[1]
                if fileType in [".HA1",".HA2",".HA3"]:
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
                        rowPosition = self.mainWindow.tableFileIE.rowCount()
                        self.mainWindow.tableFileIE.insertRow(rowPosition)
                        self.mainWindow.tableFileIE.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                        self.mainWindow.tableFileIE.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño
    
    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileIE.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            nombreArchivo = self.mainWindow.tableFileIE.item(row, 0).text()
            return nombreArchivo
        return None

    def mostrarArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        ruta_completa = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(ruta_completa):
            url_local = QUrl.fromLocalFile(ruta_completa)   # Transformamos la ruta de Windows a una URL que entienda el componente web        
            self.mainWindow.viewIE.setUrl(url_local)         # Setteamos la vista web que lo dibuje en pantalla
    
    def insertar1Error(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "No se ha seleccionado ningún archivo.")
            return
        rutaFile = os.path.join(self.carpetaArchivos, nombreArchivo)
        extension = os.path.splitext(rutaFile)[1]
        if extension not in [".HA1", ".HA2", ".HA3"]:
            QMessageBox.warning(self.mainWindow, "Aviso", "El archivo seleccionado no es un archivo Hamminizado.")
            return
        try:
            with open(rutaFile, "rb") as archivo:
                contenido = archivo.read()
            datos = bytearray(contenido)
            # Definimos los tamaño de los bloques (en bytes) y sus probabilidades segun su extension
            tamañosBloques = {".HA1": 2, ".HA2": 128, ".HA3": 2048}
            probabilidades = {".HA1": 0.3, ".HA2": 0.5, ".HA3": 0.75}

            tamañoBloque = tamañosBloques[extension]        # Tamaño de bloque del archivo actual
            prob = probabilidades[extension]                # Probabilidad de error del archivo actual

            # Insertamos el error saltandonos el header con la fecha de apertura
            for i in range(19, len(datos), tamañoBloque):       # Por cada byte se analiza si se inserta un error o no
                limite = min(i + tamañoBloque, len(datos))      # Para no pasarnos del final del archivo
                if random.random() < prob:
                    # Elegimos el bit a modificar
                    byteError = random.randint(i, limite - 1)
                    bitError = random.randint(0, 7)
                    # Invertimos el bit de la posicion elegida
                    datos[byteError] ^= (1 << bitError)
            # Guardamos el nuevo archivo con el error insertado
            match extension:
                case ".HA1":
                    archivoFinal = os.path.splitext(rutaFile)[0] + ".H1E1"
                case ".HA2":
                    archivoFinal = os.path.splitext(rutaFile)[0] + ".H1E2"
                case ".HA3":
                    archivoFinal = os.path.splitext(rutaFile)[0] + ".H1E3"
            
            with open(archivoFinal, "wb") as archivoSalida:
                archivoSalida.write(datos)
            QMessageBox.information(self.mainWindow, "Éxito", f"Inserción de error completada. \nArchivo guardado como: {os.path.basename(archivoFinal)}")
            self.refrescarPanel()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo insertar el error: {str(e)}")
    
    def insertar2Errores(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "No se ha seleccionado ningún archivo.")
            return
        rutaFile = os.path.join(self.carpetaArchivos, nombreArchivo)
        extension = os.path.splitext(rutaFile)[1]
        if extension not in [".HA1", ".HA2", ".HA3"]:
            QMessageBox.warning(self.mainWindow, "Aviso", "El archivo seleccionado no es un archivo Hamminizado.")
            return
        try:
            with open(rutaFile, "rb") as archivo:
                contenido = archivo.read()
            datos = bytearray(contenido)
            # Definimos los tamaño de los bloques (en bytes) y sus probabilidades segun su extension
            tamañosBloques = {".HA1": 2, ".HA2": 128, ".HA3": 2048}
            probabilidades = {".HA1": 0.3, ".HA2": 0.5, ".HA3": 0.75}

            tamañoBloque = tamañosBloques[extension]        # Tamaño de bloque del archivo actual
            prob = probabilidades[extension]                # Probabilidad de error del archivo actual

            # Insertamos el error saltandonos el header con la fecha de apertura
            for i in range(19, len(datos), tamañoBloque):       # Por cada byte se analiza si se inserta un error o no
                limite = min(i + tamañoBloque, len(datos))      # Para no pasarnos del final del archivo
                if random.random() < prob:
                # Primer error
                    # Elegimos el bit a modificar
                    byteError1 = i
                    bitError1 = 2   # Bit de dato
                    # Invertimos el bit de la posicion elegida
                    datos[byteError1] ^= (1 << bitError1)
                # Segundo Error
                    # Elegimos el bit a modificar
                    byteError2 = i
                    bitError2 = 5   # Bit de dato
                    # Invertimos el bit de la posicion elegida
                    datos[byteError2] ^= (1 << bitError2)

            # Guardamos el nuevo archivo con el error insertado
            match extension:
                case ".HA1":
                    archivoFinal = os.path.splitext(rutaFile)[0] + ".H2E1"
                case ".HA2":
                    archivoFinal = os.path.splitext(rutaFile)[0] + ".H2E2"
                case ".HA3":
                    archivoFinal = os.path.splitext(rutaFile)[0] + ".H2E3"
            
            with open(archivoFinal, "wb") as archivoSalida:
                archivoSalida.write(datos)
            QMessageBox.information(self.mainWindow, "Éxito", f"Inserción de error completada. \nArchivo guardado como: {os.path.basename(archivoFinal)}")
            self.refrescarPanel()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo insertar el error: {str(e)}")
    