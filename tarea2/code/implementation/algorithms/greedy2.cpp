/*
 * Algoritmo Greedy 2 para el problema de productividad de CppCorp
 *
 * Referencias:
 * - Enunciado Tarea 2, INF-221 Algoritmos y Complejidad 2025-2
 *
 * Descripción:
 * Heurística greedy que agrupa empleados mientras la productividad
 * incremental sea positiva.
 *
 * Estrategia: Expandir el equipo actual mientras agregar el siguiente
 * empleado no disminuya demasiado la productividad. Si la productividad
 * del equipo extendido es menor que formar equipos separados, cortar.
 *
 * Complejidad: O(n^2) donde n es el número de empleados
 */

#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <climits>

using namespace std;

struct Employee {
    long long A;  // Productividad con lenguaje favorito
    long long B;  // Productividad con otro lenguaje
    string C;     // Lenguaje favorito
};

// Calcula la productividad de un equipo [l, r]
long long teamProductivity(const vector<Employee>& employees, int l, int r) {
    // Contar frecuencia de cada lenguaje
    map<string, int> frequency;
    for (int i = l; i <= r; i++) {
        frequency[employees[i].C]++;
    }

    // Encontrar frecuencia máxima
    int maxFreq = 0;
    for (const auto& pair : frequency) {
        maxFreq = max(maxFreq, pair.second);
    }

    // Obtener todos los lenguajes con frecuencia máxima
    vector<string> maxFreqLanguages;
    for (const auto& pair : frequency) {
        if (pair.second == maxFreq) {
            maxFreqLanguages.push_back(pair.first);
        }
    }

    // Calcular productividad para cada lenguaje con frecuencia máxima
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

// Greedy 2: Expansión mientras sea beneficioso
// Expandir equipos mientras la productividad del equipo expandido
// sea mayor que formar el siguiente empleado como equipo separado
long long solveGreedy2(const vector<Employee>& employees) {
    int n = employees.size();
    long long totalProductivity = 0;
    int currentPos = 0;

    while (currentPos < n) {
        int teamEnd = currentPos;

        // Expandir el equipo mientras sea beneficioso
        for (int next = currentPos + 1; next < n; next++) {
            long long currentTeamProd = teamProductivity(employees, currentPos, teamEnd);
            long long nextAloneProd = teamProductivity(employees, next, next);
            long long expandedProd = teamProductivity(employees, currentPos, next);

            // Si expandir es mejor que tener equipos separados, expandir
            if (expandedProd >= currentTeamProd + nextAloneProd) {
                teamEnd = next;
            } else {
                break;  // No conviene expandir más
            }
        }

        totalProductivity += teamProductivity(employees, currentPos, teamEnd);
        currentPos = teamEnd + 1;
    }

    return totalProductivity;
}

int main() {
    int n;
    cin >> n;

    vector<Employee> employees(n);
    for (int i = 0; i < n; i++) {
        cin >> employees[i].A >> employees[i].B >> employees[i].C;
    }

    long long result = solveGreedy2(employees);
    cout << result << endl;

    return 0;
}
