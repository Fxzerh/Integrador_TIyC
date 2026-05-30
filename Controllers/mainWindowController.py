from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6 import uic
# Importamos todos los controladores
from Controllers.inicioController import InicioController




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Ventanas/mainWindow.ui", self)
        self.setWindowTitle("PM 2: Huffman")

        self.stackedWidget = QStackedWidget()      # Creamos el StackedWidget
        self.setCentralWidget(self.stackedWidget)  # Al StackedWidget no ponemos como principal de la ventana principal

        # Instanciamos los controladores
        self.inicioController = InicioController(self)      # Con self hacemos que puedan acceder a MainWindow
        

        # Añadimos el controlador al StackedWidget
        self.stackedWidget.addWidget(self.inicioController)         # Indice 0
        


        self.stackedWidget.setCurrentWidget(self.inicioController)      # Mostramos el panel_inicio al iniciar la aplicación, se puede cambiar a otro panel usando setCurrentWidget() con el panel deseado

    def cambiar_pantalla(self, indice):
        self.stackedWidget.setCurrentIndex(indice)


