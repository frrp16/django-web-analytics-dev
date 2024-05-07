# from django.db import models

# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User

# from tensorflow import keras
# from io import BytesIO

# import h5py

# import uuid

# class MLModel(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     algorithm = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)    
#     file_extension = models.CharField(max_length=255, null=True)   
#     features = models.CharField(max_length=511, null=True, default='all') 
#     target = models.CharField(max_length=255, null=True, default='all')    
#     dataset = models.CharField(max_length=255, null=True)
#     model_file = models.BinaryField(null=True)

#     def __str__(self):
#         return self.name
    
#     def get_model_summary(self):
#         try:
#             with h5py.File(BytesIO(self.model_file), 'r') as file:
#                 model = keras.models.load_model(file)
#                 stringlist = []
#                 model.summary(print_fn=lambda x: stringlist.append(x))
#                 model_summary = "\n".join(stringlist)
#             return model_summary
#         except Exception as e:
#             raise Exception(e)