import re
import os
import Levenshtein
from unidecode import unidecode

#esta funcion lo que hace es agarrrar el archivo y dividirlo por espacios, cada cadena de carcateres entre es espacio es un elemento de lista 
#escupe la lista
def cargar_palabras(archivo):
    with open(archivo, 'r') as file:
        palabras = file.read().split()
    return palabras

def cargar_palabras_desde_carpeta(carpeta):
    palabras = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".txt"):
            ruta_completa = os.path.join(carpeta, archivo)
            with open(ruta_completa, "r", encoding="utf-8") as archivo_txt:
                contenido = archivo_txt.read()
                palabras.extend(contenido.split())  # Dividir el contenido en palabras
    return palabras

#ESTA LO QUE HACE ES AGARRAR UNA PALABRA (palabra) y la busca en una lista (palabras), Y TE DEVUELVE CUAL ES LA PALABRA QUE MAS SE PARECE DE LA LISTA RESPECTO A LA QUE METISTE 

#Levenshtein.distance(s1, s2, *, weights=(1, 1, 1), processor=None, score_cutoff=None) #ejemplo documentacion
def encontrar_palabra_similar(palabra, palabras):
    distancia_minima = 1000000
    distancia_minima2= 1000000
    palabra_similares = []
    palabra_min = palabra.lower()

    for p in palabras:
        
        p_min = p.lower()
      
        distancia = Levenshtein.distance(palabra_min, p_min,score_cutoff=distancia_minima)
        
        if distancia <= distancia_minima:
            
            distancia_minima = distancia
            palabra_similares.append(p)
            if distancia_minima==0:
                return p
    palabra_min_uni=unidecode(palabra_min)
    for palabra in palabra_similares:
        palabra=palabra.lower()
        palabraUni=unidecode(palabra)
        distancia = Levenshtein.distance(palabra_min_uni, palabraUni)
        if distancia < distancia_minima2: #debe ser <= para detectar de que diccionario viene
            distancia_minima2 = distancia
            palabra_similar=palabra
    return palabra_similar


#elimina todos los guiones agrupados
def eliminar_consecutivos(match):
    return match.group(1).replace("-", "")

def comparar_palabras(OCR, carpeta_diccionario, corregido, nombre_archivo):
    #palabras_diccionario = cargar_palabras(diccionario)
    palabras_diccionario = cargar_palabras_desde_carpeta(carpeta_diccionario)

    with open(OCR, 'r') as file:
        texto_extraido = file.read()
    
    # Eliminar todos los guiones antes de saltos de línea y unir palabras
    while re.search(r'(-+)\n', texto_extraido):
        texto_extraido = re.sub(r'(-+)\n', eliminar_consecutivos, texto_extraido)


    #separadores
    palabras_extraidas = re.findall(r'[^\s+,\.\(\)/\'"#:;#&$°%£"“_”—’=-]+', texto_extraido)

    palabras_sustitutas = []
 
    total_distancia = 0  # Contador para la suma de distancias
    total_palabras = 0   # Contador para el número total de palabras mal escritas
    
    #for palabra_extraida in palabras_extraidas:
    #    palabras_separadas = re.split(r'[\+,\.\(\)/\'"#:;]', palabra_extraida)
    
    for palabra_extraida in palabras_extraidas:
#palabras que no se que el ocr fallaba conmunente
        if palabra_extraida.lower() == "avifia":
            palabra_extraida = "aviña"
        if palabra_extraida.lower() == "cal":
            palabra_extraida = "col"
        if palabra_extraida.lower() == "avia":
            palabra_extraida = "aviña"
        if palabra_extraida.lower() == "cafiada":
            palabra_extraida = "cañada"
        if palabra_extraida.lower() == "aviha":
            palabra_extraida = "aviña"
        if palabra_extraida.lower() == "comin":
            palabra_extraida = "común"
        if palabra_extraida.lower() == "arrollo":
            palabra_extraida = "arroyo"
        if palabra_extraida.lower() == "jestis":
            palabra_extraida = "jesus"
        if palabra_extraida.lower() == "aviiia":
            palabra_extraida = "aviña"
        if palabra_extraida.lower() == "jess":
            palabra_extraida = "jesus"
        if palabra_extraida.lower() == "cahada":
            palabra_extraida = "cañada"
        if palabra_extraida.lower() == "l6pez":
            palabra_extraida = "López"
        if palabra_extraida.lower() == "lépez":
            palabra_extraida = "López"
        if palabra_extraida.lower() == "allo":
            palabra_extraida = "alto"
        if palabra_extraida.lower() == "avihia":
            palabra_extraida = "aviña"
        if palabra_extraida.lower() == "kouth":
            palabra_extraida = "Kunth"
        if palabra_extraida.lower() == "avifa":
            palabra_extraida = "aviña"
        if palabra_extraida.lower() == "aviria":
            palabra_extraida = "aviña"
        if palabra_extraida.lower() == "barial":
            palabra_extraida = "barrial"
        if palabra_extraida.lower() == "ldépez":
            palabra_extraida = "Loópez"
        palabra_similar = encontrar_palabra_similar(palabra_extraida, palabras_diccionario)
        distancia = Levenshtein.distance(palabra_extraida.lower(), palabra_similar.lower())
        total_distancia += distancia
        total_palabras += 1

        #palabra_similar = '+'.join(palabras_terminadas)
        palabras_sustitutas.append(palabra_similar)

    texto_corregido = re.sub(r'[^\s+,\.\(\)/\'"#:;#&$°%£"“_”—’=-]+', lambda x: palabras_sustitutas.pop(0), texto_extraido)

    with open(corregido, 'w') as file:
        file.write(texto_corregido)
    
    # Calcular el promedio de la distancia de Levenshtein
    if total_palabras==0:
        promedio_distancia=0
    else:
        promedio_distancia = total_distancia / total_palabras
    print("Promedio Leven:", promedio_distancia)
    archivo_resultados.write(f"{nombre_archivo}, Promedio Leven: {promedio_distancia}\n")

print("Iniciando la etapa de correccion")

#borramos todo de la primera carpeta para evitar errores
carpeta_a_eliminar = './proceso/comparador/texto_extraido_corregido'
for archivo in os.listdir(carpeta_a_eliminar):
    ruta_archivo = os.path.join(carpeta_a_eliminar, archivo)
    if os.path.isfile(ruta_archivo):
        os.remove(ruta_archivo)

ruta_carpeta_de_diccionarios = './proceso/diccionarios/diccionarios'
extension = '.txt'

carpeta_entrada = './proceso/tesseract/textoExtraido'


carpeta_salida = './proceso/comparador/texto_extraido_corregido'
#####
# Ruta base de las imágenes
base_path = './proceso/tesseract/textoExtraido'
archivos = os.listdir(base_path)
archivo_resultados = open('Promedio_de_distancias.txt', 'w')
for archivo in archivos:
    text_in = os.path.join(base_path, archivo)

    # Obtener el nombre del archivo sin la extensión
    nombre_archivo = os.path.splitext(archivo)[0]
    text_out= os.path.join(carpeta_salida, nombre_archivo + ".txt")


    comparar_palabras(text_in, ruta_carpeta_de_diccionarios, text_out, nombre_archivo)

archivo_resultados.close()