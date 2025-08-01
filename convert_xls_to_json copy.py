#!/usr/bin/env python3
"""
Script para converter arquivo XLS para JSON
"""

import pandas as pd
import json
import sys
import os

def convert_xls_to_json(xls_file, json_file=None):
    """
    Converte um arquivo XLS para JSON
    
    Args:
        xls_file (str): Caminho para o arquivo XLS
        json_file (str): Caminho para o arquivo JSON de saída (opcional)
    """
    
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(xls_file):
            print(f"Erro: Arquivo {xls_file} não encontrado!")
            return False
        
        print(f"Lendo arquivo XLS: {xls_file}")
        
        # Ler o arquivo XLS
        # Primeiro, vamos ver todas as planilhas disponíveis
        excel_file = pd.ExcelFile(xls_file)
        sheet_names = excel_file.sheet_names
        
        print(f"Planilhas encontradas: {sheet_names}")
        
        # Dicionário para armazenar todas as planilhas
        all_sheets = {}
        
        # Ler cada planilha
        for sheet_name in sheet_names:
            print(f"Processando planilha: {sheet_name}")
            df = pd.read_excel(xls_file, sheet_name=sheet_name)
            
            # Mostrar informações sobre a planilha
            print(f"  - Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
            print(f"  - Colunas: {list(df.columns)}")
            
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
        print("Uso: python3 convert_xls_to_json.py <arquivo.xls> [arquivo_saida.json]")
        print("")
        print("Exemplos:")
        print("  python3 convert_xls_to_json.py contas.xls")
        print("  python3 convert_xls_to_json.py dados.xlsx resultado.json")
        print("  python3 convert_xls_to_json.py /caminho/para/planilha.xls")
        sys.exit(1)
    
    # Nome do arquivo XLS vem do argumento
    xls_file = sys.argv[1]
    
    # Arquivo JSON de saída (opcional)
    json_file = None
    if len(sys.argv) >= 3:
        json_file = sys.argv[2]
    
    # Verificar se o arquivo existe antes de tentar converter
    if not os.path.exists(xls_file):
        print(f"❌ Erro: Arquivo '{xls_file}' não encontrado!")
        print(f"   Verifique se o caminho está correto.")
        sys.exit(1)
    
    print(f"🚀 Iniciando conversão de: {xls_file}")
    if json_file:
        print(f"📝 Arquivo de saída: {json_file}")
    
    # Converter
    success = convert_xls_to_json(xls_file, json_file)
    
    if success:
        print("\n✅ Conversão realizada com sucesso!")
    else:
        print("\n❌ Erro na conversão!")
        sys.exit(1)
