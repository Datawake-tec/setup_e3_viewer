# setup_e3_viewer

### DESCRIÇÃO
O SetupE3 é uma aplicação desenvolvida para automatizar e padronizar a configuração do Viewer do Elipse E3 em ambiente industrial. A ferramenta permite configurar parâmetros de execução de forma rápida, segura e padronizada, eliminando a necessidade de permissões administrativas.

### OBJETIVO
•	Padronizar a configuração do Viewer
•	Reduzir erros operacionais
•	Automatizar a criação de atalhos
•	Evitar execução direta do Viewer

### CARACTERÍSTICAS
•	Automação da configuração
•	Execução sem necessidade de administrador
•	Interface gráfica simples (Tkinter)
•	Parametrização dinâmica
•	Criação automática de atalhos

### CONCEITO
O SetupE3 funciona como um launcher, ou seja, uma aplicação responsável por preparar e configurar a execução de outro sistema. Neste caso, o sistema prepara o ambiente de execução do Viewer do Elipse E3, sem realizar sua abertura automática.

### FUNCIONALIDADES
•	Localização automática do Viewer.exe
•	Seleção manual do Viewer
•	Salvamento do caminho do Viewer
•	Configuração de parâmetros (Linha, Estação, etc.)
•	Criação e atualização de atalhos
•	Execução sem necessidade de privilégios administrativos

### INSTALAÇÃO
Gerar executável:
pyinstaller --onefile --noconsole --name SetupE3 main.py

### USO
•	Informar o servidor
•	Selecionar o projeto
•	Selecionar o quadro
•	Preencher os parâmetros
•	Executar

### FLUXO DE FUNCIONAMENTO
•	Usuário informa servidor
•	Seleciona projeto
•	Seleciona quadro
•	Preenche parâmetros
•	Sistema localiza o Viewer
•	Sistema monta argumentos
•	Sistema cria ou atualiza atalho
•	Sistema salva configuração
•	Viewer não é executado

### ESTRUTURA DO PROJETO
SetupE3_Python/
├── main.py
├── services/
│   ├── config_service.py
│   ├── viewer_service.py
│   ├── setup_service.py
│   └── shortcut_service.py

### DESCRIÇÃO DOS MÓDULOS
main.py – Interface gráfica e controle principal
config_service.py – Gerenciamento de configurações
viewer_service.py – Localização e preparação do Viewer
setup_service.py – Configuração inicial do ambiente
shortcut_service.py – Criação e atualização de atalhos

### REQUISITOS
•	Python 3.8+
•	Tkinter
•	Viewer do Elipse E3 instalado

### OBSERVAÇÕES
•	O Viewer não é executado automaticamente
•	O sistema não requer privilégios administrativos
•	Configuração armazenada localmente

### ARQUIVO DE CONFIGURAÇÃO (config.json)
O sistema utiliza um arquivo de configuração local (config.json) para armazenar informações necessárias ao funcionamento da aplicação de forma persistente.
Esse arquivo é responsável por guardar dados que precisam ser reutilizados entre execuções, evitando que o usuário tenha que repetir configurações sempre que o sistema for iniciado.
•	Finalidade:
•	Armazenar o caminho do executável do Viewer do Elipse E3
•	Manter configurações da aplicação entre execuções
•	Facilitar a automação do processo de configuração
Funcionamento:
Na primeira execução, o sistema localiza ou solicita o caminho do Viewer. Essa informação é salva no arquivo config.json e reutilizada automaticamente nas execuções seguintes.
Exemplo de conteúdo:
{
  "viewer_path": "C:\\Program Files\\Elipse Software\\Elipse E3\\Bin32\\Viewer.exe"
}
Localização:
C:\Users\USUARIO\SetupE3\
•	Observações:
•	O arquivo é gerado automaticamente pelo sistema
•	Não armazena informações sensíveis
•	Pode ser removido para forçar nova configuração
•	Garante maior praticidade e padronização no uso da aplicação
