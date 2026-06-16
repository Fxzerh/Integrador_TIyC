from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

class InicioController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.compactarInicio_btn.clicked.connect(lambda: self.cambiarPanel(1))
        self.mainWindow.descompactarInicio_btn.clicked.connect(lambda: self.cambiarPanel(2))
        self.mainWindow.verDCInicio_btn.clicked.connect(lambda: self.cambiarPanel(3))
        self.mainWindow.protegerInicio_btn.clicked.connect(lambda: self.cambiarPanel(4))
        self.mainWindow.insertarErrorInicio_btn.clicked.connect(lambda: self.cambiarPanel(5))
        self.mainWindow.desprotegerInicio_btn.clicked.connect(lambda: self.cambiarPanel(6))
        self.mainWindow.verDPInicio_btn.clicked.connect(lambda: self.cambiarPanel(7))
        self.mainWindow.estadisticasInicio_btn.clicked.connect(lambda: self.cambiarPanel(8))
    
    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)