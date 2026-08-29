from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):

    def __init__(self, page_size=10, max_page_size=100):
        super().__init__()
        self.page_size = page_size
        self.page_size_query_param = 'page_size'
        self.max_page_size = max_page_size

    