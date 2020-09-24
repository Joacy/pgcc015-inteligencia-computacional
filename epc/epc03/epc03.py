# -*- coding: utf-8 -*-
"""epc03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NQQprUpM9AEubecDos7q3ryn6gGo6q99
"""

# Importando pandas 
import pandas as pd

# Importando numpy
import numpy as np

def generate_empty_matrix(rows, cols):
  matrix = [];
  for i in range(rows):
    line = [];
    for j in range(cols):
      line.append(np.zeros(1)[0]);
    matrix.append(line);
  return np.array(matrix);

# Importando dados de treinamento e dados de teste para Iris plants data set
for i in range(1):
  train_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/iris-plants/iris-10-'+ str(i + 1) +'tra.txt', sep=',');
  test_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/iris-plants/iris-10-'+ str(i + 1) +'tst.txt', sep=',');

  # Separando entradas e saídas para o treinamento
  x_train = train_data.iloc[:,0:4];
  y_train_text = train_data.iloc[:,4:5];
  
  # Separando entradas e saídas para o teste
  x_test = test_data.iloc[:,0:4];
  y_test_text = test_data.iloc[:,4:5];

  # Adicionando o bias como uma entrada
  bias_train = (-1 * np.ones(y_train_text.size)).tolist();
  x_train['bias'] = bias_train;

  bias_test = (-1 * np.ones(y_test_text.size)).tolist();
  x_test['bias'] = bias_test;

  possible_outputs = 3;

  # Codificando as saídas do treinamento e do teste
  y_train = generate_empty_matrix(y_train_text.size, possible_outputs);
  out_train = np.array(y_train_text);
  
  for i in range(y_train_text.size):
    if out_train[i] == ' Iris-setosa':
      y_train[i][0] = 1;
    elif out_train[i] == ' Iris-versicolor':
      y_train[i][1] = 1;
    elif out_train[i] == ' Iris-virginica':
      y_train[i][2] = 1;
  
  y_test = generate_empty_matrix(y_test_text.size, possible_outputs);
  out_test = np.array(y_test_text);

  for i in range(y_test_text.size):
    if out_test[i] == ' Iris-setosa':
      y_test[i][0] = 1;
    elif out_test[i] == ' Iris-versicolor':
      y_test[i][1] = 1;
    elif out_test[i] == ' Iris-virginica':
      y_test[i][2] = 1;

# # Importando dados de treinamento e dados de teste para Glass Identification data set
# for i in range(10):
#   train_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/glass-identification/glass-10-'+ str(i + 1) +'tra.txt', sep=',');
#   test_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/glass-identification/glass-10-'+ str(i + 1) +'tst.txt', sep=',');

#   # Separando entradas e saídas para o treinamento
#   x_train = train_data.iloc[:,0:9];
#   y_train = train_data.iloc[:,9:10];

#   # Separando entradas e saídas para o teste
#   x_test = test_data.iloc[:,0:9];
#   y_test = test_data.iloc[:,9:10];

#   # Adicionando o bias como uma entrada
#   bias_train = (-1 * np.ones(y_train.size)).tolist();
#   x_train['bias'] = bias_train;

#   bias_test = (-1 * np.ones(y_test.size)).tolist();
#   x_test['bias'] = bias_test;

#   possible_outputs = 7;

# # Importando dados de treinamento e dados de teste para White Wine Quality data set
# for i in range(10):
#   train_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/white-wine-quality/winequality-white-10-'+ str(i + 1) +'tra.txt', sep=',');
#   test_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/white-wine-quality/winequality-white-10-'+ str(i + 1) +'tst.txt', sep=',');
  
  # # Separando entradas e saídas para o treinamento
  # x_train = train_data.iloc[:,0:11];
  # y_train = train_data.iloc[:,11:12];

  # # Separando entradas e saídas para o teste
  # x_test = test_data.iloc[:,0:11];
  # y_test = test_data.iloc[:,11:12];

  # # Adicionando o bias como uma entrada
  # bias_train = (-1 * np.ones(y_train.size)).tolist();
  # x_train['bias'] = bias_train;

  # bias_test = (-1 * np.ones(y_test.size)).tolist();
  # x_test['bias'] = bias_test;

  # possible_outputs = 11;

def sigmoid(u):
  beta = 0.5;
  return (1 / (1 + np.exp(-beta * u)));

def dsigmoid_du(u):
  beta = 0.5;
  return (beta * sigmoid(u) * (1 - sigmoid(u)));

def generate_matrix(rows, cols):
  matrix = [];
  for i in range(rows):
    line = [];
    for j in range(cols):
      line.append(np.random.rand(1)[0]);
    matrix.append(line);
  return np.array(matrix);

def generate_layers(input_size, hidden_size, output_size):
  hidden_layer = generate_matrix(hidden_size, input_size + 1);
  output_layer = generate_matrix(output_size, hidden_size + 1);

  return hidden_layer, output_layer;

hidden_layer, output_layer = generate_layers(x_train.columns.size - 1, x_train.columns.size - 1, possible_outputs);

x = np.array(x_train);

eta = 0.1;
error = 1e-06;

eqm_prev = 99999999;
eqm_current = 1;
epochs = 0;

errors = np.zeros(4000);

while (abs(eqm_current - eqm_prev) > error):
  eqm_prev = eqm_current;

  u = generate_empty_matrix(int(x_train.size / x_train.columns.size), hidden_layer.shape[1]);
  u[:, (hidden_layer.shape[1] - 1)] = -1;

  gu = generate_empty_matrix(int(x_train.size / x_train.columns.size), hidden_layer.shape[1]);

  y = generate_empty_matrix(u.shape[0], output_layer.shape[0]);
  gy = generate_empty_matrix(u.shape[0], output_layer.shape[0]);

  delta_output = generate_empty_matrix(y.shape[0], y.shape[1]);
  error_output = generate_empty_matrix(y.shape[0], y.shape[1]);
  delta_hidden = generate_empty_matrix(u.shape[0], hidden_layer.shape[0]);

  # Fase de forward
  for i in range(int(x_train.size / x_train.columns.size)):
    # Cálculo da saída da camada escondida
    for j in range(hidden_layer.shape[0]):
      u[i][j] = x[i] @ hidden_layer[j];
    gu = sigmoid(u);
    gu[:, (hidden_layer.shape[1] - 1)] = -1;
    
    # Cálculo da saída da rede
    for j in range(output_layer.shape[0]):
      y[i][j] = gu[i] @ output_layer[j];
    gy = sigmoid(y)

  # Fase de Backward
  for i in range(int(x_train.size / x_train.columns.size)):
    delta_output[i] = (y_train[i] @ dsigmoid_du(gy[i])) - (gy[i] @ dsigmoid_du(gy[i]));
    
    for j in range(hidden_layer.shape[0]):
      for k in range(output_layer.shape[0]):
        delta_hidden[i][j] = dsigmoid_du(gu[i][j]) * delta_output[i][k] * output_layer[k,j];
  
  epochs = epochs + 1;

  # Cálculo do eqm da época
  error_output = 0;
  for i in range(y_train.shape[0]):
    for j in range(y_train.shape[1]):
      error_output += np.power((y_train[i][j] - gy[i][j]), 2);
  error_output = error_output / y_train.size;
  
  eqm_current = error_output;
  
  errors[epochs] = eqm_current;

print('Épocas de treinamento:', epochs);

delta_output

delta_hidden

hidden_layer

output_layer