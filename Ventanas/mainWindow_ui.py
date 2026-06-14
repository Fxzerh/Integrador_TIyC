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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHeaderView,
    QLabel, QLayout, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QLabel{\n"
"	font: 700 \"Yu Gothic UI\";\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(200, 0))
        self.frame.setStyleSheet(u"QPushButton{\n"
"	background-color: transparent;\n"
"	border: 1px;\n"
"	font: 11pt \"Yu Gothic UI\";\n"
"	height: 50px;\n"
"	text-align: left;\n"
"	padding-left: 20px;\n"
"}\n"
"QPushButton:hover{\n"
"	Background-color: #4a4a4a;\n"
"}")
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

        self.insertarError_btn = QPushButton(self.frame)
        self.insertarError_btn.setObjectName(u"insertarError_btn")

        self.verticalLayout.addWidget(self.insertarError_btn)

        self.desproteger_btn = QPushButton(self.frame)
        self.desproteger_btn.setObjectName(u"desproteger_btn")

        self.verticalLayout.addWidget(self.desproteger_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"Qlabel{\n"
"	font: \"Yu Gothic UI\";\n"
"}")
        self.inicioPanel = QWidget()
        self.inicioPanel.setObjectName(u"inicioPanel")
        self.inicioPanel.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.inicioPanel)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(15, 15, 20, 15)
        self.compactarInicio_btn = QPushButton(self.inicioPanel)
        self.compactarInicio_btn.setObjectName(u"compactarInicio_btn")
        self.compactarInicio_btn.setMinimumSize(QSize(0, 120))
        font2 = QFont()
        font2.setFamilies([u"Yu Gothic UI"])
        font2.setPointSize(20)
        font2.setBold(False)
        self.compactarInicio_btn.setFont(font2)

        self.gridLayout.addWidget(self.compactarInicio_btn, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 3, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 1, 1, 2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 3, 3, 1)

        self.desprotegerInicio_btn = QPushButton(self.inicioPanel)
        self.desprotegerInicio_btn.setObjectName(u"desprotegerInicio_btn")
        self.desprotegerInicio_btn.setMinimumSize(QSize(0, 120))
        font3 = QFont()
        font3.setFamilies([u"Yu Gothic UI"])
        font3.setPointSize(20)
        self.desprotegerInicio_btn.setFont(font3)

        self.gridLayout.addWidget(self.desprotegerInicio_btn, 4, 2, 1, 1)

        self.verTextosInicio_btn = QPushButton(self.inicioPanel)
        self.verTextosInicio_btn.setObjectName(u"verTextosInicio_btn")
        self.verTextosInicio_btn.setMinimumSize(QSize(0, 120))
        self.verTextosInicio_btn.setFont(font3)

        self.gridLayout.addWidget(self.verTextosInicio_btn, 3, 1, 1, 1)

        self.descompactarInicio_btn = QPushButton(self.inicioPanel)
        self.descompactarInicio_btn.setObjectName(u"descompactarInicio_btn")
        self.descompactarInicio_btn.setMinimumSize(QSize(0, 120))
        self.descompactarInicio_btn.setFont(font3)

        self.gridLayout.addWidget(self.descompactarInicio_btn, 2, 2, 1, 1)

        self.insertarErrorInicio_btn = QPushButton(self.inicioPanel)
        self.insertarErrorInicio_btn.setObjectName(u"insertarErrorInicio_btn")
        self.insertarErrorInicio_btn.setMinimumSize(QSize(0, 120))
        self.insertarErrorInicio_btn.setFont(font3)

        self.gridLayout.addWidget(self.insertarErrorInicio_btn, 4, 1, 1, 1)

        self.protegerInicio_btn = QPushButton(self.inicioPanel)
        self.protegerInicio_btn.setObjectName(u"protegerInicio_btn")
        self.protegerInicio_btn.setMinimumSize(QSize(0, 120))
        self.protegerInicio_btn.setFont(font3)

        self.gridLayout.addWidget(self.protegerInicio_btn, 3, 2, 1, 1)

        self.titulo = QLabel(self.inicioPanel)
        self.titulo.setObjectName(u"titulo")
        font4 = QFont()
        font4.setFamilies([u"Yu Gothic UI"])
        font4.setPointSize(40)
        font4.setBold(True)
        font4.setItalic(False)
        self.titulo.setFont(font4)
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.titulo, 0, 1, 1, 2)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(2, 3)
        self.gridLayout.setRowStretch(3, 3)
        self.gridLayout.setRowStretch(4, 3)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 1)
        self.stackedWidget.addWidget(self.inicioPanel)
        self.compactarPanel = QWidget()
        self.compactarPanel.setObjectName(u"compactarPanel")
        font5 = QFont()
        font5.setFamilies([u"Yu Gothic UI"])
        font5.setPointSize(9)
        font5.setBold(False)
        self.compactarPanel.setFont(font5)
        self.gridLayout_3 = QGridLayout(self.compactarPanel)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(15, 15, 20, 15)
        self.label_3 = QLabel(self.compactarPanel)
        self.label_3.setObjectName(u"label_3")
        font6 = QFont()
        font6.setFamilies([u"Yu Gothic UI"])
        font6.setPointSize(12)
        font6.setBold(True)
        font6.setItalic(False)
        self.label_3.setFont(font6)

        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.verticalSpacer_5, 5, 0, 1, 3)

        self.subirArchivoC_btn = QPushButton(self.compactarPanel)
        self.subirArchivoC_btn.setObjectName(u"subirArchivoC_btn")
        self.subirArchivoC_btn.setMinimumSize(QSize(200, 60))
        font7 = QFont()
        font7.setFamilies([u"Yu Gothic UI"])
        font7.setPointSize(12)
        self.subirArchivoC_btn.setFont(font7)

        self.gridLayout_3.addWidget(self.subirArchivoC_btn, 6, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_8 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.verticalSpacer_8, 2, 0, 1, 3)

        self.compactarArchivo_btn = QPushButton(self.compactarPanel)
        self.compactarArchivo_btn.setObjectName(u"compactarArchivo_btn")
        self.compactarArchivo_btn.setMinimumSize(QSize(300, 60))
        self.compactarArchivo_btn.setFont(font7)

        self.gridLayout_3.addWidget(self.compactarArchivo_btn, 6, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.tableWidgetC = QTableWidget(self.compactarPanel)
        if (self.tableWidgetC.columnCount() < 3):
            self.tableWidgetC.setColumnCount(3)
        font8 = QFont()
        font8.setFamilies([u"Yu Gothic UI"])
        font8.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font8)
        self.tableWidgetC.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font8)
        self.tableWidgetC.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font8)
        self.tableWidgetC.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidgetC.setObjectName(u"tableWidgetC")
        self.tableWidgetC.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_3.addWidget(self.tableWidgetC, 4, 0, 1, 1)

        self.webEngineViewC = QWebEngineView(self.compactarPanel)
        self.webEngineViewC.setObjectName(u"webEngineViewC")
        self.webEngineViewC.setUrl(QUrl(u"about:blank"))

        self.gridLayout_3.addWidget(self.webEngineViewC, 4, 2, 1, 1)

        self.label_2 = QLabel(self.compactarPanel)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setFont(font4)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 3)

        self.label_4 = QLabel(self.compactarPanel)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font6)

        self.gridLayout_3.addWidget(self.label_4, 3, 2, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 4, 1, 1, 1)

        self.gridLayout_3.setRowStretch(4, 3)
        self.gridLayout_3.setRowStretch(6, 2)
        self.gridLayout_3.setColumnStretch(0, 2)
        self.gridLayout_3.setColumnStretch(2, 3)
        self.stackedWidget.addWidget(self.compactarPanel)
        self.descompactarPanel = QWidget()
        self.descompactarPanel.setObjectName(u"descompactarPanel")
        font9 = QFont()
        font9.setFamilies([u"Yu Gothic UI"])
        self.descompactarPanel.setFont(font9)
        self.gridLayout_4 = QGridLayout(self.descompactarPanel)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(15, 15, 20, 15)
        self.descompactarArchivo_btn = QPushButton(self.descompactarPanel)
        self.descompactarArchivo_btn.setObjectName(u"descompactarArchivo_btn")
        self.descompactarArchivo_btn.setMinimumSize(QSize(300, 60))
        self.descompactarArchivo_btn.setFont(font7)

        self.gridLayout_4.addWidget(self.descompactarArchivo_btn, 5, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_6 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_4.addItem(self.verticalSpacer_6, 4, 0, 1, 3)

        self.webEngineViewDC = QWebEngineView(self.descompactarPanel)
        self.webEngineViewDC.setObjectName(u"webEngineViewDC")
        self.webEngineViewDC.setUrl(QUrl(u"about:blank"))

        self.gridLayout_4.addWidget(self.webEngineViewDC, 3, 2, 1, 1)

        self.label_5 = QLabel(self.descompactarPanel)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font4)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 3)

        self.label_7 = QLabel(self.descompactarPanel)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font6)

        self.gridLayout_4.addWidget(self.label_7, 2, 2, 1, 1)

        self.subirArchivoDC_btn = QPushButton(self.descompactarPanel)
        self.subirArchivoDC_btn.setObjectName(u"subirArchivoDC_btn")
        self.subirArchivoDC_btn.setMinimumSize(QSize(200, 60))
        self.subirArchivoDC_btn.setFont(font7)

        self.gridLayout_4.addWidget(self.subirArchivoDC_btn, 5, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.tableWidgetDC = QTableWidget(self.descompactarPanel)
        if (self.tableWidgetDC.columnCount() < 3):
            self.tableWidgetDC.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font8)
        self.tableWidgetDC.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font8)
        self.tableWidgetDC.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        font10 = QFont()
        font10.setFamilies([u"Yu Gothic UI"])
        font10.setBold(True)
        font10.setKerning(True)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font10)
        self.tableWidgetDC.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.tableWidgetDC.setObjectName(u"tableWidgetDC")
        self.tableWidgetDC.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tableWidgetDC.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_4.addWidget(self.tableWidgetDC, 3, 0, 1, 1)

        self.label_6 = QLabel(self.descompactarPanel)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font6)

        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_4.addItem(self.verticalSpacer_7, 1, 0, 1, 3)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_6, 3, 1, 1, 1)

        self.gridLayout_4.setRowStretch(3, 3)
        self.gridLayout_4.setRowStretch(5, 2)
        self.gridLayout_4.setColumnStretch(0, 2)
        self.gridLayout_4.setColumnStretch(2, 3)
        self.stackedWidget.addWidget(self.descompactarPanel)
        self.verTextosPanel = QWidget()
        self.verTextosPanel.setObjectName(u"verTextosPanel")
        font11 = QFont()
        font11.setFamilies([u"Segoe UI Black"])
        self.verTextosPanel.setFont(font11)
        self.gridLayout_5 = QGridLayout(self.verTextosPanel)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(15, 15, 20, 15)
        self.verticalSpacer_9 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_5.addItem(self.verticalSpacer_9, 4, 2, 1, 1)

        self.webEngineViewVT_R = QWebEngineView(self.verTextosPanel)
        self.webEngineViewVT_R.setObjectName(u"webEngineViewVT_R")
        self.webEngineViewVT_R.setUrl(QUrl(u"about:blank"))

        self.gridLayout_5.addWidget(self.webEngineViewVT_R, 5, 2, 1, 1)

        self.label_10 = QLabel(self.verTextosPanel)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font6)

        self.gridLayout_5.addWidget(self.label_10, 2, 2, 1, 1)

        self.label_8 = QLabel(self.verTextosPanel)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font4)
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 3)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_4, 3, 1, 1, 1)

        self.webEngineViewVT_O = QWebEngineView(self.verTextosPanel)
        self.webEngineViewVT_O.setObjectName(u"webEngineViewVT_O")
        self.webEngineViewVT_O.setUrl(QUrl(u"about:blank"))

        self.gridLayout_5.addWidget(self.webEngineViewVT_O, 3, 2, 1, 1)

        self.label_9 = QLabel(self.verTextosPanel)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font6)

        self.gridLayout_5.addWidget(self.label_9, 2, 0, 1, 1)

        self.tableWidgetVT = QTableWidget(self.verTextosPanel)
        if (self.tableWidgetVT.columnCount() < 3):
            self.tableWidgetVT.setColumnCount(3)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font8)
        self.tableWidgetVT.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font8)
        self.tableWidgetVT.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font8)
        self.tableWidgetVT.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        self.tableWidgetVT.setObjectName(u"tableWidgetVT")
        self.tableWidgetVT.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_5.addWidget(self.tableWidgetVT, 3, 0, 3, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_5.addItem(self.verticalSpacer_14, 1, 0, 1, 3)

        self.gridLayout_5.setRowStretch(3, 2)
        self.gridLayout_5.setRowStretch(5, 2)
        self.gridLayout_5.setColumnStretch(0, 1)
        self.gridLayout_5.setColumnStretch(2, 2)
        self.stackedWidget.addWidget(self.verTextosPanel)
        self.protegerPanel = QWidget()
        self.protegerPanel.setObjectName(u"protegerPanel")
        self.gridLayout_6 = QGridLayout(self.protegerPanel)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(15, 15, 20, 15)
        self.subirArchivoP_btn = QPushButton(self.protegerPanel)
        self.subirArchivoP_btn.setObjectName(u"subirArchivoP_btn")
        self.subirArchivoP_btn.setMinimumSize(QSize(200, 60))
        self.subirArchivoP_btn.setFont(font7)

        self.gridLayout_6.addWidget(self.subirArchivoP_btn, 7, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer_10 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_6.addItem(self.verticalSpacer_10, 1, 0, 1, 5)

        self.label_13 = QLabel(self.protegerPanel)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font6)

        self.gridLayout_6.addWidget(self.label_13, 4, 2, 1, 1)

        self.hamming16384_btn = QPushButton(self.protegerPanel)
        self.hamming16384_btn.setObjectName(u"hamming16384_btn")
        self.hamming16384_btn.setMinimumSize(QSize(0, 60))
        self.hamming16384_btn.setFont(font7)

        self.gridLayout_6.addWidget(self.hamming16384_btn, 7, 4, 1, 1)

        self.hamming1024_btn = QPushButton(self.protegerPanel)
        self.hamming1024_btn.setObjectName(u"hamming1024_btn")
        self.hamming1024_btn.setMinimumSize(QSize(0, 60))
        self.hamming1024_btn.setFont(font7)

        self.gridLayout_6.addWidget(self.hamming1024_btn, 7, 3, 1, 1)

        self.tableWidgetP = QTableWidget(self.protegerPanel)
        if (self.tableWidgetP.columnCount() < 3):
            self.tableWidgetP.setColumnCount(3)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setFont(font8)
        self.tableWidgetP.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font8)
        self.tableWidgetP.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFont(font8)
        self.tableWidgetP.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        self.tableWidgetP.setObjectName(u"tableWidgetP")
        self.tableWidgetP.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetP.verticalHeader().setCascadingSectionResizes(False)

        self.gridLayout_6.addWidget(self.tableWidgetP, 5, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_5, 5, 1, 1, 1)

        self.label_12 = QLabel(self.protegerPanel)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font6)

        self.gridLayout_6.addWidget(self.label_12, 4, 0, 1, 1)

        self.webEngineViewP = QWebEngineView(self.protegerPanel)
        self.webEngineViewP.setObjectName(u"webEngineViewP")
        self.webEngineViewP.setUrl(QUrl(u"about:blank"))

        self.gridLayout_6.addWidget(self.webEngineViewP, 5, 2, 1, 3)

        self.label_11 = QLabel(self.protegerPanel)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font4)
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_6.addWidget(self.label_11, 0, 0, 1, 5)

        self.hamming8_btn = QPushButton(self.protegerPanel)
        self.hamming8_btn.setObjectName(u"hamming8_btn")
        self.hamming8_btn.setMinimumSize(QSize(0, 60))
        self.hamming8_btn.setFont(font7)

        self.gridLayout_6.addWidget(self.hamming8_btn, 7, 2, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_6.addItem(self.verticalSpacer_11, 6, 0, 1, 5)

        self.gridLayout_6.setRowStretch(5, 3)
        self.gridLayout_6.setRowStretch(7, 2)
        self.gridLayout_6.setColumnStretch(0, 2)
        self.gridLayout_6.setColumnStretch(2, 1)
        self.gridLayout_6.setColumnStretch(3, 1)
        self.gridLayout_6.setColumnStretch(4, 1)
        self.stackedWidget.addWidget(self.protegerPanel)
        self.insertarErrorPanel = QWidget()
        self.insertarErrorPanel.setObjectName(u"insertarErrorPanel")
        self.gridLayout_7 = QGridLayout(self.insertarErrorPanel)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(15, 15, 20, 15)
        self.insertar1Error_btn = QPushButton(self.insertarErrorPanel)
        self.insertar1Error_btn.setObjectName(u"insertar1Error_btn")
        self.insertar1Error_btn.setMinimumSize(QSize(300, 60))
        self.insertar1Error_btn.setFont(font7)

        self.gridLayout_7.addWidget(self.insertar1Error_btn, 5, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.label_14 = QLabel(self.insertarErrorPanel)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font4)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.label_14, 0, 0, 1, 4)

        self.subirArchivoIE_btn = QPushButton(self.insertarErrorPanel)
        self.subirArchivoIE_btn.setObjectName(u"subirArchivoIE_btn")
        self.subirArchivoIE_btn.setMinimumSize(QSize(200, 60))
        self.subirArchivoIE_btn.setFont(font7)

        self.gridLayout_7.addWidget(self.subirArchivoIE_btn, 5, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.insertar2Errores_btn = QPushButton(self.insertarErrorPanel)
        self.insertar2Errores_btn.setObjectName(u"insertar2Errores_btn")
        self.insertar2Errores_btn.setMinimumSize(QSize(300, 60))
        self.insertar2Errores_btn.setFont(font7)

        self.gridLayout_7.addWidget(self.insertar2Errores_btn, 5, 3, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.tableWidgetIE = QTableWidget(self.insertarErrorPanel)
        if (self.tableWidgetIE.columnCount() < 3):
            self.tableWidgetIE.setColumnCount(3)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFont(font8)
        self.tableWidgetIE.setHorizontalHeaderItem(0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFont(font8)
        self.tableWidgetIE.setHorizontalHeaderItem(1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFont(font8)
        self.tableWidgetIE.setHorizontalHeaderItem(2, __qtablewidgetitem14)
        self.tableWidgetIE.setObjectName(u"tableWidgetIE")
        self.tableWidgetIE.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_7.addWidget(self.tableWidgetIE, 3, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_7, 3, 1, 1, 1)

        self.label_15 = QLabel(self.insertarErrorPanel)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font6)

        self.gridLayout_7.addWidget(self.label_15, 2, 0, 1, 1)

        self.label_16 = QLabel(self.insertarErrorPanel)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font6)

        self.gridLayout_7.addWidget(self.label_16, 2, 2, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_7.addItem(self.verticalSpacer_12, 1, 0, 1, 4)

        self.webEngineViewIE = QWebEngineView(self.insertarErrorPanel)
        self.webEngineViewIE.setObjectName(u"webEngineViewIE")
        self.webEngineViewIE.setUrl(QUrl(u"about:blank"))

        self.gridLayout_7.addWidget(self.webEngineViewIE, 3, 2, 1, 2)

        self.verticalSpacer_13 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_7.addItem(self.verticalSpacer_13, 4, 0, 1, 4)

        self.gridLayout_7.setRowStretch(3, 3)
        self.gridLayout_7.setRowStretch(5, 2)
        self.gridLayout_7.setColumnStretch(0, 2)
        self.gridLayout_7.setColumnStretch(2, 2)
        self.gridLayout_7.setColumnStretch(3, 2)
        self.stackedWidget.addWidget(self.insertarErrorPanel)
        self.desprotegerPanel = QWidget()
        self.desprotegerPanel.setObjectName(u"desprotegerPanel")
        self.gridLayout_8 = QGridLayout(self.desprotegerPanel)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(15, 15, 20, 15)
        self.desprotegerArchivo_btn = QPushButton(self.desprotegerPanel)
        self.desprotegerArchivo_btn.setObjectName(u"desprotegerArchivo_btn")
        self.desprotegerArchivo_btn.setMinimumSize(QSize(300, 60))
        self.desprotegerArchivo_btn.setFont(font7)

        self.gridLayout_8.addWidget(self.desprotegerArchivo_btn, 5, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer_8 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_8, 3, 1, 1, 1)

        self.subirArchivoDP_btn = QPushButton(self.desprotegerPanel)
        self.subirArchivoDP_btn.setObjectName(u"subirArchivoDP_btn")
        self.subirArchivoDP_btn.setMinimumSize(QSize(200, 60))
        self.subirArchivoDP_btn.setFont(font7)

        self.gridLayout_8.addWidget(self.subirArchivoDP_btn, 5, 0, 1, 1, Qt.AlignmentFlag.AlignHCenter)

        self.tableWidgetDP = QTableWidget(self.desprotegerPanel)
        if (self.tableWidgetDP.columnCount() < 3):
            self.tableWidgetDP.setColumnCount(3)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFont(font8)
        self.tableWidgetDP.setHorizontalHeaderItem(0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFont(font8)
        self.tableWidgetDP.setHorizontalHeaderItem(1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFont(font8)
        self.tableWidgetDP.setHorizontalHeaderItem(2, __qtablewidgetitem17)
        self.tableWidgetDP.setObjectName(u"tableWidgetDP")
        self.tableWidgetDP.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_8.addWidget(self.tableWidgetDP, 3, 0, 1, 1)

        self.label_19 = QLabel(self.desprotegerPanel)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font6)

        self.gridLayout_8.addWidget(self.label_19, 2, 2, 1, 1)

        self.webEngineViewDP = QWebEngineView(self.desprotegerPanel)
        self.webEngineViewDP.setObjectName(u"webEngineViewDP")
        self.webEngineViewDP.setUrl(QUrl(u"about:blank"))

        self.gridLayout_8.addWidget(self.webEngineViewDP, 3, 2, 1, 1)

        self.label_17 = QLabel(self.desprotegerPanel)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font4)
        self.label_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_8.addWidget(self.label_17, 0, 0, 1, 3)

        self.label_18 = QLabel(self.desprotegerPanel)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font6)

        self.gridLayout_8.addWidget(self.label_18, 2, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_8.addItem(self.verticalSpacer_3, 4, 0, 1, 3)

        self.verticalSpacer_4 = QSpacerItem(20, 25, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_8.addItem(self.verticalSpacer_4, 1, 0, 1, 3)

        self.gridLayout_8.setRowStretch(3, 3)
        self.gridLayout_8.setRowStretch(5, 2)
        self.gridLayout_8.setColumnStretch(0, 2)
        self.gridLayout_8.setColumnStretch(2, 3)
        self.stackedWidget.addWidget(self.desprotegerPanel)

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)


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
        self.insertarError_btn.setText(QCoreApplication.translate("MainWindow", u"Introducir Error", None))
        self.desproteger_btn.setText(QCoreApplication.translate("MainWindow", u"Desproteger", None))
        self.compactarInicio_btn.setText(QCoreApplication.translate("MainWindow", u"Compactar", None))
        self.desprotegerInicio_btn.setText(QCoreApplication.translate("MainWindow", u"Desproteger", None))
        self.verTextosInicio_btn.setText(QCoreApplication.translate("MainWindow", u"Ver Textos", None))
        self.descompactarInicio_btn.setText(QCoreApplication.translate("MainWindow", u"Descompactar", None))
        self.insertarErrorInicio_btn.setText(QCoreApplication.translate("MainWindow", u"Insertar Error", None))
        self.protegerInicio_btn.setText(QCoreApplication.translate("MainWindow", u"Proteger Archivo", None))
        self.titulo.setText(QCoreApplication.translate("MainWindow", u"Bienvenido", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Seleccione el archivo a compactar:", None))
        self.subirArchivoC_btn.setText(QCoreApplication.translate("MainWindow", u"Subir Archivo", None))
        self.compactarArchivo_btn.setText(QCoreApplication.translate("MainWindow", u"Compactar Archivo", None))
        ___qtablewidgetitem = self.tableWidgetC.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Archivo", None))
        ___qtablewidgetitem1 = self.tableWidgetC.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        ___qtablewidgetitem2 = self.tableWidgetC.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Compactar Archivo", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Contenido del archivo:", None))
        self.descompactarArchivo_btn.setText(QCoreApplication.translate("MainWindow", u"Descompactar Archivo", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Descompactar Archivo", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Contenido del archivo:", None))
        self.subirArchivoDC_btn.setText(QCoreApplication.translate("MainWindow", u"Subir Archivo", None))
        ___qtablewidgetitem3 = self.tableWidgetDC.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Archivo", None))
        ___qtablewidgetitem4 = self.tableWidgetDC.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        ___qtablewidgetitem5 = self.tableWidgetDC.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Seleccione el archivo a descompactar:", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Contenidos:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Comparacion de Textos", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Seleccione un archivo:", None))
        ___qtablewidgetitem6 = self.tableWidgetVT.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Archivo", None))
        ___qtablewidgetitem7 = self.tableWidgetVT.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        ___qtablewidgetitem8 = self.tableWidgetVT.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o", None))
        self.subirArchivoP_btn.setText(QCoreApplication.translate("MainWindow", u"Subir Archivo", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Contenido del archivo:", None))
        self.hamming16384_btn.setText(QCoreApplication.translate("MainWindow", u"Modulo 16384", None))
        self.hamming1024_btn.setText(QCoreApplication.translate("MainWindow", u"Modulo 1024", None))
        ___qtablewidgetitem9 = self.tableWidgetP.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Archivo", None))
        ___qtablewidgetitem10 = self.tableWidgetP.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        ___qtablewidgetitem11 = self.tableWidgetP.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Seleccione el archivo a proteger:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Proteger Archivo", None))
        self.hamming8_btn.setText(QCoreApplication.translate("MainWindow", u"Modulo 8", None))
        self.insertar1Error_btn.setText(QCoreApplication.translate("MainWindow", u"Insertar 1 error", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Insertar Error al Archivo", None))
        self.subirArchivoIE_btn.setText(QCoreApplication.translate("MainWindow", u"Subir Archivo", None))
        self.insertar2Errores_btn.setText(QCoreApplication.translate("MainWindow", u"Insertar 2 errores", None))
        ___qtablewidgetitem12 = self.tableWidgetIE.horizontalHeaderItem(0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Archivo", None))
        ___qtablewidgetitem13 = self.tableWidgetIE.horizontalHeaderItem(1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        ___qtablewidgetitem14 = self.tableWidgetIE.horizontalHeaderItem(2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Seleccione el archivo a insertar error:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Contenido del archivo:", None))
        self.desprotegerArchivo_btn.setText(QCoreApplication.translate("MainWindow", u"Desproteger Archivo", None))
        self.subirArchivoDP_btn.setText(QCoreApplication.translate("MainWindow", u"Subir Archivo", None))
        ___qtablewidgetitem15 = self.tableWidgetDP.horizontalHeaderItem(0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Archivo", None))
        ___qtablewidgetitem16 = self.tableWidgetDP.horizontalHeaderItem(1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Tipo", None))
        ___qtablewidgetitem17 = self.tableWidgetDP.horizontalHeaderItem(2)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Contenido del archivo:", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Desproteger Archivo", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Seleccione el archivo a desproteger:", None))
    # retranslateUi

