from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

# Importamos todos los controladores
from Controllers.inicioController import InicioController
from Controllers.compactarController import CompactarController
from Controllers.descompactarController import DescompactarController
from Controllers.verTextosController import VerTextosController
from Controllers.protegerController import ProtegerController
from Controllers.insertarError1Controller import InsertarError1Controller
from Controllers.insertarError2Controller import InsertarError2Controller


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Ventanas/mainWindow.ui", self)
        self.setWindowTitle("PM 2: Huffman")

        # Vinculamos cada QWidget (panel) del stackedWidget a su controlador
        self.inicioController = InicioController(self.inicioPanel)          # Con self hacemos que puedan acceder a MainWindow
        self.compactarController = CompactarController(self.compactarPanel)
        self.descompactarController = DescompactarController(self.descompactarPanel)
        self.verTextosController = VerTextosController(self.verTextosPanel)
        self.protegerController = ProtegerController(self.protegerPanel)
        self.insertarError1Controller = InsertarError1Controller(self.insertarError1Panel)
        self.insertarError2Controller = InsertarError2Controller(self.insertarError2Panel)

        self.stackedWidget.setCurrentIndex(0)      # Mostramos el panel de inicio al iniciar la aplicación
        
    def cambiar_pantalla(self, indice):
        self.stackedWidget.setCurrentIndex(indice)


