#!/usr/bin/env python3
"""Script para converter arquivo XLS para JSON"""

import pandas as pd
import json
import sys
import os

def convert_xls_to_json(xls_file, filter_time=None):
    """Converte XLS para JSON com filtro opcional por time"""
    
    # Verificações básicas
    if not os.path.exists(xls_file):
        print(f"❌ Arquivo '{xls_file}' não encontrado!")
        return False
    
    try:
        # Ler arquivo Excel
        df = pd.read_excel(xls_file)
        
        if df.empty:
            print("❌ Arquivo vazio!")
            return False
        
        # Converter colunas para minúsculas
        df.columns = df.columns.str.lower()
        
        # Converter valores string para minúsculas
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.lower()
        
        # Filtrar por time se especificado
        if filter_time and 'time' in df.columns:
            original_count = len(df)
            df = df[df['time'] == filter_time.lower()]
            if len(df) == 0:
                print(f"❌ Time '{filter_time}' não encontrado!")
                return False
            print(f"🎯 Filtrado para time '{filter_time}': {len(df)} registros")
        elif filter_time and 'time' not in df.columns:
            print("❌ Coluna 'time' não encontrada!")
            return False
        
        # Converter para JSON
        records = df.to_dict('records')
        
        # Salvar arquivo
        json_file = f"{os.path.splitext(xls_file)[0]}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Convertido: {json_file} ({len(records)} registros)")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 convert_xls_to_json.py <arquivo.xls> [time]")
        sys.exit(1)
    
    xls_file = sys.argv[1]
    filter_time = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_xls_to_json(xls_file, filter_time)
    sys.exit(0 if success else 1)