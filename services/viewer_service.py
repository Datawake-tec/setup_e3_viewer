import os
import json
from tkinter import filedialog, messagebox


def _get_app_data_dir():
    pasta = os.path.join(os.path.expanduser("~"), "SetupE3")
    os.makedirs(pasta, exist_ok=True)
    return pasta


def _get_config_path():
    return os.path.join(_get_app_data_dir(), "viewer_path.json")


def salvar_caminho_viewer(caminho):
    with open(_get_config_path(), "w", encoding="utf-8") as f:
        json.dump({"viewer_path": caminho}, f, ensure_ascii=False, indent=2)


def carregar_caminho_viewer():
    caminho_cfg = _get_config_path()

    if not os.path.exists(caminho_cfg):
        return None

    try:
        with open(caminho_cfg, "r", encoding="utf-8") as f:
            dados = json.load(f)
            caminho = dados.get("viewer_path")
            if caminho and os.path.exists(caminho):
                return caminho
    except Exception:
        pass

    return None


def procurar_viewer_automaticamente():
    caminhos_fixos = [
        r"C:\Program Files\Elipse Software\Elipse E3\Bin32\Viewer.exe",
        r"C:\Program Files (x86)\Elipse Software\Elipse E3\Bin\Viewer.exe"
    ]

    for caminho in caminhos_fixos:
        if os.path.exists(caminho):
            return caminho

    pastas_base = [
        r"C:\Program Files\Elipse Software",
        r"C:\Program Files (x86)\Elipse Software"
    ]

    for pasta_base in pastas_base:
        if os.path.exists(pasta_base):
            for raiz, _, arquivos in os.walk(pasta_base):
                for arquivo in arquivos:
                    if arquivo.lower() == "viewer.exe":
                        return os.path.join(raiz, arquivo)

    return None


def obter_viewer():
    caminho_salvo = carregar_caminho_viewer()
    if caminho_salvo and os.path.exists(caminho_salvo):
        return caminho_salvo

    caminho_auto = procurar_viewer_automaticamente()
    if caminho_auto:
        salvar_caminho_viewer(caminho_auto)
        return caminho_auto

    messagebox.showwarning(
        "Viewer não encontrado",
        "O Viewer do Elipse não foi encontrado automaticamente.\n\n"
        "Selecione manualmente o arquivo Viewer.exe."
    )

    caminho_escolhido = filedialog.askopenfilename(
        title="Selecione o Viewer.exe",
        filetypes=[("Executável", "*.exe")]
    )

    if caminho_escolhido and os.path.exists(caminho_escolhido):
        salvar_caminho_viewer(caminho_escolhido)
        return caminho_escolhido

    raise FileNotFoundError("Viewer do Elipse não encontrado.")


def executar_viewer(viewer_path, argumentos):
    pasta_trabalho = os.path.dirname(viewer_path)
    parametros = " ".join(argumentos)

    return {
        "viewer_path": viewer_path,
        "pasta_trabalho": pasta_trabalho,
        "parametros": parametros
    }