
# Enviar Comunicados - Colégio Xingu

Este projeto automatiza o envio de comunicados do **Colégio Xingu** pelo **ClassApp**, com ou sem anexos, para grupos de alunos ou destinatários específicos, conforme o dicionário de mensagens.

O projeto visa otimizar o tempo gasto pelo Departamento de Comunicação em períodos de matrícula, onde
é necessário realizar o envio de mensagens para os alunos novos. 

---

## 📁 Estrutura de pastas

```
project_root/
├── REAMDE.md
├── src/
│   ├── enviar_comunicado.py
├── data/
│   ├── alunos.xlsx              # Planilha com dados dos alunos (colunas: rm, nome, turma)
│   ├── anexos/                  # Pasta com os arquivos anexos
│   ├── msgs/                    # Pasta com os arquivos .txt contendo o conteúdo das mensagens
│   └── dicionario_msgs.json      # Dicionário com metadados das mensagens
├── config/
│   └── token.txt                 # Arquivo com o token da API do ClassApp
```

---

## ⚙️ Pré-requisitos

- **Python 3.x**
- Bibliotecas:
  - `pandas`
  - `requests`
  
Instale as dependências com:

```bash
pip install pandas requests
```

---

## 📝 Como funciona

1. O script lê o arquivo `alunos.xlsx` para obter os RMs, nomes e turmas dos alunos.
2. Lê o arquivo `dicionario_msgs.json` que contém a configuração das mensagens:
   - Título
   - Nome do arquivo de conteúdo
   - Se a mensagem é específica (personalizada por aluno)
   - Grupos (turmas ou 'todos')
   - Lista de anexos e seus tipos MIME
3. Para cada mensagem:
   - Gera o conteúdo substituindo variáveis (ex.: nome e RM) se for específico.
   - Filtra os RMs destinatários conforme o grupo.
   - Envia:
     - Para todos os alunos do grupo de uma vez (mensagens gerais)
     - Para cada aluno individualmente (mensagens específicas)
   - Se houver anexos, envia pela API `message-file`.
   - Se não houver anexos, envia pela API `message`.

---

## 📨 API do ClassApp

URLs utilizadas:

- `https://api.classapp.com.br/v1/message` → mensagens sem anexo
- `https://api.classapp.com.br/v1/message-file` → mensagens com anexo

O token da API deve estar no arquivo: `config/token.txt` e é adquirido diretamente com a ClassApp

---

## 📌 Formato do `dicionario_msgs.json`

Exemplo:

```json
"msg1": {
  "titulo": "Bem-vinda ao ClassApp do Colégio Xingu!",
  "conteudo": "txt1",
  "especifico": 0,
  "grupo": ["todos"],
  "anexo": ["bem vinda ao xingu 24.png", "video pais.mp4"],
  "mime": ["image/png", "video/mp4"]
}
```

- **titulo**: título do comunicado
- **conteudo**: nome do arquivo `.txt` (na pasta `msgs/`) com o corpo da mensagem
- **especifico**: 1 se a mensagem deve ser personalizada por aluno, 0 se geral
- **grupo**: lista de turmas ou `todos`
- **anexo**: lista de nomes de arquivos (na pasta `anexos/`)
- **mime**: lista dos tipos MIME correspondentes aos anexos

---

## 🚀 Como executar

No terminal, na pasta do projeto, rode:

```bash
python enviar_comunicado.py
```

O script irá:
- Percorrer o dicionário de mensagens.
- Enviar cada comunicado conforme sua configuração.

---

## 💡 Observações

- Os arquivos `.txt` contendo o conteúdo das mensagens devem estar na pasta `data/msgs/`.
- Os arquivos de anexo devem estar na pasta `data/anexos/`.
- O `alunos.xlsx` deve ter ao menos as colunas: `rm`, `nome`, `turma`.
- O script ignora mensagens sem grupo correspondente na planilha.
- O arquivo `token.txt` deve conter apenas o token da API do ClassApp.

---

## 👨‍💻 Autor

Este projeto foi desenvolvido por José Orlando de Queiroz para o envio automatizado de comunicados do **Colégio Xingu**.
