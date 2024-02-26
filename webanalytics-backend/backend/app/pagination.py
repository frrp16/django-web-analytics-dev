from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

import math

class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

    # def page(self):
    #     return super().page()
    
    # def get_next_link(self):
    #     return super().get_next_link()
    
    # def get_previous_link(self):
    #     return super().get_previous_link()

#     def paginate_dataframe(self, df, request):
#         self.page_size = self.get_page_size(request)
#         if not self.page_size:
#             return None

#         page_size = self.page_size
#         count = len(df)
#         self.page = self.get_page_number(request, self.page_size)

#         self.request = request

#         if count > page_size and self.template is not None:
#             self.display_page_controls = True

#         self.count = count
#         self.total_pages = math.ceil(count / page_size)
#         self.next = self.get_next_link()
#         self.previous = self.get_previous_link()

#         total_page = math.ceil(self.page.paginator.count / self.page_size)

#         start = (self.page - 1) * page_size
#         end = start + page_size
#         return {
# '           links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'total_page': total_page,
#             'result': df[start:end]
#         }

    # def get_paginated_response(self, data):
    #     if self.request.query_params.get('page_size'):
    #         self.page_size = int(self.request.query_params.get('page_size'))

    #     total_page = math.ceil(self.page.paginator.count / self.page_size)

    #     return Response({
    #         'links': {
    #             'next': self.get_next_link(),
    #             'previous': self.get_previous_link()
    #         },
    #         'count': self.page.paginator.count,
    #         'total_page': total_page,
    #         'results': data
    #     })