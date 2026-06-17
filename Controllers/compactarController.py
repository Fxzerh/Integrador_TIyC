from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.cargarArchivo import Cargar
from Clases.nodo import Nodo 
import json
import os


class CompactarController:
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.cargar = Cargar()
        self.directorioBase = os.path.dirname(os.path.abspath(__file__))            # Directorio Actual
        self.carpetaArchivos = os.path.join(self.directorioBase, "..", "Archivos")  # Carpeta donde se guardan los archivos

        self.fileSelect = None              # Variable para guardar el nombre del archivo que se selecciona de la tabla
        self.raiz = None                    # Variable para guardar la raiz del arbol de huffman
        self.dicCaracteres = {}             # Variable para guardar el diccionario de caracteres y sus frecuencias
        self.tablaCodigos = {}              # Variable para guardar los codigos de huffman
        self.cantNodos = 0

        # ---------- SETEOS INICIALES ---------------------------------------------------------------------------------------------------------
        try:
            self.mainWindow.tableFileC.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)   # Para que la columna ocupe el espacio libre
            self.mainWindow.tableFileC.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Para que se selecciones la fila completa
            self.mainWindow.tableFileC.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Para que permita seleccionar una fila a la vez
            self.mainWindow.tableFileC.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Para que no permita editar las celdas
            self.mainWindow.tableFileC.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
            self.cargarTabla()          # Cargamos la tabla
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.subirArchivoC_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.tableFileC.itemClicked.connect(self.mostrarArchivo)
        self.mainWindow.compactarArchivo_btn.clicked.connect(self.comprimirArchivo)
    

    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)
    
    def refrescarPanel(self):
        self.mainWindow.tableFileC.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewC.setUrl(QUrl("about:blank"))

    def cargarTabla(self):
        if os.path.exists(self.carpetaArchivos):
            files = os.listdir(self.carpetaArchivos)
            for f in files:
                fileType = os.path.splitext(f)[1]
                file_path = os.path.join(self.carpetaArchivos, f)   # Ruta completa del archivo f
                if os.path.isfile(file_path):  # Pregunta si f es un archivo (y no una carpeta)
                    # Obtenemos el tamaño de f
                    tamaño = os.path.getsize(file_path)

                    # Convertir tamaño a formato B, KB o MB
                    if tamaño < 1024:
                        tamaño_str = f"{tamaño} B"
                    elif tamaño < 1024 * 1024:
                        tamaño_str = f"{tamaño / 1024:.2f} KB"
                    else:
                        tamaño_str = f"{tamaño / (1024 * 1024):.2f} MB"
                    
                    # Agregamos el archivo a la tabla
                    rowPosition = self.mainWindow.tableFileC.rowCount()
                    self.mainWindow.tableFileC.insertRow(rowPosition)
                    self.mainWindow.tableFileC.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                    self.mainWindow.tableFileC.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño

    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileC.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            nombreArchivo = self.mainWindow.tableFileC.item(row, 0).text()
            return nombreArchivo
        return None

    def mostrarArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        ruta_completa = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(ruta_completa):
            url_local = QUrl.fromLocalFile(ruta_completa)   # Transformamos la ruta de Windows a una URL que entienda el componente web        
            self.mainWindow.viewC.setUrl(url_local)         # Setteamos la vista web que lo dibuje en pantalla

    def comprimirArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "No se ha seleccionado ningún archivo.")
            return
        rutaFile = os.path.join(self.carpetaArchivos, nombreArchivo)
        try:
            if os.path.exists(rutaFile):
                with open(rutaFile, "rb") as f:
                    contenido = f.read()
                    if len(contenido) == 0:
                        QMessageBox.warning(self.mainWindow, "Archivo Vacío", "No se puede comprimir un archivo que no contiene datos.")
                        return
                
                # CREAMOS EL ARBOL DE HUFFMAN
                self.arbolHuffman(contenido)

                # GENERAMOS LOS CODIGOS DE HUFFMAN
                self.generarCodigos(self.raiz, "")

                # COMPRIMIMOS EL CONTENIDO DEL ARCHIVO
                lista_codigos = [self.tablaCodigos[byte_val] for byte_val in contenido]     # Creamos una lista para juntar los códigos rápidamente
                bits_juntos = "".join(lista_codigos)

                cantPadding = 0
                longitud_bits = len(bits_juntos)
                cantPadding = (8 - (longitud_bits % 8)) % 8     # Calculamos la cantidad de bits de padding necesarios
                if cantPadding > 0:                             # Agregamos bits de padding (0s) para que el string sea multiplo de 8
                    bits_juntos += "0" * cantPadding
                
                bytesComprimidos = bytearray()                  # Convertimos el string de bits a bytes para poder escribirlo en el archivo binario
                for i in range(0, len(bits_juntos), 8):         # Vamos tomando de a 8 bits para convertirlos a bytes
                    bytesComprimidos.append(int(bits_juntos[i:i+8], 2))
                
                # GUARDAMOS EL ARCHIVO COMPRIMIDO
                dicParaJson = {}
                # Recorremos el diccionario original uno por uno
                for k, v in self.dicCaracteres.items():
                    # Convertimos la llave 'k' a string y le asignamos el valor 'v'
                    llave_string = str(k)
                    dicParaJson[llave_string] = v
                
                dicBytes = json.dumps(dicParaJson).encode()
                nombreFile = os.path.splitext(nombreArchivo)[0]  # Obtener el nombre del archivo sin la extensión
                #  Formato del archivo comprimido: [Header][Contenido Comprimido]
                with open(os.path.join(self.carpetaArchivos, nombreFile + ".huf"), "wb") as f:
                    # Agregamos el header 
                    f.write(cantPadding.to_bytes(1, byteorder='big'))       # Guardamos la cantidad de bits de padding en el header
                    f.write(len(dicBytes).to_bytes(4, byteorder='big'))     # Guardamos la cantidad de caractereres del diccionario en el header
                    f.write(dicBytes)                                       # Guardamos el diccionario de caracteres en el header
                    # Agregamos el contenido comprimido
                    f.write(bytesComprimidos)  
                self.dicCaracteres = {}     # Limpiamos el diccionario de caracteres para la proxima compresion
                self.tablaCodigos = {}      # Limpiamos la tabla de codigos para la proxima compresion                                 
                self.refrescarPanel()
                QMessageBox.information(self.mainWindow, "Éxito", f"Archivo comprimido con Huffman correctamente. \nGuardado en '{nombreFile}.huf'.")               
                
            else:
                QMessageBox.warning(self.mainWindow, "Error", "El archivo no existe en la ruta especificada.")
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo comprimir el archivo: {str(e)}")

    def arbolHuffman(self, texto):
        self.dicCaracteres = {}
        listNodos = []

        for byte in texto:     # Creamos el diccionario con la frecuencia de cada caracter
            self.dicCaracteres[byte] = self.dicCaracteres.get(byte, 0) + 1

        for par in self.dicCaracteres.items():      # Por cada par (caracter, frecuencia) del diccionario creamos un nodo
            nodo = Nodo(simbolo=par[0], frecuencia=par[1])
            listNodos.append(nodo)
        
        self.cantNodos = len(listNodos)
        while len(listNodos) > 1:           # Creamos nodos padres hasta llegar a la raiz y crear asi el arbol de Huffman
            listNodos.sort()                # Ordenamos la lista de nodos por frecuencia
            nodoI = listNodos.pop(0)
            nodoD = listNodos.pop(0)
            padre = Nodo(simbolo=None, frecuencia=nodoI.frecuencia + nodoD.frecuencia)  # Creamos el nodo padre de los 2 nodos con menos frecuencia
            padre.hijoIzq = nodoI
            padre.hijoDer = nodoD
            listNodos.append(padre)         # Agregamos el padre a la lista de nodos para seguir creando el arbol
        self.raiz = listNodos[0]
    
    def generarCodigos(self, nodo, codigo=""):                  # Creamos la tabla de codigos de Huffman recorriendo recursivamente el arbol
        if self.cantNodos == 1:                         # Caso especial donde el archivo original solo tiene 1 unico caracter, por lo que la raiz seria una hoja
            self.tablaCodigos[nodo.simbolo] = "0"
            return
        
        if nodo.simbolo != None:
            self.tablaCodigos[nodo.simbolo] = codigo            # Si el nodo es una hoja, guardamos el codigo en la tabla
        else:
            self.generarCodigos(nodo.hijoIzq, codigo + "0")     # Si el nodo es interno, seguimos recorriendo el arbol por izq agregando "0" al codigo
            self.generarCodigos(nodo.hijoDer, codigo + "1")     # Si el nodo es interno, seguimos recorriendo el arbol por der agregando "1" al codigo