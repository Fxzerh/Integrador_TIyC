from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl, QTimer
from Clases.cargarArchivo import Cargar
from datetime import datetime
import json
import os


EXTENSIONES_VISIBLES = {'.dhu', '.DC1', '.DC2', '.DC3', '.DE1', '.DE2', '.DE3'}


class VerDCController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")
        self._temp_arriba = None
        self._temp_abajo = None

        try:
            self.mainWindow.tableFileVDC.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.mainWindow.tableFileVDC.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.mainWindow.tableFileVDC.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            self.mainWindow.tableFileVDC.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.mainWindow.tableFileVDC.setRowCount(0)
            self.cargarTabla()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        self.mainWindow.tableFileVDC.itemClicked.connect(self.mostrarArchivo)

    def cambiarPanel(self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileVDC.setRowCount(0)
        self.cargarTabla()
        self._limpiarTemps()

    def _limpiarTemps(self):
        self.mainWindow.viewVDC_O.setUrl(QUrl("about:blank"))
        self.mainWindow.viewVDC_R.setUrl(QUrl("about:blank"))
        archivos = [r for r in (self._temp_arriba, self._temp_abajo) if r]
        self._temp_arriba = None
        self._temp_abajo = None
        if archivos:
            QTimer.singleShot(300, lambda: self._borrarArchivos(archivos))

    def _borrarArchivos(self, rutas):
        for ruta in rutas:
            try:
                if os.path.exists(ruta):
                    os.remove(ruta)
            except OSError:
                pass

    def cargarTabla(self):
        if os.path.exists(self.carpetaArchivos):
            for f in sorted(os.listdir(self.carpetaArchivos)):
                ext = os.path.splitext(f)[1]
                ruta = os.path.join(self.carpetaArchivos, f)
                if os.path.isfile(ruta) and ext in EXTENSIONES_VISIBLES:
                    tamaño = os.path.getsize(ruta)
                    if tamaño < 1024:
                        tamaño_str = f"{tamaño} B"
                    elif tamaño < 1024 * 1024:
                        tamaño_str = f"{tamaño / 1024:.2f} KB"
                    else:
                        tamaño_str = f"{tamaño / (1024 * 1024):.2f} MB"
                    fila = self.mainWindow.tableFileVDC.rowCount()
                    self.mainWindow.tableFileVDC.insertRow(fila)
                    self.mainWindow.tableFileVDC.setItem(fila, 0, QTableWidgetItem(f))
                    self.mainWindow.tableFileVDC.setItem(fila, 1, QTableWidgetItem(tamaño_str))

    def obtenerSeleccionado(self):
        filas = self.mainWindow.tableFileVDC.selectionModel().selectedRows()
        if filas:
            return self.mainWindow.tableFileVDC.item(filas[0].row(), 0).text()
        return None

    def _verificarFechaApertura(self, datos):
        try:
            fechaTexto = datos[:19].decode('utf-8')
            fechaApertura = datetime.strptime(fechaTexto, "%Y-%m-%d %H:%M:%S")
            return datetime.now().date() == fechaApertura.date(), fechaTexto
        except Exception:
            return False, ""

    def mostrarArchivo(self):
        nombre = self.obtenerSeleccionado()
        if not nombre:
            return
        marcador = os.path.splitext(nombre)[1]
        self._limpiarTemps()

        # Archivos Huffman descomprimidos: solo mostrar en panel inferior
        if marcador == '.dhu':
            ruta = os.path.join(self.carpetaArchivos, nombre)
            if os.path.exists(ruta):
                self.mainWindow.viewVDC_R.setUrl(QUrl.fromLocalFile(ruta))
            return

        # Archivos .DC* o .DE*: buscar el archivo Hamming original
        rutaHamming = os.path.join(self.carpetaArchivos, os.path.splitext(nombre)[0])
        if not os.path.exists(rutaHamming):
            QMessageBox.warning(self.mainWindow, "Aviso",
                "No se encontró el archivo Hamming original para este registro.")
            return

        extHamming = os.path.splitext(rutaHamming)[1]
        try:
            with open(rutaHamming, "rb") as f:
                datosHamming = f.read()

            permitido, fechaTexto = self._verificarFechaApertura(datosHamming)
            if not permitido:
                QMessageBox.warning(self.mainWindow, "Bloqueado",
                    f"Este archivo solo puede verse el {fechaTexto}.\n"
                    "Antes o después de esa fecha no es posible decodificarlo.")
                return

            # Panel superior: siempre decodificado sin corregir errores
            if extHamming in (".HA1", ".HE1", ".H1E1", ".H2E1"):
                sinCorregir = self._decodificarBytesHA1SinCorregir(datosHamming)
            else:
                sinCorregir = self._decodificarBytesHA2_3SinCorregir(datosHamming, extHamming)

            tipoArriba = self.detectarExtension(sinCorregir)
            tempArriba = os.path.join(self.carpetaArchivos, "_vdc_arriba" + tipoArriba)
            with open(tempArriba, "wb") as f:
                f.write(sinCorregir)
            self._temp_arriba = tempArriba
            self.mainWindow.viewVDC_O.setUrl(QUrl.fromLocalFile(tempArriba))

            # Panel inferior
            if extHamming in (".H2E1", ".H2E2", ".H2E3"):
                # 2 errores: no se puede corregir, mostrar igual que arriba
                QMessageBox.warning(self.mainWindow, "Aviso", "Tiene 2 o más errores, no puede ser arreglado.")
                tempAbajo = os.path.join(self.carpetaArchivos, "_vdc_abajo" + tipoArriba)
                with open(tempAbajo, "wb") as f:
                    f.write(sinCorregir)
                self._temp_abajo = tempAbajo
                self.mainWindow.viewVDC_R.setUrl(QUrl.fromLocalFile(tempAbajo))
            elif marcador.startswith('.DC'):
                # Archivo con corrección: panel inferior muestra con error corregido
                if extHamming in (".HA1", ".HE1", ".H1E1"):
                    corregido = self._decodificarBytesHA1Corregido(datosHamming)
                else:
                    corregido = self._decodificarBytesHA2_3Corregido(datosHamming, extHamming)
                tipoAbajo = self.detectarExtension(corregido)
                tempAbajo = os.path.join(self.carpetaArchivos, "_vdc_abajo" + tipoAbajo)
                with open(tempAbajo, "wb") as f:
                    f.write(corregido)
                self._temp_abajo = tempAbajo
                self.mainWindow.viewVDC_R.setUrl(QUrl.fromLocalFile(tempAbajo))
            else:
                # Archivo .DE: sin corrección en ambos paneles
                tempAbajo = os.path.join(self.carpetaArchivos, "_vdc_abajo" + tipoArriba)
                with open(tempAbajo, "wb") as f:
                    f.write(sinCorregir)
                self._temp_abajo = tempAbajo
                self.mainWindow.viewVDC_R.setUrl(QUrl.fromLocalFile(tempAbajo))

        except Exception:
            self._limpiarTemps()

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

    def _decodificarBytesHA2_3SinCorregir(self, datos, extension):
        TAM_CABECERA = 19
        tamBloque = 1035 if extension in (".HA2", ".HE2", ".H1E2", ".H2E2") else 16399
        bits = "".join(f"{b:08b}" for b in datos[TAM_CABECERA:])
        l1 = ""
        for c in range(0, len(bits), tamBloque):
            bloque = bits[c:c + tamBloque]
            if len(bloque) < tamBloque:
                break
            l1 += self.sacarParidad(bloque)
        return bytes(int(l1[k:k+8], 2) for k in range(0, len(l1) - len(l1) % 8, 8))

    def _decodificarBytesHA2_3Corregido(self, datos, extension):
        TAM_CABECERA = 19
        tamBloque = 1035 if extension in (".HA2", ".HE2", ".H1E2", ".H2E2") else 16399
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
                    listapp[xy_r - 1] = '1' if listapp[xy_r - 1] == '0' else '1'
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
                    listapp[8 + xy_r - 1] = '1' if listapp[8 + xy_r - 1] == '0' else '1'
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
