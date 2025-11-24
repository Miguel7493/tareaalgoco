#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de graficos para analisis de algoritmos de CppCorp

Referencias:
- Enunciado Tarea 2, INF-221 Algoritmos y Complejidad 2025-2

Descripci�n:
Este script lee los archivos de medici�n generados por los algoritmos
y crea gr�ficos comparativos en formato PNG.

Los gr�ficos se guardan en: code/implementation/data/plots/
"""

import os
import sys
import glob
import re
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def parse_measurement_file(filepath):
    """
    Lee un archivo de medici�n y extrae los datos

    Returns:
        dict con las claves: n, time_ms, memory_kb, result
    """
    data = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()

                    if key in ['n', 'memory_kb']:
                        data[key] = int(value)
                    elif key in ['time_ms']:
                        data[key] = float(value)
                    elif key == 'result':
                        data[key] = int(value)
    except Exception as e:
        print(f"Error leyendo {filepath}: {e}")
        return None

    return data if data else None

def collect_measurements(measurements_dir):
    """
    Recolecta todas las mediciones de los archivos

    Returns:
        dict con estructura: {algorithm: [(n, time_ms, memory_kb, result), ...]}
    """
    measurements = defaultdict(list)

    # Buscar todos los archivos de medici�n
    pattern = os.path.join(measurements_dir, "*.txt")
    files = glob.glob(pattern)

    for filepath in files:
        filename = os.path.basename(filepath)

        # Extraer informaci�n del nombre del archivo
        # Formato esperado: testcases_{n}_{id}_{algorithm}.txt
        match = re.search(r'testcases_(\d+)_\w+_([^.]+)\.txt', filename)
        if match:
            algorithm = match.group(2)
            data = parse_measurement_file(filepath)

            if data and 'n' in data and 'time_ms' in data:
                measurements[algorithm].append((
                    data.get('n', 0),
                    data.get('time_ms', 0),
                    data.get('memory_kb', 0),
                    data.get('result', 0)
                ))

    # Ordenar por n
    for algorithm in measurements:
        measurements[algorithm].sort(key=lambda x: x[0])

    return measurements

def plot_time_comparison(measurements, output_dir):
    """Genera gr�fico de comparaci�n de tiempos"""
    plt.figure(figsize=(12, 8))

    algorithms = ['brute-force', 'greedy1', 'greedy2', 'dynamic-programming']
    colors = {'brute-force': 'red', 'greedy1': 'blue',
              'greedy2': 'green', 'dynamic-programming': 'purple'}
    labels = {'brute-force': 'Fuerza Bruta',
              'greedy1': 'Greedy 1',
              'greedy2': 'Greedy 2',
              'dynamic-programming': 'Programaci�n Din�mica'}

    for algo in algorithms:
        if algo in measurements and measurements[algo]:
            data = measurements[algo]
            n_values = [x[0] for x in data]
            times = [x[1] for x in data]

            plt.plot(n_values, times, 'o-',
                    color=colors.get(algo, 'black'),
                    label=labels.get(algo, algo),
                    linewidth=2, markersize=6)

    plt.xlabel('N�mero de empleados (n)', fontsize=12)
    plt.ylabel('Tiempo de ejecuci�n (ms)', fontsize=12)
    plt.title('Comparaci�n de Tiempos de Ejecuci�n', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(output_dir, 'time_comparison.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gr�fico generado: {output_file}")
    plt.close()

def plot_time_log_scale(measurements, output_dir):
    """Genera gr�fico de tiempos con escala logar�tmica"""
    plt.figure(figsize=(12, 8))

    algorithms = ['brute-force', 'greedy1', 'greedy2', 'dynamic-programming']
    colors = {'brute-force': 'red', 'greedy1': 'blue',
              'greedy2': 'green', 'dynamic-programming': 'purple'}
    labels = {'brute-force': 'Fuerza Bruta',
              'greedy1': 'Greedy 1',
              'greedy2': 'Greedy 2',
              'dynamic-programming': 'Programaci�n Din�mica'}

    for algo in algorithms:
        if algo in measurements and measurements[algo]:
            data = measurements[algo]
            n_values = [x[0] for x in data]
            times = [max(x[1], 0.001) for x in data]  # Evitar log(0)

            plt.semilogy(n_values, times, 'o-',
                        color=colors.get(algo, 'black'),
                        label=labels.get(algo, algo),
                        linewidth=2, markersize=6)

    plt.xlabel('N�mero de empleados (n)', fontsize=12)
    plt.ylabel('Tiempo de ejecuci�n (ms) - Escala Log', fontsize=12)
    plt.title('Comparaci�n de Tiempos (Escala Logar�tmica)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()

    output_file = os.path.join(output_dir, 'time_comparison_log.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gr�fico generado: {output_file}")
    plt.close()

def plot_memory_comparison(measurements, output_dir):
    """Genera gr�fico de comparaci�n de uso de memoria"""
    plt.figure(figsize=(12, 8))

    algorithms = ['brute-force', 'greedy1', 'greedy2', 'dynamic-programming']
    colors = {'brute-force': 'red', 'greedy1': 'blue',
              'greedy2': 'green', 'dynamic-programming': 'purple'}
    labels = {'brute-force': 'Fuerza Bruta',
              'greedy1': 'Greedy 1',
              'greedy2': 'Greedy 2',
              'dynamic-programming': 'Programaci�n Din�mica'}

    for algo in algorithms:
        if algo in measurements and measurements[algo]:
            data = measurements[algo]
            n_values = [x[0] for x in data]
            memory = [x[2] for x in data]

            if any(m > 0 for m in memory):  # Solo graficar si hay datos de memoria
                plt.plot(n_values, memory, 'o-',
                        color=colors.get(algo, 'black'),
                        label=labels.get(algo, algo),
                        linewidth=2, markersize=6)

    plt.xlabel('N�mero de empleados (n)', fontsize=12)
    plt.ylabel('Uso de memoria (KB)', fontsize=12)
    plt.title('Comparaci�n de Uso de Memoria', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(output_dir, 'memory_comparison.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gr�fico generado: {output_file}")
    plt.close()

def plot_algorithm_efficiency(measurements, output_dir):
    """Genera gr�fico de eficiencia (resultado vs tiempo)"""
    plt.figure(figsize=(12, 8))

    algorithms = ['greedy1', 'greedy2', 'dynamic-programming']
    colors = {'greedy1': 'blue', 'greedy2': 'green',
              'dynamic-programming': 'purple'}
    labels = {'greedy1': 'Greedy 1',
              'greedy2': 'Greedy 2',
              'dynamic-programming': 'Programaci�n Din�mica'}

    for algo in algorithms:
        if algo in measurements and measurements[algo]:
            data = measurements[algo]
            times = [x[1] for x in data]
            results = [x[3] for x in data]

            plt.scatter(times, results,
                       color=colors.get(algo, 'black'),
                       label=labels.get(algo, algo),
                       s=50, alpha=0.6)

    plt.xlabel('Tiempo de ejecuci�n (ms)', fontsize=12)
    plt.ylabel('Productividad obtenida', fontsize=12)
    plt.title('Eficiencia: Productividad vs Tiempo', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(output_dir, 'efficiency_comparison.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gr�fico generado: {output_file}")
    plt.close()

def plot_individual_algorithm(measurements, algorithm, output_dir):
    """Genera gr�fico detallado de un algoritmo espec�fico"""
    if algorithm not in measurements or not measurements[algorithm]:
        return

    data = measurements[algorithm]
    n_values = [x[0] for x in data]
    times = [x[1] for x in data]

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times, 'o-', color='blue', linewidth=2, markersize=8)
    plt.xlabel('N�mero de empleados (n)', fontsize=12)
    plt.ylabel('Tiempo de ejecuci�n (ms)', fontsize=12)
    plt.title(f'Rendimiento: {algorithm}', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = os.path.join(output_dir, f'{algorithm}_performance.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Gr�fico generado: {output_file}")
    plt.close()

def main():
    """Funci�n principal"""
    # Determinar directorios
    if len(sys.argv) > 1:
        measurements_dir = sys.argv[1]
        plots_dir = sys.argv[2] if len(sys.argv) > 2 else "data/plots"
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        measurements_dir = os.path.join(script_dir, "..", "data", "measurements")
        plots_dir = os.path.join(script_dir, "..", "data", "plots")

    # Crear directorio de salida
    os.makedirs(plots_dir, exist_ok=True)

    print(f"Leyendo mediciones de: {measurements_dir}")
    print(f"Guardando gr�ficos en: {plots_dir}")
    print("=" * 60)

    # Recolectar mediciones
    measurements = collect_measurements(measurements_dir)

    if not measurements:
        print("No se encontraron archivos de medici�n.")
        return

    print(f"\nAlgoritmos encontrados: {list(measurements.keys())}")

    # Generar gr�ficos
    print("\nGenerando gr�ficos...")
    plot_time_comparison(measurements, plots_dir)
    plot_time_log_scale(measurements, plots_dir)
    plot_memory_comparison(measurements, plots_dir)
    plot_algorithm_efficiency(measurements, plots_dir)

    # Gr�ficos individuales
    for algo in measurements.keys():
        plot_individual_algorithm(measurements, algo, plots_dir)

    print("\n" + "=" * 60)
    print("Generaci�n de gr�ficos completada!")

if __name__ == "__main__":
    main()
