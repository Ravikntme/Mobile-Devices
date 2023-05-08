from django.urls import path
from .api_views import *

urlpatterns = [
    path('api/user-login',LoginView.as_view()),
    path('api/mobile-create',MobileDevicesCreate.as_view()),
    path('api/delete',MobileDevicesDelete.as_view()),
    path('api/mobile-filter',MobilewithFilter.as_view()),
    path('api/mobile-list',MobileList.as_view()),
    path('api/mobile-price-range',MobileListwithPriceRange.as_view()),
    path('api/list-order',MobilewListinOrder.as_view()),
]
