# Teacher.py

# Defines the teacher model for training

import tensorflow as tf
from tensorflow.keras import *
from tensorflow.keras.layers import *
from mlp import MLP_Model

privileged_input = Input(shape=(3,), name='Privileged data')    # Shape is the shape of the privledged information
robot_state = Input(shape=(9,), name='Robot state')             # This shape is defined by the robot state info, from sensors

encoder = Dense(72, activation='tanh')(privileged_input)
encoder = Dense(64, activation='tanh')(encoder)

mlp_model = MLP_Model(inputs=[encoder, robot_state])

teacher_model = Model(inputs=[privileged_input, robot_state], outputs=mlp_model, name='Teacher')