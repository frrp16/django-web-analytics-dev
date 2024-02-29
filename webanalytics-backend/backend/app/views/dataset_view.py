from django.contrib.auth.models import User
from django.core.cache import cache

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination


from ..pagination import CustomPagination

from ..models import Dataset, DatabaseConnection
from ..serializers import DatasetSerializer, CreateDatasetSerializer
from ..services import user_service

from ..api import get_dataset_monitorlog, create_monitorlog


import pandas as pd
import math

# redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

class DatasetViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]    
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    serializer_class = CreateDatasetSerializer
    pagination_class = PageNumberPagination
    
    def list(self, request):   
        try:     
            # Check if user is authenticated as admin user
            if request.user.is_staff:
                queryset = Dataset.objects.all()
                serializer = DatasetSerializer(queryset, many=True)
                return Response(serializer.data)   
                             
            user = user_service.get_user_from_token(request.headers.get('Authorization').split()[1])
            queryset = Dataset.objects.filter(user=user.id)
            serializer = DatasetSerializer(queryset, many=True)
            # get dataset monitor log for each dataset
            for dataset in serializer.data:
                print('Dataset:', dataset)
                monitor_log = get_dataset_monitorlog(dataset['id'])
                # Add monitor log to serializer data
                dataset['monitor_log'] = monitor_log

            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
    def retrieve(self, request, pk=None):    
        if request.user.is_staff:
            queryset = Dataset.objects.get(id=pk)            
            serializer = DatasetSerializer(queryset)
            return Response(serializer.data)
        user = user_service.get_user_from_token(request.headers.get('Authorization').split()[1])  
        queryset = Dataset.objects.filter(user=user.id)
        dataset = queryset.get(id=pk)
        serializer = DatasetSerializer(dataset)
        # get dataset monitor log
        monitor_log = get_dataset_monitorlog(dataset.id)
        # Add monitor log to serializer data
        serializer.data['monitor_log'] = monitor_log
        return Response(serializer.data)
    
    # # Create partial update method
    def partial_update(self, request, pk=None):
        try:
            if request.user.is_staff:
                dataset = Dataset.objects.get(id=pk)         
                serializer = DatasetSerializer(dataset, data=request.data, partial=True)        
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                user = user_service.get_user_from_token(request.headers.get('Authorization').split()[1])
                dataset = Dataset.objects.filter(user=user.id).get(id=pk)
                serializer = DatasetSerializer(dataset, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request):
        name = request.data.get('name')
        description = request.data.get('description')
        table_name = request.data.get('table_name')

        if not all([name, table_name]):
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
        
        # Get user id
        user_id = 0
        token = request.headers.get('Authorization').split()[1]
        try:
            user_id = AccessToken(token).get('user_id')
            if not user_id:
                return Response("User not found or token is not valid", status=400)
        except Exception as e:
            return Response(str(e), status=400)
        
        # Get DatabaseConnection from user_id
        db_connection = DatabaseConnection.objects.get(user=user_id)

        # Get data from database
        try:
            # Build connection engine
            engine = db_connection.engine_instance
            # Read using pandas
            df = pd.read_sql_table(table_name, con=engine)   
            # Get column count and row count
            column_count = len(df.columns)
            row_count = len(df.index)
            
            # Create a new Dataset instance       
            dataset_instance = Dataset(
                name=name, description=description, table_name=table_name, 
                user=User.objects.get(id=user_id), connection=db_connection,
            )
            # Create a new DatasetMonitorLog instance            
            dataset_instance.save()  
            create_monitorlog(str(dataset_instance.id), row_count, column_count)            
            monitor_log = get_dataset_monitorlog(str(dataset_instance.id))            
            # Serialize the Dataset instance
            serializer = DatasetSerializer(dataset_instance)
            # Add monitor log to serializer data
            serializer.data['monitor_log'] = monitor_log
            engine.dispose()
            # get dataset monitor lo
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('Error:', e)
            return Response("Internal Server Error", status=500)
        
    @action(detail=True, methods=['GET'], url_path='columns')
    def get_dataset_columns(self, request, pk=None):        
        try:            
            columns = Dataset.objects.get(id=pk).get_dataset_columns()     
            # columns = dataset_instance.get_dataset_data().columns.tolist() 
            return Response(columns, status=status.HTTP_200_OK)            
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['GET'], url_path='row_count')
    def get_dataset_row_count(self, request, pk=None):
        try:
            row_count = Dataset.objects.get(id=pk).get_dataset_row_count()            
            return Response(row_count, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['GET'], url_path='data')
    def get_dataset_data(self, request, pk=None):    
        # get column parameter to order by
        order = request.query_params.get('order')
        # column for ordering
        column = request.query_params.get('column') 
        asc = request.query_params.get('asc')    
        sample = request.query_params.get('sample')  
        # column for partial select data
        col_select = request.query_params.get('col_select')
        try:
            # print all request query params and data
            # print(request.query_params)                    
            df = Dataset.objects.get(id=pk).get_dataset_data()   
            if sample == 'true':
                if len(df) > 5000:
                    df = df.sample(5000, replace=False, random_state=1).sort_index()
            # for each column of dataset, check its type            
            for c in df.columns:
                # if there is null value and its numeric, fill it with 0
                if df[c].isnull().sum() > 0 and df[c].dtype in ['int64', 'float64']:
                    df[c].fillna(0, inplace=True)
                # if there is null value and its string, fill it with '-'
                elif df[c].isnull().sum() > 0 and df[c].dtype == 'object':
                    df[c].fillna('-', inplace=True)   

            # if column is boolean type, convert it to string
            for c in df.columns:
                if df[c].dtype == 'bool':
                    # if true, convert to 'True', else convert to 'False'
                    df[c] = df[c].apply(lambda x: 'True' if x else 'False')
            
            if col_select is not None:                
                df = df[col_select.split(',')]

            # if order is true and column is not None, sort the dataframe      
            if order == 'true' and column is not None:
                if asc == 'true':
                    df = df.sort_values(by=[column], ascending=True)    
                else:
                    df = df.sort_values(by=[column], ascending=False)                                 
            paginator = self.pagination_class()
            # get page_size from query params if exists
            page_size = request.query_params.get('page_size')
            if page_size:
                paginator.page_size = int(page_size)                
            
            p = paginator.paginate_queryset(df.to_dict(orient='records'), request)  
            paginated_data = paginator.get_paginated_response(p)
            return Response(paginated_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error:', e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['GET'], url_path='pages_count')
    def get_pages_count(self, request, pk=None):
        sample = request.query_params.get('sample')  
        try:
            user = user_service.get_user_from_token(request.headers.get('Authorization').split()[1])
            df = Dataset.objects.filter(user=user.id).get(id=pk).get_dataset_data()       
            if sample == 'true':
                if len(df) > 5000:
                    df = df.sample(5000, replace=False, random_state=1).sort_index()                             
            paginator = self.pagination_class()
            # get page_size from query params if exists
            page_size = request.query_params.get('page_size')
            if page_size:
                paginator.page_size = int(page_size)                
            total_pages = math.ceil(len(df) / paginator.page_size)
            return Response(total_pages, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error:', e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @action(detail=True, methods=['GET'], url_path='data/all')
    # def get_all_dataset_data(self, request, pk=None):    
    #     try:
    #         user = user_service.get_user_from_token(request.headers.get('Authorization').split()[1])
    #         df = Dataset.objects.filter(user=user.id).get(id=pk).get_dataset_data()                   
    #         # for each column of dataset, check its type
    #         for column in df.columns:
    #             # if there is null value and its numeric, fill it with 0
    #             if df[column].isnull().sum() > 0 and df[column].dtype in ['int64', 'float64']:
    #                 df[column].fillna(0, inplace=True)
    #             # if there is null value and its string, fill it with '-'
    #             elif df[column].isnull().sum() > 0 and df[column].dtype == 'object':
    #                 df[column].fillna('-', inplace=True)             
    #         return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)
    #     except Exception as e:
    #         print('Error:', e)
    #         return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)