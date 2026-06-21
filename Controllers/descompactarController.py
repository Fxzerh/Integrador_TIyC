from PyQt6.QtWidgets import QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QUrl
from Clases.nodo import Nodo
from Clases.cargarArchivo import Cargar
import json
import os


class DescompactarController:
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
            self.mainWindow.tableFileDC.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)   # Para que la columna ocupe el espacio libre
            self.mainWindow.tableFileDC.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Para que se selecciones la fila completa
            self.mainWindow.tableFileDC.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)    # Para que permita seleccionar una fila a la vez
            self.mainWindow.tableFileDC.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)      # Para que no permita editar las celdas
            self.mainWindow.tableFileDC.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
            self.cargarTabla()          # Cargamos la tabla
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo cargar la tabla: {str(e)}")

        # ---------------------------- ACCIONES Y EVENTOS ---------------------------------------------------------------------------------------------------------
        self.mainWindow.subirArchivoDC_btn.clicked.connect(lambda: self.cargar.seleccionar_y_guardar(self))
        self.mainWindow.tableFileDC.itemClicked.connect(self.mostrarArchivo)
        self.mainWindow.descompactarArchivo_btn.clicked.connect(self.descomprimirArchivo)
        

    
    def cambiarPanel (self, indice):
        self.mainWindow.cambiar_pantalla(indice)
    
    def refrescarPanel(self):
        self.mainWindow.tableFileDC.setRowCount(0)
        self.cargarTabla()
        self.mainWindow.viewDC.setUrl(QUrl("about:blank"))

    def cargarTabla(self):
        if os.path.exists(self.carpetaArchivos):
            files = os.listdir(self.carpetaArchivos)
            for f in files:
                fileType = os.path.splitext(f)[1]
                if fileType in [".huf"]:
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
                        rowPosition = self.mainWindow.tableFileDC.rowCount()
                        self.mainWindow.tableFileDC.insertRow(rowPosition)
                        self.mainWindow.tableFileDC.setItem(rowPosition, 0, QTableWidgetItem(f))             # Nombre
                        self.mainWindow.tableFileDC.setItem(rowPosition, 1, QTableWidgetItem(tamaño_str))    # Tamaño
    
    def obtenerSeleccionado(self):
        selectedRows = self.mainWindow.tableFileDC.selectionModel().selectedRows()
        if selectedRows:
            row = selectedRows[0].row()
            nombreArchivo = self.mainWindow.tableFileDC.item(row, 0).text()
            return nombreArchivo
        return None
    
    def mostrarArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        ruta_completa = os.path.join(self.carpetaArchivos, nombreArchivo)
        if os.path.exists(ruta_completa):
            url_local = QUrl.fromLocalFile(ruta_completa)   # Transformamos la ruta de Windows a una URL que entienda el componente web        
            self.mainWindow.viewDC.setUrl(url_local)         # Setteamos la vista web que lo dibuje en pantalla

    def descomprimirArchivo(self):
        nombreArchivo = self.obtenerSeleccionado()
        if not nombreArchivo:
            QMessageBox.warning(self.mainWindow, "Aviso", "No se ha seleccionado ningún archivo.")
            return
        rutaFile = os.path.join(self.carpetaArchivos, nombreArchivo)
        try:
            if os.path.exists(rutaFile):
                with open(rutaFile, "rb") as f:
                    # Extraemos la informacion del heap del archivo comprimido
                    padding = f.read(1)
                    cantPadding = int.from_bytes(padding, byteorder='big')      # Obtenemos la cantidad de bits que son de relleno (padding)
                    tamañoDic = f.read(4)
                    longDic = int.from_bytes(tamañoDic, byteorder='big')        # Obtenemos la longitud del diccionario (en bytes) para luego leerlo
                    dicBytes = f.read(longDic)                                  # Recuperamos el diccionario con las frecuencias de cada caracter
                    dicAux = json.loads(dicBytes.decode())          # Convertimos el diccionario de bytes a un diccionario de python
                    self.dicCaracteres = {}
                    for caracter, frecuencia in dicAux.items():
                        llaveInt = int(caracter)
                        self.dicCaracteres[llaveInt] = frecuencia
                    
                    # Recuperamos el contenido comprimido del archivo
                    contenido = f.read()
                    lista_bits = [format(byte, '08b') for byte in contenido]    # Convertimos todos los bytes a binario en una lista y los unimos
                    strBytes = "".join(lista_bits)

                    if cantPadding > 0:
                        strBytes = strBytes[:-cantPadding]               # Eliminamos los bits de relleno (padding) del ultimo byte

                    # Reconstruir el arbol de Huffman
                    self.reconstruirArbol()
                    # Descomprimimos el texto
                    textoOriginal = self.descomprimirTexto(strBytes)

                    # Guardamos el archivo descomprimido
                    # Si el stem ya tiene una extensión conocida (ej: foto.HA2), la conservamos sin agregar .dhu
                    nombreFile = os.path.splitext(nombreArchivo)[0]
                    extensiones_conocidas = {".pdf", ".png", ".jpg", ".zip", ".txt",
                                             ".HA1", ".HA2", ".HA3", ".HE1", ".HE2", ".HE3",
                                             ".H1E1", ".H1E2", ".H1E3", ".H2E1", ".H2E2", ".H2E3"}
                    _, extStem = os.path.splitext(nombreFile)
                    if extStem in extensiones_conocidas:
                        archivoFinal = nombreFile          # foto.HA2.huf → foto.HA2
                    else:
                        archivoFinal = nombreFile + ".dhu" # foto.huf → foto.dhu
                    with open(os.path.join(self.carpetaArchivos, archivoFinal), "wb") as f:
                        f.write(textoOriginal)
                    self.refrescarPanel()

                    QMessageBox.information(self.mainWindow, "Éxito", f"Archivo descomprimido correctamente. \nGuardado en '{archivoFinal}'.")                    
            else:
                QMessageBox.warning(self.mainWindow, "Error", "El archivo no existe en la ruta especificada.")
        except Exception as e:
            QMessageBox.critical(self.mainWindow, "Error", f"No se pudo descomprimir el archivo: {str(e)}")

    def reconstruirArbol(self):
        listNodos = []
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
    
    def descomprimirTexto(self, textoComprimido):
        nodoActual = self.raiz                              # Agarramos la raiz para recorrer el arbol de huffman generado
        textoDescomprimido = bytearray()
        for bit in textoComprimido:     
            if self.cantNodos != 1:                         # Por cada caracter del archivo comprimido recorremos el arbol
                if bit == "0":
                    nodoActual = nodoActual.hijoIzq                 # Si el bit es 0 vamos al hijo izquierdo
                else:
                    nodoActual = nodoActual.hijoDer                 # Si el bit es 1 vamos al hijo derecho
                
                if nodoActual.simbolo != None:                      # Si el simbolo del nodo es distinto a None, llegamos a una hoja por lo que es un simbolo del texto original
                    textoDescomprimido.append(nodoActual.simbolo)   # Agregamos el simbolo al texto descomprimido
                    nodoActual = self.raiz                          # Volvemos a la raiz para seguir recorriendo el arbol con los siguientes bits del texto comprimido

            else:                   
                textoDescomprimido.append(nodoActual.simbolo)       # Caso especial en donde el archivo original solo tiene 1 caracter, por lo que la raiz es una hoja

        return bytes(textoDescomprimido)