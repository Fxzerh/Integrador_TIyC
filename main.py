import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from Controllers.mainWindowController import MainWindow

QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Activamos el plugin de PDFs de forma global para todo el programa
    QWebEngineProfile.defaultProfile().settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())