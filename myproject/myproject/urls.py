from django.contrib import admin
from django.urls import path, include
from myapp.views import UserProgressView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('api/user-progress/<str:user_id>/', UserProgressView.as_view(), name='total-enrolled-courses'),
 
]
