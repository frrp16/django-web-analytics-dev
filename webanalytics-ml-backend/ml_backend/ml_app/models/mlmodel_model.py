from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from tensorflow import keras
from io import BytesIO

import h5py
import os
import numpy as np
import tensorflow_decision_forests as tfdf

import uuid

class MLModel(models.Model):
    class Task(models.TextChoices):
        REGRESSION = 'Regression'
        CLASSIFICATION = 'Classification'
        ANOMALY_DETECTION = 'Anomaly Detection'
    class Status(models.TextChoices):
        UNTRAINED = 'untrained'
        TRAINED = 'trained'
        TRAINING = 'training'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.UNTRAINED)
    # DEEP LEARNING CELLS: MLP: Dense, LSTM: LSTM, CNN: Conv2D
    algorithm = models.CharField(max_length=255)       
    file_extension = models.CharField(max_length=255, null=True)  
    input_shape = models.IntegerField(null=True)
    output_shape = models.IntegerField(null=True) 
    hidden_layers = models.TextField(null=True, default='100,100')
    features = models.TextField(null=True) 
    target = models.TextField(max_length=255, null=True) 
    task = models.CharField(max_length=255, choices=Task.choices, null=True)
    epocs = models.IntegerField(default=100)
    batch_size = models.IntegerField(default=32)
    timesteps = models.IntegerField(null=True)
    # HIDDEN LAYER ACTIVATION FUNCTION. relu, sigmoid, linear, softmax, tanh
    activation = models.CharField(max_length=255, null=True)  
    # OPTIMIZER: adam, sgd, rmsprop, adagrad, adadelta, adamax, nadam, ftrl
    optimizer = models.CharField(max_length=255, null=True)    
    # random forest parameters
    num_trees = models.IntegerField(null=True)
    max_depth = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True) 
    history = models.TextField(null=True)
    model_file = models.BinaryField(null=True)
    

    def __str__(self):
        return self.name
    
    def build_and_compile_model(self):
        hidden_layers = [int(x) for x in self.hidden_layers.split(',')]
        # if activation is provided, use it, otherwise use relu
        if self.activation:
            self.activation = self.activation
        else:
            self.activation = 'relu' 

        # if optimizer is provided, use it, otherwise use adam
        if self.optimizer:
            self.optimizer = self.optimizer
        else:
            self.optimizer = 'adam'

        # if task is classification, use softmax, otherwise use linear
        if self.task == 'classification':        
            self.loss = 'categorical_crossentropy'
            self.metrics = ['accuracy']
            self.activation_output = 'softmax'    
        else:
            self.loss = 'mse'
            self.metrics = ['mse']
            self.activation_output = 'linear'   

        match self.algorithm:            
            case "MLP":
                model = keras.models.Sequential(name=self.name)
                if hidden_layers:
                    model.add(keras.layers.Dense(hidden_layers[0], input_dim=self.input_shape, activation=self.activation))
                    for units in hidden_layers[1:]:
                        model.add(keras.layers.Dense(units, activation=self.activation))   
                    model.add(keras.layers.Dense(self.output_shape, activation=self.activation_output))
                    model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
                return model
            case "LSTM":
                model = keras.models.Sequential(name=self.name)
                if hidden_layers:
                    model.add(keras.layers.LSTM(hidden_layers[0], input_shape=(self.timesteps, self.input_shape), activation=self.activation, return_sequences=True))
                    model.add(keras.layers.LSTM(hidden_layers[1], activation=self.activation))
                    model.add(keras.layers.Dense(self.output_shape, activation=self.activation_output))
                model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
                return model
            case "CNN":
                model = keras.models.Sequential(name=self.name)
                if hidden_layers:
                    model.add(keras.layers.Conv2D(hidden_layers[0], (3,3), input_shape=(self.input_shape), activation=self.activation))
                    model.add(keras.layers.MaxPooling2D((2,2)))
                    model.add(keras.layers.Conv2D(hidden_layers[1], (3,3), activation=self.activation))
                    model.add(keras.layers.MaxPooling2D((2,2)))
                    model.add(keras.layers.Flatten())
                    model.add(keras.layers.Dense(self.output_shape, activation=self.activation_output))
                model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
                return model
            case "RANDOM_FOREST":
                if self.num_trees and self.max_depth:
                    model = tfdf.keras.RandomForestModel(task=self.task, num_trees=self.num_trees, max_depth=self.max_depth)
                else: 
                    model = tfdf.keras.RandomForestModel(task=self.task)
                return model
            case _:
                raise Exception("Invalid algorithm")            
    
    def get_model_summary(self):
        try:
            with h5py.File(BytesIO(self.model_file), 'r') as file:
                model = keras.models.load_model(file)
                stringlist = []
                model.summary(print_fn=lambda x: stringlist.append(x))
                model_summary = "\n".join(stringlist)
            return model_summary
        except Exception as e:
            raise Exception(e)
        
    def get_model_layers(self):
        # get layers of the model with output shape
        try:
            with h5py.File(BytesIO(self.model_file), 'r') as file:
                model = keras.models.load_model(file)
                layers = [(layer.name, layer.output_shape) for layer in model.layers]
            return layers
        except Exception as e: 
            raise Exception(e)
        
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int, batch_size: int):
        try:
            with h5py.File(BytesIO(self.model_file), 'r') as file:
                model = keras.models.load_model(file)
                history = model.fit(X, y, 
                          epochs=epochs, 
                          batch_size=batch_size, 
                          validation_split=0.2,
                          callback=[keras.callbacks.EarlyStopping(patience=5)]
                          ) 
                self.history = history.history
                model.save(f'tmp/{self.name}.h5')                                
                self.model_file = open(f'tmp/{self.name}.h5', 'rb').read()
                self.save()
                # delete tmp file
                os.remove(f'tmp/{self.name}.h5')
            return model
        except Exception as e:
            raise Exception(e)

    def predict(self, data):
        try:
            with h5py.File(BytesIO(self.model_file), 'r') as file:
                model = keras.models.load_model(file)
                prediction = model.predict(data) 
            return prediction
        except Exception as e:
            raise Exception(e)
    
    def lstm_data_transform(x_data, y_data, num_steps=5):
        """ Changes data to the format for LSTM training 
        for sliding window approach """       
        X, y = list(), list()
        for i in range(x_data.shape[0]):        
            end_ix = i + num_steps            
            if end_ix >= x_data.shape[0]:
                break            
            seq_X = x_data[i:end_ix]            
            seq_y = y_data[end_ix]            
            X.append(seq_X)
            y.append(seq_y)        
        x_array = np.array(X)
        y_array = np.array(y)
        return x_array, y_array