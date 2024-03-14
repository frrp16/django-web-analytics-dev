from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from tensorflow import keras
from io import BytesIO

import traceback
import h5py
import time
import os
import numpy as np
import pandas as pd
import tensorflow_decision_forests as tfdf

import uuid

class MLModel(models.Model):
    class Task(models.TextChoices):
        REGRESSION = 'Regression'
        CLASSIFICATION = 'Classification'
        BINARY_CLASSIFICATION = 'Binary'
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
    epochs = models.IntegerField(default=100)
    batch_size = models.IntegerField(default=32)
    timesteps = models.IntegerField(null=True, default=5)

    default_model = models.BooleanField(default=False) 
    # HIDDEN LAYER ACTIVATION FUNCTION. relu, sigmoid, linear, softmax, tanh
    activation = models.CharField(max_length=255, null=True, default='relu')  
    # OPTIMIZER: adam, sgd, rmsprop, adagrad, adadelta, adamax, nadam, ftrl
    optimizer = models.CharField(max_length=255, null=True, default='adam')    
    # random forest parameters
    num_trees = models.IntegerField(null=True, default=300)
    max_depth = models.IntegerField(null=True, default=16) 

    scaler = models.CharField(max_length=255, null=True) 
    sample_size = models.IntegerField(null=True)
    sample_frac = models.FloatField(null=True, default=0.8)
    created_at = models.DateTimeField(auto_now_add=True) 
    history = models.TextField(null=True)
    last_trained = models.DateTimeField(null=True)
    training_time = models.FloatField(null=True)
    model_file = models.BinaryField(null=True)   
    scaler_file = models.BinaryField(null=True) 

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
        if self.task == 'Classification':        
            self.loss = 'categorical_crossentropy'
            self.metrics = ['accuracy']
            self.activation_output = 'softmax'  
        elif self.task == 'Binary':
            self.loss = 'binary_crossentropy'
            self.metrics = ['accuracy']
            self.activation_output = 'sigmoid'  
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
                    model.add(keras.layers.Input(shape=(self.input_shape, )))
                    model.add(keras.layers.RepeatVector(self.timesteps))
                    model.add(keras.layers.Conv1D(hidden_layers[0], 2, activation=self.activation))
                    model.add(keras.layers.MaxPooling1D())
                    model.add(keras.layers.Flatten())
                    model.add(keras.layers.Dense(hidden_layers[1], activation=self.activation))
                    model.add(keras.layers.Dense(self.output_shape, activation=self.activation_output))                    
                model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
                return model
            case "RANDOM_FOREST":
                model = tfdf.keras.RandomForestModel()
                if self.num_trees and self.max_depth:
                    model = tfdf.keras.RandomForestModel(num_trees=self.num_trees, max_depth=self.max_depth)
                model.compile(metrics=self.metrics)                
                return model
            case _:
                raise Exception("Invalid algorithm")    

    def save_model(self, models):
        try:
            if self.algorithm == 'RANDOM_FOREST':
                # model can be saved if trained, no need to save model
                self.model_file = None
            else:
                models.save(f'tmp/{self.name}.h5')
                self.file_extension = 'h5'
                with open(f'tmp/{self.name}.h5', 'rb') as file:
                    self.model_file = file.read()                    
                self.save()                 
        except Exception as e:
            raise Exception(e)      
    
    def get_model_summary(self):
        try:
            if self.algorithm == 'RANDOM_FOREST':
                return "Can be printed after training."        
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
            if self.algorithm == 'RANDOM_FOREST':
                return "Can be printed after training."
            with h5py.File(BytesIO(self.model_file), 'r') as file:
                model = keras.models.load_model(file)
                layers = [(layer.name, layer.output_shape) for layer in model.layers]
            return layers
        except Exception as e: 
            traceback.print_exc()
            raise Exception(e)
        
    def preprocess_data(self, dataset: pd.DataFrame):
        try:
            # combine feature and target as selected_columns
            selected_columns = self.features + [self.target]
            if self.sample_frac:
                dataset = dataset.sample(frac=self.sample_frac)
            if self.sample_size:
                dataset = dataset.sample(n=self.sample_size)

            X = dataset[self.features]
            y = dataset[self.target]

            return X, y
        except Exception as e:
            raise Exception(e)


        
    def train(self, X: np.ndarray, y: np.ndarray):
        try:
            self.status = 'training'
            start_time = time.time()
            self.save()

            if self.algorithm == 'RANDOM_FOREST':
                model = tfdf.keras.RandomForestModel()
                if self.num_trees and self.max_depth:
                    model = tfdf.keras.RandomForestModel(num_trees=self.num_trees, max_depth=self.max_depth)
                history = model.fit(X, y, epochs=1, batch_size=int(self.batch_size))
                self.history = history.history
                model.save(f'assets/{self.name}_{self.id}')                                
                # self.model_file = open(f'tmp/{self.name}_trained.tf', 'rb').read()
                self.status = 'trained'
                self.training_time = time.time() - start_time
                self.last_trained = timezone.now()
                self.save()
                # delete tmp file                
                
                return model 
            
            with h5py.File(BytesIO(self.model_file), 'r') as file:
                model = keras.models.load_model(file)
                if self.algorithm == 'LSTM':
                    X, y = self.lstm_data_transform(X, y)
                history = model.fit(X, y, 
                          epochs=int(self.epochs), batch_size=int(self.batch_size), 
                          validation_split=0.2,
                          callbacks=[keras.callbacks.EarlyStopping(patience=5, monitor='val_loss')]
                          ) 
                self.history = history.history
                model.save(f'tmp/{self.name}_trained.h5')                                
                self.model_file = open(f'tmp/{self.name}_trained.h5', 'rb').read()
                self.status = 'trained'
                self.training_time = time.time() - start_time
                self.last_trained = timezone.now()
                self.save()
                # delete tmp file
                os.remove(f'tmp/{self.name}_trained.h5')
                
            return model
        except Exception as e:
            self.status = 'untrained'
            raise Exception(e)

    def predict(self, data):
        try:
            if self.algorithm == "RANDOM_FOREST":
                model = keras.models.load_model(f'assets/{self.name}_{self.id}')
                prediction = model.predict(data)
                return prediction
            else:
                with h5py.File(BytesIO(self.model_file), 'r') as file:
                    model = keras.models.load_model(file)
                    prediction = model.predict(data)
                    return prediction
        except Exception as e:
            raise Exception(e)
    
    def lstm_data_transform(self, x_data, y_data):
        """ Changes data to the format for LSTM training 
        for sliding window approach """       
        X, y = list(), list()
        for i in range(x_data.shape[0]):        
            end_ix = i + self.timesteps            
            if end_ix >= x_data.shape[0]:
                break            
            seq_X = x_data[i:end_ix]            
            seq_y = y_data[end_ix]            
            X.append(seq_X)
            y.append(seq_y)        
        x_array = np.array(X)
        y_array = np.array(y)
        return x_array, y_array

class PredictionModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
    data = models.TextField()
    prediction = models.TextField()
    loss = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def get_prediction_by_model_id(self, model_id):
        try:
            return self.objects.filter(model=model_id)
        except Exception as e:
            raise Exception(e)

    def __str__(self):
        return self.model.name
