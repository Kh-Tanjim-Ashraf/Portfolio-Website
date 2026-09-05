from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):

    def __init__(self, page_size=10, max_page_size=100):
        super().__init__()
        self.page_size = page_size  # Total items exists in each page
        self.page_size_query_param = 'page_size'   # Dynamically handles the quantity of items in a page through passing this query in the URL
        self.max_page_size = max_page_size  # Total items divides into max amount of pages