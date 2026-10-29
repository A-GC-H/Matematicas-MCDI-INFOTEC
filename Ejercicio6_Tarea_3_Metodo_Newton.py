# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 10:56:21 2026

@author: chalg
"""

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Función objetivo simplificada
def cost_function(x):
    q, t = x[0], x[1]
    if q <= 0 or t <= 0:
        return np.inf
        
    term_fijo = 12.5 + 0.50 + 0.90
    t1 = (2.09e4 * (t**-0.3017)) / 360
    t2 = (1.064e6 * (t**0.4925)) / (52.47 * q * 360)
    
    num3 = 4.242e4 * 0.20 * (t**0.7952) + 1.813 * 0.10 * 7000 * ((2*t + 1.2*q)**0.861)
    t3 = num3 / (52.47 * q * 360)
    
    t4 = (4.25e3 * 0.20 * (2*t + 1.2*q)) / (52.47 * q * 360)
    t5 = (5.042e3 * (q**-0.1899)) / 360
    t6 = (0.1049 * (q**0.671)) / 360
    
    return term_fijo + t1 + t2 + t3 + t4 + t5 + t6

# Jacobiano numérico
def jac_approx(x):
    eps = 1e-5
    grad = np.zeros_like(x)
    for idx in range(len(x)):
        x_plus, x_minus = np.copy(x), np.copy(x)
        x_plus[idx] += eps
        x_minus[idx] -= eps
        grad[idx] = (cost_function(x_plus) - cost_function(x_minus)) / (2 * eps)
    return grad

# Punto de partida
x0 = np.array([5000.0, 20000.0])

# Optimizaciones
res_bfgs = minimize(cost_function, x0, method='BFGS')
res_newton = minimize(cost_function, x0, method='Newton-CG', jac=jac_approx)

# Resultados
print(f"\nÓptimo Método quasi-Newton: q = {res_bfgs.x[0]:.2f}; t = {res_bfgs.x[1]:.2f}; Costo = ${res_bfgs.fun:.4f}")
print(f"Óptimo Método de Newton: q = {res_newton.x[0]:.2f}; t = {res_newton.x[1]:.2f}; Costo = ${res_newton.fun:.4f}\n")

# Gráfica
# Definir el rango de visualización alrededor de las soluciones encontradas
# Ajustamos rangos lógicos para q y t
q_min, q_max = max(100, res_bfgs.x[0] - 4000), res_bfgs.x[0] + 6000
t_min, t_max = max(100, res_bfgs.x[1] - 15000), res_bfgs.x[1] + 25000

q_space = np.linspace(q_min, q_max, 100)
t_space = np.linspace(t_min, t_max, 100)
Q, T = np.meshgrid(q_space, t_space)

# Calcular el costo para cada punto de la cuadrícula
Z = np.zeros_like(Q)
for i in range(Q.shape[0]):
    for j in range(Q.shape[1]):
        val = cost_function([Q[i, j], T[i, j]])
        # Limitar valores excesivamente altos para mantener una buena escala visual
        Z[i, j] = val if val < 200 else 200 

# Crear la figura 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficar la superficie
surf = ax.plot_surface(Q, T, Z, cmap='viridis', edgecolor='none', alpha=0.8)

# Graficar los puntos de convergencia encontrados por los métodos
if res_bfgs.success:
    ax.scatter(res_bfgs.x[0], res_bfgs.x[1], res_bfgs.fun, color='red', s=100, marker='X',
               label=f'Óptimo quasi-Newton (${res_bfgs.fun:.2f})', depthshade=False, zorder=10)

if res_newton.success:
    ax.scatter(res_newton.x[0], res_newton.x[1], res_newton.fun, color='green', s=50, marker='o', 
               label=f'Óptimo Método de Newton (${res_newton.fun:.2f})', depthshade=False, zorder=11)

# Configuración de etiquetas y títulos
ax.set_title('Superficie de Costo Económico 3D de la Refinería', fontsize=14, pad=20)
ax.set_xlabel('Capacidad Refinería (q en bbl/día)', fontsize=11, labelpad=10)
ax.set_ylabel('Tamaño Petrolero (t en kL)', fontsize=11, labelpad=10)
ax.set_zlabel('Costo ($ por kL)', fontsize=11, labelpad=10)
ax.legend(loc='upper right')

# Añadir barra de colores para interpretar mejor los niveles de costo
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Costo por kL')

# Ajustar ángulo de visión inicial para apreciar mejor la curvatura del "valle"
ax.view_init(elev=30, azim=-60)

plt.tight_layout()
plt.show()