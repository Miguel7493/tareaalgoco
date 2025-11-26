import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Configuraci�n de estilo para gr�ficos profesionales
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Rutas
BASE_DIR = Path(__file__).parent.parent
MEASUREMENTS_DIR = BASE_DIR / 'data' / 'measurements'
PLOTS_DIR = BASE_DIR / 'data' / 'plots'

# Crear directorio de plots si no existe
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def load_measurements():
    """
    Carga los archivos de mediciones desde archivos .txt
    Formato esperado por línea: testcases_N_TIPO_ID,?,tiempo_s,memoria_bytes,resultado
    Nombre del archivo indica el algoritmo (ej: brute-force.txt, greedy1.txt)
    """
    data_rows = []

    for file in MEASUREMENTS_DIR.glob('*.txt'):
        if file.name == 'a.txt':  # Ignorar archivos placeholder
            continue

        # Extraer nombre del algoritmo del archivo
        algorithm_name = file.stem  # brute-force, greedy1, etc.

        with open(file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Parsear: testcases_10_bloques_0,1,0.003,3584,26
                parts = line.split(',')
                if len(parts) < 5:
                    continue

                # Extraer info del nombre del test
                test_name = parts[0]  # testcases_10_bloques_0
                test_parts = test_name.split('_')

                if len(test_parts) >= 3:
                    n = int(test_parts[1])  # tamaño de entrada
                    input_type = test_parts[2]  # bloques, random, etc.
                else:
                    continue

                # Extraer métricas
                time_s = float(parts[2])  # tiempo en segundos
                time_ms = time_s * 1000  # convertir a milisegundos

                memory_bytes = float(parts[3])
                memory_kb = memory_bytes / 1024  # convertir a KB

                result_value = float(parts[4])

                data_rows.append({
                    'n': n,
                    'algorithm': algorithm_name,
                    'input_type': input_type,
                    'time_ms': time_ms,
                    'memory_kb': memory_kb,
                    'result_value': result_value
                })

    if not data_rows:
        print("No se encontraron archivos de mediciones (.txt) en:", MEASUREMENTS_DIR)
        print("Archivos encontrados:", list(MEASUREMENTS_DIR.glob('*.txt')))
        return None

    return pd.DataFrame(data_rows)

def plot_1_time_vs_n(df):
    """Gr�fico 1: Tiempo de ejecuci�n vs tama�o de entrada (n)"""
    plt.figure(figsize=(12, 7))

    algorithms = df['algorithm'].unique()
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    markers = ['o', 's', '^', 'D']

    for i, algo in enumerate(algorithms):
        algo_data = df[df['algorithm'] == algo].groupby('n')['time_ms'].mean().reset_index()
        plt.plot(algo_data['n'], algo_data['time_ms'],
                marker=markers[i % len(markers)],
                color=colors[i % len(colors)],
                linewidth=2, markersize=8,
                label=algo, alpha=0.8)

    plt.xlabel('Tama�o de entrada (n)', fontweight='bold')
    plt.ylabel('Tiempo de ejecuci�n (ms)', fontweight='bold')
    plt.title('Comparaci�n de Tiempo de Ejecuci�n vs Tama�o de Entrada',
              fontweight='bold', pad=20)
    plt.legend(frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '01_tiempo_vs_n.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" Gr�fico 1 generado: Tiempo vs n")

def plot_2_memory_vs_n(df):
    """Gr�fico 2: Uso de memoria vs tama�o de entrada (n)"""
    plt.figure(figsize=(12, 7))

    algorithms = df['algorithm'].unique()
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    markers = ['o', 's', '^', 'D']

    for i, algo in enumerate(algorithms):
        algo_data = df[df['algorithm'] == algo].groupby('n')['memory_kb'].mean().reset_index()
        plt.plot(algo_data['n'], algo_data['memory_kb'],
                marker=markers[i % len(markers)],
                color=colors[i % len(colors)],
                linewidth=2, markersize=8,
                label=algo, alpha=0.8)

    plt.xlabel('Tama�o de entrada (n)', fontweight='bold')
    plt.ylabel('Memoria utilizada (KB)', fontweight='bold')
    plt.title('Comparaci�n de Uso de Memoria vs Tama�o de Entrada',
              fontweight='bold', pad=20)
    plt.legend(frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '02_memoria_vs_n.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" Gr�fico 2 generado: Memoria vs n")

def plot_3_optimal_vs_n(df):
    """Gr�fico 3: Valor �ptimo vs tama�o de entrada (n)"""
    plt.figure(figsize=(12, 7))

    # Filtrar solo el algoritmo �ptimo (brute-force o dynamic-programming)
    optimal_algos = ['brute-force', 'dynamic-programming']
    df_optimal = df[df['algorithm'].isin(optimal_algos)]

    if len(df_optimal) == 0:
        print("� No se encontraron datos para algoritmos �ptimos")
        return

    # Agrupar por n y tomar el m�ximo valor (asumiendo problema de maximizaci�n)
    optimal_values = df_optimal.groupby('n')['result_value'].max().reset_index()

    plt.plot(optimal_values['n'], optimal_values['result_value'],
            marker='o', color='#27ae60', linewidth=2.5, markersize=10,
            label='Soluci�n �ptima', alpha=0.8)

    plt.xlabel('Tama�o de entrada (n)', fontweight='bold')
    plt.ylabel('Valor de la soluci�n �ptima', fontweight='bold')
    plt.title('Evoluci�n de la Soluci�n �ptima seg�n Tama�o de Entrada',
              fontweight='bold', pad=20)
    plt.legend(frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '03_optimo_vs_n.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" Gr�fico 3 generado: �ptimo vs n")

def plot_4_time_vs_input_type(df):
    """Gr�fico 4: Tiempo vs n comparando tipos de input (bloques vs random)"""
    plt.figure(figsize=(12, 7))

    if 'input_type' not in df.columns:
        print("� No se encontr� la columna 'input_type' en los datos")
        return

    input_types = df['input_type'].unique()
    colors = {'random': '#e74c3c', 'bloques': '#3498db', 'blocks': '#3498db'}
    markers = {'random': 'o', 'bloques': 's', 'blocks': 's'}

    # Seleccionar un algoritmo representativo (preferiblemente greedy o dynamic)
    representative_algo = df['algorithm'].mode()[0]
    df_filtered = df[df['algorithm'] == representative_algo]

    for input_type in input_types:
        type_data = df_filtered[df_filtered['input_type'] == input_type].groupby('n')['time_ms'].mean().reset_index()

        color = colors.get(input_type, '#95a5a6')
        marker = markers.get(input_type, '^')

        plt.plot(type_data['n'], type_data['time_ms'],
                marker=marker, color=color,
                linewidth=2, markersize=8,
                label=f'Input {input_type.capitalize()}', alpha=0.8)

    plt.xlabel('Tama�o de entrada (n)', fontweight='bold')
    plt.ylabel('Tiempo de ejecuci�n (ms)', fontweight='bold')
    plt.title(f'Impacto del Tipo de Input en Tiempo de Ejecuci�n ({representative_algo})',
              fontweight='bold', pad=20)
    plt.legend(frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '04_tiempo_vs_tipo_input.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" Gr�fico 4 generado: Tiempo vs tipo de input")

def plot_5_greedy_quality(df):
    """Gr�fico 5: Calidad de soluci�n de greedy vs n"""
    plt.figure(figsize=(12, 7))

    # Identificar algoritmos greedy y el �ptimo
    greedy_algos = [algo for algo in df['algorithm'].unique() if 'greedy' in algo.lower()]
    optimal_algos = ['brute-force', 'dynamic-programming']

    if len(greedy_algos) == 0:
        print("� No se encontraron algoritmos greedy")
        return

    # Obtener valores �ptimos por n
    df_optimal = df[df['algorithm'].isin(optimal_algos)]
    optimal_by_n = df_optimal.groupby('n')['result_value'].max().reset_index()
    optimal_by_n.rename(columns={'result_value': 'optimal_value'}, inplace=True)

    colors = ['#e67e22', '#9b59b6', '#1abc9c']
    markers = ['s', '^', 'D']

    for i, greedy_algo in enumerate(greedy_algos):
        greedy_data = df[df['algorithm'] == greedy_algo].groupby('n')['result_value'].mean().reset_index()

        # Merge con valores �ptimos para calcular calidad
        merged = greedy_data.merge(optimal_by_n, on='n', how='inner')
        merged['quality'] = (merged['result_value'] / merged['optimal_value']) * 100

        plt.plot(merged['n'], merged['quality'],
                marker=markers[i % len(markers)],
                color=colors[i % len(colors)],
                linewidth=2, markersize=8,
                label=greedy_algo, alpha=0.8)

    # L�nea del 100% (�ptimo)
    if len(optimal_by_n) > 0:
        plt.axhline(y=100, color='#27ae60', linestyle='--', linewidth=2,
                   label='�ptimo (100%)', alpha=0.7)

    plt.xlabel('Tama�o de entrada (n)', fontweight='bold')
    plt.ylabel('Calidad de la soluci�n (%)', fontweight='bold')
    plt.title('Comparaci�n de Calidad: Algoritmos Greedy vs Soluci�n �ptima',
              fontweight='bold', pad=20)
    plt.ylim([0, 105])
    plt.legend(frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '05_calidad_greedy_vs_n.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" Gr�fico 5 generado: Calidad de greedy vs n")

def main():
    """Funci�n principal para generar todos los gr�ficos"""
    print("\n" + "="*60)
    print("GENERADOR DE GR�FICOS - TAREA 2 INF221")
    print("="*60 + "\n")

    # Cargar datos
    print("Cargando datos de mediciones...")
    df = load_measurements()

    if df is None or len(df) == 0:
        print("\n� No hay datos para procesar.")
        print("Aseg�rate de tener archivos CSV en:", MEASUREMENTS_DIR)
        print("\nFormato esperado del CSV:")
        print("n,algorithm,input_type,time_ms,memory_kb,result_value")
        return

    print(f" Datos cargados: {len(df)} registros\n")

    # Generar los 5 gr�ficos
    print("Generando gr�ficos...")
    print("-" * 60)

    plot_1_time_vs_n(df)
    plot_2_memory_vs_n(df)
    plot_3_optimal_vs_n(df)
    plot_4_time_vs_input_type(df)
    plot_5_greedy_quality(df)

    print("-" * 60)
    print(f"\n Todos los gr�ficos generados exitosamente en: {PLOTS_DIR}")
    print("\nGr�ficos generados:")
    print("  1. 01_tiempo_vs_n.png")
    print("  2. 02_memoria_vs_n.png")
    print("  3. 03_optimo_vs_n.png")
    print("  4. 04_tiempo_vs_tipo_input.png")
    print("  5. 05_calidad_greedy_vs_n.png")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
