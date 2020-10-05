# -*- coding: utf-8 -*-
"""epc03.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JJshKrd8oWxXw7KBjjYK-wPCjh3eBhSQ
"""

# Importando pandas 
import pandas as pd

# Importando numpy
import numpy as np

# Importando `StandardScaler` de `sklearn.preprocessing`
from sklearn.preprocessing import StandardScaler

# Importando `train_test_split` de `sklearn.model`
from sklearn.model_selection import train_test_split

# Importando constante de tempo
import time

# Importando statistics
import statistics

def generate_empty_matrix(rows, cols):
  matrix = [];
  for i in range(rows):
    line = [];
    for j in range(cols):
      line.append(np.zeros(1)[0]);
    matrix.append(line);
  return np.array(matrix);

def generate_weights(rows, cols):
  matrix = [];
  for i in range(rows):
    line = [];
    for j in range(cols):
      line.append(np.random.rand(1)[0]);
      # line.append(0.1);
    matrix.append(line);
  return np.array(matrix);

def generate_layers(input_size, hidden_size, output_size):
  hidden_layer = generate_weights(hidden_size, input_size + 1);
  output_layer = generate_weights(output_size, hidden_size + 1);

  return hidden_layer, output_layer;

def multiply_matrix(a, b):
  result = generate_empty_matrix(a.shape[0], b.shape[0]);
  
  for i in range(result.shape[0]):
    for j in range(result.shape[1]):
      result[i][j] = a[i] * b[j];
      
  return result;

def add_bias(array):
  rows = array.shape[0];
  cols = array.shape[1];

  matrix = [];
  for i in range(rows):
    line = [];
    for j in range(cols + 1):
      if j == 0:
        line.append((-1) * np.ones(1)[0]);
      else:
        line.append(array[i][j-1]);
    matrix.append(line);
  return np.array(matrix);

def sigmoid(u):
  beta = 0.5;
  return (1 / (1 + np.exp(-beta * u)));

def dsigmoid_du(u):
  beta = 0.5;
  return (beta * sigmoid(u) * (1 - sigmoid(u)));

def train(x_train, y_train, hidden_size, output_size):
  hidden_layer, output_layer = generate_layers(x_train.shape[1] - 1, hidden_size, output_size);

  print('Pesos iniciais da camada escondida:\n', hidden_layer);
  print('\nPesos iniciais da camada de saída:\n', output_layer);

  eta = 0.1;
  error = 1e-06;

  eqm_prev = 99999999;
  eqm_current = 1;
  epochs = 0;

  errors = np.zeros(2000);

  while (abs(eqm_current - eqm_prev) > error):
    eqm_prev = eqm_current;

    ih = generate_empty_matrix(x_train.shape[0], hidden_layer.shape[0]);
    ih = add_bias(ih);
      
    yh = generate_empty_matrix(ih.shape[0], ih.shape[1]);

    io = generate_empty_matrix(yh.shape[0], output_layer.shape[0]);
    yo = generate_empty_matrix(io.shape[0], io.shape[1]);

    delta_output = generate_empty_matrix(yo.shape[0], yo.shape[1]);
    delta_hidden = generate_empty_matrix(ih.shape[0], hidden_layer.shape[0]);

    error_output = generate_empty_matrix(yo.shape[0], yo.shape[1]);
    
    # Fase de forward
    for i in range(x_train.shape[0]): # percorre todas as entradas de teste
      # Cálculo da saída da camada escondida
      for j in range(hidden_layer.shape[0]): # percorre todas as linhas da camada de esconndida
        for k in range(hidden_layer.shape[1]): # percorre todas as colunas da camada de esconndida
          ih[i][j + 1] += x_train[i][k] * hidden_layer[j][k];
      yh = sigmoid(ih);
      yh[:, (0)] = -1;
      
      # Cálculo da saída da rede
      for j in range(output_layer.shape[0]): # percorre todas as linhas da camada de saída
        for k in range(output_layer.shape[1]): # percorre todas as colunas da camada de saída
          io[i][j] += yh[i][k] * output_layer[j][k];
      yo = sigmoid(io);

    # Fase de Backward
    for i in range(x_train.shape[0]): # percorre todas as entradas de teste
      for j in range(output_layer.shape[0]): # percorre todas as linhas da camada de saída
        delta_output[i][j] = (y_train[i][j] - yo[i][j]) * dsigmoid_du(io[i][j]);
      
      output_layer = output_layer + eta * multiply_matrix(delta_output[i], yh[i]);

      for j in range(hidden_layer.shape[0]): # percorre todas as linhas da camada escondida
        for k in range(output_layer.shape[0]): # percorre todas as linhas da camada de saída
          aux2 = multiply_matrix(delta_output[i], output_layer[k]);
          delta_hidden[i][j] = aux2[k][j] * dsigmoid_du(yh[i][j]);

      hidden_layer = hidden_layer + eta * multiply_matrix(delta_hidden[i], x_train[i]);

    epochs = epochs + 1;

    # Cálculo do eqm da época
    error_output = 0;
    for i in range(y_train.shape[0]):
      for j in range(y_train.shape[1]):
        error_output = error_output + np.power((y_train[i][j] - yo[i][j]), 2);
    error_output = (0.5 * error_output) / (y_train.shape[0]);
    
    eqm_current = error_output;
    
    if epochs > 1999:
      break;

    errors[epochs] = eqm_current;

  return epochs, eqm_current, errors, hidden_layer, output_layer;

# Função para tratar saída

def pp(y):
  for i in range(y.shape[0]):
    for j in range(y.shape[1]):
      if y[i][j] >= 0.5:
        y[i][j] = 1;
      else:
        y[i][j] = 0;
  return y;

def calc_accuracy(y_calculated, y_expected):
  size = y_expected.shape[0];
  outs = y_expected.shape[1];
  aux = y_calculated - y_expected;
  correct = 0;

  for i in range(aux.shape[0]):
    soma = 0;
    for j in range(aux.shape[1]):
      if (aux[i][j] == 0):
        soma += 1;
    if soma == outs:
        correct += 1;

  return (correct / size);

# Validação
def val(x_val, y_val, hidden_layer, output_layer):
  ih = generate_empty_matrix(x_val.shape[0], hidden_layer.shape[0]);
  ih = add_bias(ih);
  
  yh = generate_empty_matrix(ih.shape[0], ih.shape[1]);
  
  io = generate_empty_matrix(yh.shape[0], output_layer.shape[0]);
  yo = generate_empty_matrix(io.shape[0], io.shape[1]);
  
  for i in range(x_val.shape[0]):
    # Cálculo da saída da camada escondida
    for j in range(hidden_layer.shape[0]):
      for k in range(hidden_layer.shape[1]):
        ih[i][j] += x_val[i][k] * hidden_layer[j][k];
      yh = sigmoid(ih);
      yh[:, (0)] = -1;
    
    # Cálculo da saída da rede
    for j in range(output_layer.shape[0]):
      for k in range(output_layer.shape[1]):
        io[i][j] += yh[i][k] * output_layer[j][k];
      yo = sigmoid(io);
  
  yo = pp(yo);
  
  accuracy = calc_accuracy(yo, y_val);
  
  return accuracy;

# Teste
def test(x_test, y_test, hidden_layer, output_layer):
  ih = generate_empty_matrix(x_test.shape[0], hidden_layer.shape[0]);
  ih = add_bias(ih);
  
  yh = generate_empty_matrix(ih.shape[0], ih.shape[1]);
  
  io = generate_empty_matrix(yh.shape[0], output_layer.shape[0]);
  yo = generate_empty_matrix(io.shape[0], io.shape[1]);
  
  for i in range(x_test.shape[0]):
    # Cálculo da saída da camada escondida
    for j in range(hidden_layer.shape[0]):
      for k in range(hidden_layer.shape[1]):
        ih[i][j] += x_test[i][k] * hidden_layer[j][k];
      yh = sigmoid(ih);
      yh[:, (0)] = -1;
    
    # Cálculo da saída da rede
    for j in range(output_layer.shape[0]):
      for k in range(output_layer.shape[1]):
        io[i][j] += yh[i][k] * output_layer[j][k];
      yo = sigmoid(io);
  
  yo = pp(yo);
  
  accuracy = calc_accuracy(yo, y_test);
  
  return accuracy;

for exec in range(3):
  exec_eqms = generate_empty_matrix(10, 3);
  exec_epochs = generate_empty_matrix(10, 3);
  exec_time = generate_empty_matrix(10, 3);
  exec_val_accuracy = generate_empty_matrix(10, 3);
  exec_test_accuracy = generate_empty_matrix(10, 3);

  # Importando dados de treinamento e dados de teste para Iris plants data set
  for i in range(10):
    train_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/iris-plants/iris-10-'+ str(i + 1) +'tra.txt', sep=',');
    test_data = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/iris-plants/iris-10-'+ str(i + 1) +'tst.txt', sep=',');

    # Separando entradas e saídas para o treinamento
    x_train = train_data.iloc[:,0:4];
    y_train_text = train_data.iloc[:,4:5];

    # Separando entradas e saídas para o teste
    x_test = test_data.iloc[:,0:4];
    y_test_text = test_data.iloc[:,4:5];

    # Normalização dos dados
    scaler = StandardScaler().fit(x_train);

    # Normalizando dados do treinamento
    x_train = scaler.transform(x_train);

    # Normalizando dados do teste
    x_test = scaler.transform(x_test);

    # Adicionando o bias como uma entrada
    x_train = add_bias(x_train);
    x_test = add_bias(x_test);
    
    possible_outputs = 3;

    # Codificando as saídas do treinamento e do teste
    y_train = generate_empty_matrix(y_train_text.size, possible_outputs);
    out_train = np.array(y_train_text);
    
    for j in range(y_train_text.size):
      if out_train[j] == ' Iris-setosa':
        y_train[j][0] = 1;
      elif out_train[i] == ' Iris-versicolor':
        y_train[j][1] = 1;
      elif out_train[j] == ' Iris-virginica':
        y_train[j][2] = 1;
    
    y_test = generate_empty_matrix(y_test_text.size, possible_outputs);
    out_test = np.array(y_test_text);

    for j in range(y_test_text.size):
      if out_test[j] == ' Iris-setosa':
        y_test[j][0] = 1;
      elif out_test[j] == ' Iris-versicolor':
        y_test[j][1] = 1;
      elif out_test[i] == ' Iris-virginica':
        y_test[j][2] = 1;

    # Separando o conjunto de validação
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.11, random_state=0)

    start = time.time(); # Início do treinamento
    epochs, eqm, errors, hidden_layer, output_layer = train(x_train, y_train, 4, 3);
    end = time.time(); # Fim do treinamento

    print('\nÉpocas: ', epochs, '\n');
    print('EQM: ', eqm, '\n');
    print('Pesos Finais da Camada Escondida:\n', hidden_layer, '\n');
    print('Pesos Finais da Camada de Saída:\n', output_layer, '\n');

    val_accuracy = val(x_val, y_val, hidden_layer, output_layer) * 100;
    print('Precisão de Validação:', val_accuracy, '\n');

    test_accuracy = test(x_test, y_test, hidden_layer, output_layer) * 100;
    print('Precisão de Teste:', test_accuracy, '\n');

    exec_eqms[i][exec] = eqm;
    exec_epochs[i][exec] = epochs;
    exec_time[i][exec] = end - start;
    exec_val_accuracy[i][exec] = val_accuracy;
    exec_test_accuracy[i][exec] = test_accuracy;

mean_eqms = mean(exec_eqms);
dev_eqms = stdev(exec_eqms);

mean_epochs = mean(exec_epochs);
dev_epochs = stdev(exec_epochs);

mean_time = mean(exec_time);
dev_time = stdev(exec_time);

mean_val_accuracy = mean(exec_val_accuracy);
dev_val_accuracy = stdev(exec_val_accuracy);

mean_test_accuracy = mean(exec_test_accuracy);
dev_test_accuracy = stdev(exec_test_accuracy);

print('EQM -> Média: ', mean_eqms, 'Desvio Padrão: ', dev_eqms, '\n');
print('Épocas -> Média: ', mean_epochs, 'Desvio Padrão: ', dev_epochs, '\n');
print('Tempo de Execução -> Média: ', mean_time, 'Desvio Padrão: ', dev_time, '\n');
print('Acurácia de Validação -> Média: ', mean_val_accuracy, 'Desvio Padrão: ', dev_val_accuracy, '\n');
print('Acurácia de Teste -> Média: ', mean_test_accuracy, 'Desvio Padrão: ', dev_test_accuracy);

for exec in range(3):
  exec_eqms2 = generate_empty_matrix(10, 3);
  exec_epochs2 = generate_empty_matrix(10, 3);
  exec_time2 = generate_empty_matrix(10, 3);
  exec_val_accuracy2 = generate_empty_matrix(10, 3);
  exec_test_accuracy2 = generate_empty_matrix(10, 3);

  # Importando dados de treinamento e dados de teste para White Wine Quality data set
  for i in range(10):
    train_data2 = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/white-wine-quality/winequality-white-10-'+ str(i + 1) +'tra.txt', sep=',');
    test_data2 = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc03/white-wine-quality/winequality-white-10-'+ str(i + 1) +'tst.txt', sep=',');
    
    # Separando entradas e saídas para o treinamento
    x_train2 = train_data2.iloc[:,0:11];
    y_train_text2 = train_data2.iloc[:,11:12];

    # Separando entradas e saídas para o teste
    x_test2 = test_data2.iloc[:,0:11];
    y_test_text2 = test_data2.iloc[:,11:12];
    
    # Normalização dos dados
    scaler2 = StandardScaler().fit(x_train2);

    # Normalizando dados do treinamento
    x_train2 = scaler2.transform(x_train2);

    # Normalizando dados do teste
    x_test2 = scaler2.transform(x_test2);

    # Adicionando o bias como uma entrada
    x_train2 = add_bias(x_train2);
    x_test2 = add_bias(x_test2);
    
    possible_outputs = 11;

    # Codificando as saídas do treinamento e do teste
    y_train2 = generate_empty_matrix(y_train_text2.size, 4);
    out_train2 = np.array(y_train_text2);
    
    for j in range(y_train_text2.size):
      if out_train2[j] == 0:
        y_train2[j][0] = 0;
        y_train2[j][1] = 0;
        y_train2[j][2] = 0;
        y_train2[j][3] = 0;
      elif out_train2[j] == 1:
        y_train2[j][0] = 0;
        y_train2[j][1] = 0;
        y_train2[j][2] = 0;
        y_train2[j][3] = 1;
      elif out_train2[j] == 2:
        y_train2[j][0] = 0;
        y_train2[j][1] = 0;
        y_train2[j][2] = 1;
        y_train2[j][3] = 0;
      elif out_train2[j] == 3:
        y_train2[j][0] = 0;
        y_train2[j][1] = 0;
        y_train2[j][2] = 1;
        y_train2[j][3] = 1;
      elif out_train2[j] == 4:
        y_train2[j][0] = 0;
        y_train2[j][1] = 1;
        y_train2[j][2] = 0;
        y_train2[j][3] = 0;
      elif out_train2[j] == 5:
        y_train2[j][0] = 0;
        y_train2[j][1] = 1;
        y_train2[j][2] = 0;
        y_train2[j][3] = 1;
      elif out_train2[j] == 6:
        y_train2[j][0] = 0;
        y_train2[j][1] = 1;
        y_train2[j][2] = 1;
        y_train2[j][3] = 0;
      elif out_train2[j] == 7:
        y_train2[j][0] = 0;
        y_train2[j][1] = 1;
        y_train2[j][2] = 1;
        y_train2[j][3] = 1;
      elif out_train2[j] == 8:
        y_train2[j][0] = 1;
        y_train2[j][1] = 0;
        y_train2[j][2] = 0;
        y_train2[j][3] = 0;
      elif out_train2[j] == 9:
        y_train2[j][0] = 1;
        y_train2[j][1] = 0;
        y_train2[j][2] = 0;
        y_train2[j][3] = 1;
      elif out_train2[j] == 10:
        y_train2[j][0] = 1;
        y_train2[j][1] = 0;
        y_train2[j][2] = 1;
        y_train2[j][3] = 0;
    
    y_test2 = generate_empty_matrix(y_test_text2.size, 4);
    out_test2 = np.array(y_test_text2);
    
    for j in range(y_test_text2.size):
      if out_test2[j] == 0:
        y_test2[j][0] = 0;
        y_test2[j][1] = 0;
        y_test2[j][2] = 0;
        y_test2[j][3] = 0;
      elif out_test2[j] == 1:
        y_test2[j][0] = 0;
        y_test2[j][1] = 0;
        y_test2[j][2] = 0;
        y_test2[j][3] = 1;
      elif out_test2[j] == 2:
        y_test2[j][0] = 0;
        y_test2[j][1] = 0;
        y_test2[j][2] = 1;
        y_test2[j][3] = 0;
      elif out_test2[j] == 3:
        y_test2[j][0] = 0;
        y_test2[j][1] = 0;
        y_test2[j][2] = 1;
        y_test2[j][3] = 1;
      elif out_test2[j] == 4:
        y_test2[j][0] = 0;
        y_test2[j][1] = 1;
        y_test2[j][2] = 0;
        y_test2[j][3] = 0;
      elif out_test2[j] == 5:
        y_test2[j][0] = 0;
        y_test2[j][1] = 1;
        y_test2[j][2] = 0;
        y_test2[j][3] = 1;
      elif out_test2[j] == 6:
        y_test2[j][0] = 0;
        y_test2[j][1] = 1;
        y_test2[j][2] = 1;
        y_test2[j][3] = 0;
      elif out_test2[j] == 7:
        y_test2[j][0] = 0;
        y_test2[j][1] = 1;
        y_test2[j][2] = 1;
        y_test2[j][3] = 1;
      elif out_test2[j] == 8:
        y_test2[j][0] = 1;
        y_test2[j][1] = 0;
        y_test2[j][2] = 0;
        y_test2[j][3] = 0;
      elif out_test2[j] == 9:
        y_test2[j][0] = 1;
        y_test2[j][1] = 0;
        y_test2[j][2] = 0;
        y_test2[j][3] = 1;
      elif out_test2[j] == 10:
        y_test2[j][0] = 1;
        y_test2[j][1] = 0;
        y_test2[j][2] = 1;
        y_test2[j][3] = 0;

    # Separando o conjunto de validação
    x_train2, x_val2, y_train2, y_val2 = train_test_split(x_train2, y_train2, test_size=0.11, random_state=0)

    start = time.time(); # Início do treinamento
    epochs, eqm, errors, hidden_layer, output_layer = train(x_train2, y_train2, 11, 4);
    end = time.time(); # Fim do treinamento

    print('\nÉpocas: ', epochs, '\n');
    print('EQM: ', eqm, '\n');
    print('Pesos Finais da Camada Escondida:\n', hidden_layer, '\n');
    print('Pesos Finais da Camada de Saída:\n', output_layer, '\n');

    val_accuracy = val(x_val2, y_val2, hidden_layer, output_layer) * 100;
    print('Precisão de Validação:', val_accuracy, '\n');

    test_accuracy = test(x_test2, y_test2, hidden_layer, output_layer) * 100;
    print('Precisão de Teste:', test_accuracy, '\n');
    
    exec_eqms2[i][exec] = eqm;
    exec_epochs2[i][exec] = epochs;
    exec_time2[i][exec] = end - start;
    exec_val_accuracy2[i][exec] = val_accuracy;
    exec_test_accuracy2[i][exec] = test_accuracy;

mean_eqms2 = mean(exec_eqms2);
dev_eqms2 = stdev(exec_eqms2);

mean_epochs2 = mean(exec_epochs2);
dev_epochs2 = stdev(exec_epochs2);

mean_time2 = mean(exec_time2);
dev_time2 = stdev(exec_time2);

mean_val_accuracy2 = mean(exec_val_accuracy2);
dev_val_accuracy2 = stdev(exec_val_accuracy2);

mean_test_accuracy2 = mean(exec_test_accuracy2);
dev_test_accuracy2 = stdev(exec_test_accuracy2);

print('EQM -> Média: ', mean_eqms2, 'Desvio Padrão: ', dev_eqms2, '\n');
print('Épocas -> Média: ', mean_epochs2, 'Desvio Padrão: ', dev_epochs2, '\n');
print('Tempo de Execução -> Média: ', mean_time2, 'Desvio Padrão: ', dev_time2, '\n');
print('Acurácia de Validação -> Média: ', mean_val_accuracy2, 'Desvio Padrão: ', dev_val_accuracy2, '\n');
print('Acurácia de Teste -> Média: ', mean_test_accuracy2, 'Desvio Padrão: ', dev_test_accuracy2);

import matplotlib
import matplotlib.pyplot as plt

fig, ax = plt.subplots();
plt.xlim(0, epochs + 1);

ax.plot(errors[1:epochs + 1]);
ax.set(xlabel='Nº de Épocas',
       ylabel='EQM',
       title='EQM ao longo das épocas de treinamento');
ax.grid();