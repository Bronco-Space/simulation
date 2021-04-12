# mlp.py

# Defines the multilayer percepton model that is used in both the teacher and 
# the student to generate an action from the robot state and latent encoded
# representation of the enviroment.

import tensorflow as tf
from tensorflow.keras import *
from tensorflow.keras.layers import *


latent_size = 64

e_input = Input(shape=(latent_size,))
robot_state = Input(shape=(9,))         # This shape is defined by the robot state info, from sensors

mlp = concatenate([e_input, robot_state])
mlp = Dense(256, activation='tanh')(mlp)
mlp = Dense(128, activation='tanh')(mlp)
mlp = Dense(64, activation='tanh')(mlp)
action = Dense(16, activation='relu')(mlp)

MLP_Model = Model(inputs=[e_input, robot_state], outputs=action, name='MLP')