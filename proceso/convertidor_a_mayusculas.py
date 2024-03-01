import os
print("Escribiendo...")

# Ruta de la carpeta origen y destino
carpeta_origen = "./proceso/comparador/texto_extraido_corregido"
carpeta_destino = "./texto_extraido"

#borramos todo de la primera carpeta para evitar errores
for archivo in os.listdir(carpeta_destino):
    ruta_archivo = os.path.join(carpeta_destino, archivo)
    if os.path.isfile(ruta_archivo):
        os.remove(ruta_archivo)


# Obtener la lista de archivos en la carpeta origen
archivos = os.listdir(carpeta_origen)

# Iterar sobre los archivos y procesarlos
for archivo in archivos:
    # Verificar si el archivo es un archivo de texto
    if archivo.endswith(".txt"):
        # Leer el contenido del archivo y convertirlo a mayúsculas
        with open(os.path.join(carpeta_origen, archivo), "r") as file:
            contenido = file.read()
            contenido_en_mayusculas = contenido.upper()
        
        # Escribir el contenido en mayúsculas en el nuevo archivo
        with open(os.path.join(carpeta_destino, archivo), "w") as file:
            file.write(contenido_en_mayusculas)
        
        # Opcional: Eliminar el archivo original si se desea
        # os.remove(os.path.join(carpeta_origen, archivo))



