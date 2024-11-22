
from django.contrib import admin
from django.urls import path

from accounts.views import home, signup_view, login_view, logout_view,UserProgressView

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('api/user-progress/<str:user_id>/', UserProgressView.as_view(), name='total-enrolled-courses')
]
