import pandas as pd
import json
from keras import models, layers
from django.conf import settings
from ..models import MLModel

class BaseModel():
    def __init__(self, name: str, features: list, hidden_layers: list, target : list, task : str, dataset_id: str):
        self.name = name
        self.features = features
        self.target = target
        self.task = task
        self.hidden_layers = hidden_layers    
        self.model = self.build_and_compile_model()
        self.dataset = dataset_id

    def build_and_compile_model(self):
        pass

    def summary(self):
        stringlist = []
        self.model.summary(print_fn=lambda x: stringlist.append(x))
        model_summary = "\n".join(stringlist)
        return model_summary

    def train(self, X, y, epochs=100, batch_size=10):     
        # Convert pandas dataframe to numpy array
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.2)

    def save(self):
        try:
            self.model.save(f'tmp/{self.name}.h5')                            
        except Exception as e:
            raise Exception(e)

    def save_model_instance(self):
        try:
            with open(f'{settings.BASE_DIR}/tmp/{self.name}.h5', 'rb') as file:
                binary_model = file.read()
                model_instance = MLModel(
                    name=self.name, dataset=self.dataset, model_file=binary_model,
                    file_extension='h5', features=json.dumps(self.features), target=json.dumps(self.target)
                    )
                model_instance.save()
                file.close()
        except Exception as e:
            raise Exception(e)    

class MultilayerPerceptron(BaseModel):
    def __init__(self, name: str, features: list, hidden_layers: list, target : list,  task : str, dataset_id: str):                
        self.algorithm = "MLP"    
        # self.model = self.build_and_compile_model()
        super().__init__(name, features, hidden_layers, target, task, dataset_id) 
        self.model = self.build_and_compile_model()       

    def build_and_compile_model(self):
        try:
            model = models.Sequential(name=self.name)
            # model.add(layers.Dense(100, input_dim=1, activation='relu'))
            # model.add(layers.Dense(100, activation='relu'))
            # model.add(layers.Dense(1, activation='linear'))     
                   
            if self.hidden_layers:
                model.add(layers.Dense(self.hidden_layers[0], input_dim=len(self.features), activation='relu'))
                for units in self.hidden_layers[1:]: 
                    model.add(layers.Dense(units, activation='relu'))            
            if self.task == 'classification':
                model.add(layers.Dense(len(self.target), activation='softmax'))
                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            else:
                model.add(layers.Dense(len(self.target), activation='linear'))
                model.compile(loss='mse', optimizer='adam', metrics=['mse'])        
            return model
        except Exception as e:
            raise Exception(e)
        

# def mlp_model():
#     model = models.Sequential()
#     model.add(layers.Dense(100, input_dim=1, activation='relu'))
#     model.add(layers.Dense(100, activation='relu'))
#     model.add(layers.Dense(1, activation='linear'))
#     return model