from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
import re
import os

EXTS_ORIGINALES = {'.pdf', '.txt', '.jpg', '.jpeg', '.png', '.bmp', '.docx', '.xlsx'}
HA_EXT_RE = re.compile(r'^\.HA\d+$', re.IGNORECASE)


class EstadisticasController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")

        try:
            tabla = self.mainWindow.tableFileE
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            tabla.setRowCount(0)

            tabla.setHorizontalHeaderItem(0, QTableWidgetItem("Archivo Original"))
            tabla.setHorizontalHeaderItem(1, QTableWidgetItem("Tamaño Original"))
            tabla.setHorizontalHeaderItem(2, QTableWidgetItem("Archivo Derivado"))
            tabla.setHorizontalHeaderItem(3, QTableWidgetItem("Tamaño Derivado"))
            tabla.setHorizontalHeaderItem(4, QTableWidgetItem("% Variación"))

            self.cargarTabla()
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

    def refrescarPanel(self):
        self.mainWindow.tableFileE.setRowCount(0)
        self.cargarTabla()

    def _formatearTamaño(self, bytes_val):
        if bytes_val < 1024:
            return f"{bytes_val} B"
        elif bytes_val < 1024 * 1024:
            return f"{bytes_val / 1024:.2f} KB"
        else:
            return f"{bytes_val / (1024 * 1024):.2f} MB"

    def _agregarFila(self, nombre_orig, tam_orig, nombre_der, tam_der):
        pct = ((tam_der - tam_orig) / tam_orig * 100) if tam_orig > 0 else 0.0
        pct_str = f"{pct:+.1f}%"  # siempre muestra el signo: -30.5% o +25.0%

        tabla = self.mainWindow.tableFileE
        fila = tabla.rowCount()
        tabla.insertRow(fila)
        tabla.setItem(fila, 0, QTableWidgetItem(nombre_orig))
        tabla.setItem(fila, 1, QTableWidgetItem(self._formatearTamaño(tam_orig)))
        tabla.setItem(fila, 2, QTableWidgetItem(nombre_der))
        tabla.setItem(fila, 3, QTableWidgetItem(self._formatearTamaño(tam_der)))
        tabla.setItem(fila, 4, QTableWidgetItem(pct_str))

    def cargarTabla(self):
        if not os.path.exists(self.carpetaArchivos):
            return

        all_files = set(
            f for f in os.listdir(self.carpetaArchivos)
            if os.path.isfile(os.path.join(self.carpetaArchivos, f))
        )

        # Solo los archivos con extensión original conocida (.pdf, .txt, .jpg, etc.)
        originales = sorted(
            f for f in all_files
            if os.path.splitext(f)[1].lower() in EXTS_ORIGINALES
        )

        for original in originales:
            stem = os.path.splitext(original)[0]
            tam_orig = os.path.getsize(os.path.join(self.carpetaArchivos, original))

            # Par Huffman: stem.huf
            huf = stem + '.huf'
            if huf in all_files:
                tam_huf = os.path.getsize(os.path.join(self.carpetaArchivos, huf))
                self._agregarFila(original, tam_orig, huf, tam_huf)

            # Pares Hamming: stem.HA1, stem.HA2, stem.HA3, ...
            for f in sorted(all_files):
                f_stem, f_ext = os.path.splitext(f)
                if f_stem == stem and HA_EXT_RE.match(f_ext):
                    tam_ha = os.path.getsize(os.path.join(self.carpetaArchivos, f))
                    self._agregarFila(original, tam_orig, f, tam_ha)
