# Conversor XLS para JSON

Script Python para converter arquivos Excel (XLS/XLSX) para formato JSON de forma dinâmica.

## 🚀 Funcionalidades

- ✅ **Dinâmico**: Detecta automaticamente planilhas e colunas
- ✅ **Conversão para minúsculas**: Todos os valores de string
- ✅ **Estrutura limpa**: JSON sem raiz desnecessária (para planilha única)
- ✅ **Múltiplas planilhas**: Suporte completo
- ✅ **Argumentos flexíveis**: Nome de arquivo via linha de comando

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Clone ou baixe os arquivos do projeto

### 2. Instale as dependências

```bash
# Instalar dependências diretamente
pip install -r requirements.txt

# OU instalar manualmente
pip install pandas openpyxl xlrd
```

### 3. (Opcional) Usar ambiente virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

## 🌍 Como usar em um novo ambiente

### **Método 1: Instalação simples**
```bash
# 1. Baixar os arquivos do projeto
# 2. Instalar dependências
pip install -r requirements.txt

# 3. Testar o script
python3 convert_xls_to_json.py arquivo.xls
```

### **Método 2: Com ambiente virtual (recomendado)**
```bash
# 1. Baixar os arquivos do projeto
# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# OU
venv\Scripts\activate     # Windows

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Usar o script
python3 convert_xls_to_json.py arquivo.xls

# 6. Desativar ambiente virtual (quando terminar)
deactivate
```

### **Método 3: Verificação passo a passo**
```bash
# 1. Verificar versão do Python
python3 --version  # Deve ser 3.7+

# 2. Verificar se pip está instalado
pip --version

# 3. Instalar dependências uma por uma (se necessário)
pip install pandas
pip install openpyxl
pip install xlrd

# 4. Verificar instalação
pip list | grep -E "(pandas|openpyxl|xlrd)"

# 5. Testar o script
python3 convert_xls_to_json.py contas.xls
```

### **Solução de problemas comuns:**
```bash
# Se der erro de permissão no Linux/Mac
sudo pip install -r requirements.txt

# Se não encontrar python3
python convert_xls_to_json.py arquivo.xls

# Para atualizar dependências
pip install --upgrade -r requirements.txt
```

## 💻 Uso

### Uso básico
```bash
python3 convert_xls_to_json.py arquivo.xls
```

### Com arquivo de saída personalizado
```bash
python3 convert_xls_to_json.py arquivo.xls saida_personalizada.json
```

### Exemplos
```bash
# Converte contas.xls para contas.json
python3 convert_xls_to_json.py contas.xls

# Converte dados.xlsx para resultado.json
python3 convert_xls_to_json.py dados.xlsx resultado.json

# Funciona com caminhos completos
python3 convert_xls_to_json.py /caminho/completo/planilha.xls
```

## 📊 Exemplo de Saída

### Entrada (Excel):
| time | aws    | regiao     | ambiente |
|------|--------|------------|----------|
| fv4  | 123456 | Us-east-1  | Dev      |
| ei7  | 789012 | Sa-east-1  | Prod     |

### Saída (JSON):
```json
[
  {
    "time": "fv4",
    "aws": 123456,
    "regiao": "us-east-1",
    "ambiente": "dev"
  },
  {
    "time": "ei7",
    "aws": 789012,
    "regiao": "sa-east-1", 
    "ambiente": "prod"
  }
]
```

## 🎯 Características

- **Nomes de colunas**: Convertidos para minúsculas
- **Valores de string**: Convertidos para minúsculas
- **Valores numéricos**: Preservados
- **Planilha única**: JSON como array direto
- **Múltiplas planilhas**: JSON com estrutura de objetos

## 🐛 Solução de Problemas

### Erro: "No module named 'pandas'"
```bash
pip install pandas openpyxl xlrd
```

### Erro: "No module named 'openpyxl'"
```bash
pip install openpyxl
```

### Erro: "Arquivo não encontrado"
- Verifique se o caminho do arquivo está correto
- Certifique-se de que a extensão é .xls ou .xlsx

## 📁 Estrutura do Projeto

```
oidc/
├── convert_xls_to_json.py  # Script principal
├── requirements.txt        # Dependências
├── README.md              # Este arquivo
├── contas.xls             # Arquivo de exemplo
└── contas.json            # Saída gerada
```

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias ou reportar bugs!
