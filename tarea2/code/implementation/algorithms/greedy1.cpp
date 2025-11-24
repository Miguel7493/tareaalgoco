/*
 * Algoritmo Greedy 1 para el problema de productividad de CppCorp
 *
 * Referencias:
 * - Enunciado Tarea 2, INF-221 Algoritmos y Complejidad 2025-2
 *
 * Descripción:
 * Heurística greedy que selecciona equipos de forma voraz maximizando
 * la productividad local en cada paso.
 *
 * Estrategia: Desde cada posición, formar el equipo que maximice la
 * productividad sin considerar el impacto en el resto de empleados.
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

// Greedy 1: Maximización local
// En cada paso, forma el equipo que maximice la productividad local
long long solveGreedy1(const vector<Employee>& employees) {
    int n = employees.size();
    long long totalProductivity = 0;
    int currentPos = 0;

    while (currentPos < n) {
        long long maxLocalProd = LLONG_MIN;
        int bestEnd = currentPos;

        // Buscar el mejor segmento que empieza en currentPos
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

int main() {
    int n;
    cin >> n;

    vector<Employee> employees(n);
    for (int i = 0; i < n; i++) {
        cin >> employees[i].A >> employees[i].B >> employees[i].C;
    }

    long long result = solveGreedy1(employees);
    cout << result << endl;

    return 0;
}
