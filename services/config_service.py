import json
import os
import sys


def carregar_config():
    if getattr(sys, "frozen", False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    caminho = os.path.join(base_dir, "config.json")

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)