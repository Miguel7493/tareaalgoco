/*
 * Programa Principal para ejecutar y comparar algoritmos de CppCorp
 *
 * Referencias:
 * - Enunciado Tarea 2, INF-221 Algoritmos y Complejidad 2025-2
 *
 * Descripción:
 * Este programa ejecuta todos los algoritmos implementados (fuerza bruta,
 * greedy1, greedy2, y programación dinámica) y mide su tiempo de ejecución
 * y uso de memoria.
 *
 * Genera archivos de salida en:
 * - code/implementation/data/measurements/
 * - code/implementation/data/outputs/
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <climits>
#include <chrono>
#include <sys/resource.h>

using namespace std;
using namespace std::chrono;

struct Employee {
    long long A;  // Productividad con lenguaje favorito
    long long B;  // Productividad con otro lenguaje
    string C;     // Lenguaje favorito
};

// Calcula la productividad de un equipo [l, r]
long long teamProductivity(const vector<Employee>& employees, int l, int r) {
    map<string, int> frequency;
    for (int i = l; i <= r; i++) {
        frequency[employees[i].C]++;
    }

    int maxFreq = 0;
    for (const auto& pair : frequency) {
        maxFreq = max(maxFreq, pair.second);
    }

    vector<string> maxFreqLanguages;
    for (const auto& pair : frequency) {
        if (pair.second == maxFreq) {
            maxFreqLanguages.push_back(pair.first);
        }
    }

    long long minProductivity = LLONG_MAX;
    for (const string& lang : maxFreqLanguages) {
        long long productivity = 0;
        for (int i = l; i <= r; i++) {
            if (employees[i].C == lang) {
                productivity += employees[i].A;
            } else {
                productivity += employees[i].B;
            }
        }
        minProductivity = min(minProductivity, productivity);
    }

    return minProductivity;
}

// ========== FUERZA BRUTA ==========
long long bruteForceSolve(const vector<Employee>& employees, int start, int n) {
    if (start >= n) return 0;

    long long maxProd = LLONG_MIN;
    for (int end = start; end < n; end++) {
        long long currentTeamProd = teamProductivity(employees, start, end);
        long long remainingProd = bruteForceSolve(employees, end + 1, n);
        maxProd = max(maxProd, currentTeamProd + remainingProd);
    }
    return maxProd;
}

long long solveBruteForce(const vector<Employee>& employees) {
    return bruteForceSolve(employees, 0, employees.size());
}

// ========== GREEDY 1 ==========
long long solveGreedy1(const vector<Employee>& employees) {
    int n = employees.size();
    long long totalProductivity = 0;
    int currentPos = 0;

    while (currentPos < n) {
        long long maxLocalProd = LLONG_MIN;
        int bestEnd = currentPos;

        for (int end = currentPos; end < n; end++) {
            long long prod = teamProductivity(employees, currentPos, end);
            if (prod > maxLocalProd) {
                maxLocalProd = prod;
                bestEnd = end;
            }
        }

        totalProductivity += maxLocalProd;
        currentPos = bestEnd + 1;
    }

    return totalProductivity;
}

// ========== GREEDY 2 ==========
long long solveGreedy2(const vector<Employee>& employees) {
    int n = employees.size();
    long long totalProductivity = 0;
    int currentPos = 0;

    while (currentPos < n) {
        int teamEnd = currentPos;

        for (int next = currentPos + 1; next < n; next++) {
            long long currentTeamProd = teamProductivity(employees, currentPos, teamEnd);
            long long nextAloneProd = teamProductivity(employees, next, next);
            long long expandedProd = teamProductivity(employees, currentPos, next);

            if (expandedProd >= currentTeamProd + nextAloneProd) {
                teamEnd = next;
            } else {
                break;
            }
        }

        totalProductivity += teamProductivity(employees, currentPos, teamEnd);
        currentPos = teamEnd + 1;
    }

    return totalProductivity;
}

// ========== PROGRAMACIÓN DINÁMICA ==========
long long solveDynamicProgramming(const vector<Employee>& employees) {
    int n = employees.size();
    vector<long long> dp(n + 1);
    dp[0] = 0;

    for (int i = 1; i <= n; i++) {
        dp[i] = LLONG_MIN;
        for (int j = 0; j < i; j++) {
            long long teamProd = teamProductivity(employees, j, i - 1);
            dp[i] = max(dp[i], dp[j] + teamProd);
        }
    }

    return dp[n];
}

// Obtener uso de memoria en KB
long getMemoryUsage() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    return usage.ru_maxrss;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Uso: " << argv[0] << " <archivo_entrada> [algoritmo]" << endl;
        cerr << "Algoritmos: brute-force, greedy1, greedy2, dynamic-programming, all" << endl;
        return 1;
    }

    string inputFile = argv[1];
    string algorithm = (argc >= 3) ? argv[2] : "all";

    // Leer entrada
    ifstream input(inputFile);
    if (!input.is_open()) {
        cerr << "Error: no se pudo abrir el archivo " << inputFile << endl;
        return 1;
    }

    int n;
    input >> n;

    vector<Employee> employees(n);
    for (int i = 0; i < n; i++) {
        input >> employees[i].A >> employees[i].B >> employees[i].C;
    }
    input.close();

    // Extraer nombre base del archivo
    size_t lastSlash = inputFile.find_last_of("/\\");
    size_t lastDot = inputFile.find_last_of(".");
    string baseName = inputFile.substr(lastSlash + 1, lastDot - lastSlash - 1);

    // Ejecutar algoritmos
    vector<string> algorithms;
    if (algorithm == "all") {
        // Solo ejecutar brute-force para n pequeño
        if (n <= 20) {
            algorithms.push_back("brute-force");
        }
        algorithms.push_back("greedy1");
        algorithms.push_back("greedy2");
        algorithms.push_back("dynamic-programming");
    } else {
        algorithms.push_back(algorithm);
    }

    for (const string& algo : algorithms) {
        long long result = 0;
        long memBefore = getMemoryUsage();
        auto start = high_resolution_clock::now();

        if (algo == "brute-force") {
            result = solveBruteForce(employees);
        } else if (algo == "greedy1") {
            result = solveGreedy1(employees);
        } else if (algo == "greedy2") {
            result = solveGreedy2(employees);
        } else if (algo == "dynamic-programming") {
            result = solveDynamicProgramming(employees);
        }

        auto end = high_resolution_clock::now();
        long memAfter = getMemoryUsage();

        auto duration = duration_cast<microseconds>(end - start);
        double timeMs = duration.count() / 1000.0;
        long memUsed = memAfter - memBefore;

        // Guardar resultado
        string outputFile = "data/outputs/" + baseName + "_" + algo + ".txt";
        ofstream output(outputFile);
        output << result << endl;
        output.close();

        // Guardar mediciones
        string measurementFile = "data/measurements/" + baseName + "_" + algo + ".txt";
        ofstream measurement(measurementFile);
        measurement << "n: " << n << endl;
        measurement << "time_ms: " << timeMs << endl;
        measurement << "memory_kb: " << memUsed << endl;
        measurement << "result: " << result << endl;
        measurement.close();

        cout << algo << ": " << result << " (tiempo: " << timeMs << " ms)" << endl;
    }

    return 0;
}
