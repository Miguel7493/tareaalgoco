import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from collections import defaultdict

# Configuración de estilo para gráficos profesionales
plt.style.use('seaborn-v0_8-whitegrid')
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

ALGORITMOS = {
    'brute-force': {'nombre': 'Fuerza Bruta', 'color': '#e74c3c', 'marker': 'o'},
    'greedy1': {'nombre': 'Greedy 1', 'color': '#3498db', 'marker': 's'},
    'greedy2': {'nombre': 'Greedy 2', 'color': '#2ecc71', 'marker': '^'},
    'dynamic-programming': {'nombre': 'Prog. Dinámica', 'color': '#9b59b6', 'marker': 'd'}
}

def load_measurements():
    """
    Carga los archivos de mediciones desde archivos .txt con formato:
    testcase,n,time_ms,memory_kb,result
    """
    mediciones = defaultdict(list)
    
    for file in MEASUREMENTS_DIR.glob('measurements_*.txt'):
        algo = file.stem.replace('measurements_', '')
        
        with open(file, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(',')
                if len(partes) == 5:
                    testcase = partes[0]
                    n = int(partes[1])
                    time_ms = float(partes[2])
                    memory_kb = int(partes[3])
                    result = int(partes[4])
                    
                    tipo = "unknown"
                    if "_random_" in testcase:
                        tipo = "random"
                    elif "_bloques_" in testcase:
                        tipo = "bloques"
                    
                    mediciones[algo].append({
                        'n': n,
                        'time_ms': time_ms,
                        'memory_kb': memory_kb,
                        'result': result,
                        'tipo': tipo
                    })
    
    return mediciones

def plot_1_time_vs_n(mediciones):
    """Gráfico 1: Tiempo de ejecución vs tamaño de entrada (n) - Separado por tipo de input"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    fig.suptitle('Comparación de Tiempo de Ejecución vs Tamaño de Entrada',
                 fontweight='bold', fontsize=16, y=0.98)
    
    # Gráfico 1a: Input Random
    for algo, info in ALGORITMOS.items():
        if algo not in mediciones:
            continue
        
        datos = mediciones[algo]
        n_values = defaultdict(list)
        for d in datos:
            if d['tipo'] == 'random':
                n_values[d['n']].append(d['time_ms'])
        
        if not n_values:
            continue
        
        x = sorted(n_values.keys())
        y = [np.mean(n_values[n]) for n in x]
        
        ax1.plot(x, y, marker=info['marker'], color=info['color'],
                linewidth=2.5, markersize=7, label=info['nombre'], alpha=0.85)
    
    ax1.set_xlabel('Tamaño de entrada (n)', fontweight='bold')
    ax1.set_ylabel('Tiempo de ejecución (ms) [Escala Log]', fontweight='bold')
    ax1.set_title('Input Random', fontweight='bold', pad=15)
    ax1.set_yscale('log')
    ax1.legend(frameon=True, shadow=True, loc='upper left')
    ax1.grid(True, alpha=0.3, which='both')
    
    # Gráfico 1b: Input Bloques
    for algo, info in ALGORITMOS.items():
        if algo not in mediciones:
            continue
        
        datos = mediciones[algo]
        n_values = defaultdict(list)
        for d in datos:
            if d['tipo'] == 'bloques':
                n_values[d['n']].append(d['time_ms'])
        
        if not n_values:
            continue
        
        x = sorted(n_values.keys())
        y = [np.mean(n_values[n]) for n in x]
        
        ax2.plot(x, y, marker=info['marker'], color=info['color'],
                linewidth=2.5, markersize=7, label=info['nombre'], alpha=0.85)
    
    ax2.set_xlabel('Tamaño de entrada (n)', fontweight='bold')
    ax2.set_ylabel('Tiempo de ejecución (ms) [Escala Log]', fontweight='bold')
    ax2.set_title('Input Bloques', fontweight='bold', pad=15)
    ax2.set_yscale('log')
    ax2.legend(frameon=True, shadow=True, loc='upper left')
    ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '01_tiempo_vs_n.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 1 generado: Tiempo vs n (Random y Bloques separados)")

def plot_2_memory_vs_n(mediciones):
    """Gráfico 2: Uso de memoria vs tamaño de entrada (n)"""
    plt.figure(figsize=(12, 7))
    
    for algo, info in ALGORITMOS.items():
        if algo not in mediciones:
            continue
        
        datos = mediciones[algo]
        n_values = defaultdict(list)
        for d in datos:
            if d['memory_kb'] > 0:
                n_values[d['n']].append(d['memory_kb'])
        
        if not n_values:
            continue
        
        x = sorted(n_values.keys())
        y = [np.mean(n_values[n]) for n in x]
        
        plt.plot(x, y, marker=info['marker'], color=info['color'],
                linewidth=2, markersize=6, label=info['nombre'], alpha=0.8)
    
    plt.xlabel('Tamaño de entrada (n)', fontweight='bold')
    plt.ylabel('Memoria utilizada (KB)', fontweight='bold')
    plt.title('Comparación de Uso de Memoria vs Tamaño de Entrada',
              fontweight='bold', pad=20)
    plt.legend(frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '02_memoria_vs_n.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" Gráfico 2 generado: Memoria vs n")

def plot_3_optimal_vs_n(mediciones):
    """Gráfico 3: Valor óptimo vs tamaño de entrada (n)"""
    plt.figure(figsize=(12, 7))
    
    # Usar dynamic-programming como óptimo
    algo_optimo = 'dynamic-programming'
    if algo_optimo not in mediciones:
        print("⚠ No se encontraron datos para dynamic-programming")
        return
    
    datos = mediciones[algo_optimo]
    n_values = defaultdict(list)
    for d in datos:
        n_values[d['n']].append(d['result'])
    
    x = sorted(n_values.keys())
    y = [np.max(n_values[n]) for n in x]
    
    plt.plot(x, y, marker='o', color='#27ae60', linewidth=2.5, markersize=8,
            label='Solución Óptima', alpha=0.8)
    
    plt.xlabel('Tamaño de entrada (n)', fontweight='bold')
    plt.ylabel('Valor de la solución óptima', fontweight='bold')
    plt.title('Evolución de la Solución Óptima según Tamaño de Entrada',
              fontweight='bold', pad=20)
    plt.legend(frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '03_optimo_vs_n.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" Gráfico 3 generado: Óptimo vs n")

def plot_4_time_vs_input_type(mediciones):
    """Gráfico 4: Tiempo vs n comparando tipos de input para todos los algoritmos"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Impacto del Tipo de Input en Tiempo de Ejecución por Algoritmo',
                 fontweight='bold', fontsize=16, y=0.995)
    
    algos_order = ['brute-force', 'dynamic-programming', 'greedy1', 'greedy2']
    
    for idx, algo in enumerate(algos_order):
        ax = axes[idx // 2, idx % 2]
        
        if algo not in mediciones:
            ax.set_visible(False)
            continue
        
        datos = mediciones[algo]
        
        # Separar por tipo
        random_data = defaultdict(list)
        bloques_data = defaultdict(list)
        
        for d in datos:
            if d['tipo'] == 'random':
                random_data[d['n']].append(d['time_ms'])
            elif d['tipo'] == 'bloques':
                bloques_data[d['n']].append(d['time_ms'])
        
        if random_data:
            x = sorted(random_data.keys())
            y = [np.mean(random_data[n]) for n in x]
            ax.plot(x, y, marker='o', color='#e74c3c', linewidth=2.5, markersize=6,
                   label='Random', alpha=0.8)
        
        if bloques_data:
            x = sorted(bloques_data.keys())
            y = [np.mean(bloques_data[n]) for n in x]
            ax.plot(x, y, marker='s', color='#3498db', linewidth=2.5, markersize=6,
                   label='Bloques', alpha=0.8)
        
        ax.set_xlabel('Tamaño de entrada (n)', fontweight='bold')
        ax.set_ylabel('Tiempo (ms)', fontweight='bold')
        ax.set_title(ALGORITMOS[algo]['nombre'], fontweight='bold', pad=10)
        ax.legend(frameon=True, shadow=True)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '04_tiempo_vs_tipo_input.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico 4 generado: Tiempo vs tipo de input (todos los algoritmos)")

def plot_5_greedy_quality(mediciones):
    """Gráfico 5: Calidad de solución de greedy vs n"""
    plt.figure(figsize=(12, 7))
    
    # Obtener valores óptimos
    if 'dynamic-programming' not in mediciones:
        print("⚠ No se encontraron datos para calcular calidad de greedy")
        return
    
    optimos = {}
    for d in mediciones['dynamic-programming']:
        key = (d['n'], d['tipo'])
        if key not in optimos or d['result'] > optimos[key]:
            optimos[key] = d['result']
    
    # Calcular calidad para cada greedy
    greedy_algos = ['greedy1', 'greedy2']
    colors = ['#e67e22', '#9b59b6']
    markers = ['s', '^']
    
    for i, greedy in enumerate(greedy_algos):
        if greedy not in mediciones:
            continue
        
        calidad_por_n = defaultdict(list)
        
        for d in mediciones[greedy]:
            key = (d['n'], d['tipo'])
            if key in optimos and optimos[key] > 0:
                calidad = (d['result'] / optimos[key]) * 100
                calidad_por_n[d['n']].append(calidad)
        
        if not calidad_por_n:
            continue
        
        x = sorted(calidad_por_n.keys())
        y = [np.mean(calidad_por_n[n]) for n in x]
        
        plt.plot(x, y, marker=markers[i], color=colors[i],
                linewidth=2, markersize=6, label=ALGORITMOS[greedy]['nombre'], alpha=0.8)
    
    # Línea del 100% (óptimo)
    plt.axhline(y=100, color='#27ae60', linestyle='--', linewidth=2,
               label='Óptimo (100%)', alpha=0.7)
    
    plt.xlabel('Tamaño de entrada (n)', fontweight='bold')
    plt.ylabel('Calidad de la solución (%)', fontweight='bold')
    plt.title('Comparación de Calidad: Algoritmos Greedy vs Solución Óptima',
              fontweight='bold', pad=20)
    plt.ylim([0, 110])
    plt.legend(frameon=True, shadow=True)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / '05_calidad_greedy_vs_n.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(" Gráfico 5 generado: Calidad de greedy vs n")

def main():
    """Función principal para generar todos los gráficos"""
    
    print("Cargando datos de mediciones...")
    mediciones = load_measurements()

    if not mediciones or len(mediciones) == 0:
        print("\n⚠ No hay datos para procesar.")
        print("Asegúrate de tener archivos .txt en:", MEASUREMENTS_DIR)
        return

    total_registros = sum(len(v) for v in mediciones.values())
    print(f" Datos cargados: {total_registros} registros\n")

    print("Generando gráficos...")
    
    plot_1_time_vs_n(mediciones)
    plot_2_memory_vs_n(mediciones)
    plot_3_optimal_vs_n(mediciones)
    plot_4_time_vs_input_type(mediciones)
    plot_5_greedy_quality(mediciones)
    
    print(f"\n Todos los gráficos generados exitosamente en: {PLOTS_DIR}")

if __name__ == "__main__":
    main()
