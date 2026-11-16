# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 13:00:34 2026

@author: chalg
"""

import numpy as np
from scipy.optimize import linprog

# Definición de matriz de costos (12 periodos x 6 meses)
# Se emplea costo gigante (M) como penalización matemática para evitar 
# que el algoritmo envíe unidades a meses pasados (backorders).
M = 1e6 
costos = np.array([
    [110.0, 115.0, 120.0, 125.0, 130.0, 135.0], # Periodo 1 (Reg M1)
    [165.0, 170.0, 175.0, 180.0, 185.0, 190.0], # Periodo 2 (Extra M1)
    [M,      93.0,  98.0, 103.0, 108.0, 113.0], # Periodo 3 (Reg M2)
    [M,     139.5, 144.5, 149.5, 154.5, 159.5], # Periodo 4 (Extra M2)
    [M,     M,     145.0, 150.0, 155.0, 160.0], # Periodo 5 (Reg M3)
    [M,     M,     217.5, 222.5, 227.5, 232.5], # Periodo 6 (Extra M3)
    [M,     M,     M,     106.0, 111.0, 116.0], # Periodo 7 (Reg M4)
    [M,     M,     M,     159.0, 164.0, 169.0], # Periodo 8 (Extra M4)
    [M,     M,     M,     M,     129.0, 134.0], # Periodo 9 (Reg M5)
    [M,     M,     M,     M,     193.5, 198.5], # Periodo 10 (Extra M5)
    [M,     M,     M,     M,     M,      99.0], # Periodo 11 (Reg M6)
    [M,     M,     M,     M,     M,     148.5]  # Periodo 12 (Extra M6)
])

# Convierte la matriz de costos en un vector plano de 72 elementos
c = costos.flatten() 

# Restricciones de Capacidad (A_ub * x <= b_ub)
capacidades = [220, 110, 300, 150, 220, 110, 350, 175, 290, 145, 230, 115]
A_ub = np.zeros((12, 72))
for i in range(12):
    # Asignar '1' a las celdas correspondientes al periodo i
    A_ub[i, i*6 : (i+1)*6] = 1
b_ub = np.array(capacidades)

# Restricciones de Demanda (A_eq * x == b_eq)
demandas = [250, 280, 300, 270, 270, 320]
A_eq = np.zeros((6, 72))
for j in range(6):
    # Asignar '1' a saltos de 6 para alinear columnas de cada mes j
    A_eq[j, j::6] = 1
b_eq = np.array(demandas)

# Resolución del modelo
# Nota matemática: Al ser un problema de transporte (matriz totalmente unimodular), 
# la solución continua caerá automáticamente en números enteros perfectos.
resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')

# Resultados
if resultado.success:
    print("Solución Óptima\n")
    
    # Reconstruye, , el vector solución a la matriz de 12x6
    matriz_solucion = resultado.x.reshape((12, 6))
    
    for i in range(12):
        for j in range(6):
            valor = round(matriz_solucion[i, j])
            if valor > 0 and costos[i, j] != M:
                tipo = "Regular" if i % 2 == 0 else "Extra"
                mes_prod = (i // 2) + 1
                print(f"Producir en M{mes_prod} ({tipo}) para Demanda M{j+1}: {valor} unidades")
                
    print(f"\nCosto Total Minimizado: ${resultado.fun:,.2f}")
else:
    print("No se encontró solución:", resultado.message)