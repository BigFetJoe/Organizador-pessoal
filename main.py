import tkinter as tk
from tkinter import ttk
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

    # Adiciona a tarefa à lista
    tarefas.append({
        "titulo": titulo,
        "data": data,
        "prioridade": prioridade,
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
    calc_score()
    for tarefa in sorted(tarefas, key=lambda x: x["score"], reverse=True):
        lista.insert(tk.END, tarefa["titulo"])


def calc_score():
    """Calcula o score de cada tarefa com base no tempo restante e prioridade."""
    hoje = dtt.now()  # Obtém a data atual uma vez para evitar múltiplas chamadas

    for tarefa in tarefas:
        try:
            # Calcula o tempo restante
            data_limite = dtt.strptime(tarefa["data"], "%d-%m").replace(year=ano)
            tempo_restante = (data_limite - hoje).days

            # Calcula o score com base no tempo restante e prioridade
            if tempo_restante < 0:
                score = 17  # Tarefa atrasada
            elif tempo_restante < 3:
                score = 10
            elif tempo_restante < 7:
                score = 5
            elif tempo_restante < 14:
                score = 2
            else:
                score = 1

            # Adiciona o peso da prioridade ao score
            score += tarefa["prioridade"] * 2

            # Atualiza o score da tarefa
            tarefa["score"] = score
            tarefa["tempo_restante"] = tempo_restante  # Adiciona o tempo restante para uso futuro

        except ValueError as e:
            print(f"Erro ao calcular score para a tarefa '{tarefa['titulo']}': {e}")
            tarefa["score"] = 999  # Define um score padrão para tarefas inválidas


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
frame_entrada.pack(padx=10, pady=10, fill="x", expand=False)

# Configuração do grid no frame_entrada
frame_entrada.grid_columnconfigure(0, weight=1)  # Coluna vazia à esquerda
frame_entrada.grid_columnconfigure(1, weight=0)  # Coluna do rótulo "Título"
frame_entrada.grid_columnconfigure(2, weight=0)  # Coluna do campo de entrada "Título"
frame_entrada.grid_columnconfigure(3, weight=1)  # Coluna vazia à direita

# Campo: Título
tk.Label(frame_entrada, text="Título:").grid(row=0, column=1, sticky="w", padx=5, pady=5)
entrada_titulo = tk.Entry(frame_entrada, width=30)
entrada_titulo.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
entrada_titulo.bind("<Return>", lambda event: adicionar_tarefa())  # Adiciona tarefa ao pressionar Enter

# Campo: Data Limite
tk.Label(frame_entrada, text="Data (DD-MM):").grid(row=1, column=1, sticky="w", padx=5, pady=5)
entrada_data = tk.Entry(frame_entrada, width=30)
entrada_data.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
entrada_data.bind("<Return>", lambda event: adicionar_tarefa())  # Adiciona tarefa ao pressionar Enter

# Campo: Prioridade
tk.Label(frame_entrada, text="Prioridade (1 a 5):").grid(row=2, column=1, sticky="w", padx=5, pady=5)
entrada_prioridade = tk.Entry(frame_entrada, width=30)
entrada_prioridade.grid(row=2, column=2, sticky="ew", padx=5, pady=5)
entrada_prioridade.bind("<Return>", lambda event: adicionar_tarefa())  # Adiciona tarefa ao pressionar Enter

entrada_titulo.focus()  # Adiciona o foco ao campo de título

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
