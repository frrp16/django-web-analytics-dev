from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, show
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.models.callbacks import CustomJS

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.response import Response

from ..services.plot_service import PlotService
from ..models import Dataset

import pandas as pd
import json

class PlotView(viewsets.ViewSet):   
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        return Response('Plot', status=status.HTTP_200_OK)
      
    
    @action(detail=False, methods=['get'], url_path='time_series_plot')
    def time_series_plot(self, request):
        dataset_id = request.query_params.get('dataset_id')
        columns = request.query_params.get('columns').split(',')

        dataset_instance = Dataset.objects.get(id=dataset_id)
        df = dataset_instance.get_dataset_data()                              
        
        plot_service = PlotService(df, columns)
        plot = plot_service.create_time_series_plot()
        return Response(plot, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='pair_scatter_plot')
    def pair_scatter_plot(self, request):
        dataset_id = request.query_params.get('dataset_id')
        columns = request.query_params.get('columns').split(',')

        dataset_instance = Dataset.objects.get(id=dataset_id)
        df = dataset_instance.get_dataset_data()
                
        
        plot_service = PlotService(df, columns)
        plot = plot_service.create_pair_scatter_plot()
        return Response(plot, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='pie_chart')
    def pie_chart(self, request):
        dataset_id = request.query_params.get('dataset_id')
        column = request.query_params.get('column')

        dataset_instance = Dataset.objects.get(id=dataset_id)
        df = dataset_instance.get_dataset_data()
        plot_service = PlotService(df, column)
        plot = plot_service.create_pie_chart()
        return Response(plot, status=status.HTTP_200_OK)