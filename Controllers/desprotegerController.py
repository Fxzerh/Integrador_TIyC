from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
from datetime import datetime
import json
import os


class DesprotegerController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")

        try:
            self.mainWindow.tableFileDP.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.mainWindow.tableFileDP.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.mainWindow.tableFileDP.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            self.mainWindow.tableFileDP.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.mainWindow.tableFileDP.setRowCount(0)
            self.cargarTabla()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        self.mainWindow.subirArchivoDP_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.desprotegerArchivoSC_btn.clicked.connect(self.desprotegerSinCorregir)
        self.mainWindow.desprotegerArchivoC_btn.clicked.connect(self.desprotegerCorrigiendo)

    def cambiarPanel(self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileDP.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewDP.setUrl(QUrl("about:blank"))

    def cargarTabla(self):
        extensiones = {".HA1", ".HA2", ".HA3", ".HE1", ".HE2", ".HE3",
                       ".H1E1", ".H1E2", ".H1E3", ".H2E1", ".H2E2", ".H2E3"}
        if os.path.exists(self.carpetaArchivos):
            for f in os.listdir(self.carpetaArchivos):
                ext = os.path.splitext(f)[1]
                ruta = os.path.join(self.carpetaArchivos, f)
                if ext in extensiones and os.path.isfile(ruta):
                    tamaño = os.path.getsize(ruta)
                    if tamaño < 1024:
                        tamaño_str = f"{tamaño} B"
                    elif tamaño < 1024 * 1024:
                        tamaño_str = f"{tamaño / 1024:.2f} KB"
                    else:
                        tamaño_str = f"{tamaño / (1024 * 1024):.2f} MB"
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
            return datetime.now().date() == fechaApertura.date(), fechaTexto
        except Exception:
            return False, ""

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
                QMessageBox.warning(self.mainWindow, "Bloqueado",
                    f"Este archivo no se puede decodificar hasta el {fechaTexto}.")
                return
            if extension in (".HA1", ".HE1", ".H1E1", ".H2E1"):
                resultado = self._decodificarBytesHA1SinCorregir(datos)
            else:
                resultado = self._decodificarBytesHA2_3SinCorregir(datos, extension)
            rutaMostrar = self._guardarDecodificado(ruta, extension, resultado, corregido=False)
            self.mainWindow.viewDP.setUrl(QUrl.fromLocalFile(rutaMostrar))
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo decodificar el archivo: {str(e)}")

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
                QMessageBox.warning(self.mainWindow, "Bloqueado",
                    f"Este archivo no se puede decodificar hasta el {fechaTexto}.")
                return
            if extension in (".HA1", ".HE1", ".H1E1"):
                resultado = self._decodificarBytesHA1Corregido(datos)
            else:
                resultado = self._decodificarBytesHA2_3Corregido(datos, extension)
            rutaMostrar = self._guardarDecodificado(ruta, extension, resultado, corregido=True)
            self.mainWindow.viewDP.setUrl(QUrl.fromLocalFile(rutaMostrar))
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo decodificar el archivo: {str(e)}")

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
        tamBloque = 1035 if extHamming in (".HA2", ".HE2", ".H1E2", ".H2E2") else 16399
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
        tamBloque = 1035 if extHamming in (".HA2", ".HE2", ".H1E2", ".H2E2") else 16399
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
