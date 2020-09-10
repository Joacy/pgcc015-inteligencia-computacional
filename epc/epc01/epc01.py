# -*- coding: utf-8 -*-
"""epc01

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pYOPOYzlAXPwPcF6AN6u_9VMsCnpBA7G
"""

# Importando pandas 
import pandas as pd

# Importando numpy
import numpy as np

# Importando dados de treinamento e dados de teste
dataset = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc01/dados.txt', header=None, sep=' ');
x_test = pd.read_csv('https://raw.githubusercontent.com/Joacy/pgcc015-inteligencia-computacional/master/epc/epc01/teste.txt', header=None, sep=' ');

# Separando entradas e saídas para o treinamento
x_train = dataset.iloc[:,0:4];

y_train = dataset.iloc[:,4:5];

# Função sinal

def sinal(u):
  return 1 if u >= 0 else -1

# Inicialização da taxa de aprendizado
eta = 0.01;

cols = x_train.columns.size;
rows = int(x_train.size / cols);

# Inicialização do vetor de pesos
weights = np.random.rand(cols);

print('Pesos iniciais:', weights);

# Treinamento
x = np.array(x_train);

d = np.array(y_train);

y = np.zeros((rows));

epochs = 0;

error = True;
while (error):
  error = False;
  for i in range(rows):
    u = np.zeros((rows));
    for j in range(cols):
      u[i] += x[i][j] * weights[j];
    y[i] = sinal(u[i]);
    
    if (d[i] != y[i]):
      for k in range(cols):
        weights[k] = weights[k] + eta*(d[i] - y[i])*x[i][k];
        error = True;
  epochs = epochs + 1;

print('Épocas de treinamento:', epochs, '\nPesos finais:', weights);

# Teste
rows = int(x_test.size / cols);
x_test = np.array(x_test);
y_test = np.zeros(rows);

for i in range(rows):
  for j in range(cols):
    y_test[i] += x_test[i][j] * weights[j];
  if (sinal(y_test[i]) == 1):
    print('O óleo pertence a classe C2');
  else:
    print('O óleo pertence a classe C1');