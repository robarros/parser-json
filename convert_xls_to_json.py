#!/usr/bin/env python3
"""
Script para converter arquivo XLS para JSON
"""

import pandas as pd
import json
import sys
import os

def convert_xls_to_json(xls_file, json_file=None, filter_time=None):
    """
    Converte um arquivo XLS para JSON com filtro opcional por time
    
    Args:
        xls_file (str): Caminho para o arquivo XLS
        json_file (str): Caminho para o arquivo JSON de saída (opcional)
        filter_time (str): Time específico para filtrar (opcional)
    """
    
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(xls_file):
            print(f"❌ Erro: Arquivo '{xls_file}' não encontrado!")
            print(f"   Verifique se o caminho está correto.")
            return False
        
        # Verificar se é um arquivo (não diretório)
        if not os.path.isfile(xls_file):
            print(f"❌ Erro: '{xls_file}' não é um arquivo válido!")
            return False
        
        # Verificar extensão do arquivo
        valid_extensions = ['.xls', '.xlsx', '.xlsm', '.xlsb']
        file_ext = os.path.splitext(xls_file)[1].lower()
        if file_ext not in valid_extensions:
            print(f"❌ Erro: Extensão '{file_ext}' não é suportada!")
            print(f"   Extensões válidas: {', '.join(valid_extensions)}")
            return False
        
        # Verificar se o arquivo não está vazio
        if os.path.getsize(xls_file) == 0:
            print(f"❌ Erro: Arquivo '{xls_file}' está vazio!")
            return False
        
        print(f"Lendo arquivo XLS: {xls_file}")
        if filter_time:
            print(f"🎯 Filtro ativo: apenas registros do time '{filter_time}'")
        
        # Ler o arquivo XLS com tratamento de erro específico
        try:
            excel_file = pd.ExcelFile(xls_file)
        except ValueError as ve:
            print(f"❌ Erro: Arquivo não é um Excel válido!")
            print(f"   Detalhes: {str(ve)}")
            return False
        except Exception as ee:
            print(f"❌ Erro ao ler arquivo Excel!")
            print(f"   Detalhes: {str(ee)}")
            return False
        
        sheet_names = excel_file.sheet_names
        
        # Verificar se há planilhas no arquivo
        if not sheet_names:
            print(f"❌ Erro: Nenhuma planilha encontrada no arquivo!")
            return False
        
        print(f"Planilhas encontradas: {sheet_names}")
        
        # Dicionário para armazenar todas as planilhas
        all_sheets = {}
        
        # Ler cada planilha
        for sheet_name in sheet_names:
            print(f"Processando planilha: {sheet_name}")
            
            try:
                df = pd.read_excel(xls_file, sheet_name=sheet_name)
            except Exception as se:
                print(f"⚠️  Erro ao ler planilha '{sheet_name}': {str(se)}")
                continue
            
            # Verificar se a planilha tem dados
            if df.empty:
                print(f"  ⚠️  Planilha '{sheet_name}' está vazia, pulando...")
                all_sheets[sheet_name] = []
                continue
            
            # Mostrar informações sobre a planilha
            print(f"  - Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
            print(f"  - Colunas: {list(df.columns)}")
            
            # Verificar se tem a coluna 'time' quando há filtro
            if filter_time and 'time' not in df.columns:
                print(f"  ⚠️  Planilha '{sheet_name}' não possui coluna 'time', pulando filtro...")
            
            # Converter DataFrame para dicionário
            # Substituir valores NaN por None para JSON válido
            df_clean = df.where(pd.notna(df), None)
            
            # Converter para lista de dicionários (cada linha é um objeto)
            records = df_clean.to_dict('records')
            
            # Converter valores de string para minúsculas
            processed_records = []
            for record in records:
                processed_record = {}
                for key, value in record.items():
                    # Converter chave para minúscula
                    key_lower = key.lower() if isinstance(key, str) else key
                    
                    # Converter valor para minúscula se for string
                    if isinstance(value, str):
                        processed_record[key_lower] = value.lower()
                    else:
                        processed_record[key_lower] = value
                
                processed_records.append(processed_record)
            
            # Aplicar filtro por time se especificado
            if filter_time:
                filter_time_lower = filter_time.lower()
                original_count = len(processed_records)
                
                # Verificar se realmente tem a coluna 'time'
                if 'time' in [key.lower() for key in processed_records[0].keys()] if processed_records else []:
                    processed_records = [
                        record for record in processed_records 
                        if record.get('time') == filter_time_lower
                    ]
                    filtered_count = len(processed_records)
                    print(f"  - Filtro aplicado: {original_count} → {filtered_count} registros (time='{filter_time}')")
                    
                    # Avisar se não encontrou nenhum registro do time
                    if filtered_count == 0:
                        print(f"  ⚠️  Nenhum registro encontrado para o time '{filter_time}' nesta planilha")
                else:
                    print(f"  ⚠️  Coluna 'time' não encontrada, mantendo todos os registros")
            
            all_sheets[sheet_name] = processed_records
        
        # Definir nome do arquivo JSON se não foi fornecido
        if json_file is None:
            base_name = os.path.splitext(xls_file)[0]
            json_file = f"{base_name}.json"
        
        # Salvar como JSON
        print(f"Salvando como JSON: {json_file}")
        
        # Se houver apenas uma planilha, salvar diretamente o array
        # Se houver múltiplas planilhas, manter a estrutura com nomes das planilhas
        if len(all_sheets) == 1:
            # Pegar o conteúdo da única planilha e salvar como array direto
            sheet_data = list(all_sheets.values())[0]
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(sheet_data, f, ensure_ascii=False, indent=2, default=str)
        else:
            # Múltiplas planilhas - manter estrutura original
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(all_sheets, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"Conversão concluída com sucesso!")
        print(f"Arquivo JSON criado: {json_file}")
        
        # Mostrar estatísticas do filtro se aplicado
        if filter_time:
            total_filtered = sum(len(sheet_data) for sheet_data in all_sheets.values())
            print(f"📊 Registros do time '{filter_time}': {total_filtered}")
            
            # Avisar se não encontrou nenhum registro em todo o arquivo
            if total_filtered == 0:
                print(f"⚠️  ATENÇÃO: Nenhum registro encontrado para o time '{filter_time}' em todo o arquivo!")
                print(f"   Verifique se o nome do time está correto.")
        
        # Verificar se há dados para salvar
        total_records = sum(len(sheet_data) for sheet_data in all_sheets.values())
        if total_records == 0:
            print(f"⚠️  ATENÇÃO: Nenhum dado para salvar no arquivo JSON!")
            if filter_time:
                print(f"   Isso pode acontecer se o time '{filter_time}' não existir nos dados.")
            print(f"   O arquivo JSON será criado vazio.")
        
        # Mostrar preview do JSON de forma dinâmica
        print("\n" + "="*60)
        print("📊 PREVIEW DO JSON GERADO")
        print("="*60)
        
        # Se houver apenas uma planilha, o preview é diferente
        if len(all_sheets) == 1:
            sheet_name = list(all_sheets.keys())[0]
            data = list(all_sheets.values())[0]
            
            print(f"\n📋 Estrutura: Array direto (sem raiz '{sheet_name}')")
            print("-" * 50)
            
            if data:
                # Mostrar informações gerais
                print(f"📈 Total de registros: {len(data)}")
                
                # Obter todas as colunas dinamicamente do primeiro registro
                first_record = data[0]
                columns = list(first_record.keys())
                print(f"📊 Colunas encontradas ({len(columns)}): {', '.join(columns)}")
                
                # Mostrar preview dos primeiros registros (máximo 3)
                preview_count = min(3, len(data))
                print(f"\n🔍 Preview dos primeiros {preview_count} registro(s):")
                
                for i, record in enumerate(data[:preview_count], 1):
                    print(f"\n  📄 Registro {i}:")
                    # Mostrar cada campo dinamicamente
                    for col, value in record.items():
                        # Limitar o tamanho do valor para exibição
                        display_value = str(value)
                        if len(display_value) > 50:
                            display_value = display_value[:47] + "..."
                        print(f"    • {col}: {display_value}")
                        
            else:
                print("  ⚠️  Array vazio")
        else:
            # Múltiplas planilhas - preview original
            for sheet_name, data in all_sheets.items():
                print(f"\n📋 Planilha: '{sheet_name}'")
                print("-" * 40)
                
                if data:
                    # Mostrar informações gerais
                    print(f"📈 Total de registros: {len(data)}")
                    
                    # Obter todas as colunas dinamicamente do primeiro registro
                    first_record = data[0]
                    columns = list(first_record.keys())
                    print(f"📊 Colunas encontradas ({len(columns)}): {', '.join(columns)}")
                    
                    # Mostrar preview dos primeiros registros (máximo 3)
                    preview_count = min(3, len(data))
                    print(f"\n🔍 Preview dos primeiros {preview_count} registro(s):")
                    
                    for i, record in enumerate(data[:preview_count], 1):
                        print(f"\n  📄 Registro {i}:")
                        # Mostrar cada campo dinamicamente
                        for col, value in record.items():
                            # Limitar o tamanho do valor para exibição
                            display_value = str(value)
                            if len(display_value) > 50:
                                display_value = display_value[:47] + "..."
                            print(f"    • {col}: {display_value}")
                            
                else:
                    print("  ⚠️  Planilha vazia")
        
        return True
        
    except Exception as e:
        print(f"Erro durante a conversão: {str(e)}")
        return False

if __name__ == "__main__":
    # Verificar se foi fornecido um arquivo como argumento
    if len(sys.argv) < 2:
        print("Uso: python3 convert_xls_to_json.py <arquivo.xls> [time] [arquivo_saida.json]")
        print("")
        print("Exemplos:")
        print("  python3 convert_xls_to_json.py contas.xls")
        print("  python3 convert_xls_to_json.py contas.xls NOME_TIME")
        print("")
        print("Parâmetros:")
        print("  arquivo.xls    - Arquivo Excel de entrada (obrigatório)")
        print("  time          - Filtrar apenas este time (opcional)")
        print("  arquivo.json  - Arquivo JSON de saída (opcional)")
        sys.exit(1)
    
    # Nome do arquivo XLS vem do argumento
    xls_file = sys.argv[1]
    
    # Verificar se o segundo argumento é um filtro de time ou arquivo de saída
    filter_time = None
    json_file = None
    
    if len(sys.argv) >= 3:
        second_arg = sys.argv[2]
        # Se termina com .json, é arquivo de saída
        if second_arg.endswith('.json'):
            json_file = second_arg
        else:
            # Caso contrário, é filtro de time
            filter_time = second_arg
    
    # Terceiro argumento é sempre arquivo de saída (se presente)
    if len(sys.argv) >= 4:
        json_file = sys.argv[3]
    
    # Verificar se o arquivo existe antes de tentar converter
    if not os.path.exists(xls_file):
        # Verificar se o usuário pode ter passado apenas o filtro sem o arquivo
        if not xls_file.lower().endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
            print(f"❌ Erro: Parece que você esqueceu de especificar o arquivo XLS!")
            print(f"   Você passou: '{xls_file}' (que pode ser um filtro de time)")
            print(f"")
            print(f"✅ Uso correto:")
            print(f"   python3 convert_xls_to_json.py <arquivo.xls> [time] [arquivo_saida.json]")
            print(f"")
            print(f"📋 Exemplos:")
            print(f"   python3 convert_xls_to_json.py contas.xls NOME_TIME")
            print(f"   python3 convert_xls_to_json.py dados.xlsx NOME_TIME")
        else:
            print(f"❌ Erro: Arquivo '{xls_file}' não encontrado!")
            print(f"   Verifique se o caminho está correto.")
        sys.exit(1)
    
    print(f"🚀 Iniciando conversão de: {xls_file}")
    if filter_time:
        print(f"🎯 Filtro de time: {filter_time}")
    if json_file:
        print(f"📝 Arquivo de saída: {json_file}")
    
    # Converter
    success = convert_xls_to_json(xls_file, json_file, filter_time)
    
    if success:
        print("\n✅ Conversão realizada com sucesso!")
    else:
        print("\n❌ Erro na conversão!")
        sys.exit(1)
