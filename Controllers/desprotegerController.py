from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
import os


class DesprotegerController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")

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
        self.mainWindow.viewDP.setUrl(QUrl("about:blank"))

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
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            return
        ruta_completa = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(ruta_completa):
            self.mainWindow.viewDP.setUrl(QUrl.fromLocalFile(ruta_completa))

    def desprotegerSinCorregir(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "Seleccione un archivo de la tabla.")
            return
        rutaFile = os.path.join(self.carpetaArchivos, nombreArchivo)
        ext = os.path.splitext(rutaFile)[1]
        try:
            if ext in (".HA1", ".HE1", ".H1E1", ".H2E1"):
                archivoFinal = self.sacarbitsSinCorregir8(rutaFile)
            else:
                archivoFinal = self.sacarbitsSinCorregir(rutaFile)
            self.mainWindow.viewDP.setUrl(QUrl.fromLocalFile(archivoFinal))
            QMessageBox.information(self.mainWindow, "Éxito", f"Archivo desprotegido correctamente. \nGuardado en '{os.path.basename(archivoFinal)}'.")
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo desproteger el archivo: {str(e)}")

    def desprotegerCorrigiendo(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "Seleccione un archivo de la tabla.")
            return
        rutaFile = os.path.join(self.carpetaArchivos, nombreArchivo)
        ext = os.path.splitext(rutaFile)[1]
        if ext in (".H2E1", ".H2E2", ".H2E3"):
            QMessageBox.warning(self.mainWindow, "Aviso", "Este archivo contiene 2 errores por bloque y no puede ser corregido ni desprotegido.")
            return
        try:
            if ext in (".HA1", ".HE1", ".H1E1"):
                archivoFinal = self.sacarbitsCorregir8(rutaFile)
            else:
                archivoFinal = self.sacarbitsCorregido(rutaFile)
            self.mainWindow.viewDP.setUrl(QUrl.fromLocalFile(archivoFinal))
            QMessageBox.information(self.mainWindow, "Éxito", f"Archivo desprotegido correctamente. \nGuardado en '{os.path.basename(archivoFinal)}'.")
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo desproteger el archivo: {str(e)}")

    # ---- Deshamminizar sin corregir ----

    def sacarbitsSinCorregir(self, rutaFile):
        TAM_CABECERA = 19
        ext = os.path.splitext(rutaFile)[1]
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

        base = os.path.splitext(rutaFile)[0]
        match ext:
            case ".HA2" | ".HE2" | ".H1E2" | ".H2E2":
                archivoFinal = base + ".DE2"
            case ".HA3" | ".HE3" | ".H1E3" | ".H2E3":
                archivoFinal = base + ".DE3"
        with open(archivoFinal, "wb") as f:
            f.write(decodificado)
        return archivoFinal

    def sacarbitsSinCorregir8(self, rutaFile):
        TAM_CABECERA = 19
        TAM_GRUPO = TAM_CABECERA + 2  # 19 bytes de cabecera + 2 bytes Hamming por byte original

        with open(rutaFile, "rb") as f:
            datos_brutos = f.read()
        decodificado = bytearray()
        for c in range(0, len(datos_brutos), TAM_GRUPO):
            grupo = datos_brutos[c:c + TAM_GRUPO]
            if len(grupo) < TAM_GRUPO:
                break
            bytes_hamming = grupo[TAM_CABECERA:]  # Saltamos los 19 bytes de cabecera
            bloque = f"{bytes_hamming[0]:08b}{bytes_hamming[1]:08b}"
            decodificado.append(int(self.sacarParidad8(bloque), 2))

        base = os.path.splitext(rutaFile)[0]
        archivoFinal = base + ".DE1"
        with open(archivoFinal, "wb") as f:
            f.write(decodificado)
        return archivoFinal

    # ---- Deshamminizar corrigiendo ----

    def sacarbitsCorregir8(self, rutaFile):
        TAM_CABECERA = 19
        TAM_GRUPO = TAM_CABECERA + 2

        with open(rutaFile, "rb") as f:
            datos_brutos = f.read()
        decodificado = bytearray()
        for c in range(0, len(datos_brutos), TAM_GRUPO):
            grupo = datos_brutos[c:c + TAM_GRUPO]
            if len(grupo) < TAM_GRUPO:
                break
            bytes_hamming = grupo[TAM_CABECERA:]
            bloque = f"{bytes_hamming[0]:08b}{bytes_hamming[1]:08b}"
            corregido = self.hamming_ver8(bloque)
            decodificado.append(int(self.sacarParidad8(corregido), 2))

        base = os.path.splitext(rutaFile)[0]
        archivoFinal = base + ".DC1"
        with open(archivoFinal, "wb") as f:
            f.write(decodificado)
        return archivoFinal

    def sacarbitsCorregido(self, rutaFile):
        TAM_CABECERA = 19
        ext = os.path.splitext(rutaFile)[1]
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

        base = os.path.splitext(rutaFile)[0]
        match ext:
            case ".HA2" | ".HE2" | ".H1E2" | ".H2E2":
                archivoFinal = base + ".DC2"
            case ".HA3" | ".HE3" | ".H1E3" | ".H2E3":
                archivoFinal = base + ".DC3"
        with open(archivoFinal, "wb") as f:
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
