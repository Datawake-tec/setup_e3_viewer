import tkinter as tk
from tkinter import ttk, messagebox
import traceback

from services.config_service import carregar_config
from services.viewer_service import obter_viewer, executar_viewer
from services.setup_service import preparar_ambiente
from services.shortcut_service import criar_ou_substituir_atalho


COR_FUNDO = "#414141"
COR_TEXTO = "#FFFFFF"
COR_BOTAO = "#FDBD13"


class SetupE3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Setup E3")
        self.root.geometry("420x520")
        self.root.configure(bg=COR_FUNDO)

        self.config = carregar_config()
        self.projeto_atual = None
        self.quadro_atual = None
        self.param_entries = {}

        self.criar_interface()

        # Se quiser ativar depois
        # preparar_ambiente()

    def criar_interface(self):
        frame = tk.Frame(self.root, bg=COR_FUNDO)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(frame, text="Servidor / Nome da Máquina", fg=COR_TEXTO, bg=COR_FUNDO).pack(anchor="w")
        self.entry_servidor = tk.Entry(frame)
        self.entry_servidor.pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="Projeto", fg=COR_TEXTO, bg=COR_FUNDO).pack(anchor="w")
        self.combo_projeto = ttk.Combobox(frame, state="readonly")
        self.combo_projeto.pack(fill="x", pady=(0, 10))
        self.combo_projeto["values"] = [p["nome"] for p in self.config["projetos"]]
        self.combo_projeto.bind("<<ComboboxSelected>>", self.on_projeto_change)

        tk.Label(frame, text="Quadro", fg=COR_TEXTO, bg=COR_FUNDO).pack(anchor="w")
        self.combo_quadro = ttk.Combobox(frame, state="readonly")
        self.combo_quadro.pack(fill="x", pady=(0, 10))
        self.combo_quadro.bind("<<ComboboxSelected>>", self.on_quadro_change)

        self.frame_parametros = tk.Frame(frame, bg=COR_FUNDO)
        self.frame_parametros.pack(fill="x", pady=(10, 10))

        self.btn_executar = tk.Button(
            frame,
            text="Executar",
            bg=COR_BOTAO,
            fg="black",
            height=2,
            command=self.executar
        )
        self.btn_executar.pack(fill="x", pady=(20, 0))

    def on_projeto_change(self, event=None):
        nome_projeto = self.combo_projeto.get()

        self.projeto_atual = next(
            (p for p in self.config["projetos"] if p["nome"] == nome_projeto),
            None
        )

        if self.projeto_atual:
            self.combo_quadro["values"] = [q["nome"] for q in self.projeto_atual["quadros"]]
            self.combo_quadro.set("")
            self.limpar_parametros()

    def on_quadro_change(self, event=None):
        nome_quadro = self.combo_quadro.get()

        if not self.projeto_atual:
            return

        self.quadro_atual = next(
            (q for q in self.projeto_atual["quadros"] if q["nome"] == nome_quadro),
            None
        )

        self.montar_parametros()

    def limpar_parametros(self):
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()
        self.param_entries = {}

    def montar_parametros(self):
        self.limpar_parametros()

        if not self.quadro_atual:
            return

        for param in self.quadro_atual["parametros"]:
            tk.Label(
                self.frame_parametros,
                text=param,
                fg=COR_TEXTO,
                bg=COR_FUNDO
            ).pack(anchor="w")

            entry = tk.Entry(self.frame_parametros)
            entry.pack(fill="x", pady=(0, 8))

            self.param_entries[param] = entry

    def executar(self):
        try:
            servidor = self.entry_servidor.get().strip()

            if not servidor:
                messagebox.showwarning("Aviso", "Informe o servidor.")
                return

            if not self.quadro_atual:
                messagebox.showwarning("Aviso", "Selecione um quadro.")
                return

            viewer = obter_viewer()

            argumentos_lista = [
                servidor,
                "-screen", self.quadro_atual["nome"],
                "-params"
            ]

            parametros_str_lista = []
            for param in self.quadro_atual["parametros"]:
                valor = self.param_entries[param].get().strip()
                parametros_str_lista.append(f"{param}={valor}")
                argumentos_lista.append(f"{param}={valor}")

            argumentos_str = (
                f'{servidor} -screen {self.quadro_atual["nome"]} -params '
                + " ".join(parametros_str_lista)
            )

            nome_atalho = "Viewer"
            if "bancada" in self.param_entries:
                bancada_valor = self.param_entries["bancada"].get().strip()
                if bancada_valor:
                    nome_atalho = bancada_valor

            criar_ou_substituir_atalho(viewer, argumentos_str, nome_atalho)

            # Agora só prepara, não abre
            executar_viewer(viewer, argumentos_lista)

            messagebox.showinfo(
                "Sucesso",
                f"Propriedades atualizadas e atalho '{nome_atalho}' atualizado.\n\n"
            )

        except Exception as e:
            erro = f"Erro em executar():\n{e}\n\n{traceback.format_exc()}"
            print(erro)
            messagebox.showerror("Erro", erro)


if __name__ == "__main__":
    print("Iniciando aplicação...")
    root = tk.Tk()
    app = SetupE3App(root)
    root.mainloop()