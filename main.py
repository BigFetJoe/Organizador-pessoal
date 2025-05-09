import tkinter as tk
from datetime import datetime as dtt
import json
import os

# --- Variáveis Globais ---
tarefas = []
ano = dtt.now().year  # Obtém o ano atual
caminho = os.path.expanduser("~/tarefas.json")  # Caminho do arquivo JSON

#\--\--\--\--\--\--\--\--\--\--\---\--\ JANELA \--\--\--\--\--\--\--\--\--\--\--\--\--\
janela = tk.Tk()
janela.title("Organizador de Tarefas")
janela.geometry("400x600")



# \--\--\--\--\--\--\--\--\--\ FUNÇÕES \--\--\--\--\--\--\--\--\--\--\--\--\--\--\--\
def adicionar_tarefa():
    """Adiciona uma nova tarefa à lista."""
    titulo = entrada_titulo.get().strip()
    data = entrada_data.get().strip()
    prioridade = entrada_prioridade.get().strip()

    if not titulo or not data or not prioridade:
        print("Erro: Todos os campos devem ser preenchidos.")
        return

    try:
        prioridade = int(prioridade)
        if prioridade < 1 or prioridade > 5:
            raise ValueError("A prioridade deve estar entre 1 e 5.")
    except ValueError as e:
        print(f"Erro: {e}")
        return

    try:
        hoje = dtt.now()
        data_limite = dtt.strptime(data, "%d-%m").replace(year=ano)
        tempo_restante = (data_limite - hoje).days
    except ValueError as e:
        print(f"Erro: {e}")
        print("Por favor, insira uma data válida no formato DD-MM.")
        return

    # Calcula o score com base no tempo restante e prioridade
    score = 0
    if tempo_restante < 0:
        score = 17  # Tarefa atrasada
    elif tempo_restante < 3:
        score += 10
    elif 3 <= tempo_restante < 7:
        score += 5
    elif 7 <= tempo_restante < 14:
        score += 2
    elif 14 <= tempo_restante:
        score += 1
    score += prioridade * 2

    # Adiciona a tarefa à lista
    tarefas.append({
        "titulo": titulo,
        "data": data,
        "prioridade": prioridade,
        "tempo_restante": tempo_restante,
        "score": score
    })

    # Limpa os campos de entrada
    entrada_titulo.delete(0, tk.END)
    entrada_data.delete(0, tk.END)
    entrada_prioridade.delete(0, tk.END)

    # Atualiza a lista e salva as tarefas
    mostrar_lista()
    salvar_tarefas()

def concluir_tarefa(event=None):
    """Conclui a tarefa selecionada no Listbox."""
    selecao = lista.curselection()
    if selecao:
        indice = selecao[0]
        tarefas.pop(indice)  # Remove a tarefa da lista
        mostrar_lista()  # Atualiza a lista exibida
        salvar_tarefas()  # Salva as alterações no arquivo JSON

def mostrar_lista():
    """Exibe as tarefas no Listbox."""
    lista.delete(0, tk.END)  # Limpa o Listbox
    for tarefa in sorted(tarefas, key=lambda x: x["score"], reverse=True):
        lista.insert(tk.END, tarefa["titulo"])

def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON."""
    if os.path.exists(caminho):
        with open(caminho, "r") as arquivo:
            return json.load(arquivo)
    return []

def salvar_tarefas():
    """Salva as tarefas no arquivo JSON."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4)

#\--\--\--\--\--\--\--\--\--\--\---\--\ WIDGETS \--\--\--\--\--\--\--\--\--\--\--\--\--\
# Frame de Título
frame_titulo = tk.Frame(janela)
frame_titulo.pack(pady=10, fill="x")
tk.Label(frame_titulo, text="Organizador de Tarefas", font=("Arial", 16)).pack()

# Frame de Entrada
frame_entrada = tk.Frame(janela)
frame_entrada.pack(padx=10, pady=10, fill="x")

# Campo: Título
tk.Label(frame_entrada, text="Título:").grid(row=0, column=0)
entrada_titulo = tk.Entry(frame_entrada, width=30)
entrada_titulo.grid(row=0, column=1)

# Campo: Data Limite
tk.Label(frame_entrada, text="Data (DD-MM):").grid(row=1, column=0)
entrada_data = tk.Entry(frame_entrada, width=30)
entrada_data.grid(row=1, column=1)

# Campo: Prioridade
tk.Label(frame_entrada, text="Prioridade (1 a 5):").grid(row=2, column=0)
entrada_prioridade = tk.Entry(frame_entrada, width=30)
entrada_prioridade.grid(row=2, column=1)

# Botão: Adicionar Tarefa
botao_adicionar = tk.Button(janela, text="Adicionar Tarefa", command=adicionar_tarefa)
botao_adicionar.pack(pady=10)

# Frame da Lista
frame_lista = tk.Frame(janela, bg="lightgray")
frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

# Título da Lista
tk.Label(frame_lista, text="Lista de Tarefas", bg="lightgray").pack(pady=5, fill="x")

# Listbox
lista = tk.Listbox(frame_lista)
lista.pack(pady=10, fill="both", expand=True)
lista.bind("<Double-Button-1>", concluir_tarefa)


#\--\--\--\--\--\--\--\--\--\--\---\--\ INICIALIZAÇÃO \--\--\--\--\--\--\--\--\--\--\--\--\--\
tarefas = carregar_tarefas()  # Carrega as tarefas do arquivo JSON
mostrar_lista()  # Exibe as tarefas carregadas

# Loop Principal
janela.mainloop()
