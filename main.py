import tkinter as tk
from datetime import datetime as dtt

# Declaração de variáveis globais
tarefas = []
ano = dtt.now().year  # Obtém o ano atual
hoje = dtt.now()

# Cria a janela principal
janela = tk.Tk()  # Instância da janela principal
janela.title("Organizador de Tarefas")  # Título da janela
janela.geometry("400x600")  # Tamanho: largura x altura em pixels

# --- Frame de entrada ---
frame_entrada = tk.Frame(janela)
frame_entrada.pack(padx=10, fill="x")

# Campo: Título
tk.Label(frame_entrada, text="Título:").grid(row=0, column=0)
entrada_titulo = tk.Entry(frame_entrada, width=30)
entrada_titulo.grid(row=0, column=1)


# Campo: Data limite
tk.Label(frame_entrada, text="Data (DD-MM):").grid(row=1, column=0)
entrada_data = tk.Entry(frame_entrada, width=30)
entrada_data.grid(row=1, column=1)

# Campo: Prioridade
tk.Label(frame_entrada, text="Prioridade (1 a 5):").grid(row=2, column=0)
entrada_prioridade = tk.Entry(frame_entrada, width=30)
entrada_prioridade.grid(row=2, column=1)


# Função para capturar a tarefa
def adicionar_tarefa():
    titulo = entrada_titulo.get()
    data = entrada_data.get()
    prioridade = entrada_prioridade.get()

    try:
        # Valida e converte a data inserida
        data_limite = dtt.strptime(data, "%d-%m").replace(year=ano)
        tempo_restante = (data_limite - hoje).days
    except ValueError as e:
        print(f"Erro: {e}")
        print("Por favor, insira uma data válida no formato DD-MM.")
        return

    # Calculo do score com base no tempo restante
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
    
    score += int(prioridade)*2   # Adiciona a prioridade ao scored

    # Exibe a tarefa no console
    print(f"Tarefa adicionada: {titulo}")
    print(f"Data limite: {data} ({tempo_restante} dias restantes)")
    print(f"Prioridade: {prioridade}")
    
   #Adiciona a tarefa à lista de tarefas

    tarefas.append({
        "titulo": titulo,
        "data": data,
        "prioridade": prioridade,
        "tempo_restante": tempo_restante,
        "score": score
    })

    ###apaga os campos###
    entrada_titulo.delete(0, tk.END)
    entrada_data.delete(0, tk.END)
    entrada_prioridade.delete(0, tk.END)



# Botão: Adicionar
botao_adicionar = tk.Button(janela, text="Adicionar Tarefa", command=adicionar_tarefa)
botao_adicionar.pack(pady=10)

##Lista##
frame_lista = tk.Frame(janela, bg="lightgray")
frame_lista.pack(padx=10, fill="both", expand=True)

ttlframelista = tk.Label(frame_lista, text = "lista de tarefas")
def mostrar_lista():
    lista = tk.Listbox(frame_lista)
    lista.pack(pady=10, fill="both", expand=True)
    
    for tito in tarefas:
        lista.insert(tk.END, tito["titulo"])


botao_mostrar = tk.Button(janela, text="mostrar lista", command=mostrar_lista)
botao_mostrar.pack(padx=10)

# Loop principal da aplicação
janela.mainloop()  # Mantém a janela aberta e aguardando ações do usuário
