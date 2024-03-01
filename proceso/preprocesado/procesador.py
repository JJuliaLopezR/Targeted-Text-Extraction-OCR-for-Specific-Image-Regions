from email.mime import image
import cv2
import numpy as np
import tempfile
from PIL import Image
import subprocess
import shutil
import os

print("Iniciando la aplicacion de filtros")
#borramos todo de la primera carpeta para evitar errores
carpeta_a_eliminar = './proceso/preprocesado/imagenesProcesadas'
for archivo in os.listdir(carpeta_a_eliminar):
    ruta_archivo = os.path.join(carpeta_a_eliminar, archivo)
    if os.path.isfile(ruta_archivo):
        os.remove(ruta_archivo)

#filtro cero
def gamma(input_file, output_file):
    command = f"convert {input_file} -auto-gamma {output_file}"
    subprocess.run(command, shell=True)



#primer filtro
#primer filtro, este filtro lo que hace es redistribuir los valores de la matrices entre 0 255, es decir si solo tenemos valores entre 100 y 200 al aplicar el filtro los vlaore sminimos   (100) ahora seran 0 y los maximos (200) ahora seran 255
def normal(file_path):
    img = cv2.imread(file_path)  # Lee la imagen en color original
    norm_img = np.zeros((img.shape[0], img.shape[1], img.shape[2]), dtype=np.uint8)
    img2 = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite("imagen_normalizada.JPG", img2)  # Guarda la imagen normalizada en un archivo de salida

#segundo filtro
def redim(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / max(length_x, width_y)))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.LANCZOS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename = temp_file.name
    im_resized.save('imagen_redimensionada.JPG', dpi=(300, 300))#salida del segundo filtro
    return temp_filename

#tercer filtro

def noise(file_path):
    img = cv2.imread(file_path)
    denoised_img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)  # Aplica el método de promediado no local para quitar el ruido
    cv2.imwrite("imagen_sin_ruido.JPG", denoised_img)  # Guarda la imagen sin ruido en un archivo de salida
    return denoised_img


carpeta_a = './proceso/recortador/etiquetas_recortadas'
carpeta_b = './proceso/preprocesado/imagenesProcesadas'

# Obtener la lista de archivos en la carpeta A
archivos = os.listdir(carpeta_a)

# Mover y renombrar cada archivo de la carpeta A a la carpeta B uno por uno

for archivo in archivos:
    # Crear la ruta completa del archivo en la carpeta A
    ruta_origen = os.path.join(carpeta_a, archivo)
    ruta_destino = os.path.join(carpeta_b, archivo)

    try:
        gamma(ruta_origen,'image.JPG')
        normal('image.JPG')
        redim('imagen_normalizada.JPG')
        noise('imagen_redimensionada.JPG')
        shutil.move('imagen_sin_ruido.JPG', ruta_destino)
        os.remove('image.JPG')
        os.remove('imagen_normalizada.JPG')
        os.remove('imagen_redimensionada.JPG')
    except Exception as e:
        print(f"Error en la aplicacion de filtros: '{archivo}': {e}")


