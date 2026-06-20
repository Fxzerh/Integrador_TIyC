from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl, QTimer
from Clases.cargarArchivo import Cargar
import os


class DesprotegerController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")
        self._temp_arriba = None
        self._temp_abajo = None

        # ---------- SETEOS INICIALES
        try:
            self.mainWindow.tableFileDP.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.mainWindow.tableFileDP.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.mainWindow.tableFileDP.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            self.mainWindow.tableFileDP.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.mainWindow.tableFileDP.setRowCount(0)
            self.cargarTabla()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------- ACCIONES Y EVENTOS
        self.mainWindow.subirArchivoDP_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.tableFileDP.itemClicked.connect(self.mostrarArchivo)
        self.mainWindow.desprotegerArchivoSC_btn.clicked.connect(self.desprotegerSinCorregir)
        self.mainWindow.desprotegerArchivoC_btn.clicked.connect(self.desprotegerCorrigiendo)

    def cambiarPanel(self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileDP.setRowCount(0)
        self.cargarTabla()
        self._limpiarTemps()

    def _limpiarTemps(self):
        self.mainWindow.viewDP.setUrl(QUrl("about:blank"))
        self.mainWindow.viewDP_R.setUrl(QUrl("about:blank"))
        archivos = [r for r in (self._temp_arriba, self._temp_abajo) if r]
        self._temp_arriba = None
        self._temp_abajo = None
        if archivos:
            # Delay para que el motor web libere el handle antes de borrar (necesario en Windows)
            QTimer.singleShot(300, lambda: self._borrarArchivos(archivos))

    def _borrarArchivos(self, rutas):
        for ruta in rutas:
            try:
                if os.path.exists(ruta):
                    os.remove(ruta)
            except OSError:
                pass

    def cargarTabla(self):
        extensiones = {".HA1", ".HA2", ".HA3", ".HE1", ".HE2", ".HE3",
                       ".H1E1", ".H1E2", ".H1E3", ".H2E1", ".H2E2", ".H2E3"}
        if os.path.exists(self.carpetaArchivos):
            for f in os.listdir(self.carpetaArchivos):
                ext = os.path.splitext(f)[1]
                file_path = os.path.join(self.carpetaArchivos, f)
                if ext in extensiones and os.path.isfile(file_path):
                    tamaño = os.path.getsize(file_path)
                    if tamaño < 1024:
                        tamaño_str = f"{tamaño} B"
                    elif tamaño < 1024 * 1024:
                        tamaño_str = f"{tamaño / 1024:.2f} KB"
                    else:
                        tamaño_str = f"{tamaño / (1024 * 1024):.2f} MB"

                    rowPosition = self.mainWindow.tableFileDP.rowCount()
                    self.mainWindow.tableFileDP.insertRow(rowPosition)
                    self.mainWindow.tableFileDP.setItem(rowPosition, 0, QTableWidgetItem(f))
                    self.mainWindow.tableFileDP.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))

    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileDP.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            return self.mainWindow.tableFileDP.item(row, 0).text()
        return None

    def mostrarArchivo(self):
        nombre = self.obtenerSeleccionado()
        if not nombre:
            return
        ruta = os.path.join(self.carpetaArchivos, nombre)
        if not os.path.exists(ruta):
            return
        extension = os.path.splitext(ruta)[1]
        self._limpiarTemps()  # borra los temporales anteriores antes de crear los nuevos
        try:
            # Panel superior: decodificado sin tocar errores
            if extension in (".HA1", ".HE1", ".H1E1", ".H2E1"):
                sinCorregir = self._decodificarHA1SinCorregir(ruta)
            else:
                sinCorregir = self._decodificarHA2_3SinCorregir(ruta)

            tipoArchivo = self.detectarExtension(sinCorregir)
            previoArriba = os.path.join(self.carpetaArchivos, "_previo_arriba" + tipoArchivo)
            with open(previoArriba, "wb") as f:
                f.write(sinCorregir)
            self._temp_arriba = previoArriba
            self.mainWindow.viewDP.setUrl(QUrl.fromLocalFile(previoArriba))

            # Panel inferior: corregido si se puede, si no popup y muestra igual con errores
            if extension in (".H2E1", ".H2E2", ".H2E3"):
                QMessageBox.warning(self.mainWindow, "Aviso", "Tiene 2 o más errores, no puede ser arreglado")
                previoAbajo = os.path.join(self.carpetaArchivos, "_previo_abajo" + tipoArchivo)
                with open(previoAbajo, "wb") as f:
                    f.write(sinCorregir)
                self._temp_abajo = previoAbajo
                self.mainWindow.viewDP_R.setUrl(QUrl.fromLocalFile(previoAbajo))
            else:
                if extension in (".HA1", ".HE1", ".H1E1"):
                    corregido = self._decodificarHA1Corregido(ruta)
                else:
                    corregido = self._decodificarHA2_3Corregido(ruta)

                tipoArchivoCorregido = self.detectarExtension(corregido)
                previoAbajo = os.path.join(self.carpetaArchivos, "_previo_abajo" + tipoArchivoCorregido)
                with open(previoAbajo, "wb") as f:
                    f.write(corregido)
                self._temp_abajo = previoAbajo
                self.mainWindow.viewDP_R.setUrl(QUrl.fromLocalFile(previoAbajo))
        except Exception:
            self._limpiarTemps()

    def _decodificarSinCorregir(self, rutaFile):
        ext = os.path.splitext(rutaFile)[1]
        if ext in (".H2E1",):
            return self._decodificarHA1SinCorregir(rutaFile)
        else:
            return self._decodificarHA2_3SinCorregir(rutaFile)

    def _decodificarHA1SinCorregir(self, rutaFile):
        TAM_CABECERA = 19
        with open(rutaFile, "rb") as f:
            datos = f.read()
        payload = datos[TAM_CABECERA:]  # cabecera escrita una sola vez al inicio
        resultado = bytearray()
        for c in range(0, len(payload) - 1, 2):
            bloque = f"{payload[c]:08b}{payload[c+1]:08b}"
            resultado.append(int(self.sacarParidad8(bloque), 2))
        return bytes(resultado)

    def _decodificarHA1Corregido(self, rutaFile):
        TAM_CABECERA = 19
        with open(rutaFile, "rb") as f:
            datos = f.read()
        payload = datos[TAM_CABECERA:]  # cabecera escrita una sola vez al inicio
        resultado = bytearray()
        for c in range(0, len(payload) - 1, 2):
            bloque = f"{payload[c]:08b}{payload[c+1]:08b}"
            corregido = self.hamming_ver8(bloque)
            resultado.append(int(self.sacarParidad8(corregido), 2))
        return bytes(resultado)

    def _decodificarHA2_3SinCorregir(self, rutaFile):
        TAM_CABECERA = 19
        ext = os.path.splitext(rutaFile)[1]
        tam_bloque = 1035 if ext in (".HA2", ".HE2", ".H1E2", ".H2E2") else 16399
        with open(rutaFile, "rb") as f:
            datos = f.read()
        bits = "".join(f"{b:08b}" for b in datos[TAM_CABECERA:])
        l1 = ""
        for c in range(0, len(bits), tam_bloque):
            bloque = bits[c:c + tam_bloque]
            if len(bloque) < tam_bloque:
                break
            l1 += self.sacarParidad(bloque)
        return bytes(int(l1[k:k+8], 2) for k in range(0, len(l1) - len(l1) % 8, 8))

    def _decodificarHA2_3Corregido(self, rutaFile):
        TAM_CABECERA = 19
        ext = os.path.splitext(rutaFile)[1]
        tam_bloque = 1035 if ext in (".HA2", ".HE2", ".H1E2", ".H2E2") else 16399
        with open(rutaFile, "rb") as f:
            datos = f.read()
        bits = "".join(f"{b:08b}" for b in datos[TAM_CABECERA:])
        l1 = ""
        for c in range(0, len(bits), tam_bloque):
            bloque = bits[c:c + tam_bloque]
            if len(bloque) < tam_bloque:
                break
            sindrome = self.calcularSindrome(bloque)
            if 0 < sindrome <= len(bloque):
                lst = list(bloque)
                lst[sindrome - 1] = '0' if lst[sindrome - 1] == '1' else '1'
                bloque = ''.join(lst)
            l1 += self.sacarParidad(bloque)
        return bytes(int(l1[k:k+8], 2) for k in range(0, len(l1) - len(l1) % 8, 8))

    def desprotegerSinCorregir(self):
        nombre = self.obtenerSeleccionado()
        if not nombre:
            QMessageBox.warning(self.mainWindow, "Aviso", "Seleccione un archivo de la tabla.")
            return
        ruta = os.path.join(self.carpetaArchivos, nombre)
        extension = os.path.splitext(ruta)[1]
        try:
            if extension in (".HA1", ".HE1", ".H1E1", ".H2E1"):
                resultado = self._decodificarHA1SinCorregir(ruta)
            else:
                resultado = self._decodificarHA2_3SinCorregir(ruta)
            self._guardarDecodificado(ruta, extension, resultado, corregido=False)
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo guardar el archivo: {str(e)}")

    def desprotegerCorrigiendo(self):
        nombre = self.obtenerSeleccionado()
        if not nombre:
            QMessageBox.warning(self.mainWindow, "Aviso", "Seleccione un archivo de la tabla.")
            return
        ruta = os.path.join(self.carpetaArchivos, nombre)
        extension = os.path.splitext(ruta)[1]
        if extension in (".H2E1", ".H2E2", ".H2E3"):
            QMessageBox.warning(self.mainWindow, "Aviso", "Tiene 2 o más errores, no puede ser arreglado")
            return
        try:
            if extension in (".HA1", ".HE1", ".H1E1"):
                resultado = self._decodificarHA1Corregido(ruta)
            else:
                resultado = self._decodificarHA2_3Corregido(ruta)
            self._guardarDecodificado(ruta, extension, resultado, corregido=True)
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo guardar el archivo: {str(e)}")

    def _guardarDecodificado(self, ruta, extension, datos, corregido):
        tieneError = extension in (".H1E1", ".H2E1", ".H1E2", ".H2E2", ".H1E3", ".H2E3")
        base = ruta if tieneError else os.path.splitext(ruta)[0]
        sufijo = "DC" if corregido else "DE"
        match extension:
            case ".HA1" | ".HE1" | ".H1E1" | ".H2E1":
                numero = "1"
            case ".HA2" | ".HE2" | ".H1E2" | ".H2E2":
                numero = "2"
            case _:
                numero = "3"
        archivoFinal = base + f".{sufijo}{numero}"
        if os.path.exists(archivoFinal):
            return  # ya estaba guardado, no hace falta repetir
        tipoArchivo = self.detectarExtension(datos)
        with open(base + tipoArchivo, "wb") as f:
            f.write(datos)
        with open(archivoFinal, "wb") as f:
            f.write(datos)

    # ---- Deshamminizar sin corregir ----

    def sacarbitsSinCorregir(self, rutaFile):
        TAM_CABECERA = 19
        ext = os.path.splitext(rutaFile)[1]
        esArchivoConError = ext in (".H1E2", ".H2E2", ".H1E3", ".H2E3")

        # Tamaño del bloque CODIFICADO: datos + bits de paridad que agrega aplicarHamming
        if ext in (".HA2", ".HE2", ".H1E2", ".H2E2"):
            tam_bloque = 1035   # 1024 datos + 11 paridad
        elif ext in (".HA3", ".HE3", ".H1E3", ".H2E3"):
            tam_bloque = 16399  # 16384 datos + 15 paridad
        else:
            raise ValueError("Formato no soportado.")

        with open(rutaFile, "rb") as f:
            datos_brutos = f.read()
        datos_brutos = datos_brutos[TAM_CABECERA:]  # Saltamos el encabezado con la fecha de apertura
        cadena_bits = "".join(f"{byte:08b}" for byte in datos_brutos)

        l1 = ""
        for c in range(0, len(cadena_bits), tam_bloque):
            bloque = cadena_bits[c:c + tam_bloque]
            if len(bloque) < tam_bloque:
                break
            l1 += self.sacarParidad(bloque)

        decodificado = bytearray()
        for k in range(0, len(l1), 8):
            btd = l1[k:k + 8]
            if len(btd) == 8:
                decodificado.append(int(btd, 2))

        # Los archivos con error conservan su extension en el nombre para no pisar el archivo original
        base = rutaFile if esArchivoConError else os.path.splitext(rutaFile)[0]
        extension_real = self.detectarExtension(decodificado)
        archivoFinal = base + extension_real
        with open(archivoFinal, "wb") as f:
            f.write(decodificado)
        match ext:
            case ".HA2" | ".HE2" | ".H1E2" | ".H2E2":
                with open(base + ".DE2", "wb") as f:
                    f.write(decodificado)
            case ".HA3" | ".HE3" | ".H1E3" | ".H2E3":
                with open(base + ".DE3", "wb") as f:
                    f.write(decodificado)
        return archivoFinal

    def sacarbitsSinCorregir8(self, rutaFile):
        TAM_CABECERA = 19
        ext = os.path.splitext(rutaFile)[1]
        esArchivoConError = ext in (".H1E1", ".H2E1")

        with open(rutaFile, "rb") as f:
            datos_brutos = f.read()
        payload = datos_brutos[TAM_CABECERA:]  # cabecera escrita una sola vez al inicio
        decodificado = bytearray()
        for c in range(0, len(payload) - 1, 2):
            bloque = f"{payload[c]:08b}{payload[c+1]:08b}"
            decodificado.append(int(self.sacarParidad8(bloque), 2))

        base = rutaFile if esArchivoConError else os.path.splitext(rutaFile)[0]
        extension_real = self.detectarExtension(decodificado)
        archivoFinal = base + extension_real
        with open(archivoFinal, "wb") as f:
            f.write(decodificado)
        with open(base + ".DE1", "wb") as f:
            f.write(decodificado)
        return archivoFinal

    # ---- Deshamminizar corrigiendo ----

    def sacarbitsCorregir8(self, rutaFile):
        TAM_CABECERA = 19
        ext = os.path.splitext(rutaFile)[1]
        esArchivoConError = ext in (".H1E1", ".H2E1")

        with open(rutaFile, "rb") as f:
            datos_brutos = f.read()
        payload = datos_brutos[TAM_CABECERA:]  # cabecera escrita una sola vez al inicio
        decodificado = bytearray()
        for c in range(0, len(payload) - 1, 2):
            bloque = f"{payload[c]:08b}{payload[c+1]:08b}"
            corregido = self.hamming_ver8(bloque)
            decodificado.append(int(self.sacarParidad8(corregido), 2))

        base = rutaFile if esArchivoConError else os.path.splitext(rutaFile)[0]
        extension_real = self.detectarExtension(decodificado)
        archivoFinal = base + extension_real
        with open(archivoFinal, "wb") as f:
            f.write(decodificado)
        with open(base + ".DC1", "wb") as f:
            f.write(decodificado)
        return archivoFinal

    def sacarbitsCorregido(self, rutaFile):
        TAM_CABECERA = 19
        ext = os.path.splitext(rutaFile)[1]
        esArchivoConError = ext in (".H1E2", ".H2E2", ".H1E3", ".H2E3")

        # Tamaño del bloque CODIFICADO: datos + bits de paridad que agrega aplicarHamming
        if ext in (".HA2", ".HE2", ".H1E2", ".H2E2"):
            tam_bloque = 1035   # 1024 datos + 11 paridad
        elif ext in (".HA3", ".HE3", ".H1E3", ".H2E3"):
            tam_bloque = 16399  # 16384 datos + 15 paridad
        else:
            raise ValueError("Formato no soportado.")

        with open(rutaFile, "rb") as f:
            datos_brutos = f.read()
        datos_brutos = datos_brutos[TAM_CABECERA:]  # Saltamos el encabezado con la fecha de apertura
        cadena_bits = "".join(f"{byte:08b}" for byte in datos_brutos)

        # Pasada única: detectar error doble, corregir error simple y extraer datos
        l1 = ""
        for c in range(0, len(cadena_bits), tam_bloque):
            bloque = cadena_bits[c:c + tam_bloque]
            if len(bloque) < tam_bloque:
                break
            sindrome = self.calcularSindrome(bloque)
            if sindrome > len(bloque):
                pass  # Dos errores en este bloque, no corregible → dejamos el bloque sin corregir
            elif sindrome > 0:
                # Un error → corregir el bit indicado por el síndrome
                lista = list(bloque)
                lista[sindrome - 1] = '0' if lista[sindrome - 1] == '1' else '1'
                bloque = ''.join(lista)
            l1 += self.sacarParidad(bloque)

        decodificado = bytearray()
        for k in range(0, len(l1), 8):
            btd = l1[k:k + 8]
            if len(btd) == 8:
                decodificado.append(int(btd, 2))

        base = rutaFile if esArchivoConError else os.path.splitext(rutaFile)[0]
        extension_real = self.detectarExtension(decodificado)
        archivoFinal = base + extension_real
        with open(archivoFinal, "wb") as f:
            f.write(decodificado)
        match ext:
            case ".HA2" | ".HE2" | ".H1E2" | ".H2E2":
                with open(base + ".DC2", "wb") as f:
                    f.write(decodificado)
            case ".HA3" | ".HE3" | ".H1E3" | ".H2E3":
                with open(base + ".DC3", "wb") as f:
                    f.write(decodificado)
        return archivoFinal

    def calcularSindrome(self, bloque):
        """Calcula el síndrome de Hamming estándar del bloque codificado.
        Retorna 0 si no hay error, la posición del bit erróneo (1-indexado)
        si hay un error, o un valor mayor que len(bloque) si hay dos o más errores."""
        n = len(bloque)
        sindrome = 0
        potencia = 1
        while potencia <= n:
            paridad = 0
            pos = potencia - 1  # índice 0-based del primer bit cubierto
            while pos < n:
                for j in range(pos, min(pos + potencia, n)):
                    paridad ^= int(bloque[j])
                pos += 2 * potencia
            if paridad:
                sindrome |= potencia
            potencia <<= 1
        return sindrome

    def detectarExtension(self, datos):
        if datos[:4] == b'%PDF':
            return '.pdf'
        if datos[:8] == b'\x89PNG\r\n\x1a\n':
            return '.png'
        if datos[:2] == b'\xff\xd8':
            return '.jpg'
        if datos[:4] in (b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08'):
            return '.zip'
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
                while i <= 4:  # Solo P1, P2, P4 — excluir P8 que es paridad global
                    y_sin += y_bloque[i - 1]
                    z_sin += l[0:8][i - 1]
                    j += 1
                    i = 2 ** j
                xy = "".join(str(int(y_sin[k]) ^ int(z_sin[k])) for k in range(len(y_sin)))
                xy_r = int(xy[::-1], 2)
                if 0 < xy_r <= 7:  # Posiciones válidas 1–7 del código Hamming(7,4)
                    listapp[xy_r - 1] = '1' if listapp[xy_r - 1] == '0' else '0'

            if l[8:16] != y1_bloque:
                i = 1
                y_sin = ""
                z_sin = ""
                j = 0
                while i <= 4:  # Solo P1, P2, P4
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
