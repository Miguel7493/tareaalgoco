/*
 * Algoritmo de Programación Dinámica para el problema de productividad de CppCorp
 *
 * Referencias:
 * - Enunciado Tarea 2, INF-221 Algoritmos y Complejidad 2025-2
 * - Cormen et al., "Introduction to Algorithms" - Dynamic Programming
 *
 * Descripción:
 * Solución óptima usando programación dinámica.
 *
 * Estado: dp[i] = máxima productividad considerando los primeros i empleados
 * Transición: dp[i] = max(dp[j] + productividad_equipo(j, i-1)) para todo j < i
 *
 * Complejidad: O(n^3) donde n es el número de empleados
 * - O(n^2) estados y transiciones
 * - O(n) para calcular productividad de cada equipo
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

// Programación Dinámica
long long solveDynamicProgramming(const vector<Employee>& employees) {
    int n = employees.size();

    // dp[i] = máxima productividad considerando los primeros i empleados
    vector<long long> dp(n + 1);
    dp[0] = 0;  // Sin empleados, productividad 0

    // Para cada posición
    for (int i = 1; i <= n; i++) {
        dp[i] = LLONG_MIN;

        // Probar formar el último equipo desde j hasta i-1
        for (int j = 0; j < i; j++) {
            long long teamProd = teamProductivity(employees, j, i - 1);
            dp[i] = max(dp[i], dp[j] + teamProd);
        }
    }

    return dp[n];
}

int main() {
    int n;
    cin >> n;

    vector<Employee> employees(n);
    for (int i = 0; i < n; i++) {
        cin >> employees[i].A >> employees[i].B >> employees[i].C;
    }

    long long result = solveDynamicProgramming(employees);
    cout << result << endl;

    return 0;
}
