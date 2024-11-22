from django.urls import path
from . import views
from myapp.views import UserProgressView
urlpatterns = [
    path('', views.home, name='home'),
    path('api/user-progress/<str:user_id>/', UserProgressView.as_view(), name='total-enrolled-courses'),
   
]
