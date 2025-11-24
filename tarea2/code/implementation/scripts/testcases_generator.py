#!/usr/bin/env python3
"""
Generador de casos de prueba para el problema de productividad de CppCorp

Referencias:
- Enunciado Tarea 2, INF-221 Algoritmos y Complejidad 2025-2

Descripción:
Este script genera casos de prueba válidos para el problema, guardándolos en
el directorio code/implementation/data/inputs/

Formato de archivo: testcases_{n}_{i}.txt
donde n es el número de empleados e i es el identificador del caso
"""

import random
import os
import sys

def generate_test_case(n, case_id, output_dir="data/inputs"):
    """
    Genera un caso de prueba con n empleados

    Args:
        n: Número de empleados (1 <= n <= 10^4)
        case_id: Identificador único del caso
        output_dir: Directorio donde guardar el archivo
    """
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Nombre del archivo
    filename = f"{output_dir}/testcases_{n}_{case_id}.txt"

    # Lista de lenguajes de programación comunes
    languages = [
        "cpp", "python", "java", "javascript", "go", "rust",
        "c", "csharp", "ruby", "php", "swift", "kotlin",
        "typescript", "scala", "haskell", "perl"
    ]

    with open(filename, 'w') as f:
        # Escribir número de empleados
        f.write(f"{n}\n")

        # Generar datos para cada empleado
        for i in range(n):
            # Productividades entre -10^9 y 10^9
            A = random.randint(-10**9, 10**9)
            B = random.randint(-10**9, 10**9)

            # Lenguaje favorito
            C = random.choice(languages)

            f.write(f"{A} {B} {C}\n")

    print(f"Generado: {filename}")
    return filename

def generate_small_cases(output_dir="data/inputs"):
    """Genera casos de prueba pequeños para testing"""
    sizes = [1, 2, 3, 5, 8, 10, 15, 20]
    for size in sizes:
        for i in range(3):  # 3 casos por tamaño
            generate_test_case(size, i, output_dir)

def generate_medium_cases(output_dir="data/inputs"):
    """Genera casos de prueba medianos"""
    sizes = [50, 100, 200, 500]
    for size in sizes:
        for i in range(5):  # 5 casos por tamaño
            generate_test_case(size, i, output_dir)

def generate_large_cases(output_dir="data/inputs"):
    """Genera casos de prueba grandes"""
    sizes = [1000, 2000, 5000, 10000]
    for size in sizes:
        for i in range(3):  # 3 casos por tamaño
            generate_test_case(size, i, output_dir)

def generate_edge_cases(output_dir="data/inputs"):
    """Genera casos de prueba de borde específicos"""

    # Caso 1: Todos con el mismo lenguaje
    n = 10
    filename = f"{output_dir}/testcases_{n}_same_lang.txt"
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for i in range(n):
            A = random.randint(1, 100)
            B = random.randint(-100, -1)
            f.write(f"{A} {B} cpp\n")
    print(f"Generado caso especial: {filename}")

    # Caso 2: Todos con lenguajes diferentes
    filename = f"{output_dir}/testcases_{n}_diff_lang.txt"
    languages = ["cpp", "python", "java", "javascript", "go",
                 "rust", "c", "csharp", "ruby", "php"]
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for i in range(n):
            A = random.randint(-100, 100)
            B = random.randint(-100, 100)
            f.write(f"{A} {B} {languages[i]}\n")
    print(f"Generado caso especial: {filename}")

    # Caso 3: Productividades extremas
    filename = f"{output_dir}/testcases_{n}_extreme.txt"
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        for i in range(n):
            A = random.choice([-10**9, 10**9])
            B = random.choice([-10**9, 10**9])
            C = random.choice(["cpp", "python", "java"])
            f.write(f"{A} {B} {C}\n")
    print(f"Generado caso especial: {filename}")

def generate_examples_from_statement(output_dir="data/inputs"):
    """Genera los ejemplos del enunciado"""

    # Ejemplo 1
    filename = f"{output_dir}/testcases_5_example1.txt"
    with open(filename, 'w') as f:
        f.write("5\n")
        f.write("10 5 cpp\n")
        f.write("-8 9 python\n")
        f.write("-20 4 cpp\n")
        f.write("-7 2 java\n")
        f.write("30 -5 cpp\n")
    print(f"Generado ejemplo 1: {filename}")

    # Ejemplo 2
    filename = f"{output_dir}/testcases_6_example2.txt"
    with open(filename, 'w') as f:
        f.write("6\n")
        f.write("10 5 cpp\n")
        f.write("-5 20 c\n")
        f.write("30 -5 cpp\n")
        f.write("20 -1 java\n")
        f.write("-10 10 python\n")
        f.write("10 5 java\n")
    print(f"Generado ejemplo 2: {filename}")

def main():
    """Función principal"""
    # Determinar directorio de salida
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        # Intentar determinar la ruta correcta
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "..", "data", "inputs")

    print(f"Generando casos de prueba en: {output_dir}")
    print("=" * 60)

    # Generar ejemplos del enunciado
    print("\n1. Ejemplos del enunciado:")
    generate_examples_from_statement(output_dir)

    # Generar casos pequeños
    print("\n2. Casos pequeños (para fuerza bruta):")
    generate_small_cases(output_dir)

    # Generar casos medianos
    print("\n3. Casos medianos:")
    generate_medium_cases(output_dir)

    # Generar casos grandes
    print("\n4. Casos grandes:")
    generate_large_cases(output_dir)

    # Generar casos de borde
    print("\n5. Casos de borde:")
    generate_edge_cases(output_dir)

    print("\n" + "=" * 60)
    print("Generación de casos de prueba completada!")

if __name__ == "__main__":
    main()
