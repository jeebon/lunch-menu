from django.urls import path, include
from rest_framework.routers import DefaultRouter

from menu import views


router = DefaultRouter()
router.register('restaurants', views.RestaurantViewSet)
router.register('votes', views.VoteViewSet)
router.register('menus', views.MenuViewSet)

app_name = 'menu'

urlpatterns = [
    path('', include(router.urls))
]


