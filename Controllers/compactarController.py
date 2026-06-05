from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

class CompactarController(QWidget):
    def __init__(self, vista_compactar):
        super().__init__()
        #uic.loadUi("Ventanas/compactarPanel.ui", self)
        self.vista = vista_compactar

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        #self.loadFile_btn.clicked.connect(lambda: self.cambiarPanel(1))     # Cambia al panel de carga de archivos, el indice 1 es el loadFilePanel
        #self.compactFile_btn.clicked.connect(lambda: self.cambiarPanel(2))    # Cambia al panel de codificacion, el indice 2 es el compactFilePanel
        #self.decompactFile_btn.clicked.connect(lambda: self.cambiarPanel(3))      # Cambia al panel de añadir error, el indice 3 es el decompactFilePanel
        #self.showFiles_btn.clicked.connect(lambda: self.cambiarPanel(4))   # Cambia al panel de decodificacion y correccion, el indice 4 es el showFilePanel
        #self.estadisticas_btn.clicked.connect(lambda: self.cambiarPanel(5))     # Cambia al panel de decodificacion sin correccion, el indice 5 es el estaditicasPanel
    
    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)