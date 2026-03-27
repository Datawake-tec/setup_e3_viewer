import os
import zipfile


def extrair_zip(zip_path, destino):
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {zip_path}")

    if os.path.exists(destino):
        return

    os.makedirs(destino, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(destino)


def preparar_ambiente():
    if getattr(__import__("sys"), "frozen", False):
        import sys
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    resources_dir = os.path.join(base_dir, "resources")

    base_usuario = os.path.join(os.path.expanduser("~"), "SetupE3")

    extrair_zip(os.path.join(resources_dir, "Datawake.zip"), os.path.join(base_usuario, "Datawake"))
    extrair_zip(os.path.join(resources_dir, "ZebraElipse.zip"), os.path.join(base_usuario, "ZebraElipse"))
    extrair_zip(os.path.join(resources_dir, "netcat.zip"), os.path.join(base_usuario, "NetCat"))
    extrair_zip(os.path.join(resources_dir, "FonteDigital.zip"), os.path.join(base_usuario, "FonteDigital"))
    extrair_zip(os.path.join(resources_dir, "FonteExo.zip"), os.path.join(base_usuario, "FonteExo"))