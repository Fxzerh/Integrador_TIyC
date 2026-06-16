from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
import os


class ProtegerController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))            # Directorio Actual
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")  # Carpeta donde se guardan los archivos

        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
        try:
            self.mainWindow.tableFileP.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)   # Para que la columna ocupe el espacio libre
            self.mainWindow.tableFileP.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Para que se selecciones la fila completa
            self.mainWindow.tableFileP.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Para que permita seleccionar una fila a la vez
            self.mainWindow.tableFileP.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Para que no permita editar las celdas
            self.mainWindow.tableFileP.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
            self.cargarTabla()          # Cargamos la tabla
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.subirArchivoP_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.tableFileP.itemClicked.connect(self.mostrar)
        self.mainWindow.hamming8_btn.clicked.connect(self.hamming_8)
        self.mainWindow.hamming1024_btn.clicked.connect(lambda: self.procesarHamming(1024, ".HA2"))
        self.mainWindow.hamming16384_btn.clicked.connect(lambda: self.procesarHamming(16384, ".HA3"))
        

    
    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileP.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewP.setUrl(QUrl("about:blank"))

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
                    rowPosition = self.mainWindow.tableFileP.rowCount()
                    self.mainWindow.tableFileP.insertRow(rowPosition)
                    self.mainWindow.tableFileP.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                    self.mainWindow.tableFileP.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño

    def mostrarArchivo(self, nombre_archivo):
        ruta_completa = os.path.join(self.carpetaArchivos, nombre_archivo)
        if os.path.exists(ruta_completa):
            url_local = QUrl.fromLocalFile(ruta_completa)   # Transformamos la ruta de Windows a una URL que entienda el componente web        
            self.mainWindow.viewP.setUrl(url_local)         # Setteamos la vista web que lo dibuje en pantalla

    def mostrar(self, item):
        fila = item.row()      # Obtenemos el número de la fila que el usuario tocó
        nombre = self.mainWindow.tableFileP.item(fila, 0)    # Extraemos el objeto celda de la columna 0 (Nombre) en esa fila
        nombreArchivo = nombre.text()    # Sacamos el texto plano (el nombre real del archivo)
        self.mostrarArchivo(nombreArchivo)     # Le pasamos el nombre a la función que lo carga en el visor web

    def obtenerArchivoSeleccionado(self):
        selectedRows = self.mainWindow.tableFileP.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            nombreArchivo = self.mainWindow.tableFileP.item(row, 0).text()
            return nombreArchivo
        return None
    
    def procesarHamming(self, tamanoBloqueDatos, extensionArchivo):
        self.fileSelect = self.obtenerArchivoSeleccionado()
        if not self.fileSelect:
            QMessageBox.warning(self.mainWindow, "Advertencia", "No se ha seleccionado ningún archivo.")
            return

        nombreFile = os.path.splitext(self.fileSelect)[0]
        rutaOrigen = os.path.join(self.carpetaArchivos, self.fileSelect)
        rutaDestino = os.path.join(self.carpetaArchivos, nombreFile + extensionArchivo)

        try:
            with open(rutaOrigen, 'rb') as archivo:
                contenidoBytes = archivo.read()

            # Convertimos todo el archivo a una sola cadena de bits
            cadenaBitsTotal = "".join(f"{byte:08b}" for byte in contenidoBytes)

            bitsProtegidos = ""

            # Troceamos la cadena en los bloques de datos requeridos
            for i in range(0, len(cadenaBitsTotal), tamanoBloqueDatos):
                bloqueOriginal = cadenaBitsTotal[i : i + tamanoBloqueDatos]         # Agarra los primeros "tamanoBloqueDatos" bits del string
                
                # Si el último bloque queda corto, le añadimos relleno (Padding) de ceros
                if len(bloqueOriginal) < tamanoBloqueDatos:
                    bloqueOriginal = bloqueOriginal.ljust(tamanoBloqueDatos, '0')
                    
                # Aplicamos Hamming
                bloqueProtegido = self.aplicarHamming(bloqueOriginal)
                bitsProtegidos += bloqueProtegido

            bloquesHamming = bytearray()                  # Lista vacía para almacenar bytes mutables
            for i in range(0, len(bitsProtegidos), 8):      # Separamos la cadena de bits protegidos en grupos de 8 bits (1 byte)
                unByteEnBits = bitsProtegidos[i : i + 8]
                
                # Si el final no completa 8 bits, rellenamos con ceros a la derecha
                if len(unByteEnBits) < 8:
                    unByteEnBits = unByteEnBits.ljust(8, '0')
                    
                # Convertimos los 8 bits de texto a un número entero y lo añadimos al bytearray
                bloquesHamming.append(int(unByteEnBits, 2))     # Combertimos un valor en base 2 a uno en base 10

            # Guardamos en el archivo de texto usando espacios como separadores
            with open(rutaDestino, 'wb') as archivoSalida:
                archivoSalida.write(bloquesHamming)

            QMessageBox.information(self.mainWindow, "Éxito", f"Archivo protegido correctamente.\nGuardado en '{nombreFile}{extensionArchivo}'.")
            self.refrescarPanel()

        except FileNotFoundError:
            QMessageBox.critical(self.mainWindow, "Error", "No se pudo encontrar el archivo seleccionado.")

    def hamming_8(self):
        self.fileSelect = self.obtenerArchivoSeleccionado()
        if not self.fileSelect:
            QMessageBox.warning(self.mainWindow, "Advertencia", "No se ha seleccionado ningún archivo.")
            return

        baseFile = os.path.splitext(self.fileSelect)[0]
        rutaOrigen = os.path.join(self.carpetaArchivos, self.fileSelect)
        rutaDestino = os.path.join(self.carpetaArchivos, baseFile + ".HA1")

        try:
            with open(rutaOrigen, 'rb') as archivo:
                contenidoBytes = archivo.read()

            with open(rutaDestino, 'wb') as archivoSalida:
                for byte in contenidoBytes:
                    bloqueBits = f"{byte:08b}"
                    # Dividimos el bloque de 8 bits en 2 mitades de 4 bits
                    primeraMitad = bloqueBits[0:4]
                    segundaMitad = bloqueBits[4:8]
                    # Aplicamos hamming a cada mitad
                    trama1 = self.aplicarHamming(primeraMitad)
                    trama2 = self.aplicarHamming(segundaMitad)
                    # Rellenamos las tramas con 0 a la derecha para que tengan 8 bits cada una
                    trama1 = trama1.ljust(8, '0')
                    trama2 = trama2.ljust(8, '0')
                    # Pasamos los bytes a enteros
                    primerByte = int(trama1, 2)
                    segundoByte = int(trama2, 2)
                    archivoSalida.write(bytes([primerByte, segundoByte]))

            QMessageBox.information(self.mainWindow, "Éxito", f"Archivo protegido con Hamming (mod 8) correctamente.\nGuardado en '{baseFile}.HA1'.")
            self.refrescarPanel()

        except FileNotFoundError:
            QMessageBox.critical(self.mainWindow, "Error", "No se pudo encontrar el archivo seleccionado.")
    
    def aplicarHamming(self, bitsDatos):
        longitudDatos = len(bitsDatos)
        bitsParidad = 0
        
        # Calcular cuántos bits de paridad se necesitan matemáticamente
        while (2 ** bitsParidad) < (longitudDatos + bitsParidad + 1):
            bitsParidad += 1
            
        longitudTotal = longitudDatos + bitsParidad
        trama = ['0'] * longitudTotal
        
        # Ubicamos los bits de datos saltándonos los de paridad
        indiceDatos = 0
        for i in range(longitudTotal):
            posicionReal = i + 1
            # Si NO es potencia de 2 (un bit de paridad), ponemos un bit de datos
            if (posicionReal & (posicionReal - 1)) != 0:
                trama[i] = bitsDatos[indiceDatos]
                indiceDatos += 1
                
        # Calculamos el valor XOR correcto para cada bit de paridad
        for l in range(bitsParidad):            # Recorremos cada bit de paridad
            posicionParidad = 2 ** l
            xorSuma = 0
            for i in range(longitudTotal):      # 
                posicionReal = i + 1
                # Si la posición actual participa en el calculo del bit de paridad, lo incluimos en la suma XOR
                if (posicionReal & posicionParidad) != 0 and posicionReal != posicionParidad:
                    xorSuma ^= int(trama[i])
            trama[posicionParidad - 1] = str(xorSuma)
            
        return "".join(trama)
    