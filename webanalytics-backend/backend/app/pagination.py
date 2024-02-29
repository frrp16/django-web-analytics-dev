from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

import math

class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000