
pca_result <- prcomp(USArrests, scale = TRUE)
names(pca_result)

# Media
pca_result$center

# Desviaciones Estándar
pca_result$scale

# Matriz de Rotación
pca_result$rotation

# Modificación de Sentido de Rotación
pca_result$rotation <- -pca_result$rotation
pca_result$rotation

# Puntuaciones de los Componentes Principales
pca_result$x <- - pca_result$x
head(pca_result$x)

# Gráfica
biplot(pca_result, scale = 0, main = "PCA Biplot - USArrests (PC1 vs PC2)")

# Desviación Estándard de cada Componente Principal
pca_result$sdev

# Varianza por cada Componente Principal
(VE <- pca_result$sdev^2)

# Proporción de Varianza por cada Componente Principal
PVE <- VE / sum(VE)
round(PVE, 2)
