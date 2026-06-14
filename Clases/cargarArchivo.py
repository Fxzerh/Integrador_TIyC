from PyQt6.QtWidgets import QFileDialog, QMessageBox, QWidget
import shutil
import os

class Cargar(QWidget):

    def seleccionar_y_guardar(self, controlador):
        ventana = controlador.mainWindow

        # Abrimos el buscador de archivos
        ruta_origen, _ = QFileDialog.getOpenFileName(
            ventana, 
            "Seleccionar archivo", 
            "", 
            "Todos los archivos (*.*)"
        )

        if ruta_origen:
            try:
                # Obtenemos la carpeta destino donde queremos guardar los archivos
                directorio_actual = os.path.dirname(os.path.abspath(__file__))
                carpeta_destino = os.path.join(directorio_actual, "..", "Archivos")
                
                # Controlamos que la carpeta destino exista
                if not os.path.exists(carpeta_destino):
                    os.makedirs(carpeta_destino)

                nombre_archivo = os.path.basename(ruta_origen)              # Obtiene el nombre del archivo
                ruta_final = os.path.join(carpeta_destino, nombre_archivo)  # Obtiene la ruta que va a tener el archivo al final, dentro de la carpeta destino

                # Copiamos el archivo del origen al destino
                shutil.copy2(ruta_origen, ruta_final)

                QMessageBox.information(self, "Éxito", f"Archivo '{nombre_archivo}' guardado correctamente.")
                if hasattr(controlador, 'refrescarPanel'):          # Si el controlador tiene el metodo refrescarPanel, lo llamamos
                    controlador.refrescarPanel()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {str(e)}")