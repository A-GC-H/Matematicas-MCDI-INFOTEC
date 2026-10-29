# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 18:19:32 2026

@author: chalg
"""

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

# Se define el set de valores a evaluar
Ejemplo1 = [16.2, 16.2, 15.5, 15.4, 16.2, 16.2, 15.9, 15.8, 15.8, 16.1, 16.1, 16.1, 16.7, 17.3, 17.2, 17.4, 17.4, 17.2, 17.2, 17.4, 17.8, 17.4, 17.3, 17.1, 17.4, 17.4, 18.4, 18.3, 17.9, 18.3, 18.5]

# Se obtiene el valor de n (conteo de elementos)
Ene = len(Ejemplo1)

# Se calcula el valor de alfa (media aritmética)
Alpha = ((1/Ene)*(sum(Ejemplo1)))

# Para las aproximaciones, creamos el vector de tiempo t de 1 a n
t_vec = np.arange(1, Ene + 1)

# Se comienzan a obtener los valores para la matriz de forma óptima
yi = sum(Ejemplo1)
ti = sum(t_vec)
ti2 = sum(t_vec**2)
ti3 = sum(t_vec**3)
ti4 = sum(t_vec**4)
ti5 = sum(t_vec**5)
ti6 = sum(t_vec**6)

tiyi = sum(t_vec * Ejemplo1)
ti2yi = sum((t_vec**2) * Ejemplo1)
ti3yi = sum((t_vec**3) * Ejemplo1)

# Matrices para la aproximación lineal
LinearFun = np.array([ [Ene, ti], [ti, ti2] ])
LinearFun_Inv = np.linalg.inv(LinearFun)
Vector_resL = np.array([ [yi], [tiyi] ])
ModeloLin = LinearFun_Inv @ Vector_resL

print("La aproximación lineal queda:")
print(f"p1(t) = {ModeloLin[0][0]:.4f} + {ModeloLin[1][0]:.4f}t\n")

# Matrices para la aproximación cuadrática
CuadraticFun = np.array([ [Ene, ti, ti2], [ti, ti2, ti3], [ti2, ti3, ti4] ])
CuadraticFun_Inv = np.linalg.inv(CuadraticFun)
Vector_resC = np.array([ [yi], [tiyi], [ti2yi] ])
ModeloCuad = CuadraticFun_Inv @ Vector_resC

print("La aproximación cuadrática queda:")
print(f"p2(t) = {ModeloCuad[0][0]:.4f} + {ModeloCuad[1][0]:.4f}t + {ModeloCuad[2][0]:.4f}t^2\n")

# Matrices para la aproximación cúbica
CubicFun = np.array([ [Ene, ti, ti2, ti3], [ti, ti2, ti3, ti4], [ti2, ti3, ti4, ti5], [ti3, ti4, ti5, ti6] ])
CubicFun_Inv = np.linalg.inv(CubicFun)
Vector_resCub = np.array([ [yi], [tiyi], [ti2yi], [ti3yi] ])
ModeloCub = CubicFun_Inv @ Vector_resCub

print("La aproximación cúbica queda:")
print(f"p3(t) = {ModeloCub[0][0]:.4f} + {ModeloCub[1][0]:.4f}t + {ModeloCub[2][0]:.4f}t^2 + {ModeloCub[3][0]:.4f}t^3\n")

# Evaluar las funciones polinomiales sobre el vector de tiempo t para graficar
y_lin = ModeloLin[0] + ModeloLin[1] * t_vec
y_quad = ModeloCuad[0] + ModeloCuad[1] * t_vec + ModeloCuad[2] * t_vec**2
y_cub = ModeloCub[0] + ModeloCub[1] * t_vec + ModeloCub[2] * t_vec**2 + ModeloCub[3] * t_vec**3

# Gráficas
plt.figure(figsize=(10, 6))
t_anios = np.arange(1993, 2024)


# Datos originales expuestos como puntos para dar contexto al ajuste
plt.scatter(t_anios, Ejemplo1, color='red', label='Datos Originales', zorder=5)

# Curvas de aproximación
plt.plot(t_anios, y_lin, label='Linear: p1(t)', color='blue', linestyle='--')
plt.plot(t_anios, y_quad, label='Quadratic: p2(t)', color='green')
plt.plot(t_anios, y_cub, label='Cubic: p3(t)', color='purple')

plt.title('Ajuste de Funciones Lineal, Cuadrática y Cúbica')
plt.xlabel('Años')
plt.ylabel('Temperaturas Anuales en CDMX')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()
