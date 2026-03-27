import os
import subprocess
import tempfile


def criar_ou_substituir_atalho(viewer_path, argumentos_str, novo_nome):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    atalho_existente = None

    for arquivo in os.listdir(desktop):
        if arquivo.endswith(".lnk"):
            atalho_existente = os.path.join(desktop, arquivo)
            break

    novo_caminho = os.path.join(desktop, f"{novo_nome}.lnk")

    if atalho_existente:
        try:
            os.rename(atalho_existente, novo_caminho)
        except Exception:
            if os.path.exists(atalho_existente):
                os.remove(atalho_existente)

    working_dir = os.path.dirname(viewer_path)

    script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{novo_caminho}")
$Shortcut.TargetPath = "{viewer_path}"
$Shortcut.Arguments = '{argumentos_str}'
$Shortcut.WorkingDirectory = "{working_dir}"
$Shortcut.Description = "Viewer E3"
$Shortcut.Save()
'''

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ps1", mode="w", encoding="utf-8") as f:
        f.write(script)
        script_path = f.name

    try:
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
            check=True
        )
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)