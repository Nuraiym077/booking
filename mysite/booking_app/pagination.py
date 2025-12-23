from rest_framework.pagination import PageNumberPagination


class HotelPagination(PageNumberPagination):
    page_size = 5


class RoomPagination(PageNumberPagination):
    page_size = 8
