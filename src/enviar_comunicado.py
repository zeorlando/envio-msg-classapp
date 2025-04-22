"""
- tenho uma lista com os alunos que devem receber as msgs

- verificar se a mensagem tem anexo
- verificar se é pra todos

***

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

colocar as turmas de cada msg em uma lista, na chave  turmas

duas funções de envio: uma com anexo e outra sem anexo

dicionário de listas com as segmentações (dos categorizados)

"""

import json
import os
import pandas as pd
import requests


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
    str_rms = [str(rm) for rm in lista_rms] #passa os itens da lista para str
except IOError as e:
    print(f'{e} - Arquivo não encontrado')

try:    
    with open(caminho_dicionario_msgs, encoding='utf-8') as dicionario_msgs:
        valores_dic = json.load(dicionario_msgs)
    chaves_msgs = list(valores_dic.keys())
except IOError as e:
    print(f'{e} - Arquivo não encontrado') 

# função para enviar mensagem para todos da lista - mensagens COM anexo
def envia_msg_para_todos_com_anexo(mensagem, titulo):
    msg_dic = valores_dic[mensagem]
    arquivo_conteudo = os.path.join(caminho_mensagens, f'{mensagem}.txt') #caminho msg
    with open(os.path.join(arquivo_conteudo), "r", encoding='utf-8') as arquivo:
        msg_class = arquivo.read()
        metadata = {
            "metadata": json.dumps({ 
                "messageData": {
                "subject": str(titulo),
                "content": msg_class,
                "type": "comunicado",
                "noReply": True,
                "recipients": {
                    "eids": str_rms  
                }
                }
            })    
        }
        files = []
        for nome, tipo in zip(msg_dic["anexos"], msg_dic["mime"]):
            caminho_anexo_msg = os.path.join(caminho_anexos, nome)
            files.append(
                ("files", (nome, open(caminho_anexo_msg, "rb"), tipo))
            )
    resposta = requests.post(url_com_anexo, headers=headers_com_anexo, data=metadata, files=files)   
    if resposta.status_code == 201:
        print("Mensagem enviada com sucesso!")
        print("Resposta:", resposta.json())
    else:
        print(f"Falha ao enviar mensagem. Status code: {resposta.status_code}")
        print("Detalhes:", resposta.json()) 
    return resposta

# função para enviar mensagem para todos da lista - mensagens SEM anexo
def envia_msg_para_todos_sem_anexo(mensagem, titulo):
    arquivo_conteudo = os.path.join(caminho_mensagens, f'{mensagem}.txt') #caminho msg
    with open(os.path.join(arquivo_conteudo), "r", encoding='utf-8') as arquivo:
        msg_class = arquivo.read()
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
                                str_rms    
                        }
                    }
                }
    return print(dados)
    # resposta = requests.post(url_sem_anexo, json=dados, headers=headers_sem_anexo)
    # return resposta 
    #pass


# percorre o dicionário das mensagens
for chave in range(len(chaves_msgs)):
    mensagem = chaves_msgs[chave]
    titulo = valores_dic[chaves_msgs[chave]]['titulo']
    if valores_dic[chaves_msgs[chave]]['para_todos'] == 1:
        if valores_dic[chaves_msgs[chave]]['anexo'] == 1:
            #envia_msg_para_todos_com_anexo(mensagem,titulo)
            pass
        else:
            #envia_msg_para_todos_sem_anexo(mensagem,titulo)
            pass
    else:
        if valores_dic[chaves_msgs[chave]]['anexo'] == 1:
            print(f'{chaves_msgs[chave]} - específco com anexo')
        else:
            print(f'{chaves_msgs[chave]} - específico sem anexo')



