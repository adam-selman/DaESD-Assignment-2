from django.urls import path
from .views import views, login_view



urlpatterns = [
   path('', views.index, name='index'),
   path('login/', login_view, name='login'),
]