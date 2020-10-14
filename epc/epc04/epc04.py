# -*- coding: utf-8 -*-
"""epc04.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q0ayuWEbsJtEVLVebmPnDh-H14r3oDqL
"""

# Importando pandas 
import pandas as pd

# Importando numpy
import numpy as np

# Importando `MinMaxScaler` de `sklearn.preprocessing`
from sklearn.preprocessing import MinMaxScaler

# Importando `pyplot` de `matplotlib`
from matplotlib import pyplot as plt

# Importando constante de tempo
import time

# Importando `KMeans`de `sklearn.cluster`
from sklearn.cluster import KMeans

def generate_empty_matrix(rows, cols):
  matrix = [];
  for i in range(rows):
    line = [];
    for j in range(cols):
      line.append(np.zeros(1)[0]);
    matrix.append(line);
  return matrix;

def generate_weights(rows, cols, inputs):
  matrix = [];
  for i in range(rows):
    neuroniuns = [];
    for j in range(cols):
      weights = [];
      for k in range(inputs):
        weights.append(np.random.rand(1)[0]);
      neuroniuns.append(weights);
    matrix.append(neuroniuns);
  return matrix;

def euclidian(input, weights):
  dists = np.array(generate_empty_matrix(weights.shape[0], weights.shape[1]))

  for j in range(weights.shape[0]):
    for k in range(weights.shape[1]):
      for l in range(weights.shape[2]):
        dists[j][k] += np.power((input[l] - weights[j][k][l]), 2);
  dists = np.sqrt(dists);
  return dists

"""Geração da Matriz de Vizinhança"""

def generate_neighborhood(rows, cols):
  neighborhood = [];
  for i in range(rows):
    for j in range(cols):
      neighbors = [];
      if (i > 0) and (i < rows - 1) and (j > 0) and (j < cols - 1):
        neighbors.append({"x": i, "y": j + 1});
        neighbors.append({"x": i + 1, "y": j});
        neighbors.append({"x": i, "y": j - 1});
        neighbors.append({"x": i - 1, "y": j});
      else:
        if (i == 0):
          if (j == 0):
            neighbors.append({"x": i, "y": j + 1});
            neighbors.append({"x": i + 1, "y": j});
          elif (j == (cols - 1)):
            neighbors.append({"x": i, "y": j - 1});
            neighbors.append({"x": i + 1, "y": j});
          elif (j > 0) and (j < cols - 1):
            neighbors.append({"x": i, "y": j - 1});
            neighbors.append({"x": i, "y": j + 1});
            neighbors.append({"x": i + 1, "y": j});
        elif (i == rows - 1):
          if (j == 0):
            neighbors.append({"x": i - 1, "y": j});
            neighbors.append({"x": i, "y": j + 1});
          elif (j == (cols - 1)):
            neighbors.append({"x": i - 1, "y": j});
            neighbors.append({"x": i, "y": j - 1});
          elif (j > 0) and (j < cols - 1):
            neighbors.append({"x": i, "y": j - 1});
            neighbors.append({"x": i, "y": j + 1});
            neighbors.append({"x": i - 1, "y": j});
        if (j == 0):
          if (i > 0) and (i < cols - 1):
            neighbors.append({"x": i - 1, "y": j});
            neighbors.append({"x": i, "y": j + 1});
            neighbors.append({"x": i + 1, "y": j});
        elif (j == cols -1):
          if (i > 0) and (i < cols - 1):
            neighbors.append({"x": i - 1, "y": j});
            neighbors.append({"x": i, "y": j - 1});
            neighbors.append({"x": i + 1, "y": j});
      neighborhood.append(neighbors);
  return neighborhood;

"""Processamento dos dados"""

i = 0;

train_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/iris-plants/iris-10-'+ str(i + 1) +'tra.txt', sep=',');
test_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/iris-plants/iris-10-'+ str(i + 1) +'tst.txt', sep=',');

# Separando entradas e saídas para o treinamento
x_train = train_data.iloc[:,0:4];
y_train_text = train_data.iloc[:,4:5];

# Separando entradas e saídas para o teste
x_test = test_data.iloc[:,0:4];
y_test_text = test_data.iloc[:,4:5];

# Normalização dos dados
scaler = MinMaxScaler().fit(x_train);

# Normalizando dados do treinamento
x_train = scaler.transform(x_train);

# Normalizando dados do teste
x_test = scaler.transform(x_test);

"""Algoritmo SOM"""

def som(map_rows, map_cols, training_data, learning_rate, iterations):
  # Definindo mapa topológico
  map = np.array(generate_empty_matrix(map_rows, map_cols));

  # Montar os conjuntos de vizinhança
  neighborhood = np.array(generate_neighborhood(map.shape[0], map.shape[1])).reshape(map.shape[0], map.shape[1]);

  # Inicializar w aleatoriamente;
  weights = np.array(generate_weights(map.shape[0], map.shape[1], training_data.shape[1]));

  # Inicializar a taxa de aprendizado;
  eta = learning_rate;
  
  winners_current = []
  winners_prev = [[999, 999, 999]]

  epochs = 0;

  while True and (epochs < iterations):
    winners_prev = winners_current.copy();

    for i in range(training_data.shape[0]):
      # Cálculo da distância euclidiana
      # for j in range(map.shape[0]):
      #   for k in range(map.shape[1]):
      #     for l in range(weights.shape[2]):
      #       map[j][k] += np.power((training_data[i][l] - weights[j][k][l]), 2);
      # map = np.sqrt(map);
      map = euclidian(training_data[i], weights);
      
      # Encontrando neurônio vencedor
      min_x = 0;
      min_y = 0;
      min = 999999;
      for j in range(map.shape[0]):
        for k in range(map.shape[1]):
          if(min > map[j][k]):
            min_x = j;
            min_y = k;
            min = map[j][k];
      
      winner = []
      winner.append(min_x)
      winner.append(min_y)
      winners_current.append(winner)

      # Atualização dos pesos do neurônio vencedor
      weights[min_x][min_y] = weights[min_x][min_y] + eta * (training_data[i] - weights[min_x][min_y])
      
      # Atualização dos pesos dos vizinhos do neurônio vencedor
      for neighbor in range(len(neighborhood[min_x][min_y])):
        weights[neighborhood[min_x][min_y][neighbor]['x']][neighborhood[min_x][min_y][neighbor]['y']] = weights[neighborhood[min_x][min_y][neighbor]['x']][neighborhood[min_x][min_y][neighbor]['y']] + 0.5 * eta * (training_data[i] - weights[neighborhood[min_x][min_y][neighbor]['x']][neighborhood[min_x][min_y][neighbor]['y']])

    min_x_current = min_x
    min_y_current = min_y
    epochs = epochs + 1
    
    if (winners_current == winners_prev):
      break 

  return map, weights, min_x_current, min_y_current, epochs

"""Aplicação do Kmeans"""

def class_neuroniun(weights, clusters):
  a = []
  for j in range(weights.shape[0]):
    for k in range(weights.shape[1]):
      a.append(weights[j][k])

  kmeans = KMeans(n_clusters = clusters, init = 'random').fit(a)
  
  weights_classes = np.array(kmeans.labels_)
  weights_classes = weights_classes.reshape(weights.shape[0], weights.shape[1])
  
  centroids = np.array(kmeans.cluster_centers_)

  return weights_classes, centroids

"""Classificação das entradas"""

def predict_classes(x, weights, weights_classes, centroids):
  # map = np.array(generate_empty_matrix(weights.shape[0], weights.shape[1]));

  class_0 = []
  class_1 = []
  class_2 = []

  predict = []
  # predict_w = []

  for i in range(x.shape[0]):
    d0 = np.power((x[i] - centroids[0]), 2)
    d1 = np.power((x[i] - centroids[1]), 2)
    d2 = np.power((x[i] - centroids[2]), 2)

    d0 = np.sqrt(sum(d0))
    d1 = np.sqrt(sum(d1))
    d2 = np.sqrt(sum(d2))

    if d0 < d1 and d0 < d2:
      predict.append(0)
      class_0.append(i)
    elif d1 < d0 and d1 < d2:
      predict.append(1)
      class_1.append(i)
    elif d2 < d0 and d2 < d1:
      predict.append(2)
      class_2.append(i)

    # map = euclidian(x[i], weights);
    
    # Encontrando neurônio vencedor
    # min_x = 0;
    # min_y = 0;
    # min = 999999;
    # for j in range(map.shape[0]):
    #   for k in range(map.shape[1]):
    #     if(min > map[j][k]):
    #       min_x = j;
    #       min_y = k;
    #       min = map[j][k];

    # predict_w.append(weights_classes[min_x][min_y])
      
    # if weights_classes[min_x][min_y] == 0:
    #   class_0.append((i, weights_classes[min_x][min_y]))
    # elif weights_classes[min_x][min_y] == 1:
    #   class_1.append((i, weights_classes[min_x][min_y]))
    # elif weights_classes[min_x][min_y] == 2:
    #   class_2.append((i, weights_classes[min_x][min_y]))
  
  # print(predict_w)

  return predict, class_0, class_1, class_2

"""Topologia 1"""

start = time.time()
map1, weights1, x_min1, y_min1, epochs1 = som(5, 5, x_train, 0.001, 20000)
end = time.time()

print(end - start, epochs1)

plt.imshow(map1, interpolation='nearest')
plt.show()

plt.imshow(weights1, interpolation='nearest')
plt.show()

weights1_classes, centroids1 = class_neuroniun(weights1, 3)
print(weights1_classes, '\n')
print(centroids1)

predict_test, class_0, class_1, class_2 = predict_classes(x_test, weights1, weights1_classes, centroids1)
print(predict_test, '\n')
print(class_0, '\n')
print(class_1, '\n')
print(class_2, '\n')

plt.scatter(weights1.T[0], weights1.T[1], color='g')
plt.scatter(x_test.T[0], x_test.T[1], color='r')
plt.scatter(centroids1.T[0], centroids1.T[1], edgecolors='r', color='b')
plt.show()

"""Topologia 2"""

start = time.time()
map2, weights2, x_min2, y_min2, epochs2 = som(15, 15, x_train, 0.001, 15000)
end = time.time()
print(end - start, epochs2)

plt.imshow(map2, interpolation='nearest')
plt.show()

plt.imshow(weights2, interpolation='nearest')
plt.show()

weights2_classes, centroids2 = class_neuroniun(weights2, 3)
print(weights2_classes, '\n')
print(centroids2)

plt.scatter(weights2.T[0], weights2.T[1], color='g')
plt.scatter(x_test.T[0], x_test.T[1], color='r')
plt.scatter(centroids2.T[0], centroids2.T[1], edgecolors='r', color='b')
plt.show()

"""Topologia 3"""

start = time.time()
map3, weights3, x_min3, y_min3, epochs3 = som(30, 30, x_train, 0.001, 150000)
end = time.time()
print(end - start, epochs3)

plt.imshow(map3, interpolation='nearest')
plt.show()

plt.imshow(weights3, interpolation='nearest')
plt.show()

weights3_classes, centroids3 = class_neuroniun(weights3, 3)
print(weights3_classes, '\n')
print(centroids3)

predict, class_0, class_1, class_2 = predict_classes(x_test, weights3, weights3_classes, centroids3)
print(predict, '\n')
print(class_0, '\n')
print(class_1, '\n')
print(class_2, '\n')

plt.scatter(weights3.T[0], weights3.T[1], color='g')
plt.scatter(x_test.T[0], x_test.T[1], color='r')
plt.scatter(centroids3.T[0], centroids3.T[1], edgecolors='r', color='b')
plt.show()