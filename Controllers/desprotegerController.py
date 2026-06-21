from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView, QProgressDialog
from PyQt6.QtCore import QUrl, QThread, pyqtSignal, Qt
from Clases.cargarArchivo import Cargar
from datetime import datetime
import json
import os


class _DecodWorker(QThread):
    terminado = pyqtSignal(bytes)
    error = pyqtSignal(str)

    def __init__(self, fn, *args):
        super().__init__()
        self._fn = fn
        self._args = args

    def run(self):
        try:
            self.terminado.emit(self._fn(*self._args))
        except Exception as e:
            self.error.emit(str(e))


class DesprotegerController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))            # Directorio Actual
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")  # Carpeta donde se guardan los archivos

<<<<<<< HEAD
=======
        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
>>>>>>> parent of 3a59133 (Desproteger hecho. Probar con todos los .HA pero funciona para to2.)
        try:
            self.mainWindow.tableFileDP.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)   # Para que la columna ocupe el espacio libre
            self.mainWindow.tableFileDP.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Para que se selecciones la fila completa
            self.mainWindow.tableFileDP.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Para que permita seleccionar una fila a la vez
            self.mainWindow.tableFileDP.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Para que no permita editar las celdas
            self.mainWindow.tableFileDP.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
            self.cargarTabla()          # Cargamos la tabla
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

<<<<<<< HEAD
        self.mainWindow.subirArchivoDP_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.desprotegerArchivoSC_btn.clicked.connect(self.desprotegerSinCorregir)
        self.mainWindow.desprotegerArchivoC_btn.clicked.connect(self.desprotegerCorrigiendo)
=======
        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.subirArchivoDP_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.tableFileDP.itemClicked.connect(self.mostrarArchivo)
>>>>>>> parent of 3a59133 (Desproteger hecho. Probar con todos los .HA pero funciona para to2.)


    
    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileDP.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewDP.setUrl(QUrl("about:blank"))
    
    def cargarTabla(self):
        if os.path.exists(self.carpetaArchivos):
<<<<<<< HEAD
            for f in os.listdir(self.carpetaArchivos):
                ext = os.path.splitext(f)[1]
                ruta = os.path.join(self.carpetaArchivos, f)
                if ext in extensiones and os.path.isfile(ruta):
                    tamaño = os.path.getsize(ruta)
=======
            files = os.listdir(self.carpetaArchivos)
            for f in files:
                fileType = os.path.splitext(f)[1]
                file_path = os.path.join(self.carpetaArchivos, f)   # Ruta completa del archivo f
                if os.path.isfile(file_path):  # Pregunta si f es un archivo (y no una carpeta)
                    # Obtenemos el tamaño de f
                    tamaño = os.path.getsize(file_path)

                    # Convertir tamaño a formato B, KB o MB
>>>>>>> parent of 3a59133 (Desproteger hecho. Probar con todos los .HA pero funciona para to2.)
                    if tamaño < 1024:
                        tamaño_str = f"{tamaño} B"
                    elif tamaño < 1024 * 1024:
                        tamaño_str = f"{tamaño / 1024:.2f} KB"
                    else:
                        tamaño_str = f"{tamaño / (1024 * 1024):.2f} MB"
<<<<<<< HEAD
                    fila = self.mainWindow.tableFileDP.rowCount()
                    self.mainWindow.tableFileDP.insertRow(fila)
                    self.mainWindow.tableFileDP.setItem(fila, 0, QTableWidgetItem(f))
                    self.mainWindow.tableFileDP.setItem(fila, 1, QTableWidgetItem(tamaño_str))

    def obtenerSeleccionado(self):
        filas = self.mainWindow.tableFileDP.selectionModel().selectedRows()
        if filas:
            return self.mainWindow.tableFileDP.item(filas[0].row(), 0).text()
        return None

    def _verificarFechaApertura(self, datos):
        try:
            fechaTexto = datos[:19].decode('utf-8')
            fechaApertura = datetime.strptime(fechaTexto, "%Y-%m-%d %H:%M:%S")
            return datetime.now() <= fechaApertura, fechaTexto
        except Exception:
            return False, ""

    def _iniciarWorker(self, fn, args, ruta, extension, corregido):
        self._progreso = QProgressDialog("Desprotegiendo archivo...", None, 0, 0, self.mainWindow)
        self._progreso.setWindowTitle("Procesando")
        self._progreso.setWindowModality(Qt.WindowModality.WindowModal)
        self._progreso.setMinimumDuration(0)
        self._progreso.setValue(0)
        self._progreso.show()

        self._worker = _DecodWorker(fn, *args)
        self._worker.terminado.connect(lambda res: self._alTerminar(res, ruta, extension, corregido))
        self._worker.error.connect(self._alError)
        self._worker.start()

    def _alTerminar(self, resultado, ruta, extension, corregido):
        self._progreso.close()
        try:
            rutaMostrar = self._guardarDecodificado(ruta, extension, resultado, corregido=corregido)
            self.mainWindow.viewDP.setUrl(QUrl.fromLocalFile(rutaMostrar))
            QMessageBox.information(self.mainWindow, "Listo", "Desprotección realizada.")
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo guardar el archivo: {str(e)}")

    def _alError(self, msg):
        self._progreso.close()
        QMessageBox.critical(self.mainWindow, "Error", f"No se pudo decodificar el archivo: {msg}")

    def desprotegerSinCorregir(self):
        nombre = self.obtenerSeleccionado()
        if not nombre:
            QMessageBox.warning(self.mainWindow, "Aviso", "Seleccione un archivo de la tabla.")
            return
        ruta = os.path.join(self.carpetaArchivos, nombre)
        extension = os.path.splitext(ruta)[1]
        try:
            with open(ruta, "rb") as f:
                datos = f.read()
            permitido, fechaTexto = self._verificarFechaApertura(datos)
            if not permitido:
                QMessageBox.warning(self.mainWindow, "Bloqueado", "La fecha de ingreso ya se pasó.")
                return
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo leer el archivo: {str(e)}")
            return
        if extension in (".HA1", ".HE1", ".H1E1", ".H2E1"):
            self._iniciarWorker(self._decodificarBytesHA1SinCorregir, (datos,), ruta, extension, False)
        else:
            self._iniciarWorker(self._decodificarBytesHA2_3SinCorregir, (datos, extension), ruta, extension, False)

    def desprotegerCorrigiendo(self):
        nombre = self.obtenerSeleccionado()
        if not nombre:
            QMessageBox.warning(self.mainWindow, "Aviso", "Seleccione un archivo de la tabla.")
            return
        ruta = os.path.join(self.carpetaArchivos, nombre)
        extension = os.path.splitext(ruta)[1]
        if extension in (".H2E1", ".H2E2", ".H2E3"):
            QMessageBox.warning(self.mainWindow, "Aviso", "Tiene 2 o más errores, no puede ser arreglado.")
            return
        try:
            with open(ruta, "rb") as f:
                datos = f.read()
            permitido, fechaTexto = self._verificarFechaApertura(datos)
            if not permitido:
                QMessageBox.warning(self.mainWindow, "Bloqueado", "La fecha de ingreso ya se pasó.")
                return
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo leer el archivo: {str(e)}")
            return
        if extension in (".HA1", ".HE1", ".H1E1"):
            self._iniciarWorker(self._decodificarBytesHA1Corregido, (datos,), ruta, extension, True)
        else:
            self._iniciarWorker(self._decodificarBytesHA2_3Corregido, (datos, extension), ruta, extension, True)

    def _guardarDecodificado(self, ruta, extension, datos, corregido):
        tieneError = extension in (".H1E1", ".H2E1", ".H1E2", ".H2E2", ".H1E3", ".H2E3")
        if tieneError:
            base = ruta
            baseContenido = os.path.splitext(ruta)[0]
        else:
            base = os.path.splitext(ruta)[0]
            baseContenido = base

        sufijo = "DC" if corregido else "DE"
        match extension:
            case ".HA1" | ".HE1" | ".H1E1" | ".H2E1":
                numero = "1"
            case ".HA2" | ".HE2" | ".H1E2" | ".H2E2":
                numero = "2"
            case _:
                numero = "3"
        archivoMarca = base + f".{sufijo}{numero}"

        extensiones_conocidas = {".pdf", ".png", ".jpg", ".zip", ".txt", ".huf"}
        _, extBase = os.path.splitext(baseContenido)
        if extBase in extensiones_conocidas:
            archivoContenido = baseContenido
        else:
            archivoContenido = baseContenido + self.detectarExtension(datos)

        if not os.path.exists(archivoMarca):
            with open(archivoContenido, "wb") as f:
                f.write(datos)
            with open(archivoMarca, "wb") as f:
                f.write(datos)

        return archivoContenido

    # ---- Decodificadores Hamming en memoria ----

    def _decodificarBytesHA1SinCorregir(self, datos):
        TAM_CABECERA = 19
        payload = datos[TAM_CABECERA:]
        resultado = bytearray()
        for c in range(0, len(payload) - 1, 2):
            bloque = f"{payload[c]:08b}{payload[c+1]:08b}"
            resultado.append(int(self.sacarParidad8(bloque), 2))
        return bytes(resultado)

    def _decodificarBytesHA1Corregido(self, datos):
        TAM_CABECERA = 19
        payload = datos[TAM_CABECERA:]
        resultado = bytearray()
        for c in range(0, len(payload) - 1, 2):
            bloque = f"{payload[c]:08b}{payload[c+1]:08b}"
            corregido = self.hamming_ver8(bloque)
            resultado.append(int(self.sacarParidad8(corregido), 2))
        return bytes(resultado)

    def _decodificarBytesHA2_3SinCorregir(self, datos, extHamming):
        TAM_CABECERA = 19
        tamBloque = 1024 if extHamming in (".HA2", ".HE2", ".H1E2", ".H2E2") else 16384
        bits = "".join(f"{b:08b}" for b in datos[TAM_CABECERA:])
        l1 = ""
        for c in range(0, len(bits), tamBloque):
            bloque = bits[c:c + tamBloque]
            if len(bloque) < tamBloque:
                break
            l1 += self.sacarParidad(bloque)
        return bytes(int(l1[k:k+8], 2) for k in range(0, len(l1) - len(l1) % 8, 8))

    def _decodificarBytesHA2_3Corregido(self, datos, extHamming):
        TAM_CABECERA = 19
        tamBloque = 1024 if extHamming in (".HA2", ".HE2", ".H1E2", ".H2E2") else 16384
        bits = "".join(f"{b:08b}" for b in datos[TAM_CABECERA:])
        l1 = ""
        for c in range(0, len(bits), tamBloque):
            bloque = bits[c:c + tamBloque]
            if len(bloque) < tamBloque:
                break
            sindrome = self.calcularSindrome(bloque)
            if 0 < sindrome <= len(bloque):
                lst = list(bloque)
                lst[sindrome - 1] = '0' if lst[sindrome - 1] == '1' else '1'
                bloque = ''.join(lst)
            l1 += self.sacarParidad(bloque)
        return bytes(int(l1[k:k+8], 2) for k in range(0, len(l1) - len(l1) % 8, 8))

    # ---- Detección de tipo de archivo ----

    def _esHuffman(self, datos):
        try:
            if len(datos) < 6:
                return False
            padding = datos[0]
            if padding > 7:
                return False
            longDic = int.from_bytes(datos[1:5], byteorder='big')
            if longDic <= 0 or 5 + longDic > len(datos):
                return False
            json.loads(datos[5:5 + longDic].decode())
            return True
        except Exception:
            return False

    def detectarExtension(self, datos):
        if datos[:4] == b'%PDF':
            return '.pdf'
        if datos[:8] == b'\x89PNG\r\n\x1a\n':
            return '.png'
        if datos[:2] == b'\xff\xd8':
            return '.jpg'
        if datos[:4] in (b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08'):
            return '.zip'
        if self._esHuffman(datos):
            return '.huf'
        try:
            datos[:512].decode('utf-8')
            return '.txt'
        except (UnicodeDecodeError, ValueError):
            return '.bin'

    # ---- Funciones auxiliares de Hamming ----

    def sacarParidad(self, l):
        j = 0
        x = ""
        for s in range(len(l)):
            if 2 ** j == s + 1:
                j += 1
            else:
                x += l[s]
        return x

    def sacarParidad8(self, l):
        j = 0
        x = ""
        x1 = ""
        y = l[0:8]
        y1 = l[8:16]
        for i in range(8):
            if 2 ** j == i + 1:
                j += 1
            else:
                x += y[i]
                x1 += y1[i]
        x += x1
        return x

    def calcularSindrome(self, bloque):
        n = len(bloque)
        sindrome = 0
        potencia = 1
        while potencia <= n:
            paridad = 0
            pos = potencia - 1
            while pos < n:
                for j in range(pos, min(pos + potencia, n)):
                    paridad ^= int(bloque[j])
                pos += 2 * potencia
            if paridad:
                sindrome |= potencia
            potencia <<= 1
        return sindrome

    def hamming_ver8(self, n1):
        j = 0
        x = ""
        x1 = ""
        y_bloque = n1[0:8]
        y1_bloque = n1[8:16]
        for i in range(8):
            if 2 ** j == i + 1:
                j += 1
            else:
                x += y_bloque[i]
                x1 += y1_bloque[i]
        x += x1
        l = self.hamminization(x)
        if l != n1:
            listapp = list(n1)
            if l[0:8] != y_bloque:
                i = 1
                y_sin = ""
                z_sin = ""
                j = 0
                while i <= 4:
                    y_sin += y_bloque[i - 1]
                    z_sin += l[0:8][i - 1]
                    j += 1
                    i = 2 ** j
                xy = "".join(str(int(y_sin[k]) ^ int(z_sin[k])) for k in range(len(y_sin)))
                xy_r = int(xy[::-1], 2)
                if 0 < xy_r <= 7:
                    listapp[xy_r - 1] = '1' if listapp[xy_r - 1] == '0' else '0'
            if l[8:16] != y1_bloque:
                i = 1
                y_sin = ""
                z_sin = ""
                j = 0
                while i <= 4:
                    y_sin += y1_bloque[i - 1]
                    z_sin += l[8:16][i - 1]
                    j += 1
                    i = 2 ** j
                xy = "".join(str(int(y_sin[k]) ^ int(z_sin[k])) for k in range(len(y_sin)))
                xy_r = int(xy[::-1], 2)
                if 0 < xy_r <= 7:
                    listapp[8 + xy_r - 1] = '1' if listapp[8 + xy_r - 1] == '0' else '0'
            return "".join(listapp)
        return n1

    def hamminization(self, n1):
        long = len(n1)
        p = 0
        while 2 ** p < len(n1) + p + 1:
            p += 1
        trama1 = ['0'] * long
        trama = ['0'] * long
        j = 0
        for i in range(1, long):
            if (i & (i - 1)) != 0:
                trama[i - 1] = n1[j]
                j += 1
        for i in range(1, long):
            if (i & (i - 1)) != 0:
                trama1[i - 1] = n1[j]
                j += 1
        l = 0
        for l in range(p):
            i = 2 ** l
            s = 0
            s1 = 0
            for cont1 in range(long):
                posicion_real = cont1 + 1
                if (posicion_real & i) != 0 and posicion_real != i:
                    s ^= int(trama[cont1])
                    s1 ^= int(trama1[cont1])
            trama[i - 1] = str(s)
            trama1[i - 1] = str(s1)
        s = 0
        s1 = 0
        while l < len(trama):
            s += int(trama[l])
            s1 += int(trama1[l])
            l += 1
        trama[-1] = "1" if s % 2 == 0 else "0"
        trama1[-1] = "1" if s1 % 2 == 0 else "0"
        return "".join(trama) + "".join(trama1)
=======
                    
                    # Agregamos el archivo a la tabla
                    rowPosition = self.mainWindow.tableFileDP.rowCount()
                    self.mainWindow.tableFileDP.insertRow(rowPosition)
                    self.mainWindow.tableFileDP.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                    self.mainWindow.tableFileDP.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño

    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileDP.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            nombreArchivo = self.mainWindow.tableFileDP.item(row, 0).text()
            return nombreArchivo
        return None

    def mostrarArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        ruta_completa = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(ruta_completa):
            url_local = QUrl.fromLocalFile(ruta_completa)   # Transformamos la ruta de Windows a una URL que entienda el componente web        
            self.mainWindow.viewDP.setUrl(url_local)         # Setteamos la vista web que lo dibuje en pantalla

>>>>>>> parent of 3a59133 (Desproteger hecho. Probar con todos los .HA pero funciona para to2.)
