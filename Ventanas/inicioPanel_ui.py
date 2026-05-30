# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'inicioPanel.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Inicio(object):
    def setupUi(self, Inicio):
        if not Inicio.objectName():
            Inicio.setObjectName(u"Inicio")
        Inicio.resize(1280, 720)
        self.gridLayout = QGridLayout(Inicio)
        self.gridLayout.setObjectName(u"gridLayout")
        self.addError1_btn = QPushButton(Inicio)
        self.addError1_btn.setObjectName(u"addError1_btn")
        self.addError1_btn.setMaximumSize(QSize(1100, 70))
        self.addError1_btn.setAutoDefault(True)
        self.addError1_btn.setFlat(True)

        self.gridLayout.addWidget(self.addError1_btn, 5, 1, 1, 1)

        self.showFiles_btn_2 = QPushButton(Inicio)
        self.showFiles_btn_2.setObjectName(u"showFiles_btn_2")
        self.showFiles_btn_2.setMaximumSize(QSize(1100, 70))
        self.showFiles_btn_2.setFlat(True)

        self.gridLayout.addWidget(self.showFiles_btn_2, 3, 1, 1, 1)

        self.compact_btn = QPushButton(Inicio)
        self.compact_btn.setObjectName(u"compact_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.compact_btn.sizePolicy().hasHeightForWidth())
        self.compact_btn.setSizePolicy(sizePolicy)
        self.compact_btn.setMaximumSize(QSize(1000, 70))
        self.compact_btn.setSizeIncrement(QSize(0, 0))
        self.compact_btn.setBaseSize(QSize(0, 0))
        self.compact_btn.setAutoFillBackground(False)
        self.compact_btn.setAutoDefault(False)
        self.compact_btn.setFlat(True)

        self.gridLayout.addWidget(self.compact_btn, 1, 1, 1, 1)

        self.menuLabel = QLabel(Inicio)
        self.menuLabel.setObjectName(u"menuLabel")
        self.menuLabel.setMaximumSize(QSize(400, 65))
        font = QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setHintingPreference(QFont.PreferNoHinting)
        self.menuLabel.setFont(font)
        self.menuLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.menuLabel, 0, 1, 1, 1)

        self.protect_btn = QPushButton(Inicio)
        self.protect_btn.setObjectName(u"protect_btn")
        self.protect_btn.setMaximumSize(QSize(1100, 70))
        self.protect_btn.setFlat(True)

        self.gridLayout.addWidget(self.protect_btn, 4, 1, 1, 1)

        self.decompact_btn = QPushButton(Inicio)
        self.decompact_btn.setObjectName(u"decompact_btn")
        self.decompact_btn.setMaximumSize(QSize(1100, 70))
        self.decompact_btn.setFlat(True)

        self.gridLayout.addWidget(self.decompact_btn, 2, 1, 1, 1)

        self.addError2_btn = QPushButton(Inicio)
        self.addError2_btn.setObjectName(u"addError2_btn")
        self.addError2_btn.setMaximumSize(QSize(1100, 70))
        self.addError2_btn.setAutoDefault(True)
        self.addError2_btn.setFlat(True)

        self.gridLayout.addWidget(self.addError2_btn, 6, 1, 1, 1)


        self.retranslateUi(Inicio)

        self.showFiles_btn_2.setDefault(False)
        self.compact_btn.setDefault(False)
        self.decompact_btn.setDefault(False)


        QMetaObject.connectSlotsByName(Inicio)
    # setupUi

    def retranslateUi(self, Inicio):
        Inicio.setWindowTitle(QCoreApplication.translate("Inicio", u"Form", None))
        self.addError1_btn.setText(QCoreApplication.translate("Inicio", u"Introducir 1 Error", None))
        self.showFiles_btn_2.setText(QCoreApplication.translate("Inicio", u"Visualizar Textos", None))
        self.compact_btn.setText(QCoreApplication.translate("Inicio", u"Compactar", None))
        self.menuLabel.setText(QCoreApplication.translate("Inicio", u"Menu", None))
        self.protect_btn.setText(QCoreApplication.translate("Inicio", u"Proteger Archivos", None))
        self.decompact_btn.setText(QCoreApplication.translate("Inicio", u"Descompactar", None))
        self.addError2_btn.setText(QCoreApplication.translate("Inicio", u"Introducir 2 Errores", None))
    # retranslateUi

