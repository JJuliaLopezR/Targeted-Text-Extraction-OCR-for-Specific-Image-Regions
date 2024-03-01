from PIL import Image
import numpy as np
import os

print("Iniciando la etapa de recortado")

#borramos todo de la primera carpeta para evitar errores
carpeta_a_eliminar = './proceso/recortador/etiquetas_recortadas'
for archivo in os.listdir(carpeta_a_eliminar):
    ruta_archivo = os.path.join(carpeta_a_eliminar, archivo)
    if os.path.isfile(ruta_archivo):
        os.remove(ruta_archivo)

carpeta_de_etiquetas = './ejemplares_etiquetados'
archivos = os.listdir(carpeta_de_etiquetas)

# Filtrar solo los archivos de imagen JPG
imagenes = [archivo for archivo in archivos if archivo.endswith('.JPG')]

for imagen in imagenes:
    # Construir la ruta completa de la imagen y el archivo de texto correspondiente
    ruta_imagen = os.path.join(carpeta_de_etiquetas, imagen)
    # Construir el nombre del archivo de texto correspondiente (cambiando la extensión)
    archivo_txt = os.path.splitext(imagen)[0] + '.txt'
    ruta_txt = os.path.join(carpeta_de_etiquetas, archivo_txt)
    
    # Verificar si el archivo de texto existe
    if os.path.exists(ruta_txt):
        Datos= []
        imagen = Image.open(ruta_imagen)
        datos = np.loadtxt(ruta_txt)
        renglones= datos.size/5

        ######PARA 0-No detecto nada########################################
        if(renglones==0):
            continue
      
        ######PARA 1-solo detecto una etiqueta########################################
        if renglones == 1:
            x_norm=datos[1]
            y_norm=datos[2]
            w_norm=datos[3]
            h_norm=datos[4]

            W, H = imagen.size

            x_center=x_norm*W
            y_center=y_norm*H

            w = w_norm * W
            h = h_norm * H

            x_min = x_center - (w / 2)
            y_min = y_center - (h / 2)

            x_max = x_center + (w / 2)
            y_max = y_center + (h / 2)



            imagen_recortada = imagen.crop((x_min, y_min, x_max, y_max))

            nombre_archivo = os.path.splitext(os.path.basename(imagen.filename))[0]
            ruta_carpeta_guardado = './proceso/recortador/etiquetas_recortadas'
            # Guardar la imagen recortada
            ruta_imagen_recortada = os.path.join(ruta_carpeta_guardado, f"{nombre_archivo}_recortada.JPG")
            imagen_recortada.save(ruta_imagen_recortada)
            continue

##########PARA 2 O MAS-detecto mas de una etiqueta##############################################################################################
        else:
            for i in range(0, int(renglones), 1):
                x_norm=datos[i,1]
                y_norm=datos[i,2]
                w_norm=datos[i,3]
                h_norm=datos[i,4]

                W, H = imagen.size

                x_center=x_norm*W
                y_center=y_norm*H

                w = w_norm * W
                h = h_norm * H

                x_min = x_center - (w / 2)
                y_min = y_center - (h / 2)

                x_max = x_center + (w / 2)
                y_max = y_center + (h / 2)

                imagen_recortada = imagen.crop((x_min, y_min, x_max, y_max))

                nombre_archivo = os.path.splitext(os.path.basename(imagen.filename))[0]
                ruta_carpeta_guardado = './proceso/recortador/etiquetas_recortadas'
                # Guardar la imagen recortada
                ruta_imagen_recortada = os.path.join(ruta_carpeta_guardado, f"{nombre_archivo}_recortada_{i}.JPG")
                imagen_recortada.save(ruta_imagen_recortada)
                continue
    else:
        # Si no se encuentra el archivo de texto correspondiente, puedes manejarlo aquí
        print(f'No se encontró el archivo de cordenadas correspondiente para la imagen: {ruta_imagen}')
