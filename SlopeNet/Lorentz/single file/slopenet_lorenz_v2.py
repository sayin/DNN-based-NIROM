#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 15:19:23 2019

@author: user1
"""
legs = 1 
slopenet = "EULER" 
problem = "ODE"

import os
if os.path.isfile('best_model.hd5'):
    os.remove('best_model.hd5')

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(1)
from scipy.integrate import odeint
import matplotlib.pyplot as plt

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Input
import keras.backend as K
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from keras import optimizers


def coeff_determination(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred ))
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) )
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

#--------------------------------------------------------------------------------------------------------------#
# Lorenz system
rho = 28.0
rho1 = 1.00*28.0
sigma = 10.0
beta = 8.0 / 3.0
#beta1 = 1.05 * 8.0 / 3.0
def f(state, t):
  x, y, z = state  # unpack the state vector
  return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # derivatives

def f1(state, t):
  x, y, z = state  # unpack the state vector
  return sigma * (y - x), x * (rho1 - z) - y, x * y - beta * z  # derivatives

#state0 = [1.508870,-1.531271, 25.46091]
state0 = [-10.0, 0.0, 30.0]
#state0 = 30*(np.random.rand(3)-0.5)
t_init  = 0.0  # Initial time
t_final = 20.0 # Final time
dt = 0.01
t = np.arange(t_init, t_final, dt)
nsamples = int((t_final-t_init)/dt)
states = odeint(f, state0, t)
states1 = odeint(f1, state0, t)


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(states[:,0], states[:,1], states[:,2])
plt.show()

#%%
plt.figure()
plt.plot(t, states[:,0])
plt.plot(t, states1[:,0])

plt.figure()
plt.plot(t, states[:,1])
plt.plot(t, states1[:,1])


#%%
#--------------------------------------------------------------------------------------------------------------#
training_set1 = states
training_set2 = states1


def create_training_data(training_set1, training_set2, dt, t, nsamples):
    """ 
    This function creates the input and output of the neural network. The function takes the
    training data as an input and creates the input for DNN.
    The input for the LSTM is 3-dimensional matrix.
    For lookback = 2;  [y(n)] ------> [(y(n+1)-y(n))/dt]
    """
    m,n = training_set1.shape
    ytrain = [(training_set1[i+1]-training_set1[i])/dt for i in range(m-1)]
    ytrain = np.array(ytrain)
    t = t.reshape(nsamples,1)
    xt1 = training_set1[0:m-1]
    xt2 = training_set2[1:m]
    xtrain = np.hstack((xt1, xt2))
    return xtrain, ytrain


xtrain, ytrain = create_training_data(training_set1, training_set2, dt, t, nsamples)
mx,nx = xtrain.shape
my,ny = ytrain.shape
#%%
indices = np.random.randint(0,xtrain.shape[0],5000)
xtrainr = xtrain[indices]
ytrainr = ytrain[indices]

# scale the iput data between (-1,1) for tanh activation function
from sklearn.preprocessing import MinMaxScaler
sc_input = MinMaxScaler(feature_range=(-1,1))
sc_input = sc_input.fit(xtrain)
xtrain_scaled = sc_input.transform(xtrain)
xtrain_scaled.shape
xtrain = xtrain_scaled

# scale the output data between (-1,1) for tanh activation function
from sklearn.preprocessing import MinMaxScaler
sc_output = MinMaxScaler(feature_range=(-1,1))
sc_output = sc_output.fit(ytrain)
ytrain_scaled = sc_output.transform(ytrain)
ytrain_scaled.shape
ytrain = ytrain_scaled
#%%
#--------------------------------------------------------------------------------------------------------------#
model = Sequential()
#model.add(Dropout(0.2))
model.add(Dense(80, input_shape=(nx,), init='uniform', activation='tanh', use_bias=True))
model.add(Dense(80, init='uniform', activation='tanh', use_bias=True))
model.add(Dense(80, init='uniform', activation='tanh', use_bias=True))
#model.add(Dense(100, init='glorot_uniform', activation='tanh', use_bias=True))
#model.add(Dense(100, init='glorot_uniform', activation='tanh', use_bias=True))
#model.add(Dense(40, init='uniform', activation='tanh', use_bias=True))
#model.add(Dense(40, init='uniform', activation='tanh', use_bias=True))
model.add(Dense(ny, activation='linear', use_bias=True))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy']) # compile the model

history = model.fit(xtrain, ytrain, nb_epoch=600, batch_size=100, validation_split=0.1) # run the model

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)

plt.figure()
plt.semilogy(epochs, loss, 'b', label='Training loss')
plt.semilogy(epochs, val_loss, 'r', label='Validationloss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
'''
model = Sequential()

input_layer = Input(shape=(legs*(n-1)+1,)) # input layer

# Hidden layers
x = Dense(40, activation='tanh', use_bias=True)(input_layer)
x = Dense(40, activation='tanh', use_bias=True)(x)
x = Dense(40, activation='tanh', use_bias=True)(x)
#x = Dense(40, activation='relu', use_bias=True)(x)

op_val = Dense(3, activation='linear', use_bias=True)(x) # output layer

custom_model = Model(inputs=input_layer, outputs=op_val)
filepath = "best_model.hd5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

custom_model.compile(optimizer='adam', loss='mean_squared_error', metrics=[coeff_determination])
history_callback = custom_model.fit(xtrain, ytrain, epochs=1000, batch_size=100, verbose=1, validation_split= 0.2,
                                    callbacks=callbacks_list)

loss_history = history_callback.history["loss"]
val_loss_history = history_callback.history["val_loss"]
scores = custom_model.evaluate(xtrain, ytrain)
print("\n%s: %.2f%%" % (custom_model.metrics_names[1], scores[1]*100))

epochs = range(1, len(loss_history) + 1)

plt.figure()
plt.semilogy(epochs, loss_history, 'b', label='Training loss')
plt.semilogy(epochs, val_loss_history, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
'''
#%%
t_init  = 0.0  # Initial time
t_final = 20.0 # Final time
dt = 0.01
t = np.arange(t_init, t_final, dt)
nsamples = int((t_final-t_init)/dt)
states = odeint(f, state0, t)
states1 = odeint(f1, state0, t)
mx,nx = states.shape

#%%
plt.figure()
plt.plot(t, states[:,0])
plt.plot(t, states1[:,0])

plt.figure()
plt.plot(t, states[:,1])
plt.plot(t, states1[:,1])

#%%
testing_set = np.hstack((states[0:mx-1], states1[1:]))
mx,nx = testing_set.shape
my,ny = states.shape


ytest = np.zeros((my,nx))
ytest[0] = testing_set[0,:]

yt_ml = np.zeros((my,ny))
yt_ml[0] = states[0,:] 

xt_sc = np.zeros((1,nx))
yt_sc = np.zeros((1,ny))

#%%
for i in range(1,my):
    xt = ytest[i-1]
    xt = xt.reshape(1,nx)
    xt_sc = sc_input.transform(xt) # scale the input to the model
    yt = model.predict(xt_sc) # predict slope from the model 
    yt_sc = sc_output.inverse_transform(yt) # scale the calculated slope to the training data scale
    yt_ml[i] = yt_ml[i-1] + 1.0*dt*yt_sc # y1 at next time step
    yt_k = odeint(f1, yt_ml[i], t[0:2])
    ytemp = np.hstack((yt_ml[i], yt_k[1,:]))
    ytemp = ytemp.reshape(1,nx)
    ytest[i] = ytemp

ytest_ml = yt_ml


#%%%
#filename = slopenet+'_p=0'+str(legs)+'.csv'
#t = t.reshape(my,1)
#results = np.hstack((t, states, ytest_ml))
#np.savetxt(filename, results, delimiter=",")
#filename = slopenet+'_p=0'+str(legs)+'.csv'
#solution = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=0)
#m,n = solution.shape
#nrows = int((n-1)/2)
#t = solution[:,0]
#ytrue = solution[:,1:int((n-1)/2+1)]
#ytestplot = solution[:,int((n-1)/2+1):]
    
#%%

fig, axs = plt.subplots(ny, 1, figsize=(10,5))#, constrained_layout=True)
for i in range(ny):
    #axs[i].plot(ytrains[:,i], color='black', linestyle='-', label=r'$y_'+str(i+1)+'$'+' (True)', zorder=5)
    axs[i].plot(t,states[:,i], color='black', linestyle='-', label=r'$y_'+str(i+1)+'$'+' (True)', zorder=5)
    axs[i].plot(t,ytest_ml[:,i], color='blue', linestyle='-.', label=r'$y_'+str(i+1)+'$'+' (GP)', zorder=5) 
    axs[i].set_xlim([t[0], t[my-1]])
    axs[i].set_ylabel('$a_'+'{'+(str(i)+'}'+'$'), fontsize = 14)

fig.tight_layout() 

fig.subplots_adjust(bottom=0.1)

line_labels = ["True", "ML"]#, "ML-Train", "ML-Test"]
plt.figlegend( line_labels,  loc = 'lower center', borderaxespad=0.1, ncol=6, labelspacing=0.,  prop={'size': 13} ) #bbox_to_anchor=(0.5, 0.0), borderaxespad=0.1, 

fig.savefig('gp.eps')#, bbox_inches = 'tight', pad_inches = 0.01)

#%%    
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(states[:,0], states[:,1], states[:,2], color='blue')
ax.plot(ytest_ml[:,0], ytest_ml[:,1], ytest_ml[:,2], color='red')
plt.show()



