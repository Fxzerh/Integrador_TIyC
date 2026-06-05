# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QPushButton{\n"
"	background-color: transparent;\n"
"	border: 1px;\n"
"	font: 11pt \"Yu Gothic UI\";\n"
"	height: 50px;\n"
"	text-align: left;\n"
"	padding-left: 20px;\n"
"}\n"
"QPushButton:hover{\n"
"	Background-color: #4a4a4a;\n"
"}\n"
"QLabel{\n"
"	font: 700 \"Yu Gothic UI\";\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(200, 0))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 50))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(False)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"QLabel{\n"
"	border: none;\n"
"	border-bottom: 2px solid #262626;\n"
"	padding-left: 15px;\n"
"	padding-bottom: 5px;\n"
"}")
        self.label.setWordWrap(False)
        self.label.setMargin(20)
        self.label.setOpenExternalLinks(False)

        self.verticalLayout.addWidget(self.label)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton.setMinimumSize(QSize(0, 20))
        self.pushButton.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout.addWidget(self.pushButton)

        self.inicio_btn = QPushButton(self.frame)
        self.inicio_btn.setObjectName(u"inicio_btn")
        self.inicio_btn.setEnabled(True)
        self.inicio_btn.setMinimumSize(QSize(200, 50))
        self.inicio_btn.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.inicio_btn)

        self.compactar_btn = QPushButton(self.frame)
        self.compactar_btn.setObjectName(u"compactar_btn")

        self.verticalLayout.addWidget(self.compactar_btn)

        self.descompactar_btn = QPushButton(self.frame)
        self.descompactar_btn.setObjectName(u"descompactar_btn")

        self.verticalLayout.addWidget(self.descompactar_btn)

        self.verTextos_btn = QPushButton(self.frame)
        self.verTextos_btn.setObjectName(u"verTextos_btn")

        self.verticalLayout.addWidget(self.verTextos_btn)

        self.proteger_btn = QPushButton(self.frame)
        self.proteger_btn.setObjectName(u"proteger_btn")

        self.verticalLayout.addWidget(self.proteger_btn)

        self.insertarError1_btn = QPushButton(self.frame)
        self.insertarError1_btn.setObjectName(u"insertarError1_btn")

        self.verticalLayout.addWidget(self.insertarError1_btn)

        self.insertarError2_btn = QPushButton(self.frame)
        self.insertarError2_btn.setObjectName(u"insertarError2_btn")

        self.verticalLayout.addWidget(self.insertarError2_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.frame)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.inicioPanel = QWidget()
        self.inicioPanel.setObjectName(u"inicioPanel")
        self.titulo = QLabel(self.inicioPanel)
        self.titulo.setObjectName(u"titulo")
        self.titulo.setGeometry(QRect(400, 60, 281, 70))
        font2 = QFont()
        font2.setFamilies([u"Yu Gothic UI"])
        font2.setPointSize(40)
        font2.setBold(True)
        font2.setItalic(False)
        self.titulo.setFont(font2)
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stackedWidget.addWidget(self.inicioPanel)
        self.compactarPanel = QWidget()
        self.compactarPanel.setObjectName(u"compactarPanel")
        self.stackedWidget.addWidget(self.compactarPanel)
        self.descompactarPanel = QWidget()
        self.descompactarPanel.setObjectName(u"descompactarPanel")
        self.stackedWidget.addWidget(self.descompactarPanel)
        self.verTextosPanel = QWidget()
        self.verTextosPanel.setObjectName(u"verTextosPanel")
        self.stackedWidget.addWidget(self.verTextosPanel)
        self.protegerPanel = QWidget()
        self.protegerPanel.setObjectName(u"protegerPanel")
        self.stackedWidget.addWidget(self.protegerPanel)
        self.insertarError1Panel = QWidget()
        self.insertarError1Panel.setObjectName(u"insertarError1Panel")
        self.stackedWidget.addWidget(self.insertarError1Panel)
        self.insertarError2Panel = QWidget()
        self.insertarError2Panel.setObjectName(u"insertarError2Panel")
        self.stackedWidget.addWidget(self.insertarError2Panel)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Proyecto Final", None))
        self.pushButton.setText("")
        self.inicio_btn.setText(QCoreApplication.translate("MainWindow", u"Inicio", None))
        self.compactar_btn.setText(QCoreApplication.translate("MainWindow", u"Compactar", None))
        self.descompactar_btn.setText(QCoreApplication.translate("MainWindow", u"Descompactar", None))
        self.verTextos_btn.setText(QCoreApplication.translate("MainWindow", u"Visualizar Textos", None))
        self.proteger_btn.setText(QCoreApplication.translate("MainWindow", u"Proteger Archivos", None))
        self.insertarError1_btn.setText(QCoreApplication.translate("MainWindow", u"Introducir 1 Error", None))
        self.insertarError2_btn.setText(QCoreApplication.translate("MainWindow", u"Introducir 2 Errores", None))
        self.titulo.setText(QCoreApplication.translate("MainWindow", u"Bienvenido", None))
    # retranslateUi

