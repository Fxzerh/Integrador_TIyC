from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
from Clases.nodo import Nodo
import os


EXTENSIONES_INTERMEDIAS = {
    '.huf', '.dhu', '.VDC', '.VDP',
    '.HA1', '.HA2', '.HA3', '.HE1', '.HE2', '.HE3',
    '.H1E1', '.H1E2', '.H1E3', '.H2E1', '.H2E2', '.H2E3',
    '.DE1', '.DE2', '.DE3', '.DC1', '.DC2', '.DC3',
}


class VerDCController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")
        self.raiz = None
        self.dicCaracteres = {}
        self.tablaCodigos = {}
        self.cantNodos = 0

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
        self.mainWindow.viewVDC_O.setUrl(QUrl("about:blank"))
        self.mainWindow.viewVDC_R.setUrl(QUrl("about:blank"))

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
                    rowPosition = self.mainWindow.tableFileVDC.rowCount()
                    self.mainWindow.tableFileVDC.insertRow(rowPosition)
                    self.mainWindow.tableFileVDC.setItem(rowPosition, 0, QTableWidgetItem(f))
                    self.mainWindow.tableFileVDC.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))

    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileVDC.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            return self.mainWindow.tableFileVDC.item(row, 0).text()
        return None

    def mostrarArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            return
        rutaFile = os.path.join(self.carpetaArchivos, nombreArchivo)
        if not os.path.exists(rutaFile):
            return

        self.mainWindow.viewVDC_O.setUrl(QUrl.fromLocalFile(rutaFile))

        try:
            with open(rutaFile, "rb") as f:
                contenido = f.read()
            if len(contenido) == 0:
                QMessageBox.warning(self.mainWindow, "Aviso", "El archivo está vacío.")
                return

            # --- COMPRIMIR con Huffman ---
            self.arbolHuffman(contenido)
            self.generarCodigos(self.raiz, "")

            bits_juntos = "".join(self.tablaCodigos[b] for b in contenido)
            cantPadding = (8 - (len(bits_juntos) % 8)) % 8
            if cantPadding > 0:
                bits_juntos += "0" * cantPadding
            bytesComprimidos = bytearray(
                int(bits_juntos[i:i + 8], 2) for i in range(0, len(bits_juntos), 8)
            )

            # --- DESCOMPRIMIR ---
            strBytes = "".join(format(b, '08b') for b in bytesComprimidos)
            if cantPadding > 0:
                strBytes = strBytes[:-cantPadding]
            descomprimido = self.descomprimirTexto(strBytes)

            # Guardar resultado con la misma extension del original
            ext_original = os.path.splitext(nombreArchivo)[1]
            base = os.path.splitext(nombreArchivo)[0]
            rutaResultado = os.path.join(self.carpetaArchivos, base + "_vdc" + ext_original)
            with open(rutaResultado, "wb") as f:
                f.write(descomprimido)

            self.mainWindow.viewVDC_R.setUrl(QUrl.fromLocalFile(rutaResultado))

            self.dicCaracteres = {}
            self.tablaCodigos = {}

        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo procesar el archivo: {str(e)}")

    # --- Algoritmo Huffman ---

    def arbolHuffman(self, texto):
        self.dicCaracteres = {}
        listNodos = []
        for byte in texto:
            self.dicCaracteres[byte] = self.dicCaracteres.get(byte, 0) + 1
        for simbolo, freq in self.dicCaracteres.items():
            listNodos.append(Nodo(simbolo=simbolo, frecuencia=freq))
        self.cantNodos = len(listNodos)
        while len(listNodos) > 1:
            listNodos.sort()
            nodoI = listNodos.pop(0)
            nodoD = listNodos.pop(0)
            padre = Nodo(simbolo=None, frecuencia=nodoI.frecuencia + nodoD.frecuencia)
            padre.hijoIzq = nodoI
            padre.hijoDer = nodoD
            listNodos.append(padre)
        self.raiz = listNodos[0]

    def generarCodigos(self, nodo, codigo=""):
        if self.cantNodos == 1:
            self.tablaCodigos[nodo.simbolo] = "0"
            return
        if nodo.simbolo is not None:
            self.tablaCodigos[nodo.simbolo] = codigo
        else:
            self.generarCodigos(nodo.hijoIzq, codigo + "0")
            self.generarCodigos(nodo.hijoDer, codigo + "1")

    def descomprimirTexto(self, textoComprimido):
        nodoActual = self.raiz
        resultado = bytearray()
        for bit in textoComprimido:
            if self.cantNodos != 1:
                nodoActual = nodoActual.hijoIzq if bit == "0" else nodoActual.hijoDer
                if nodoActual.simbolo is not None:
                    resultado.append(nodoActual.simbolo)
                    nodoActual = self.raiz
            else:
                resultado.append(nodoActual.simbolo)
        return bytes(resultado)
