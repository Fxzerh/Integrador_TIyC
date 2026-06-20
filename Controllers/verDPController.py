from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
import os


EXTENSIONES_INTERMEDIAS = {
    '.huf', '.dhu', '.VDC', '.VDP',
    '.HA1', '.HA2', '.HA3', '.HE1', '.HE2', '.HE3',
    '.H1E1', '.H1E2', '.H1E3', '.H2E1', '.H2E2', '.H2E3',
    '.DE1', '.DE2', '.DE3', '.DC1', '.DC2', '.DC3',
}


class VerDPController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")

        try:
            self.mainWindow.tableFileVDP.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            self.mainWindow.tableFileVDP.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.mainWindow.tableFileVDP.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            self.mainWindow.tableFileVDP.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            self.mainWindow.tableFileVDP.setRowCount(0)
            self.cargarTabla()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        self.mainWindow.tableFileVDP.itemClicked.connect(self.mostrarArchivo)

    def cambiarPanel(self, indice):
        self.mainWindow.cambiar_pantalla(indice)

    def refrescarPanel(self):
        self.mainWindow.tableFileVDP.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewVDP_O.setUrl(QUrl("about:blank"))
        self.mainWindow.viewVDP_R.setUrl(QUrl("about:blank"))

    def cargarTabla(self):
        if os.path.exists(self.carpetaArchivos):
            for f in sorted(os.listdir(self.carpetaArchivos)):
                ext = os.path.splitext(f)[1]
                file_path = os.path.join(self.carpetaArchivos, f)
                if os.path.isfile(file_path) and ext not in EXTENSIONES_INTERMEDIAS:
                    tamaño = os.path.getsize(file_path)
                    if tamaño < 1024:
                        tamaño_str = f"{tamaño} B"
                    elif tamaño < 1024 * 1024:
                        tamaño_str = f"{tamaño / 1024:.2f} KB"
                    else:
                        tamaño_str = f"{tamaño / (1024 * 1024):.2f} MB"
                    rowPosition = self.mainWindow.tableFileVDP.rowCount()
                    self.mainWindow.tableFileVDP.insertRow(rowPosition)
                    self.mainWindow.tableFileVDP.setItem(rowPosition, 0, QTableWidgetItem(f))
                    self.mainWindow.tableFileVDP.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))

    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileVDP.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            return self.mainWindow.tableFileVDP.item(row, 0).text()
        return None

    def mostrarArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            return
        rutaFile = os.path.join(self.carpetaArchivos, nombreArchivo)
        if not os.path.exists(rutaFile):
            return

        self.mainWindow.viewVDP_O.setUrl(QUrl.fromLocalFile(rutaFile))

        try:
            with open(rutaFile, "rb") as f:
                contenido = f.read()
            if len(contenido) == 0:
                QMessageBox.warning(self.mainWindow, "Aviso", "El archivo está vacío.")
                return

            # --- CODIFICAR con Hamming (bloques de 1024 bits) ---
            TAM_BLOQUE_DATOS = 1024
            TAM_BLOQUE_COD = 1035  # 1024 datos + 11 bits de paridad

            cadenaBits = "".join(f"{byte:08b}" for byte in contenido)
            bitsProtegidos = ""
            for i in range(0, len(cadenaBits), TAM_BLOQUE_DATOS):
                bloque = cadenaBits[i:i + TAM_BLOQUE_DATOS]
                if len(bloque) < TAM_BLOQUE_DATOS:
                    bloque = bloque.ljust(TAM_BLOQUE_DATOS, '0')
                bitsProtegidos += self.aplicarHamming(bloque)

            # --- DECODIFICAR: extraer bits de datos de cada bloque de 1035 bits ---
            l1 = ""
            for i in range(0, len(bitsProtegidos), TAM_BLOQUE_COD):
                bloque = bitsProtegidos[i:i + TAM_BLOQUE_COD]
                if len(bloque) < TAM_BLOQUE_COD:
                    break
                l1 += self.sacarParidad(bloque)

            decodificado = bytearray()
            for k in range(0, len(l1), 8):
                btd = l1[k:k + 8]
                if len(btd) == 8:
                    decodificado.append(int(btd, 2))

            # Guardar resultado con la misma extension del original
            ext_original = os.path.splitext(nombreArchivo)[1]
            base = os.path.splitext(nombreArchivo)[0]
            rutaResultado = os.path.join(self.carpetaArchivos, base + "_vdp" + ext_original)
            with open(rutaResultado, "wb") as f:
                f.write(decodificado)

            self.mainWindow.viewVDP_R.setUrl(QUrl.fromLocalFile(rutaResultado))

        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo procesar el archivo: {str(e)}")

    # --- Algoritmo Hamming (igual que protegerController.aplicarHamming) ---

    def aplicarHamming(self, bitsDatos):
        longitudDatos = len(bitsDatos)
        bitsParidad = 0
        while (2 ** bitsParidad) < (longitudDatos + bitsParidad + 1):
            bitsParidad += 1
        longitudTotal = longitudDatos + bitsParidad
        trama = ['0'] * longitudTotal
        indiceDatos = 0
        for i in range(longitudTotal):
            if ((i + 1) & i) != 0:  # no es potencia de 2
                trama[i] = bitsDatos[indiceDatos]
                indiceDatos += 1
        for l in range(bitsParidad):
            posParidad = 2 ** l
            xorSuma = 0
            for i in range(longitudTotal):
                posReal = i + 1
                if (posReal & posParidad) != 0 and posReal != posParidad:
                    xorSuma ^= int(trama[i])
            trama[posParidad - 1] = str(xorSuma)
        return "".join(trama)

    # --- Extraer bits de datos eliminando posiciones de paridad ---

    def sacarParidad(self, l):
        j = 0
        x = ""
        for s in range(len(l)):
            if 2 ** j == s + 1:
                j += 1
            else:
                x += l[s]
        return x
