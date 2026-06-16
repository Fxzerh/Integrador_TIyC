from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

# Importamos todos los controladores
from Controllers.inicioController import InicioController
from Controllers.compactarController import CompactarController
from Controllers.descompactarController import DescompactarController
from Controllers.verDCController import VerDCController
from Controllers.protegerController import ProtegerController
from Controllers.insertarErrorController import InsertarErrorController
from Controllers.desprotegerController import DesprotegerController
from Controllers.verDPController import VerDPController
from Controllers.estadisticasController import EstadisticasController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Ventanas/mainWindow.ui", self)
        self.setWindowTitle("PM3: Proyecto Integrador")

        # ---------------------------- SETTEOS INICIALES ---------------------------------------------------------------------------------------------------------
        # Vinculamos cada QWidget (panel) del stackedWidget a su controlador
        # Con self hacemos que puedan acceder a MainWindow
        self.inicioController = InicioController(self)                          # Indice 0
        self.compactarController = CompactarController(self)                 # Indice 1
        self.descompactarController = DescompactarController(self)        # Indice 2
        self.verDCController = VerDCController(self)                 # Indice 3
        self.protegerController = ProtegerController(self)                    # Indice 4
        self.insertarErrorController = InsertarErrorController(self)     # Indice 5
        self.desprotegerController = DesprotegerController(self)           # Indice 6  
        self.verDPController = VerDPController(self)                 # Indice 7
        self.estadisticasController = EstadisticasController(self)                 # Indice 8


        self.controladores = [
            self.inicioController,         # Índice 0
            self.compactarController,      # Índice 1
            self.descompactarController,   # Índice 2
            self.verDCController,      # Índice 3
            self.protegerController,       # Índice 4
            self.insertarErrorController,  # Índice 5
            self.desprotegerController,     # Índice 6
            self.verDPController,          # Índice 7
            self.estadisticasController     # Índice 8
        ]

        self.stackedWidget.setCurrentIndex(0)      # Mostramos el panel de inicio al iniciar la aplicación

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.inicio_btn.clicked.connect(lambda: self.cambiar_pantalla(0))
        self.compactar_btn.clicked.connect(lambda: self.cambiar_pantalla(1))
        self.descompactar_btn.clicked.connect(lambda: self.cambiar_pantalla(2))
        self.verDC_btn.clicked.connect(lambda: self.cambiar_pantalla(3))
        self.proteger_btn.clicked.connect(lambda: self.cambiar_pantalla(4))
        self.insertarError_btn.clicked.connect(lambda: self.cambiar_pantalla(5))
        self.desproteger_btn.clicked.connect(lambda: self.cambiar_pantalla(6))
        self.verDP_btn.clicked.connect(lambda: self.cambiar_pantalla(7))
        self.estadisticas_btn.clicked.connect(lambda: self.cambiar_pantalla(8))

        
    def cambiar_pantalla(self, indice):
        self.stackedWidget.setCurrentIndex(indice)
        if hasattr(self.controladores[indice], 'refrescarPanel'):
            self.controladores[indice].refrescarPanel()


