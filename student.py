# Student.py

# Implementation of the student model which takes in Proprioceptive history data and robot state data

import tensorflow as tf
from tensorflow.keras import *
from tensorflow.keras.layers import *
from mlp import MLP_Model

generations = 50                            # The number of points in the past to pull from
history = Input(shape=(60, generations), name='Proprioceptive history')     # This shape is the points in history by the number of previous points to look at
robot_state = Input(shape=(9,), name='Robot state')                         # This shape is defined by the robot state info, from sensors

# Layer count may need to be adjusted based on actual history size
tcn_encoder = Conv1D(5, 1, dilation_rate=1, activation='relu')(history)     # Filter size might need to be changed
tcn_encoder = Conv1D(5, 1, strides=2, activation='relu')(tcn_encoder)
tcn_encoder = Conv1D(5, 1, dilation_rate=2, activation='relu')(tcn_encoder)
tcn_encoder = Conv1D(5, 1, strides=2, activation='relu')(tcn_encoder)
tcn_encoder = Conv1D(5, 1, dilation_rate=4, activation='relu')(tcn_encoder)
tcn_encoder = Conv1D(5, 1, strides=2, activation='relu')(tcn_encoder)
tcn_encoder = Flatten()(tcn_encoder)
tcn_encoder = Dense(64, activation='tanh')(tcn_encoder)

mlp_student = MLP_Model(inputs=[tcn_encoder, robot_state])

student_model = Model(inputs=[history, robot_state], outputs=mlp_student, name='Student')