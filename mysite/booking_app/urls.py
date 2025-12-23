from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileListAPIView, UserProfileDetailAPIView,
                    CityListAPIView, CityDetailAPIView,
                     HotelListAPIView, HotelDetailAPIView,
                    RoomListAPIView, RoomDetailAPIView, BookingViewSet, ReviewListAPIViewSet,
                    RegisterView, LoginView, LogoutView)

router = routers.DefaultRouter()
router.register('booking', BookingViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('city/', CityListAPIView.as_view(), name='city_list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city_detail'),
    path('hotel/', HotelListAPIView.as_view(), name='hotel_list'),
    path('hotel/<int:pk>/', HotelDetailAPIView.as_view(), name='hotel_detail'),
    path('room/', RoomListAPIView.as_view(), name='room_list'),
    path('room/<int:pk>/', RoomDetailAPIView.as_view(), name='room_detail'),
    path('review/', ReviewListAPIViewSet.as_view(), name='review_list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]