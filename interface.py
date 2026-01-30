import tkinter as tk
from tkinter import ttk
import json

ARQUIVO = "jogador.json"

"""
O sistema esta funcionando mas ainda apresenta erro quando tenta desmarcar a tarefa e quando mexe no json para False
nao devolve os pontos, continua a pontuação
"""

# ================== SALVAR / CARREGAR ==================
def salvar_progresso():
    dados = {
        "nome": nome_jogador.get(),
        "pontos": pontos,
        "nivel": nivel,
        "sequencia": sequencia,
        "tarefas": lista_tarefas
    }
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def carregar_progresso():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "nome": "",
            "pontos": 0,
            "nivel": 1,
            "sequencia": 0,
            "tarefas": []
        }

# ================== LÓGICA ==================
def atualizar_interface():
    lbl_bem_vindo.config(text=f"👋 Bem-vindo, {nome_jogador.get() or 'Jogador'}!")
    lbl_pontos.config(text=f"Pontos: {pontos}")
    lbl_nivel.config(text=f"Nível: {nivel}")
    lbl_seq.config(text=f"Sequência: {sequencia}")
    progress["value"] = pontos
    salvar_progresso()


def concluir_tarefa():
    global pontos, nivel, sequencia

    pontos += 5
    sequencia += 1
    lbl_msg.config(text="✅ Tarefa concluída! +5 pontos")

    if sequencia == 5:
        pontos += 10
        sequencia = 0
        lbl_msg.config(text="🔥 Bônus! +10 pontos")

    if pontos >= 100:
        nivel += 1
        pontos = 0
        lbl_msg.config(text="🎉 Subiu de nível!")

    atualizar_interface()


def salvar_nome():
    atualizar_interface()

# ================== TAREFAS ==================
def adicionar_tarefa():
    texto = entry_tarefa.get().strip()
    if not texto:
        return

    lista_tarefas.append({"texto": texto, "concluida": False})
    entry_tarefa.delete(0, tk.END)
    renderizar_tarefas()
    salvar_progresso()
    

def devolver_pontos():
    global pontos, sequencia

    pontos -= 5
    sequencia = max(0, sequencia - 1)
    atualizar_interface()


def alternar_tarefa(index):
    tarefa = lista_tarefas[index]

    if not tarefa["concluida"]:
        # MARCAR
        tarefa["concluida"] = True

        if not tarefa["pontuou"]:
            tarefa["pontuou"] = True
            concluir_tarefa()

    else:
        # DESMARCAR
        tarefa["concluida"] = False

        if tarefa["pontuou"]:
            tarefa["pontuou"] = False
            devolver_pontos()

    renderizar_tarefas()


def marcar_tarefa(index):
        tarefa = lista_tarefas[index]
        if not tarefa["concluida"]:
         tarefa["concluida"] = True
        tarefa["pontuou"] = True
        concluir_tarefa()
        renderizar_tarefas()


def renderizar_tarefas():
    for widget in frame_tarefas.winfo_children():
        widget.destroy()

    for i, tarefa in enumerate(lista_tarefas):
        var = tk.BooleanVar(value=tarefa["concluida"])

        chk = tk.Checkbutton(
            frame_tarefas,
            text=tarefa["texto"],
            variable=var,
            command=lambda i=i: marcar_tarefa(i)
        )

        if tarefa["concluida"]:
            chk.config(state="disabled")

        chk.pack(anchor="w")

# ================== INTERFACE ==================
root = tk.Tk()
root.title("Gerenciador de Tarefas")
root.geometry("350x400")

dados = carregar_progresso()

pontos = dados["pontos"]
nivel = dados["nivel"]
sequencia = dados["sequencia"]
lista_tarefas = dados["tarefas"]

nome_jogador = tk.StringVar(value=dados["nome"])

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# ---------- ABA PROGRESSO ----------
aba_progresso = tk.Frame(notebook)
notebook.add(aba_progresso, text="🎮 Progresso")

lbl_bem_vindo = tk.Label(aba_progresso, font=("Arial", 12, "bold"))
lbl_bem_vindo.pack(pady=5)

tk.Label(aba_progresso, text="Nome do jogador:").pack()
tk.Entry(aba_progresso, textvariable=nome_jogador).pack()

tk.Button(aba_progresso, text="Salvar nome", command=salvar_nome).pack(pady=5)

lbl_nivel = tk.Label(aba_progresso)
lbl_nivel.pack()

lbl_pontos = tk.Label(aba_progresso)
lbl_pontos.pack()

progress = ttk.Progressbar(aba_progresso, maximum=100, length=200)
progress.pack(pady=5)

lbl_seq = tk.Label(aba_progresso)
lbl_seq.pack()

lbl_msg = tk.Label(aba_progresso)
lbl_msg.pack(pady=5)

# ---------- ABA TAREFAS ----------
aba_tarefas = tk.Frame(notebook)
notebook.add(aba_tarefas, text="📝 Tarefas")

tk.Label(aba_tarefas, text="Nova tarefa:").pack(pady=5)

entry_tarefa = tk.Entry(aba_tarefas, width=30)
entry_tarefa.pack(pady=5)

tk.Button(aba_tarefas, text="Adicionar tarefa", command=adicionar_tarefa).pack(pady=5)

frame_tarefas = tk.Frame(aba_tarefas)
frame_tarefas.pack(pady=10, fill="both")

# ================== INICIAR ==================
renderizar_tarefas()
atualizar_interface()

root.mainloop()
