# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:37:13 2026

@author: chalg
"""

import networkx as nx
import matplotlib.pyplot as plt

# Inicializa el grafo dirigido
G = nx.DiGraph()

# Definición de nodos de Oferta (12 periodos de producción)
nodos_oferta = [
    "P1 (Reg M1)", "P2 (Extra M1)",
    "P3 (Reg M2)", "P4 (Extra M2)",
    "P5 (Reg M3)", "P6 (Extra M3)",
    "P7 (Reg M4)", "P8 (Extra M4)",
    "P9 (Reg M5)", "P10 (Extra M5)",
    "P11 (Reg M6)", "P12 (Extra M6)"
]

# Definición de nodos de Demanda (6 meses)
nodos_demanda = [
    "D1 (M1)", "D2 (M2)", "D3 (M3)",
    "D4 (M4)", "D5 (M5)", "D6 (M6)"
]

# Adición de nodos al grafo
G.add_nodes_from(nodos_oferta, bipartite=0)
G.add_nodes_from(nodos_demanda, bipartite=1)

# Creación de los arcos (conexiones)
# Solo se permite enviar de un periodo a un mes de demanda igual o futuro
for mes_prod in range(1, 7):
    nodo_reg = nodos_oferta[(mes_prod - 1) * 2]
    nodo_ext = nodos_oferta[(mes_prod - 1) * 2 + 1]
    
    for mes_dem in range(mes_prod, 7): # mes_dem >= mes_prod (no hay backorders)
        nodo_dest = nodos_demanda[mes_dem - 1]
        G.add_edge(nodo_reg, nodo_dest)
        G.add_edge(nodo_ext, nodo_dest)

# Definición de posiciones para el gráfico (Layout Bipartito personalizado)
posiciones = {}
# Nodos de oferta a la izquierda (x=0)
for i, nodo in enumerate(nodos_oferta):
    posiciones[nodo] = (0, 12 - i) 

# Nodos de demanda a la derecha (x=1), más espaciados para alinear visualmente
for i, nodo in enumerate(nodos_demanda):
    posiciones[nodo] = (1, 11.5 - (i * 2.2)) 

# Configuración de colores
colores_nodos = ['#5A8CD7' if 'P' in nodo else '#76B947' for nodo in G.nodes()]

# Generación del grafo
plt.figure(figsize=(12, 8))
nx.draw(G, pos=posiciones, with_labels=True, 
        node_color=colores_nodos, 
        node_size=2500, 
        font_size=10, 
        font_color='black',
        arrows=True, 
        arrowsize=15, 
        edge_color='#4d5663', 
        width=1.2, 
        alpha=0.8)

# Ajustes finales del plot
plt.title("Grafo de Red de Producción y Demanda", fontsize=18, pad=20)
plt.xlim(-0.5, 1.5) # Dar margen horizontal
plt.axis('off')
plt.tight_layout()

# Generación de la imagen
# plt.savefig("grafo_produccion.png", dpi=300, bbox_inches='tight')
plt.show()