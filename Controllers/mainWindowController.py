from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6 import uic
# Importamos todos los controladores
from Controllers.inicioController import InicioController
from Controllers.loadFileController import LoadFileController
from Controllers.compactFileController import CompactFileController
from Controllers.decompactFileController import DecompactFileController
from Controllers.showFileController import ShowFileController
from Controllers.estaditicasController import EstadisticasController



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Ventanas/mainWindow.ui", self)
        self.setWindowTitle("PM 2: Huffman")

        self.stackedWidget = QStackedWidget()      # Creamos el StackedWidget
        self.setCentralWidget(self.stackedWidget)  # Al StackedWidget no ponemos como principal de la ventana principal

        # Instanciamos los controladores
        self.inicioController = InicioController(self)      # Con self hacemos que puedan acceder a MainWindow
        self.loadFileController = LoadFileController(self)
        self.compactFileController = CompactFileController(self)
        self.decompactFileController = DecompactFileController(self)
        self.showFileController = ShowFileController(self)
        self.estadisticasController = EstadisticasController(self)

        # Añadimos el controlador al StackedWidget
        self.stackedWidget.addWidget(self.inicioController)         # Indice 0
        self.stackedWidget.addWidget(self.loadFileController)       # Indice 1
        self.stackedWidget.addWidget(self.compactFileController)    # Indice 2
        self.stackedWidget.addWidget(self.decompactFileController)  # Indice 3
        self.stackedWidget.addWidget(self.showFileController)       # Indice 4
        self.stackedWidget.addWidget(self.estadisticasController)    # Indice 5


        self.stackedWidget.setCurrentWidget(self.inicioController)      # Mostramos el panel_inicio al iniciar la aplicación, se puede cambiar a otro panel usando setCurrentWidget() con el panel deseado

    def cambiar_pantalla(self, indice):
        self.stackedWidget.setCurrentIndex(indice)


