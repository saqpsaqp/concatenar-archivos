#!/usr/bin/env python3
import os
import sys
import argparse

def concatenar_archivos(directorio_raiz, extensiones, archivo_salida, exclusiones=None):
    """
    Recorre un directorio buscando archivos con las extensiones especificadas
    y concatena su contenido en un único archivo de salida con separadores.
    
    Args:
        directorio_raiz (str): Directorio a recorrer
        extensiones (list): Lista de extensiones de archivo a buscar (sin el punto)
        archivo_salida (str): Nombre del archivo de salida
        exclusiones (dict, optional): Diccionario con listas de patrones a excluir:
            - 'carpetas': Lista de nombres o patrones de carpetas a excluir
            - 'archivos': Lista de nombres o patrones de archivos a excluir
            - 'extensiones': Lista de extensiones a excluir (sin el punto)
    """
    # Convertir extensiones a formato .ext
    extensiones = ['.' + ext if not ext.startswith('.') else ext for ext in extensiones]
    
    # Preparar listas de exclusiones
    if exclusiones is None:
        exclusiones = {'carpetas': [], 'archivos': [], 'extensiones': []}
    
    # Asegurar que todas las claves existan
    for clave in ['carpetas', 'archivos', 'extensiones']:
        if clave not in exclusiones:
            exclusiones[clave] = []
    
    # Convertir extensiones excluidas a formato .ext
    exclusiones['extensiones'] = ['.' + ext if not ext.startswith('.') else ext for ext in exclusiones['extensiones']]
    
    # Lista para almacenar las rutas de los archivos encontrados
    archivos_encontrados = []
    
    # Recorrer el directorio de forma recursiva
    for carpeta_actual, subcarpetas, archivos in os.walk(directorio_raiz, topdown=True):
        # Filtrar subcarpetas (in-place) para evitar recorrer carpetas excluidas
        subcarpetas[:] = [d for d in subcarpetas if not any(
            patron in d for patron in exclusiones['carpetas']
        )]
        
        for archivo in archivos:
            # Verificar si el archivo tiene alguna de las extensiones buscadas
            if any(archivo.endswith(ext) for ext in extensiones):
                # Verificar si el archivo no debe ser excluido
                if not any(patron in archivo for patron in exclusiones['archivos']) and \
                   not any(archivo.endswith(ext) for ext in exclusiones['extensiones']):
                    # Construir la ruta relativa al directorio raíz
                    ruta_completa = os.path.join(carpeta_actual, archivo)
                    ruta_relativa = os.path.relpath(ruta_completa, directorio_raiz)
                    archivos_encontrados.append(ruta_relativa)
    
    # Ordenar alfabéticamente los archivos encontrados
    archivos_encontrados.sort()
    
    # Crear el archivo de salida
    with open(archivo_salida, 'w', encoding='utf-8') as salida:
        for archivo in archivos_encontrados:
            # Ruta completa del archivo
            ruta_completa = os.path.join(directorio_raiz, archivo)
            
            # Escribir el separador con el nombre del archivo
            salida.write('#---------------------------------------\n')
            salida.write(f'# {archivo}\n')
            salida.write('#---------------------------------------\n')
            
            # Leer y escribir el contenido del archivo
            try:
                with open(ruta_completa, 'r', encoding='utf-8') as entrada:
                    contenido = entrada.read()
                    salida.write(contenido)
                    
                    # Asegurar que haya una línea en blanco al final
                    if contenido and not contenido.endswith('\n'):
                        salida.write('\n')
                    salida.write('\n')
            except Exception as e:
                salida.write(f'Error al leer el archivo: {str(e)}\n\n')
    
    print(f"Se ha creado el archivo '{archivo_salida}' con {len(archivos_encontrados)} archivos concatenados.")

def main():
    parser = argparse.ArgumentParser(description='Concatena archivos de un directorio según sus extensiones.')
    parser.add_argument('directorio', help='Directorio a recorrer')
    parser.add_argument('extensiones', nargs='+', help='Extensiones de archivo a buscar (sin el punto)')
    parser.add_argument('-o', '--output', default='concatenado.txt', help='Archivo de salida (por defecto: concatenado.txt)')
    parser.add_argument('--exclude-dirs', nargs='*', default=[], help='Carpetas a excluir')
    parser.add_argument('--exclude-files', nargs='*', default=[], help='Archivos a excluir (por nombre o patrón)')
    parser.add_argument('--exclude-exts', nargs='*', default=[], help='Extensiones a excluir (sin el punto)')
    
    args = parser.parse_args()
    
    # Verificar que el directorio existe
    if not os.path.isdir(args.directorio):
        print(f"Error: El directorio '{args.directorio}' no existe.")
        sys.exit(1)
    
    # Crear diccionario de exclusiones
    exclusiones = {
        'carpetas': args.exclude_dirs,
        'archivos': args.exclude_files,
        'extensiones': args.exclude_exts
    }
    
    concatenar_archivos(args.directorio, args.extensiones, args.output, exclusiones)

if __name__ == '__main__':
    main()