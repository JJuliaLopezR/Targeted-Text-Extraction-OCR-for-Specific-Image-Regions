import pytesseract
from PIL import Image
import os

print("Iniciando la etapa de extraccion de texto")

#borramos todo de la primera carpeta para evitar errores
base_save = './proceso/tesseract/textoExtraido'
for archivo in os.listdir(base_save):
    ruta_archivo = os.path.join(base_save, archivo)
    if os.path.isfile(ruta_archivo):
        os.remove(ruta_archivo)

# Ruta base de las imágenes
base_path = './proceso/preprocesado/imagenesProcesadas'
archivos = os.listdir(base_path)

for archivo in archivos:
    image_path = os.path.join(base_path, archivo)

    # Cargar la imagen utilizando la biblioteca PIL
    image = Image.open(image_path)

    # Extraer texto de la imagen utilizando Tesseract OCR
    text = pytesseract.image_to_string(image)

    # Obtener el nombre del archivo sin la extensión
    nombre_archivo = os.path.splitext(archivo)[0]

    #Definiendo la ruta donde guardaremos el texto extraido
    ruta_txt = os.path.join(base_save, nombre_archivo + ".txt")

    # Guardar el texto extraído en el archivo de texto de salida
    with open(ruta_txt, 'w') as file:
        file.write(text)
