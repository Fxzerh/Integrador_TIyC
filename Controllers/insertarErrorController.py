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
            TAM_CABECERA = 19
            probabilidades = {".HA1": 0.3, ".HA2": 0.5, ".HA3": 0.75}
            prob = probabilidades[extension]

            if extension == ".HA1":
                # HA1: grupos de 2 bytes Hamming por byte original, byte-alineados
                for i in range(TAM_CABECERA, len(datos), 2):
                    if i + 2 > len(datos):
                        break
                    if random.random() < prob:
                        byteError = random.randint(i, i + 1)
                        bitError = random.randint(0, 7)
                        datos[byteError] ^= (1 << bitError)
            else:
                # HA2/HA3: los bloques Hamming son 1035/16399 bits, no múltiplos de 8.
                # Hay que operar a nivel de bit para no cruzar fronteras de bloque.
                tamBloquesBits = {".HA2": 1035, ".HA3": 16399}
                tam_bloque_bits = tamBloquesBits[extension]
                bit_total = (len(datos) - TAM_CABECERA) * 8
                num_bloques = bit_total // tam_bloque_bits
                for h in range(num_bloques):
                    if random.random() < prob:
                        bit_en_bloque = random.randint(0, tam_bloque_bits - 1)
                        bit_abs = h * tam_bloque_bits + bit_en_bloque
                        byte_pos = TAM_CABECERA + bit_abs // 8
                        bit_en_byte = 7 - (bit_abs % 8)  # f"{byte:08b}" pone el MSB primero
                        datos[byte_pos] ^= (1 << bit_en_byte)

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
            TAM_CABECERA = 19
            probabilidades = {".HA1": 0.3, ".HA2": 0.5, ".HA3": 0.75}
            prob = probabilidades[extension]

            if extension == ".HA1":
                for i in range(TAM_CABECERA, len(datos), 2):
                    if i + 2 > len(datos):
                        break
                    if random.random() < prob:
                        datos[i] ^= (1 << 2)
                        datos[i] ^= (1 << 5)
            else:
                tamBloquesBits = {".HA2": 1035, ".HA3": 16399}
                tam_bloque_bits = tamBloquesBits[extension]
                bit_total = (len(datos) - TAM_CABECERA) * 8
                num_bloques = bit_total // tam_bloque_bits
                for h in range(num_bloques):
                    if random.random() < prob:
                        # Dos posiciones distintas dentro del bloque
                        pos1 = random.randint(0, tam_bloque_bits - 1)
                        pos2 = random.randint(0, tam_bloque_bits - 2)
                        if pos2 >= pos1:
                            pos2 += 1
                        for bit_en_bloque in (pos1, pos2):
                            bit_abs = h * tam_bloque_bits + bit_en_bloque
                            byte_pos = TAM_CABECERA + bit_abs // 8
                            bit_en_byte = 7 - (bit_abs % 8)
                            datos[byte_pos] ^= (1 << bit_en_byte)

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
    