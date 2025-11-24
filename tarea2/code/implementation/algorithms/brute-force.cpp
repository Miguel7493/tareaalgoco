/*
 * Algoritmo de Fuerza Bruta para el problema de productividad de CppCorp
 *
 * Referencias:
 * - Enunciado Tarea 2, INF-221 Algoritmos y Complejidad 2025-2
 *
 * Descripción:
 * Este algoritmo prueba todas las posibles particiones de empleados en equipos
 * y encuentra la que maximiza la productividad total.
 * Complejidad: O(2^n * n^2) donde n es el número de empleados
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

// Función recursiva para probar todas las particiones
long long bruteForceSolve(const vector<Employee>& employees, int start, int n) {
    if (start >= n) {
        return 0;
    }

    long long maxProd = LLONG_MIN;

    // Probar formar un equipo desde start hasta end
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

int main() {
    int n;
    cin >> n;

    vector<Employee> employees(n);
    for (int i = 0; i < n; i++) {
        cin >> employees[i].A >> employees[i].B >> employees[i].C;
    }

    long long result = solveBruteForce(employees);
    cout << result << endl;

    return 0;
}
