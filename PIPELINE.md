# Pipeline GitHub Actions - Conversor XLS para JSON

## 📋 Visão Geral

Esta pipeline automatiza a conversão de arquivos Excel (XLS/XLSX) para JSON usando GitHub Actions. O processo inclui validação, conversão e disponibilização dos arquivos resultantes como artefatos.

## 🚀 Como Funciona

### Triggers da Pipeline

A pipeline é executada quando:

1. **Push** na branch `main` ou `master`
2. **Pull Request** para `main` ou `master`
3. **Execução manual** com parâmetros opcionais

### Jobs da Pipeline

#### 1. **convert-xls** - Conversão Principal
- ✅ Configura ambiente Python 3.11
- ✅ Instala dependências do `requirements.txt`
- ✅ Lista arquivos disponíveis
- ✅ Executa conversão XLS → JSON
- ✅ Valida estrutura JSON
- ✅ Faz upload dos arquivos como artefatos

#### 2. **test** - Testes Básicos
- ✅ Verifica sintaxe do código Python
- ✅ Testa help/usage do script
- ✅ Valida importação das dependências

## 🔧 Execução Manual

### Via Interface GitHub

1. Vá para **Actions** no seu repositório
2. Selecione **Convert XLS to JSON**
3. Clique em **Run workflow**
4. Configure parâmetros opcionais:
   - **filter_time**: Filtrar por time específico (ex: `fv4`)
   - **output_file**: Nome do arquivo de saída (ex: `resultado.json`)

### Parâmetros da Execução Manual

```yaml
filter_time: "fv4"           # Filtra apenas registros do time 'fv4'
output_file: "resultado.json" # Nome personalizado para saída
```

## 📁 Arquivos Processados

A pipeline procura arquivos na seguinte ordem:
1. `contas.xls`
2. `contas.xlsx`
3. Qualquer arquivo `.xls*` no diretório raiz

## 📤 Artefatos Gerados

Todos os arquivos JSON gerados são salvos como artefatos do GitHub Actions:

- **Nome**: `converted-json-files`
- **Retenção**: 30 dias
- **Conteúdo**: Todos os arquivos `*.json` gerados

### Como Baixar Artefatos

1. Vá para a execução da pipeline em **Actions**
2. Role até o final da página
3. Baixe o arquivo ZIP em **Artifacts**

## 🔍 Logs e Monitoramento

### Informações nos Logs

- 📁 Lista de arquivos encontrados
- 🚀 Comando de conversão executado
- 📊 Estatísticas dos arquivos JSON
- 📄 Preview do conteúdo gerado
- ✅ Status da validação JSON

### Exemplo de Log

```
🚀 Convertendo arquivo: contas.xls
📋 Executando: python convert_xls_to_json.py contas.xls fv4
✅ Conversão realizada com sucesso!
📊 Registros do time 'fv4': 15
📈 Estatísticas: 125 linhas, 3.2KB
✅ JSON válido
```

## ⚙️ Configuração do Repositório

### Estrutura Necessária

```
seu-repo/
├── .github/
│   └── workflows/
│       └── convert-xls-to-json.yml
├── convert_xls_to_json.py
├── requirements.txt
├── contas.xls (ou .xlsx)
└── README.md
```

### Dependências

Certifique-se de que o `requirements.txt` contém:

```
pandas>=2.0.0
openpyxl>=3.1.0
xlrd>=2.0.0
```

## 🛠️ Customização

### Modificar Triggers

Para executar apenas manualmente:

```yaml
on:
  workflow_dispatch:
    # ... inputs
```

### Adicionar Novos Formatos

Modifique o step de busca de arquivos:

```bash
# Procurar também arquivos CSV
XLS_FILE=$(find . -maxdepth 1 -name "*.xls*" -o -name "*.csv" -type f | head -1)
```

### Alterar Versão Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'  # Mude aqui
```

## 🚨 Troubleshooting

### Arquivo XLS Não Encontrado

**Problema**: `⚠️ Nenhum arquivo XLS encontrado`

**Soluções**:
- Certifique-se que o arquivo está no diretório raiz
- Verifique a extensão (.xls, .xlsx, .xlsm, .xlsb)
- Confirme que o arquivo foi commitado no repositório

### Erro de Dependências

**Problema**: `ImportError: No module named 'pandas'`

**Soluções**:
- Verifique se `requirements.txt` existe
- Confirme que todas as dependências estão listadas
- Teste localmente: `pip install -r requirements.txt`

### JSON Inválido

**Problema**: `❌ JSON inválido`

**Soluções**:
- Verifique dados de entrada no Excel
- Confirme encoding dos arquivos
- Teste conversão local primeiro

## 📞 Suporte

Para problemas com a pipeline:

1. Verifique os logs da execução
2. Confirme estrutura dos arquivos
3. Teste conversão localmente
4. Verifique configuração do repositório

## 🔄 Próximos Passos

Melhorias sugeridas:

- [ ] Suporte a múltiplos arquivos XLS
- [ ] Notificações por email/Slack
- [ ] Deploy automático dos JSONs
- [ ] Testes unitários mais robustos
- [ ] Suporte a outros formatos (CSV, TSV)
