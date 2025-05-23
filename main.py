import tkinter as tk
from datetime import datetime as dtt
import json
import os

# --- Variáveis Globais ---
tarefas = []
tarefas_exibidas = []
ano = dtt.now().year  # Obtém o ano atual
mesatual = dtt.now().month  # Obtém o mês atual
caminho = os.path.expanduser("~/tarefas.json")  # Caminho do arquivo JSON
formatos_data = ["%d-%m", "%-d-%-m", "%d-%-m", "%-d-%m"]

#\--\--\--\--\--\--\--\--\--\--\---\--\ JANELA \--\--\--\--\--\--\--\--\--\--\--\--\--\
janela = tk.Tk()
janela.title("Organizador de Tarefas")
janela.geometry("500x600")



# \--\--\--\--\--\--\--\--\--\ FUNÇÕES \--\--\--\--\--\--\--\--\--\--\--\--\--\--\--\
# adicionar_tarefa: Adiciona uma nova tarefa à lista
# calc_score: Calcula o score de cada tarefa
# concluir_tarefa: Conclui a tarefa selecionada
# mostrar_lista: Exibe a lista de tarefas
# interpretar_data: Interpreta a data fornecida pelo usuário
# serializar_tarefa: Serializa a tarefa para salvar no JSON
# desserializar_tarefa: Desserializa a tarefa ao carregar do JSON
# carregar_tarefas: Carrega as tarefas do arquivo JSON
# salvar_tarefas: Salva as tarefas no arquivo JSON

### --- ### FUNÇÕES PRINCIPAIS ### --- ###

def adicionar_tarefa():
    """Adiciona uma nova tarefa à lista."""
    titulo = entrada_titulo.get().strip()
    data_input = entrada_data.get().strip()
    prioridade_input = entrada_prioridade.get().strip()

    data_obj = None  # será datetime ou None

    if not titulo:
        print("Erro: A atividade deve ter um título.")
        return

    if data_input:
        data_obj = interpretar_data(data_input)
        if not data_obj:
            data_obj = None
            return


    prioridade = int(prioridade_input)

    tarefas.append({
        "titulo": titulo,
        "prazo_formatado": data_obj.strftime("%d-%m-%Y") if data_obj else "sem prazo",
        "data_obj": data_obj,
        "prioridade": prioridade
    })

    # Limpa os campos de entrada
    entrada_titulo.delete(0, tk.END)
    entrada_data.delete(0, tk.END)
    entrada_prioridade.delete(0, tk.END)

    mostrar_lista()
    salvar_tarefas()
    entrada_titulo.focus()

def calc_score():
    hoje = dtt.now()

    for tarefa in tarefas:
        score = 0
        data_obj = tarefa.get("data_obj")

        if data_obj:
            tempo_restante = (data_obj - hoje).days

            if tempo_restante < 0:
                score += 10
            elif tempo_restante < 3:
                score += 7
            elif tempo_restante < 7:
                score += 5

            tarefa["tempo_restante"] = tempo_restante
        else:
            score -= 2  # penalidade por não ter prazo


        prioridade = tarefa.get("prioridade")

        if isinstance(prioridade, int):
            score += (5 - prioridade) * 2
        else:
            score -= 2  # penalidade para tarefas sem prioridade
        
        
        tarefa["score"] = score

### --- ### FUNÇÕES AUXILIARES ### --- ###

def mostrar_lista():
    """Exibe as tarefas no Listbox."""
    lista.delete(0, tk.END)  # Limpa o Listbox
    calc_score()
    global tarefas_exibidas
    tarefas_exibidas = []  # Limpa a lista de tarefas exibidas  
    tarefas_exibidas = sorted(tarefas, key=lambda x: x["score"], reverse=True)

    for tarefa in sorted(tarefas, key=lambda x: x["score"], reverse=True):
        titulo = tarefa["titulo"]
        prazo = tarefa.get("prazo_formatado", "sem prazo")
        texto = f"{titulo.ljust(30)} {prazo.rjust(10)}"
        lista.insert(tk.END, texto)

def concluir_tarefa(event=None):
    """Conclui a tarefa selecionada no Listbox."""
    selecao = lista.curselection()
    if selecao:
        indice = selecao[0]
        tarefa_selecionada = tarefas_exibidas[indice]

        if tarefa_selecionada in tarefas:
            tarefas.remove(tarefa_selecionada)

        tarefas_exibidas.pop(indice)  # Remove a tarefa da lista
        mostrar_lista()  # Atualiza a lista exibida
        salvar_tarefas()  # Salva as alterações no arquivo JSON

def interpretar_data(texto_data: str) -> dtt | None:
    if not texto_data:
        return None

    texto_data = texto_data.replace("/", "-").replace(".", "-").replace(" ", "-")

    #até qui é usado o imput com -

    dataret = None
    
    try:
        if "-" not in texto_data:
            dia = int(texto_data)
            dataret = dtt(year=ano, month=mesatual, day=dia)
        else :
            for formato in formatos_data:
                try:
                    dataret = dtt.strptime(texto_data, formato).replace(year=ano)
                    break
                except ValueError:
                    continue
        if dataret is None:
            raise ValueError("Formato de data inválido.")

        if dataret.month < mesatual:
            dataret = dataret.replace(year=ano + 1)

        return dataret

    except ValueError as e:
        print(f"Erro: Data inválida '{texto_data}'.")
        return None
    


### --- ### SALVAR E CARREGAR ### --- ###

def serializar_tarefa(tarefa: dict) -> dict:
    copia = tarefa.copy()  # cria uma cópia para não alterar o original
    if isinstance(copia["data_obj"], dtt):
        copia["data_obj"] = copia["data_obj"].strftime("%Y-%m-%d %H:%M:%S")
    return copia

def desserializar_tarefa(tarefa: dict) -> dict:
    if isinstance(tarefa.get("data_obj"), str) and tarefa["data_obj"] != "None":
        tarefa["data_obj"] = dtt.strptime(tarefa["data_obj"], "%Y-%m-%d %H:%M:%S")
    return tarefa

def carregar_tarefas():
    if os.path.exists(caminho):
        with open(caminho, "r") as arquivo:
            dados = json.load(arquivo)
            return [desserializar_tarefa(t) for t in dados]
    return []

def salvar_tarefas():
    tarefas_serializadas = [serializar_tarefa(t) for t in tarefas]
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(tarefas_serializadas, f, indent=4)


#\--\--\--\--\--\--\--\--\--\--\---\--\ WIDGETS \--\--\--\--\--\--\--\--\--\--\--\--\--\
# Frame de Título
frame_titulo = tk.Frame(janela)
frame_titulo.pack(pady=10, fill="x")
tk.Label(frame_titulo, text="Organizador de tarefas", font=("Arial", 16)).pack()

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
lista = tk.Listbox(frame_lista, font=("Consolas", 10))
lista.pack(pady=10, fill="both", expand=True)
lista.bind("<Double-Button-1>", concluir_tarefa)


#\--\--\--\--\--\--\--\--\--\--\---\--\ INICIALIZAÇÃO \--\--\--\--\--\--\--\--\--\--\--\--\--\
tarefas = carregar_tarefas()  # Carrega as tarefas do arquivo JSON
mostrar_lista()  # Exibe as tarefas carregadas

# Loop Principal
janela.mainloop()
