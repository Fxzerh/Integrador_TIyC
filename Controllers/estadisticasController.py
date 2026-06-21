from PyQt6.QtWidgets import (QTableWidget, QMessageBox, QTableWidgetItem,
                              QHeaderView, QDialog, QVBoxLayout, QLabel)
import re
import os
import json

EXTS_ORIGINALES = {'.pdf', '.txt', '.jpg', '.jpeg', '.png', '.bmp', '.docx', '.xlsx'}
HA_EXT_RE = re.compile(r'^\.HA\d+$', re.IGNORECASE)
HUF_EXTS = {'.huf', '.dhu'}


class EstadisticasController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")

        try:
            tabla = self.mainWindow.tableFileE
            tabla.setColumnCount(5)
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            tabla.setRowCount(0)

            tabla.setHorizontalHeaderItem(0, QTableWidgetItem("Archivo Original"))
            tabla.setHorizontalHeaderItem(1, QTableWidgetItem("Tamaño Original"))
            tabla.setHorizontalHeaderItem(2, QTableWidgetItem("Archivo Derivado"))
            tabla.setHorizontalHeaderItem(3, QTableWidgetItem("Tamaño Derivado"))
            tabla.setHorizontalHeaderItem(4, QTableWidgetItem("% Variación"))
            #tabla.setHorizontalHeaderItem(5, QTableWidgetItem("Letras Distintas"))
            #tabla.setHorizontalHeaderItem(6, QTableWidgetItem("Letras Repetidas"))

            tabla.itemClicked.connect(self._onFilaClicked)
            self.cargarTabla()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

    def refrescarPanel(self):
        self.mainWindow.tableFileE.setRowCount(0)
        self.cargarTabla()

    def _ajustarAnchosProporcionales(self):
        tabla = self.mainWindow.tableFileE
        tabla.resizeColumnsToContents()

        header = tabla.horizontalHeader()
        widths = [header.sectionSize(i) for i in range(tabla.columnCount())]
        total = sum(widths)
        available = tabla.viewport().width()
        if total <= 0 or available <= 0:
            return

        factor = max(1.0, available / total)
        for i, width in enumerate(widths):
            tabla.setColumnWidth(i, max(10, int(width * factor)))

    def _formatearTamaño(self, bytes_val):
        if bytes_val < 1024:
            return f"{bytes_val} B"
        elif bytes_val < 1024 * 1024:
            return f"{bytes_val / 1024:.2f} KB"
        else:
            return f"{bytes_val / (1024 * 1024):.2f} MB"

    def _agregarFila(self, nombre_orig, tam_orig, nombre_der, tam_der, freq_dict=None):
        pct = ((tam_der - tam_orig) / tam_orig * 100) if tam_orig > 0 else 0.0
        pct_str = f"{pct:+.1f}%"

        tabla = self.mainWindow.tableFileE
        fila = tabla.rowCount()
        tabla.insertRow(fila)
        tabla.setItem(fila, 0, QTableWidgetItem(nombre_orig))
        tabla.setItem(fila, 1, QTableWidgetItem(self._formatearTamaño(tam_orig)))
        tabla.setItem(fila, 2, QTableWidgetItem(nombre_der))
        tabla.setItem(fila, 3, QTableWidgetItem(self._formatearTamaño(tam_der)))
        tabla.setItem(fila, 4, QTableWidgetItem(pct_str))

        # if freq_dict is not None:
        #     distintas = len(freq_dict)
        #     repetidas = sum(1 for f in freq_dict.values() if f > 1)
        #     tabla.setItem(fila, 5, QTableWidgetItem(str(distintas)))
        #     tabla.setItem(fila, 6, QTableWidgetItem(str(repetidas)))

    def _leerDicHuf(self, path):
        try:
            with open(path, "rb") as f:
                f.read(1)  # padding byte
                longDic = int.from_bytes(f.read(4), byteorder='big')
                dicBytes = f.read(longDic)
                dicAux = json.loads(dicBytes.decode())
                return {int(k): v for k, v in dicAux.items()}
        except Exception:
            return None

    def _leerFrecsDhu(self, path):
        try:
            with open(path, "rb") as f:
                data = f.read()
            freq = {}
            for byte in data:
                freq[byte] = freq.get(byte, 0) + 1
            return freq
        except Exception:
            return None

    def _onFilaClicked(self, item):
        fila = item.row()
        tabla = self.mainWindow.tableFileE
        nombre_der_item = tabla.item(fila, 2)
        if not nombre_der_item:
            return
        nombre_der = nombre_der_item.text()
        ext = os.path.splitext(nombre_der)[1].lower()
        if ext not in HUF_EXTS:
            return

        ruta = os.path.join(self.carpetaArchivos, nombre_der)
        freq_dict = self._leerDicHuf(ruta) if ext == '.huf' else self._leerFrecsDhu(ruta)
        if not freq_dict:
            return
        self._mostrarPopupFreqs(nombre_der, freq_dict)

    def _mostrarPopupFreqs(self, nombre, freq_dict):
        total = sum(freq_dict.values())
        distintas = len(freq_dict)
        repetidas = sum(1 for f in freq_dict.values() if f > 1)

        dlg = QDialog(self.mainWindow)
        dlg.setWindowTitle(f"Frecuencias - {nombre}")
        dlg.resize(420, 500)
        layout = QVBoxLayout(dlg)

        resumen = QLabel(
            f"Letras distintas: {distintas}   |   "
            f"Letras repetidas: {repetidas}   |   "
            f"Total bytes: {total}"
        )
        layout.addWidget(resumen)

        t = QTableWidget(dlg)
        t.setColumnCount(4)
        t.setHorizontalHeaderLabels(["Byte", "Carácter", "Frecuencia", "%"])
        t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
        t.setRowCount(len(sorted_items))
        for i, (byte_val, freq) in enumerate(sorted_items):
            pct = freq / total * 100
            char_repr = chr(byte_val) if 32 <= byte_val < 127 else f"\\x{byte_val:02x}"
            t.setItem(i, 0, QTableWidgetItem(str(byte_val)))
            t.setItem(i, 1, QTableWidgetItem(char_repr))
            t.setItem(i, 2, QTableWidgetItem(str(freq)))
            t.setItem(i, 3, QTableWidgetItem(f"{pct:.2f}%"))

        layout.addWidget(t)
        dlg.exec()

    def cargarTabla(self):
        if not os.path.exists(self.carpetaArchivos):
            return

        all_files = set(
            f for f in os.listdir(self.carpetaArchivos)
            if os.path.isfile(os.path.join(self.carpetaArchivos, f))
        )

        originales = sorted(
            f for f in all_files
            if os.path.splitext(f)[1].lower() in EXTS_ORIGINALES
        )

        for original in originales:
            stem = os.path.splitext(original)[0]
            tam_orig = os.path.getsize(os.path.join(self.carpetaArchivos, original))

            # Par Huffman comprimido: stem.huf
            huf = stem + '.huf'
            if huf in all_files:
                tam_huf = os.path.getsize(os.path.join(self.carpetaArchivos, huf))
                freq_dict = self._leerDicHuf(os.path.join(self.carpetaArchivos, huf))
                self._agregarFila(original, tam_orig, huf, tam_huf, freq_dict)

            # Par Huffman descomprimido: stem.dhu
            dhu = stem + '.dhu'
            if dhu in all_files:
                tam_dhu = os.path.getsize(os.path.join(self.carpetaArchivos, dhu))
                freq_dict = self._leerFrecsDhu(os.path.join(self.carpetaArchivos, dhu))
                self._agregarFila(original, tam_orig, dhu, tam_dhu, freq_dict)

            # Pares Hamming: stem.HA1, stem.HA2, stem.HA3, ...
            for f in sorted(all_files):
                f_stem, f_ext = os.path.splitext(f)
                if f_stem == stem and HA_EXT_RE.match(f_ext):
                    tam_ha = os.path.getsize(os.path.join(self.carpetaArchivos, f))
                    self._agregarFila(original, tam_orig, f, tam_ha)

        self._ajustarAnchosProporcionales()
