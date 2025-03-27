# Concatenador de Archivos

Este script permite recorrer un directorio (incluidos subdirectorios) y concatenar en un único archivo de texto el contenido de todos los archivos encontrados que coincidan con las extensiones especificadas.

## Características

- Recorre directorios y subdirectorios de forma recursiva
- Permite especificar múltiples extensiones de archivo
- Sistema flexible de exclusiones para:
  - Carpetas específicas (ej: `node_modules`, `.git`)
  - Archivos por nombre o patrón (ej: `test_`, `_temp`)
  - Extensiones no deseadas (ej: `pyc`, `min.js`)
- Ordena los archivos alfabéticamente
- Añade separadores claros con la ruta relativa de cada archivo
- Maneja errores de lectura de archivos
- Configurable mediante argumentos de línea de comandos

## Requisitos

- Python 3.6 o superior

## Instalación

1. Descarga el archivo `concatenar_archivos.py`
2. Asegúrate de que tenga permisos de ejecución (opcional):
   ```bash
   chmod +x concatenar_archivos.py
   ```

## Uso

```bash
python concatenar_archivos.py [directorio] [extensiones...] [-o archivo_salida] [--exclude-dirs ...] [--exclude-files ...] [--exclude-exts ...]
```

### Parámetros

- `directorio`: La carpeta que se recorrerá en busca de archivos
- `extensiones`: Una o más extensiones de archivo a buscar (sin el punto)
- `-o, --output`: Nombre del archivo de salida (opcional, por defecto: `concatenado.txt`)
- `--exclude-dirs`: Lista de carpetas a excluir (opcional)
- `--exclude-files`: Lista de archivos a excluir por nombre o patrón (opcional)
- `--exclude-exts`: Lista de extensiones a excluir (opcional, sin el punto)

### Ejemplos

1. Concatenar todos los archivos Python en un directorio:
   ```bash
   python concatenar_archivos.py ./mi_proyecto py
   ```

2. Concatenar archivos con múltiples extensiones:
   ```bash
   python concatenar_archivos.py ./mi_proyecto py js txt
   ```

3. Especificar un nombre de archivo de salida:
   ```bash
   python concatenar_archivos.py ./mi_proyecto py -o codigo_python.txt
   ```

4. Usar el script con rutas absolutas:
   ```bash
   python concatenar_archivos.py /home/usuario/proyectos/mi_app java -o codigo_java.txt
   ```

5. Excluir carpetas específicas:
   ```bash
   python concatenar_archivos.py ./mi_proyecto py --exclude-dirs node_modules .git venv
   ```

6. Excluir archivos por patrón:
   ```bash
   python concatenar_archivos.py ./mi_proyecto py --exclude-files test_ _temp
   ```

7. Excluir extensiones:
   ```bash
   python concatenar_archivos.py ./mi_proyecto py --exclude-exts pyc pyo
   ```

8. Combinación de exclusiones:
   ```bash
   python concatenar_archivos.py ./mi_proyecto py js --exclude-dirs node_modules --exclude-files config --exclude-exts min.js
   ```

## Formato del Archivo de Salida

El archivo generado tendrá el siguiente formato:

```
#---------------------------------------
# ruta/relativa/al/archivo1.ext
#---------------------------------------
... contenido del archivo1.ext

#---------------------------------------
# ruta/relativa/al/archivo2.ext
#---------------------------------------
... contenido del archivo2.ext

... y así sucesivamente
```

## Casos de Uso

Este script es útil para:

- Crear una copia de seguridad legible de código fuente
- Preparar código para revisión o impresión
- Consolidar archivos de configuración dispersos
- Combinar archivos de registro para análisis
- Generar documentación que incluya fragmentos de código

## Solución de Problemas

- **Problema**: El script muestra "Error al leer el archivo"
  **Solución**: Verifica que tengas permisos de lectura para todos los archivos

- **Problema**: Caracteres extraños en el archivo generado
  **Solución**: El script usa codificación UTF-8. Si tus archivos usan otra codificación, modifica las líneas `encoding='utf-8'` en el código

- **Problema**: Las exclusiones no funcionan como se espera
  **Solución**: Las exclusiones funcionan mediante la búsqueda de subcadenas, no con patrones regex o glob. Por ejemplo, `--exclude-dirs temp` excluirá cualquier carpeta que contenga "temp" en su nombre (como "temp", "temporary", "template")

## Limitaciones

- El script está diseñado para archivos de texto. No funcionará correctamente con archivos binarios
- Para conjuntos muy grandes de archivos, considera el uso de archivos temporales para evitar problemas de memoria

## Licencia

Este script se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.