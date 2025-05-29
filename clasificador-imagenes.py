import os
import shutil
import time
from PIL import Image
from PIL.ExifTags import TAGS

extensiones_imagenes = (
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
    '.webp', '.heic', '.psd', '.raw', '.cr2', '.nef', '.orf', '.sr2'
)

extensiones_videos = (
    '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.mpeg',
    '.mpg', '.webm', '.3gp', '.m4v', '.mts', '.m2ts', '.ts', '.divx', '.vob'
)

def obtener_anio_exif(path_imagen):
    try:
        imagen = Image.open(path_imagen)
        exif_data = imagen._getexif()
        if exif_data:
            for tag, valor in exif_data.items():
                nombre_tag = TAGS.get(tag, tag)
                if nombre_tag == 'DateTimeOriginal':
                    return valor.split(":")[0]
    except Exception as e:
        print(f"[EXIF] Error con {path_imagen}: {e}")
    return None

def obtener_anio_archivo(path_archivo):
    try:
        timestamp = os.path.getmtime(path_archivo)
        anio = time.strftime('%Y', time.localtime(timestamp))
        return anio
    except Exception as e:
        print(f"[FS] Error con {path_archivo}: {e}")
        return None

def clasificar_archivos_por_anio(carpeta):
    print("📁 Iniciando clasificación...")
    for archivo in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, archivo)

        if not os.path.isfile(ruta_completa):
            continue

        extension = os.path.splitext(archivo)[1].lower()
        anio = None

        if extension in extensiones_imagenes:
            anio = obtener_anio_exif(ruta_completa)
            if not anio:
                anio = obtener_anio_archivo(ruta_completa)
        elif extension in extensiones_videos:
            anio = obtener_anio_archivo(ruta_completa)
        else:
            print(f"❌ Archivo no clasificado (extensión desconocida): {archivo}")
            continue

        if anio:
            carpeta_destino = os.path.join(carpeta, anio)
            os.makedirs(carpeta_destino, exist_ok=True)

            destino = os.path.join(carpeta_destino, archivo)

            # Evitar sobreescritura si ya existe
            if os.path.exists(destino):
                print(f"⚠️ Ya existe: {destino}, se omitirá.")
                continue

            shutil.move(ruta_completa, destino)
            print(f"✅ Movido: {archivo} ➜ {anio}")
        else:
            print(f"⚠️ No se pudo obtener el año de: {archivo}")

# Cambia esto a la ruta real
ruta_base = "C:/Users/TuUsuario/VideosYFotos"

if __name__ == "__main__":
    clasificar_archivos_por_anio(ruta_base)
