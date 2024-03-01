import subprocess

# Definir las rutas de los scripts
rutas_scripts = ['proceso/recortador/recortador.py', 'proceso/preprocesado/procesador.py', 'proceso/tesseract/tesseractUAS.py', 'proceso/comparador/comparador.py','proceso/convertidor_a_mayusculas.py']

# Función para ejecutar los scripts
def ejecutar_scripts(rutas):
    for ruta in rutas:
        try:
            # Ejecutar el script usando subprocess
            subprocess.run(['python3', ruta])
        except Exception as e:
            print(f'Ocurrió un error al ejecutar el script en {ruta}: {e}')

# Llamar a la función para ejecutar los scripts
ejecutar_scripts(rutas_scripts)
print('Extracción de texto finalizada')

