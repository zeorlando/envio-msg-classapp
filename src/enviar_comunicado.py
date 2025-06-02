"""
msg1 - para todos com anexo (2 anexos)
msg2 - específico com anexo, aqui varia o RM (1 anexo)
msg3 - categorizado(inf ao 1 ano) sem anexo
msg4 - categorizado(2 ano) sem anexo
msg5 - categorizado(3 e 4 ano) sem anexo
msg6 - categorizado(5 ano) sem anexo
msg7 - categorizado(6 ao 9 ano) sem anexo
msg8 - categorizado(2 ao 9 ano) sem anexo
msg9 - categorizado(6 ao 9 ano) sem anexo
msg10 - para todos sem anexo
msg11 - categorizado(inf ao 1 ano) sem anexo
msg12 - categorizado(2 ao 5 ano) sem anexo
msg13 - categorizado(6 ao 9 ano) sem anexo
msg14 - para todos sem anexo
msg15 - para todos com anexo (5 anexos)

ESTRUTURA DO DICIONÁRIO DE MENSAGENS

{
    'msg':{
        'título':'valor_titulo', //string
        'conteudo':'valor_msg', //string
        'especifico':1, // boolean
        'grupo':lita_com_turmas, //list
        'anexo':lista_com_anexos, //list
        'mime':lista_com_mime, //list 
    }
}

- grupo -> verificar quais turmas estão na lista para poder filtrar da planilha(xlsx)
rms = df[df['turma'].isin(lista_turmas)]['rm'].tolist()
lista_turmas é o campo grupo do dicionário


- anexo -> dois estados -> lista vazia ou lista com >= 1 elementos


"""

import json
import os
import pandas as pd
import requests
from string import Template


token = os.path.join('..','config','token.txt')
alunos = os.path.join('..','data', 'alunos.xlsx') 
caminho_anexos = os.path.join('..','data','anexos')
caminho_mensagens = os.path.join('..','data','msgs')
caminho_dicionario_msgs = os.path.join('..','data','dicionario_msgs.json')

lista_msgs = os.listdir(caminho_mensagens)

url_sem_anexo = "https://api.classapp.com.br/v1/message"
url_com_anexo = "https://api.classapp.com.br/v1/message-file"

try:
    with open(token,'r') as token_file:
        ler_token = token_file.read()
except IOError as e:
    print(f'{e} - Arquivo não encontrado')

#TODO verificar a questão do headers com anexo
headers_sem_anexo = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ler_token}"
}

headers_com_anexo = {
    "Authorization": f"Bearer {ler_token}"
}

try:
    # lista_alunos = []
    df = pd.read_excel(alunos)
    # for index, row in df.iterrows():
    #     lista_alunos.append(row.to_dict())
    lista_rms = df['rm'].tolist() #transforma os RMs em uma lista 
    str_rms_todos = [str(rm) for rm in lista_rms] #passa os itens da lista para str
except IOError as e:
    print(f'{e} - Arquivo não encontrado')

try:    
    with open(caminho_dicionario_msgs, encoding='utf-8') as dicionario_msgs:
        valores_dic = json.load(dicionario_msgs)
    chaves_msgs = list(valores_dic.keys())
except IOError as e:
    print(f'{e} - Arquivo não encontrado') 


def anexo(mensagem):
    files = []
    for nome, tipo in zip(valores_dic[mensagem]["anexo"], valores_dic[mensagem]["mime"]):
            caminho_anexo_msg = os.path.join(caminho_anexos, nome)
            files.append(
                ("files", (nome, open(caminho_anexo_msg, "rb"), tipo))
            )
    return files


def gera_metadata(titulo, msg_class, rms_selecionados):
    metadata = {
        "metadata": json.dumps({ 
            "messageData": {
            "subject": str(titulo),
            "content": msg_class,
            "type": "comunicado",
            "noReply": True,
            "recipients": {
                "eids": rms_selecionados    
            }
            }
        })    
    }
    return metadata


def gera_dados(titulo, msg_class, rms_selecionados):
    dados = {
            "messageData": {
                "subject": str(titulo),
                "content": msg_class, #conteudo msg
                "type": "comunicado",
                "tags": [
                    "1"
                ],
                "noReply": True,
                "label": "label",
                "recipients": {
                    "eids":
                        rms_selecionados
                }
            }
            }
    return dados

def envia_msg(mensagem):
    lista_resposta = []
    titulo = valores_dic[mensagem]['titulo']
    lista_anexo = valores_dic[mensagem]['anexo']
    especifico = valores_dic[mensagem]['especifico']
    arquivo_conteudo = os.path.join(caminho_mensagens, f'{mensagem}.txt') #caminho msg
    lista_turmas = valores_dic[mensagem]['grupo']
    rms = df[df['turma'].isin(lista_turmas)]['rm'].tolist()
    str_rms_espec = [str(rm) for rm in rms]
    rms_selecionados = str_rms_todos if 'todos' in valores_dic[mensagem]['grupo'] else str_rms_espec
    int_rms_selecionados = [int(rm) for rm in rms_selecionados]
    
    with open(os.path.join(arquivo_conteudo), "r", encoding='utf-8') as arquivo:
        msg_class = arquivo.read()

    if especifico:
        for rm in int_rms_selecionados:
            nome_df = df[df['rm'] == rm]['nome'].values[0]
            rm_df = df[df['rm'] == rm]['rm'].values[0]
            msg_trocada = Template(msg_class).substitute(nome = nome_df, rm = rm_df)
            if lista_anexo:
                resposta =  requests.post(url_com_anexo, headers=headers_com_anexo, 
                                    data=gera_metadata(titulo, msg_trocada, [str(rm)]), 
                                    files=anexo(mensagem))
                lista_resposta.append(resposta)
            else:
                resposta = requests.post(url_sem_anexo, json=gera_dados(titulo, msg_trocada, [str(rm)]), 
                                    headers=headers_sem_anexo)
                lista_resposta.append(resposta)
    else:
        if lista_anexo:
            resposta = requests.post(url_com_anexo, headers=headers_com_anexo, 
                                 data=gera_metadata(titulo, msg_class, rms_selecionados), 
                                 files=anexo(mensagem))
            lista_resposta.append(resposta)
        else:
            resposta = requests.post(url_sem_anexo, json=gera_dados(titulo, msg_class, rms_selecionados), 
                                 headers=headers_sem_anexo) 
            lista_resposta.append(resposta)
    return lista_resposta

# percorre o dicionário das mensagens
for chave in range(len(chaves_msgs)):
    mensagem = chaves_msgs[chave]
    envia_msg(mensagem)
    