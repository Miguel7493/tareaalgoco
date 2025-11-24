# Makefile para compilar los algoritmos de la Tarea 2
# INF-221 Algoritmos y Complejidad 2025-2

CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra

# Directorios
ALGO_DIR = algorithms
DATA_DIR = data
INPUTS_DIR = $(DATA_DIR)/inputs
OUTPUTS_DIR = $(DATA_DIR)/outputs
MEASUREMENTS_DIR = $(DATA_DIR)/measurements
PLOTS_DIR = $(DATA_DIR)/plots

# Archivos ejecutables
BRUTE_FORCE = brute-force
GREEDY1 = greedy1
GREEDY2 = greedy2
DYNAMIC = dynamic-programming
GENERAL = general

# Todos los ejecutables
ALL_EXECS = $(BRUTE_FORCE) $(GREEDY1) $(GREEDY2) $(DYNAMIC) $(GENERAL)

# Regla por defecto
all: $(ALL_EXECS)

# Compilar cada algoritmo
$(BRUTE_FORCE): $(ALGO_DIR)/brute-force.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

$(GREEDY1): $(ALGO_DIR)/greedy1.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

$(GREEDY2): $(ALGO_DIR)/greedy2.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

$(DYNAMIC): $(ALGO_DIR)/dynamic-programming.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

$(GENERAL): general.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

# Limpiar archivos compilados
clean:
	rm -f $(ALL_EXECS)
	rm -f $(OUTPUTS_DIR)/*
	rm -f $(MEASUREMENTS_DIR)/*

# Limpiar todo incluyendo gráficos
cleanall: clean
	rm -f $(PLOTS_DIR)/*

# Crear directorios si no existen
dirs:
	mkdir -p $(INPUTS_DIR)
	mkdir -p $(OUTPUTS_DIR)
	mkdir -p $(MEASUREMENTS_DIR)
	mkdir -p $(PLOTS_DIR)

# Ejecutar un ejemplo
test-example1: $(GENERAL) dirs
	echo "5\n10 5 cpp\n-8 9 python\n-20 4 cpp\n-7 2 java\n30 -5 cpp" | ./$(GENERAL) /dev/stdin dynamic-programming

test-example2: $(GENERAL) dirs
	echo "6\n10 5 cpp\n-5 20 c\n30 -5 cpp\n20 -1 java\n-10 10 python\n10 5 java" | ./$(GENERAL) /dev/stdin dynamic-programming

# Ayuda
help:
	@echo "Makefile para la Tarea 2 - CppCorp"
	@echo ""
	@echo "Objetivos disponibles:"
	@echo "  all              - Compilar todos los programas"
	@echo "  brute-force      - Compilar solo fuerza bruta"
	@echo "  greedy1          - Compilar solo greedy1"
	@echo "  greedy2          - Compilar solo greedy2"
	@echo "  dynamic-programming - Compilar solo programación dinámica"
	@echo "  general          - Compilar programa principal"
	@echo "  clean            - Limpiar ejecutables y resultados"
	@echo "  cleanall         - Limpiar todo incluyendo gráficos"
	@echo "  dirs             - Crear directorios necesarios"
	@echo "  test-example1    - Ejecutar ejemplo 1 del enunciado"
	@echo "  test-example2    - Ejecutar ejemplo 2 del enunciado"

.PHONY: all clean cleanall dirs help test-example1 test-example2
