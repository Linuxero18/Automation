import os
import shutil
import time
from datetime import datetime
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

def obtener_fecha_exif(path_imagen):
    """Obtiene la fecha original de una imagen desde los datos EXIF"""
    try:
        imagen = Image.open(path_imagen)
        exif_data = imagen._getexif()
        if exif_data:
            for tag, valor in exif_data.items():
                nombre_tag = TAGS.get(tag, tag)
                if nombre_tag == 'DateTimeOriginal':
                    # Formato: "YYYY:MM:DD HH:MM:SS"
                    fecha_str = valor.split(" ")[0]  # Solo tomar la fecha
                    return datetime.strptime(fecha_str, "%Y:%m:%d")
    except Exception as e:
        print(f"[EXIF] Error con {path_imagen}: {e}")
    return None

def obtener_fecha_archivo(path_archivo):
    """Obtiene la fecha de modificación del archivo"""
    try:
        timestamp = os.path.getmtime(path_archivo)
        return datetime.fromtimestamp(timestamp)
    except Exception as e:
        print(f"[FS] Error con {path_archivo}: {e}")
        return None

def clasificar_archivos(carpeta, por_mes=False):
    """
    Clasifica archivos por año o por año/mes según el parámetro por_mes
    
    Args:
        carpeta (str): Ruta de la carpeta a organizar
        por_mes (bool): Si es True, clasifica por año/mes. Si es False, solo por año
    """
    print(f"📁 Iniciando clasificación {'por mes' if por_mes else 'por año'}...")
    
    archivos_procesados = 0
    archivos_omitidos = 0
    archivos_error = 0
    
    for archivo in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, archivo)

        # Saltar si no es un archivo
        if not os.path.isfile(ruta_completa):
            continue

        extension = os.path.splitext(archivo)[1].lower()
        fecha = None

        # Obtener fecha según el tipo de archivo
        if extension in extensiones_imagenes:
            # Para imágenes, intentar primero EXIF, luego fecha del archivo
            fecha = obtener_fecha_exif(ruta_completa)
            if not fecha:
                fecha = obtener_fecha_archivo(ruta_completa)
        elif extension in extensiones_videos:
            # Para videos, usar fecha del archivo
            fecha = obtener_fecha_archivo(ruta_completa)
        else:
            print(f"❌ Archivo no clasificado (extensión desconocida): {archivo}")
            archivos_error += 1
            continue

        if fecha:
            if por_mes:
                # Formato: YYYY/MM-Nombre_Mes
                nombre_mes = fecha.strftime("%m-%B")  # Ejemplo: "01-January"
                carpeta_anio = os.path.join(carpeta, str(fecha.year))
                carpeta_destino = os.path.join(carpeta_anio, nombre_mes)
            else:
                # Solo año
                carpeta_destino = os.path.join(carpeta, str(fecha.year))
            
            # Crear carpetas si no existen
            os.makedirs(carpeta_destino, exist_ok=True)
            destino = os.path.join(carpeta_destino, archivo)

            # Evitar sobreescritura si ya existe
            if os.path.exists(destino):
                print(f"⚠️ Ya existe: {destino}, se omitirá.")
                archivos_omitidos += 1
                continue

            # Mover archivo
            try:
                shutil.move(ruta_completa, destino)
                if por_mes:
                    print(f"✅ Movido: {archivo} ➜ {fecha.year}/{nombre_mes}")
                else:
                    print(f"✅ Movido: {archivo} ➜ {fecha.year}")
                archivos_procesados += 1
            except Exception as e:
                print(f"❌ Error moviendo {archivo}: {e}")
                archivos_error += 1
        else:
            print(f"⚠️ No se pudo obtener la fecha de: {archivo}")
            archivos_error += 1

    # Mostrar resumen
    print("\n📊 RESUMEN:")
    print(f"✅ Archivos procesados: {archivos_procesados}")
    print(f"⚠️ Archivos omitidos: {archivos_omitidos}")
    print(f"❌ Archivos con error: {archivos_error}")

def main():
    """Función principal"""
    # Cambia esto a la ruta real de tu carpeta
    ruta_base = "C:/Users/TuUsuario/VideosYFotos"
    
    # PARÁMETRO PRINCIPAL: Cambiar a True para clasificar por mes
    CLASIFICAR_POR_MES = False
    
    print("🚀 Organizador de Fotos y Videos")
    print(f"📂 Carpeta: {ruta_base}")
    print(f"📅 Modo: {'Por año/mes' if CLASIFICAR_POR_MES else 'Solo por año'}")
    print("-" * 50)
    
    # Verificar que la carpeta existe
    if not os.path.exists(ruta_base):
        print(f"❌ Error: La carpeta {ruta_base} no existe")
        return
    
    # Ejecutar clasificación
    clasificar_archivos(ruta_base, por_mes=CLASIFICAR_POR_MES)
    print("\n🎉 Clasificación completada.")

if __name__ == "__main__":
    main()