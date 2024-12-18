import os
import shutil
import zipfile


def add_file_to_folder(file_path, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Crear la carpeta si no existe

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")

    # Obtener el nombre del archivo
    file_name = os.path.basename(file_path)
    # Construir la nueva ruta en la carpeta de destino
    new_file_path = os.path.join(folder_path, file_name)

    # Copiar el archivo a la carpeta
    shutil.copy(file_path, new_file_path)
    print(f"Archivo '{file_name}' añadido a la carpeta '{folder_path}'.")
    return new_file_path


def compress_folder(folder_path, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)
    print(f"Carpeta comprimida con éxito en: {output_zip_path}")
    return output_zip_path


def change_zip_to_iis(zip_file_path, output_name=None):
    if not zip_file_path.endswith('.zip'):
        raise ValueError(f"El archivo '{zip_file_path}' no tiene la extensión '.zip'.")

    # Si se proporciona un nombre de salida, usarlo, sino usar el nombre del archivo original sin la extensión
    if output_name is None:
        base_name = os.path.splitext(os.path.basename(zip_file_path))[0]
    else:
        base_name = output_name

    # Cambiar la extensión a .iis
    iis_file_path = os.path.join(os.path.dirname(zip_file_path), f"{base_name}.iis")
    os.rename(zip_file_path, iis_file_path)
    print(f"Archivo renombrado de '{zip_file_path}' a '{iis_file_path}'.")
    return iis_file_path


# Caso práctico
def create_translation_package(file_path, base_folder, output_name=None):
    # Crear la carpeta base "Translation"
    translation_folder = os.path.join(base_folder, "Translation")
    os.makedirs(translation_folder, exist_ok=True)
    print(f"Directorio creado: {translation_folder}")

    # Crear la subcarpeta "result" dentro de "Translation"
    result_folder = os.path.join(translation_folder, "result")
    os.makedirs(result_folder, exist_ok=True)
    print(f"Directorio creado: {result_folder}")

    # Añadir el archivo dado a la carpeta "result"
    add_file_to_folder(file_path, result_folder)

    # Comprimir la carpeta "result" a un archivo ZIP
    zip_file_path = os.path.join(translation_folder, "result.zip")
    compress_folder(result_folder, zip_file_path)

    # Renombrar el archivo ZIP a .iis (con nombre personalizado si se proporciona)
    iis_file_path = change_zip_to_iis(zip_file_path, output_name)

    print(f"Paquete de traducción creado: {iis_file_path}")
    return iis_file_path


# Ejemplo de uso
file = r'C:\Emulation\Process Trainer MV-31\project.xml'  # Ruta del archivo
base_folder = r'C:\Emulation\Process Trainer MV-31'       # Carpeta base
output_name = "custom_name"  # Nombre personalizado para el archivo .iis

create_translation_package(file, base_folder, output_name)
